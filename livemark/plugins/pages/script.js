document.addEventListener("DOMContentLoaded", function () {
  const groups = $("#livemark-pages li.group");
  for (const group of groups) {
    $(group)
      .children("a")
      .click((ev) => {
        ev.preventDefault();
        $(group).toggleClass("active");
        // $(group).find(".fa").toggleClass("fa-chevron-right");
        // $(group).find(".fa").toggleClass("fa-chevron-down");
      });
  }
});
