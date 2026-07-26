/* ============================================================
   CARE static site — client-side search (vanilla JS)
   Uses a manually maintained index (assets/js/search-index.js,
   loaded as window.CARE_SEARCH_INDEX so it works from file://
   without any fetch/CORS issues). Simple case-insensitive
   substring matching over title + summary + keywords.
   ============================================================ */
(function () {
  "use strict";

  var input = document.querySelector("[data-search-input]");
  var results = document.querySelector("[data-search-results]");
  var index = window.CARE_SEARCH_INDEX || [];
  if (!input || !results) return;

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function render(matches, query) {
    if (!query) {
      results.innerHTML = '<div class="search-empty">Start typing to search pages…</div>';
      return;
    }
    if (!matches.length) {
      results.innerHTML = '<div class="search-empty">No pages match “' + escapeHtml(query) + '”.</div>';
      return;
    }
    results.innerHTML = matches.map(function (m) {
      return '<a href="' + m.url + '"><div class="r-title">' + escapeHtml(m.title) +
        '</div><div class="r-summary">' + escapeHtml(m.summary) + "</div></a>";
    }).join("");
  }

  function search(query) {
    var q = query.trim().toLowerCase();
    if (!q) { render([], ""); return; }
    var matches = index.filter(function (item) {
      var hay = (item.title + " " + item.summary + " " + (item.keywords || "")).toLowerCase();
      return hay.indexOf(q) !== -1;
    }).slice(0, 12);
    render(matches, query);
  }

  input.addEventListener("input", function () { search(input.value); });
  render([], "");
})();
