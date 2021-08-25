document.addEventListener("DOMContentLoaded", function () {
  const left = document.getElementById("livemark-left");
  const mobile = document.getElementById("livemark-mobile");
  mobile.addEventListener("click", () => {
    left.classList.toggle("active");
    mobile.classList.toggle("active");
  });
  // NOTE: We can replace the selector by 'a:not[href=""]' after #57
  left.querySelectorAll("li:not(.group) a").forEach((link) => {
    link.addEventListener("click", () => {
      if (left.classList.contains("active")) {
        left.classList.remove("active");
        mobile.classList.remove("active");
      }
    });
  });
});
