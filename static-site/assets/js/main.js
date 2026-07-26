/* ============================================================
   CARE static site — interactions (vanilla JS, no dependencies)
   All behaviour is progressive enhancement: the site is fully
   readable and forms still submit if this script fails to load.
   ============================================================ */
(function () {
  "use strict";

  /* ---- Mobile nav toggle ---------------------------------- */
  var hamburger = document.querySelector("[data-nav-toggle]");
  var mobileMenu = document.querySelector("[data-mobile-menu]");
  if (hamburger && mobileMenu) {
    hamburger.addEventListener("click", function () {
      var open = mobileMenu.classList.toggle("open");
      hamburger.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  /* ---- Search overlay ------------------------------------- */
  var searchOverlay = document.querySelector("[data-search-overlay]");
  var searchOpenBtns = document.querySelectorAll("[data-search-open]");
  var searchClose = document.querySelector("[data-search-close]");
  var searchInput = document.querySelector("[data-search-input]");

  function openSearch() {
    if (!searchOverlay) return;
    searchOverlay.classList.add("open");
    if (searchInput) { searchInput.focus(); }
  }
  function closeSearch() {
    if (!searchOverlay) return;
    searchOverlay.classList.remove("open");
  }
  searchOpenBtns.forEach(function (b) { b.addEventListener("click", openSearch); });
  if (searchClose) { searchClose.addEventListener("click", closeSearch); }
  if (searchOverlay) {
    searchOverlay.addEventListener("click", function (e) {
      if (e.target === searchOverlay) { closeSearch(); }
    });
  }
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") { closeSearch(); }
  });

  /* ---- FAQ accordion -------------------------------------- */
  document.querySelectorAll(".acc-trigger").forEach(function (trigger) {
    trigger.addEventListener("click", function () {
      var expanded = trigger.getAttribute("aria-expanded") === "true";
      var panel = trigger.nextElementSibling;
      trigger.setAttribute("aria-expanded", expanded ? "false" : "true");
      if (panel) {
        panel.style.maxHeight = expanded ? null : panel.scrollHeight + "px";
      }
    });
  });

  /* ---- Tabs (news & events, etc.) ------------------------- */
  document.querySelectorAll("[data-tabs]").forEach(function (group) {
    var buttons = group.querySelectorAll(".tab-btn");
    buttons.forEach(function (btn) {
      btn.addEventListener("click", function () {
        var target = btn.getAttribute("data-tab");
        buttons.forEach(function (b) { b.setAttribute("aria-selected", "false"); });
        btn.setAttribute("aria-selected", "true");
        group.querySelectorAll(".tab-panel").forEach(function (panel) {
          panel.classList.toggle("active", panel.getAttribute("data-panel") === target);
        });
      });
    });
  });

  /* ---- Donate amount selection ---------------------------- */
  document.querySelectorAll("[data-amounts] .amount-btn").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var wrap = btn.closest("[data-amounts]");
      wrap.querySelectorAll(".amount-btn").forEach(function (b) { b.classList.remove("selected"); });
      btn.classList.add("selected");
    });
  });

  /* ---- Download bank details (client-side text file) ------ */
  var dlBtn = document.querySelector("[data-download-bank]");
  if (dlBtn) {
    dlBtn.addEventListener("click", function () {
      var rows = document.querySelectorAll("[data-bank] .bank-row");
      var lines = ["CARE — Care, Aid & Rehabilitation in Emergency", "Bank Transfer Details", ""];
      rows.forEach(function (r) {
        var k = r.querySelector(".k"), v = r.querySelector(".v");
        if (k && v) { lines.push(k.textContent.trim() + ": " + v.textContent.trim()); }
      });
      var blob = new Blob([lines.join("\n")], { type: "text/plain" });
      var url = URL.createObjectURL(blob);
      var a = document.createElement("a");
      a.href = url; a.download = "CARE-bank-details.txt";
      document.body.appendChild(a); a.click(); document.body.removeChild(a);
      URL.revokeObjectURL(url);
    });
  }

  /* ---- Form submission (progressive enhancement) ---------- */
  /* Forms carry a plain action="" + method="POST" so they still
     work without JS. When JS is present we submit via fetch and
     show an inline status message instead of a full page redirect. */
  document.querySelectorAll("form[data-ajax]").forEach(function (form) {
    var status = form.querySelector(".form-status");
    form.addEventListener("submit", function (e) {
      var action = form.getAttribute("action") || "";
      // If the Formspree ID hasn't been filled in yet, don't pretend it sent.
      if (action.indexOf("YOUR_FORM_ID") !== -1 || action === "") {
        e.preventDefault();
        if (status) {
          status.textContent = "This form isn't connected yet — add your Formspree form ID to enable submissions.";
          status.className = "form-status error show";
        }
        return;
      }
      e.preventDefault();
      var data = new FormData(form);
      var btn = form.querySelector("button[type=submit]");
      var original = btn ? btn.textContent : "";
      if (btn) { btn.disabled = true; btn.textContent = "Sending…"; }
      fetch(action, { method: "POST", body: data, headers: { Accept: "application/json" } })
        .then(function (res) {
          if (res.ok) {
            form.reset();
            if (status) { status.textContent = "Thank you — your message has been sent. We'll be in touch soon."; status.className = "form-status success show"; }
          } else {
            throw new Error("Request failed");
          }
        })
        .catch(function () {
          if (status) { status.textContent = "Sorry, something went wrong. Please email us at carejmdc22@gmail.com."; status.className = "form-status error show"; }
        })
        .finally(function () {
          if (btn) { btn.disabled = false; btn.textContent = original; }
        });
    });
  });

  /* ---- Footer year --------------------------------------- */
  var yearEl = document.querySelector("[data-year]");
  if (yearEl) { yearEl.textContent = new Date().getFullYear(); }
})();
