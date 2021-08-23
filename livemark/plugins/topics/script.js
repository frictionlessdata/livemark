document.addEventListener("DOMContentLoaded", function () {
  tocbot.init({
    // Where to render the table of contents.
    tocSelector: ".toc",
    // Where to grab the headings to build the table of contents.
    contentSelector: "#livemark-main",
    // Which headings to grab inside of the contentSelector element.
    headingSelector: "{{ plugin.selector }}",
    // For headings inside relative or absolute positioned containers within content.
    hasInnerContainers: true,
    // Called each time a heading is parsed. Expects a string in return.
    headingLabelCallback: (label) => label.replace(/(^#|#$)/g, "").trim(),
  });
});
