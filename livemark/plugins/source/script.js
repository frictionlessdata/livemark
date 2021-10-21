document.addEventListener("DOMContentLoaded", function () {
  for (const h2 of $("h2")) {
    $(h2).append(
      '<a href="" class="livemark-source-button">Show the Source</a>'
    );
  }
});
