var disqus_config = function () {
  this.page.url = "{{ plugin.link }}/{{ plugin.document.path }}.html";
  this.page.identifier = "{{ plugin.document.path }}";
};
(function () {
  // DON'T EDIT BELOW THIS LINE
  var d = document,
    s = d.createElement("script");
  s.src = "https://{{ plugin.code }}.disqus.com/embed.js";
  s.setAttribute("data-timestamp", +new Date());
  (d.head || d.body).appendChild(s);
})();
