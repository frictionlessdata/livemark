document.addEventListener("DOMContentLoaded", function () {
  const handlePopstate = async () => {
    const href = location.hash;
    if (href.startsWith("#card=")) {
      const code = href.split("=")[1];
      const response = await fetch(`/assets/cards/${code}.html`);
      const html = await response.text();
      $("#livemark-cards .modal-title").html("");
      $("#livemark-cards .modal-body").html(html);
      $("#livemark-cards h1").appendTo("#livemark-cards .modal-title");
      $("#livemark-cards .modal").modal();
      $("#livemark-cards .modal").on("hidden.bs.modal", () => {
        history.pushState("", document.title, window.location.pathname);
      });
    }
  };
  window.addEventListener("popstate", handlePopstate);
  handlePopstate();
});
