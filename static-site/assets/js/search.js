/* ============================================================
   CARE static site — client-side search (vanilla JS)
   Uses a generated index (assets/js/search-index.js, loaded as
   window.CARE_SEARCH_INDEX so it works from file:// without any
   fetch/CORS issues). Simple case-insensitive substring matching
   over title + summary + keywords.

   Result list ported from Watermelon UI's Command Search:
   grouped sections, ↑/↓ to move, Enter to open, suggestions
   shown before typing.
   ============================================================ */
(function () {
  "use strict";

  var input = document.querySelector("[data-search-input]");
  var results = document.querySelector("[data-search-results]");
  var index = window.CARE_SEARCH_INDEX || [];
  if (!input || !results) return;

  var SUGGESTED = ["donate.html", "get-involved.html", "programs.html", "contact.html"];
  var ARROW = '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>';
  var active = 0;

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function item(m, i) {
    return '<a class="r-item" id="sr-' + i + '" role="option" href="' + escapeHtml(m.url) + '">' +
      '<span class="r-ico">' + ARROW + '</span>' +
      '<span class="r-text"><div class="r-title">' + escapeHtml(m.title) + '</div>' +
      '<div class="r-summary">' + escapeHtml(m.summary) + '</div></span>' +
      '<kbd aria-hidden="true">Enter</kbd></a>';
  }

  function render(groups, query) {
    var total = groups.reduce(function (n, g) { return n + g.items.length; }, 0);
    if (!total) {
      results.innerHTML = '<div class="search-empty">No pages match “' + escapeHtml(query) + '”.</div>';
      input.removeAttribute("aria-activedescendant");
      return;
    }
    var i = 0;
    results.innerHTML = groups.map(function (g) {
      return '<div class="search-group">' + g.name + '</div>' +
        g.items.map(function (m) { return item(m, i++); }).join("");
    }).join("");
    setActive(0);
  }

  function links() { return Array.prototype.slice.call(results.querySelectorAll(".r-item")); }

  function setActive(i) {
    var all = links();
    if (!all.length) return;
    active = (i + all.length) % all.length;
    all.forEach(function (a, j) { a.classList.toggle("is-active", j === active); a.setAttribute("aria-selected", j === active ? "true" : "false"); });
    input.setAttribute("aria-activedescendant", all[active].id);
    all[active].scrollIntoView({ block: "nearest" });
  }

  function search(query) {
    var q = query.trim().toLowerCase();
    if (!q) {
      var sugg = SUGGESTED.map(function (u) {
        return index.filter(function (it) { return it.url === u; })[0];
      }).filter(Boolean);
      render([{ name: "Suggested", items: sugg }, {
        name: "All pages",
        items: index.filter(function (it) { return SUGGESTED.indexOf(it.url) === -1; })
      }], "");
      return;
    }
    var matches = index.filter(function (it) {
      var hay = (it.title + " " + it.summary + " " + (it.keywords || "")).toLowerCase();
      return hay.indexOf(q) !== -1;
    }).slice(0, 12);
    render([{ name: "Pages", items: matches }], query);
  }

  input.addEventListener("input", function () { search(input.value); });
  input.addEventListener("keydown", function (e) {
    if (e.key === "ArrowDown") { e.preventDefault(); setActive(active + 1); }
    else if (e.key === "ArrowUp") { e.preventDefault(); setActive(active - 1); }
    else if (e.key === "Enter") {
      var a = links()[active];
      if (a) { e.preventDefault(); window.location.href = a.getAttribute("href"); }
    }
  });
  results.addEventListener("mousemove", function (e) {
    var a = e.target.closest && e.target.closest(".r-item");
    if (!a) return;
    var i = links().indexOf(a);
    if (i !== active) { setActive(i); }
  });
  search("");
})();
