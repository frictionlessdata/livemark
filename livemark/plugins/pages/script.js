document.addEventListener("DOMContentLoaded", function () {
  const groups = $("#livemark-pages a.group");
  for (const group of groups) {
    $(group).click((ev) => {
      ev.preventDefault();
      $(group).toggleClass("active");
      $(group).find(".fa").toggleClass("fa-chevron-right");
      $(group).find(".fa").toggleClass("fa-chevron-down");
    });
  }
});
