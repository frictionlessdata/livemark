import re
import attrs
import inspect
import docstring_parser
from importlib import import_module
from typing import Type, ClassVar


class Reference:
    reference_type: ClassVar[str]

    @staticmethod
    def from_name(name):
        module_name, object_name = name.rsplit(".", maxsplit=1)
        module = import_module(module_name)
        object = getattr(module, object_name)
        return Reference.from_object(object)

    @staticmethod
    def from_object(object):
        if isinstance(object, type):
            return ClassReference(object)
        elif callable(object):
            return FunctionReference(object)


class FunctionReference(Reference):
    reference_type = "function"

    def __init__(self, object):
        self.object = object
        self.inspected = inspect.signature(self.object)
        self.docstring = docstring_parser.parse(inspect.getdoc(self.object) or "")

    @property
    def name(self):
        return self.object.__name__

    @property
    def title(self):
        title = f"{self.name} <small>(function)</small>"
        return title

    @property
    def description(self):
        description = self.docstring.short_description or ""
        if self.docstring.long_description:
            description += "\n\n" + self.docstring.long_description
        return description

    @property
    def signature(self):
        signature = str(self.inspected)
        signature = signature.replace("'", "")
        if signature == "()":
            signature = ""
        return signature

    @property
    def parameters(self):
        parameters = []
        for name, item in self.inspected.parameters.items():
            type = str(item.annotation) if item.annotation != item.empty else ""
            default = str(item.default) if item.default != item.empty else ""
            description = ""
            for dsitem in self.docstring.params:
                if dsitem.arg_name == name:
                    description = dsitem.description or ""
            parameter = ParameterReference(
                name=name, type=type, default=default, description=description
            )
            parameters.append(parameter)
        return parameters

    @property
    def exceptions(self):
        exceptions = []
        for item in self.docstring.raises:
            type = item.type_name or ""
            description = item.description or ""
            exception = ExceptionReference(type=type, description=description)
            exceptions.append(exception)
        return exceptions

    @property
    def result(self):
        sig = self.inspected
        type = str(sig.return_annotation) if sig.return_annotation != sig.empty else ""
        description = ""
        if self.docstring.returns:
            description = self.docstring.returns.description or ""
        return ResultReference(type=type, description=description)


class ClassReference(Reference):
    reference_type = "class"

    def __init__(self, object: Type):
        self.object = object
        self.docstring = docstring_parser.parse(inspect.getdoc(self.object) or "")

    @property
    def name(self):
        return self.object.__name__

    @property
    def title(self):
        title = f"{self.name} <small>(class)</small>"
        return title

    @property
    def description(self):
        description = self.docstring.short_description or ""
        if self.docstring.long_description:
            description += "\n\n" + self.docstring.long_description
        return description

    @property
    def constructor(self):
        predicate = inspect.isfunction
        for name, object in inspect.getmembers(self.object, predicate=predicate):
            if name == "__init__":
                return MethodReference(
                    object, class_name=self.name, docstring=inspect.getdoc(self.object)
                )

    @property
    def variables(self):
        variables = []
        if hasattr(self.object, "__annotations__"):
            code = inspect.getsource(self.object)
            for name, type in self.object.__annotations__.items():
                pattern = rf"    {name}:.*?\"\"\"(.*?)\"\"\""
                match = re.search(pattern, code, re.DOTALL)
                description = ""
                if match:
                    description = match.group(1)
                variable = VariableReference(
                    name=name, type=type, description=description, class_name=self.name
                )
                variables.append(variable)
        return variables

    @property
    def properties(self):
        properties = []
        predicat = lambda item: isinstance(item, property)
        for name, object in inspect.getmembers(self.object, predicat):
            if name not in vars(self.object):
                continue
            if name.startswith(("_", "slots_", "metadata_")):
                continue
            properties.append(PropertyReference(object, class_name=self.name))
        return properties

    @property
    def methods(self):
        methods = []
        predicate = lambda item: inspect.isfunction(item) or inspect.ismethod(item)
        for name, object in inspect.getmembers(self.object, predicate=predicate):
            if name not in vars(self.object):
                continue
            if name.startswith(("_", "slots_", "metadata_")):
                continue
            methods.append(MethodReference(object, class_name=self.name))
        return methods


