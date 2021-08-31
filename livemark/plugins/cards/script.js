document.addEventListener("DOMContentLoaded", function () {
  for (const link of $("a")) {
    const href = $(link).attr("href");
    if (href.startsWith("#card=")) {
      const code = href.split("=")[1];
      $(link).click(() => {
        $("#livemark-cards .modal").modal();
      });
    }
  }
});
