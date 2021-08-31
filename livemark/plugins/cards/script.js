document.addEventListener("DOMContentLoaded", function () {
  for (const link of $("a")) {
    const href = $(link).attr("href");
    if (href.startsWith("#card=")) {
      const code = href.split("=")[1];
      $(link).click(async () => {
        // TODO: handle errors
        const response = await fetch(`/assets/cards/${code}.html`);
        const html = await response.text();
        $("#livemark-cards .modal-body").html(html);
        $("#livemark-cards h1").appendTo("#livemark-cards .modal-title");
        $("#livemark-cards .modal").modal();
      });
    }
  }
});
