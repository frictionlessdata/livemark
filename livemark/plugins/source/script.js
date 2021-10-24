document.addEventListener("DOMContentLoaded", function () {
  // Add buttons
  $("h2").append('<a href="" class="livemark-source-button">Source</a>');

  // Enable buttons
  $(".livemark-source-button").click(async (ev) => {
    ev.preventDefault();

    // Close open
    if ($(".livemark-source-section").length) {
      $(".livemark-source-section").remove();
      return;
    }

    // Load content
    let source = location.href.replace(".html", ".md");
    if (!source.endsWith(".md")) source = `${source}index.md`;
    const heading = $(ev.target).parent().contents().get(0).nodeValue;
    response = await fetch(source);
    content = await response.text();

    // Extract section
    let isCapture;
    const lines = [];
    for (const line of content.split(/\r?\n/)) {
      if (line.startsWith("##")) {
        isCapture = line.startsWith(`## ${heading}`) ? true : false;
        continue;
      }
      if (isCapture) {
        lines.push(line);
      }
    }
    const section = _.escape(lines.join("\n").trim());

    // Show section
    $(ev.target)
      .parent()
      .after(
        `<pre class="livemark-source-section" style="white-space: pre-wrap;">${section}</pre>`
      );
  });
});
