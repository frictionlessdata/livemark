document.addEventListener("DOMContentLoaded", function () {
  const left = document.getElementById("livemark-left");
  const mobile = document.getElementById("livemark-mobile");
  mobile.addEventListener("click", () => {
    left.classList.toggle("active");
    mobile.classList.toggle("active");
  });
  left.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      if (left.classList.contains("active")) {
        left.classList.remove("active");
        mobile.classList.remove("active");
      }
    });
  });
});