@attrs.define(kw_only=True)
class VariableReference(Reference):
    reference_type = "variable"

    name: str = ""
    type: str = ""
    default: str = ""
    description: str = ""
    class_name: str

    @property
    def title(self):
        scope = self.class_name.lower()
        title = f"{scope}.{self.name} <small>(variable)</small>"
        return title


class PropertyReference(Reference):
    reference_type = "property"

    def __init__(self, object, *, class_name):
        self.object = object
        self.class_name = class_name
        self.reader = inspect.signature(self.object.fget)
        self.writer = inspect.signature(self.object.fset) if self.object.fset else None
        self.docstring = docstring_parser.parse(inspect.getdoc(self.object) or "")

    @property
    def name(self):
        return self.object.fget.__name__

    @property
    def title(self):
        scope = self.class_name.lower()
        title = f"{scope}.{self.name} <small>(property)</small>"
        return title

    @property
    def description(self):
        description = self.docstring.short_description or ""
        if self.docstring.long_description:
            description += "\n\n" + self.docstring.long_description
        return description

    @property
    def signature(self):
        signature = ""
        if self.result.type:
            signature = f"-> {self.result.type}"
        if self.parameter and self.parameter.type:
            signature = f"(self.parameter.type) {signature}"
        return signature

    @property
    def parameter(self):
        if self.writer:
            item = list(self.writer.parameters.values())[1]
            type = str(item.annotation) if item.annotation != item.empty else ""
            default = str(item.default) if item.default != item.empty else ""
            description = ""
            parameter = ParameterReference(
                name=self.name, type=type, default=default, description=description
            )
            return parameter

    @property
    def exceptions(self):
        exceptions = []
        for item in self.docstring.raises:
            type = item.type_name or ""
            description = item.description or ""
            exception = ExceptionReference(type=type, description=description)
            exceptions.append(exception)
        return exceptions

    @property
    def result(self):
        sig = self.reader
        type = str(sig.return_annotation) if sig.return_annotation != sig.empty else ""
        description = ""
        if self.docstring.returns:
            description = self.docstring.returns.description or ""
        return ResultReference(type=type, description=description)


class MethodReference(FunctionReference):
    reference_type = "method"

    def __init__(self, object, *, class_name, docstring=None):
        self.object = object
        self.class_name = class_name
        self.inspected = inspect.signature(self.object)
        self.docstring = docstring_parser.parse(
            docstring or inspect.getdoc(self.object) or ""
        )

    @property
    def title(self):
        static = "self" not in super().signature
        scope = self.class_name if static else self.class_name.lower()
        comment = "(method) (static)" if static else "(method)"
        title = f"{scope}.{self.name} <small>{comment}</small>"
        return title

    @property
    def signature(self):
        signature = super().signature
        signature = signature.replace("self, ", "")
        signature = signature.replace("self", "")
        signature = signature.replace("cls, ", "")
        signature = signature.replace("cls", "")
        if signature == "()":
            signature = ""
        return signature

    @property
    def parameters(self):
        parameters = []
        for parameter in super().parameters:
            if parameter.name not in ["cls", "self"]:
                parameters.append(parameter)
        return parameters


@attrs.define(kw_only=True)
class ParameterReference(Reference):
    reference_type = "parameter"

    name: str
    type: str = ""
    default: str = ""
    description: str = ""


@attrs.define(kw_only=True)
class ExceptionReference(Reference):
    reference_type = "exception"

    type: str = ""
    description: str = ""


@attrs.define(kw_only=True)
class ResultReference(Reference):
    reference_type = "result"

    type: str = ""
    description: str = ""
