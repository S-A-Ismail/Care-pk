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

  /* ---- Scroll reveal (progressive enhancement) ------------ */
  // The hidden state in CSS only applies under :root.js, which is added
  // here — so if this script never runs, all content stays visible.
  var revealSel = ".hero-inner, .section-title, .section-subtitle, .info-box, .card, " +
    ".feature-media, .feature-body, .flow-step, .partner-cat, .t-card, .quote-card, " +
    ".timeline-item, .team-member, .event-card, .acc-item, .donate-way, .amount-box, .anchor-nav";
  var revealEls = Array.prototype.slice.call(document.querySelectorAll(revealSel));
  if (revealEls.length) {
    document.documentElement.classList.add("js");
    var counts = (typeof Map !== "undefined") ? new Map() : null;
    revealEls.forEach(function (el) {
      el.setAttribute("data-animate", "");
      // Stagger by position within the same parent container.
      var i = 0;
      if (counts) { i = counts.get(el.parentElement) || 0; counts.set(el.parentElement, i + 1); }
      el.style.transitionDelay = (Math.min(i, 6) * 70) + "ms";
    });
    if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) { e.target.classList.add("in-view"); io.unobserve(e.target); }
        });
      }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
      revealEls.forEach(function (el) { io.observe(el); });
      // Failsafe: if nothing was revealed shortly after load (unusual
      // environments where the observer never fires), reveal everything so
      // content is never stuck hidden.
      setTimeout(function () {
        if (!document.querySelector("[data-animate].in-view")) {
          revealEls.forEach(function (el) { el.classList.add("in-view"); });
        }
      }, 1800);
    } else {
      revealEls.forEach(function (el) { el.classList.add("in-view"); });
    }
  }
})();
