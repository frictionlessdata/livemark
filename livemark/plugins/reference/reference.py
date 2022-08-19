from __future__ import annotations
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
        return FunctionReference(object)


class ClassReference(Reference):
    reference_type = "class"

    def __init__(self, object: Type):
        self.object = object

    @property
    def name(self):
        return self.object.__name__

    @property
    def varialbes(self):
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
                    name=name, type=type, description=description
                )
                variables.append(variable)
        return variables

    @property
    def properties(self):
        properties = []
        predicat = lambda item: isinstance(item, property)
        for name, object in inspect.getmembers(self.object, predicat):
            if name.startswith("_"):
                continue
            if name.startswith("slots_"):
                continue
            if name not in vars(self.object):
                continue
            properties.append(PropertyReference(object))
        return properties

    @property
    def methods(self):
        methods = []
        predicate = inspect.isfunction
        for name, object in inspect.getmembers(self.object, predicate=predicate):
            if name.startswith("_"):
                continue
            if name.startswith("slots_"):
                continue
            if name not in vars(self.object):
                continue
            methods.append(FunctionReference(object))
        return methods


class FunctionReference(Reference):
    reference_type = "function"

    def __init__(self, object):
        self.name = object.__name__
        self.object = object
        self.signature = inspect.signature(self.object)
        self.docstring = docstring_parser.parse(inspect.getdoc(self.object) or "")

    @property
    def description(self):
        description = self.docstring.short_description or ""
        if self.docstring.long_description:
            description += "\n\n" + self.docstring.long_description
        return description

    @property
    def parameters(self):
        parameters = []
        for name, item in self.signature.parameters.items():
            if name in ["self", "cls"]:
                continue
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
        sig = self.signature
        type = str(sig.return_annotation) if sig.return_annotation != sig.empty else ""
        description = ""
        if self.docstring.returns:
            description = self.docstring.returns.description or ""
        return ResultReference(type=type, description=description)


class PropertyReference(Reference):
    reference_type = "property"

    def __init__(self, object):
        self.name = object.fget.__name__
        self.object = object
        self.reader = inspect.signature(self.object.fget)
        self.writer = inspect.signature(self.object.fset) if self.object.fset else None
        self.docstring = docstring_parser.parse(inspect.getdoc(self.object) or "")

    @property
    def description(self):
        description = self.docstring.short_description or ""
        if self.docstring.long_description:
            description += "\n\n" + self.docstring.long_description
        return description

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


@attrs.define(kw_only=True)
class VariableReference(Reference):
    reference_type = "variable"

    name: str = ""
    type: str = ""
    default: str = ""
    description: str = ""


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
