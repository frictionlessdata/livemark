document.addEventListener("DOMContentLoaded", function () {
  function makeIds() {
    var content = document.querySelector("#livemark-content");
    var headings = content.querySelectorAll("h1, h2, h3, h4, h5, h6, h7");
    var headingMap = {};

    Array.prototype.forEach.call(headings, function (heading) {
      var id = heading.id
        ? heading.id
        : heading.textContent
            .trim()
            .toLowerCase()
            .split(" ")
            .join("-")
            .replace(/[!@#$%^&*():]/gi, "")
            .replace(/\//gi, "-");
      headingMap[id] = !isNaN(headingMap[id]) ? ++headingMap[id] : 0;
      if (headingMap[id]) {
        heading.id = id + "-" + headingMap[id];
      } else {
        heading.id = id;
      }
    });
  }
  makeIds();
  tocbot.init({
    // Where to render the table of contents.
    tocSelector: ".js-toc",
    // Where to grab the headings to build the table of contents.
    contentSelector: "#livemark-content",
    // Which headings to grab inside of the contentSelector element.
    {% if metadata.sidebar.navigation.selector %}
      headingSelector: "{{ metadata.sidebar.navigation.selector }}",
    {% else %}
      headingSelector: "{{ h2, h2, h4 }}",
    {% endif %}
    // For headings inside relative or absolute positioned containers within content.
    hasInnerContainers: true,
  });
});
