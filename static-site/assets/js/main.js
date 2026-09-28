/* ============================================================
   CARE static site — interactions (vanilla JS, no dependencies)
   All behaviour is progressive enhancement: the site is fully
   readable and forms still submit if this script fails to load.

   Several interactions are hand-ported from Watermelon UI
   (ui.watermelon.sh) components — Fluid Tabs, Card Split
   Accordion, Copy Confirm, Scroll Island, Command Search —
   whose originals are React + Motion. Each section below
   names the component it is ported from.
   ============================================================ */
(function () {
  "use strict";

  var FALLBACK_EMAIL = "carejmdc22@gmail.com";
  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var root = document.documentElement;
  root.classList.add("js");

  function $(sel, ctx) { return (ctx || document).querySelector(sel); }
  function $$(sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); }

  /* ---- Mobile nav toggle ---------------------------------- */
  var hamburger = $("[data-nav-toggle]");
  var mobileMenu = $("[data-mobile-menu]");
  if (hamburger && mobileMenu) {
    hamburger.addEventListener("click", function () {
      var open = mobileMenu.classList.toggle("open");
      hamburger.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  /* ---- Mobile submenu toggles (nav dropdowns) ------------- */
  $$(".m-toggle").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var item = btn.closest(".m-item");
      if (!item) return;
      var open = item.classList.toggle("open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
  });

  /* ---- Search dialog (Command Search) --------------------- */
  // Opens from the header button, "/" or Ctrl/⌘+K. Behaves as a
  // modal dialog: focus is trapped inside and returned on close.
  var searchOverlay = $("[data-search-overlay]");
  var searchInput = $("[data-search-input]");
  var lastFocus = null;

  function openSearch() {
    if (!searchOverlay || searchOverlay.classList.contains("open")) return;
    lastFocus = document.activeElement;
    searchOverlay.classList.add("open");
    document.body.style.overflow = "hidden";
    if (searchInput) { searchInput.focus(); searchInput.select(); }
  }
  function closeSearch() {
    if (!searchOverlay || !searchOverlay.classList.contains("open")) return;
    searchOverlay.classList.remove("open");
    document.body.style.overflow = "";
    if (lastFocus && lastFocus.focus) { lastFocus.focus(); }
  }
  $$("[data-search-open]").forEach(function (b) { b.addEventListener("click", openSearch); });
  $$("[data-search-close]").forEach(function (b) { b.addEventListener("click", closeSearch); });
  if (searchOverlay) {
    searchOverlay.addEventListener("click", function (e) { if (e.target === searchOverlay) { closeSearch(); } });
    searchOverlay.addEventListener("keydown", function (e) {
      if (e.key !== "Tab") return;
      var f = $$("input, button, a[href]", searchOverlay).filter(function (el) { return el.offsetParent !== null; });
      if (!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });
  }
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") { closeSearch(); closeIsland(); return; }
    var tag = (document.activeElement && document.activeElement.tagName) || "";
    var typing = tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT";
    if ((e.key === "k" || e.key === "K") && (e.metaKey || e.ctrlKey)) { e.preventDefault(); openSearch(); }
    else if (e.key === "/" && !typing) { e.preventDefault(); openSearch(); }
  });

  /* ---- FAQ accordion (Card Split Accordion) --------------- */
  // One item open at a time. Neighbour classes let CSS fuse the
  // closed items into one card and split the open one away.
  $$(".accordion").forEach(function (acc) {
    var items = $$(".acc-item", acc);
    acc.classList.add("is-split");
    function sync() {
      var openIdx = -1;
      items.forEach(function (it, i) {
        if ($(".acc-trigger", it).getAttribute("aria-expanded") === "true") { openIdx = i; }
      });
      items.forEach(function (it, i) {
        it.classList.toggle("is-open", i === openIdx);
        it.classList.toggle("before-open", openIdx > -1 && i === openIdx - 1);
        it.classList.toggle("after-open", openIdx > -1 && i === openIdx + 1);
      });
    }
    items.forEach(function (it) {
      var trigger = $(".acc-trigger", it);
      var panel = trigger.nextElementSibling;
      trigger.addEventListener("click", function () {
        var expanded = trigger.getAttribute("aria-expanded") === "true";
        items.forEach(function (other) {
          var t = $(".acc-trigger", other);
          t.setAttribute("aria-expanded", "false");
          t.nextElementSibling.style.maxHeight = null;
        });
        if (!expanded) {
          trigger.setAttribute("aria-expanded", "true");
          panel.style.maxHeight = panel.scrollHeight + "px";
        }
        sync();
      });
    });
    sync();
  });

  /* ---- Tabs (Fluid Tabs) ---------------------------------- */
  // A single pill slides to the selected tab on a spring; the
  // new label blur-flashes. Arrow keys move between tabs.
  $$("[data-tabs]").forEach(function (group) {
    var list = $(".tabs", group);
    var buttons = $$(".tab-btn", group);
    if (!list || !buttons.length) return;
    list.classList.add("is-fluid");
    var pill = document.createElement("span");
    pill.className = "fluid-pill no-anim";
    pill.setAttribute("aria-hidden", "true");
    list.insertBefore(pill, list.firstChild);

    function place() {
      var sel = buttons.filter(function (b) { return b.getAttribute("aria-selected") === "true"; })[0] || buttons[0];
      pill.style.width = sel.offsetWidth + "px";
      pill.style.transform = "translateX(" + sel.offsetLeft + "px)";
    }
    function select(btn, focus) {
      var target = btn.getAttribute("data-tab");
      buttons.forEach(function (b) {
        var on = b === btn;
        b.setAttribute("aria-selected", on ? "true" : "false");
        b.setAttribute("tabindex", on ? "0" : "-1");
      });
      $$(".tab-panel", group).forEach(function (panel) {
        panel.classList.toggle("active", panel.getAttribute("data-panel") === target);
      });
      btn.classList.remove("flash"); void btn.offsetWidth; btn.classList.add("flash");
      if (focus) { btn.focus(); }
      place();
    }
    buttons.forEach(function (btn, i) {
      btn.setAttribute("role", "tab");
      btn.setAttribute("tabindex", btn.getAttribute("aria-selected") === "true" ? "0" : "-1");
      btn.addEventListener("click", function () { select(btn); });
      btn.addEventListener("keydown", function (e) {
        var d = e.key === "ArrowRight" ? 1 : e.key === "ArrowLeft" ? -1 : 0;
        if (!d) return;
        e.preventDefault();
        select(buttons[(i + d + buttons.length) % buttons.length], true);
      });
    });
    place();
    requestAnimationFrame(function () { requestAnimationFrame(function () { pill.classList.remove("no-anim"); }); });
    window.addEventListener("resize", place);
    if (document.fonts && document.fonts.ready) { document.fonts.ready.then(place); }
    group._selectTab = select;
  });

  /* ---- Activate a tab from the URL hash (e.g. news-events.html#past) --- */
  function activateTabFromHash() {
    var h = (location.hash || "").replace("#", "");
    if (!h) return;
    $$("[data-tabs]").forEach(function (group) {
      var btn = $('.tab-btn[data-tab="' + h + '"]', group);
      if (btn) { btn.click(); }
    });
  }
  activateTabFromHash();
  window.addEventListener("hashchange", activateTabFromHash);

  /* ---- Sliding hover pill (Fluid Tabs, hover variant) ----- */
  // Used on the desktop nav and the section chips.
  function hoverPill(container, items) {
    if (!container || !items.length) return;
    container.classList.add("is-fluid");
    var pill = document.createElement("span");
    pill.className = "hover-pill";
    pill.setAttribute("aria-hidden", "true");
    container.insertBefore(pill, container.firstChild);
    var visible = false;
    function moveTo(el) {
      var c = container.getBoundingClientRect(), r = el.getBoundingClientRect();
      if (!visible) { pill.style.transition = "opacity .2s"; }
      pill.style.width = r.width + "px";
      pill.style.height = r.height + "px";
      pill.style.transform = "translate(" + (r.left - c.left) + "px," + (r.top - c.top) + "px)";
      if (!visible) { void pill.offsetWidth; pill.style.transition = ""; }
      pill.classList.add("show");
      visible = true;
    }
    items.forEach(function (el) {
      el.addEventListener("mouseenter", function () { moveTo(el); });
      el.addEventListener("focus", function () { moveTo(el); });
    });
    container.addEventListener("mouseleave", function () { pill.classList.remove("show"); visible = false; });
    container.addEventListener("focusout", function (e) {
      if (!container.contains(e.relatedTarget)) { pill.classList.remove("show"); visible = false; }
    });
  }
  hoverPill($(".nav-links"), $$(".nav-links > .nav-link, .nav-links > .nav-item > .nav-link"));
  $$(".anchor-nav").forEach(function (nav) { hoverPill(nav, $$("a", nav)); });

  /* ---- Copy buttons (Copy Confirm) ------------------------ */
  function setLabel(el, text) {
    el.innerHTML = "";
    text.split("").forEach(function (ch, i) {
      var s = document.createElement("span");
      s.className = "ch";
      s.style.setProperty("--i", i);
      s.textContent = ch === " " ? " " : ch;
      el.appendChild(s);
    });
  }
  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) { return navigator.clipboard.writeText(text); }
    return new Promise(function (resolve, reject) {
      var ta = document.createElement("textarea");
      ta.value = text; ta.setAttribute("readonly", ""); ta.style.position = "fixed"; ta.style.opacity = "0";
      document.body.appendChild(ta); ta.select();
      try { document.execCommand("copy") ? resolve() : reject(); } catch (err) { reject(err); }
      document.body.removeChild(ta);
    });
  }
  $$("[data-copy]").forEach(function (btn) {
    var label = $(".copy-label", btn);
    var idle = label ? label.textContent : "";
    var timer = null;
    btn.addEventListener("click", function () {
      copyText(btn.getAttribute("data-copy")).then(function () {
        btn.classList.add("copied");
        if (label) { setLabel(label, "Copied"); }
        clearTimeout(timer);
        timer = setTimeout(function () {
          btn.classList.remove("copied");
          if (label) { setLabel(label, idle); }
        }, 1800);
      }).catch(function () {
        if (label) { setLabel(label, "Press Ctrl+C"); }
      });
    });
  });

  /* ---- Upcoming events: hide ones whose date has passed ---- */
  // The site is static, so this runs in the visitor's browser.
  var today = new Date(); today.setHours(0, 0, 0, 0);
  $$("[data-events]").forEach(function (list) {
    var shown = 0;
    $$("[data-date]", list).forEach(function (card) {
      var d = new Date(card.getAttribute("data-date") + "T23:59:59");
      if (!isNaN(d) && d < today) { card.hidden = true; } else { shown++; }
    });
    var empty = $("[data-events-empty]", list.parentElement);
    if (empty) { empty.hidden = shown > 0; }
  });

  /* ---- Download bank details (client-side text file) ------ */
  var dlBtn = $("[data-download-bank]");
  if (dlBtn) {
    dlBtn.addEventListener("click", function () {
      var lines = ["CARE — Care, Aid & Rehabilitation in Emergency", "Bank Transfer Details", ""];
      $$("[data-bank] .bank-row").forEach(function (r) {
        var k = $(".k", r), v = $(".v", r);
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
     show an inline status message. Until a Formspree form ID is
     configured, submissions open the visitor's email app with
     the form contents pre-filled, so no enquiry is lost. */
  function fieldLabel(form, el) {
    var lab = el.id ? form.querySelector('label[for="' + el.id + '"]') : null;
    var t = lab ? lab.textContent : (el.getAttribute("aria-label") || el.name);
    return t.replace(/\*/g, "").trim();
  }
  function mailtoFallback(form, status) {
    var subject = "Website enquiry";
    var lines = [];
    $$("input, select, textarea", form).forEach(function (el) {
      if (!el.name || el.type === "submit") return;
      if (el.name === "_subject") { subject = el.value; return; }
      if (el.type === "hidden" || !el.value.trim()) return;
      if (el.name === "subject") { subject = el.value.trim(); }
      lines.push(fieldLabel(form, el) + ": " + el.value.trim());
    });
    var email = form.getAttribute("data-fallback-email") || FALLBACK_EMAIL;
    window.location.href = "mailto:" + email + "?subject=" + encodeURIComponent(subject) +
      "&body=" + encodeURIComponent(lines.join("\n"));
    if (status) {
      status.innerHTML = "Your email app should open with your message ready to send. If it doesn&rsquo;t, email us at " +
        '<a href="mailto:' + email + '" style="text-decoration:underline">' + email + "</a>.";
      status.className = "form-status success show";
    }
  }
  $$("form[data-ajax]").forEach(function (form) {
    var status = $(".form-status", form);
    form.addEventListener("submit", function (e) {
      var action = form.getAttribute("action") || "";
      e.preventDefault();
      if (action.indexOf("YOUR_FORM_ID") !== -1 || action === "") { mailtoFallback(form, status); return; }
      var data = new FormData(form);
      var btn = $("button[type=submit]", form);
      var original = btn ? btn.textContent : "";
      if (btn) { btn.disabled = true; btn.textContent = "Sending…"; }
      fetch(action, { method: "POST", body: data, headers: { Accept: "application/json" } })
        .then(function (res) {
          if (!res.ok) { throw new Error("Request failed"); }
          form.reset();
          if (status) { status.textContent = "Thank you — your message has been sent. We'll be in touch soon."; status.className = "form-status success show"; }
        })
        .catch(function () {
          if (status) { status.textContent = "Sorry, something went wrong. Please email us at " + FALLBACK_EMAIL + "."; status.className = "form-status error show"; }
        })
        .finally(function () {
          if (btn) { btn.disabled = false; btn.textContent = original; }
        });
    });
  });

  /* ---- Footer year --------------------------------------- */
  var yearEl = $("[data-year]");
  if (yearEl) { yearEl.textContent = new Date().getFullYear(); }

  /* ---- Blur-in headlines ---------------------------------- */
  $$(".hero h1, .page-banner h1").forEach(function (h) {
    if (h.children.length) return;
    var text = h.textContent;
    h.setAttribute("aria-label", text.trim());
    h.innerHTML = "";
    text.trim().split(/(\s+)/).forEach(function (part, i) {
      var s = document.createElement("span");
      s.className = "w";
      s.setAttribute("aria-hidden", "true");
      s.style.setProperty("--i", Math.floor(i / 2));
      s.textContent = part;
      h.appendChild(s);
    });
    h.classList.add("split-words");
  });

  /* ---- Number ticker -------------------------------------- */
  function tick(el) {
    var m = el.textContent.match(/^(\D*)([\d,]+)(.*)$/);
    if (!m || reduceMotion) return;
    var end = parseInt(m[2].replace(/,/g, ""), 10), start = null, dur = 1600;
    function frame(ts) {
      if (start === null) { start = ts; }
      var p = Math.min(1, (ts - start) / dur);
      var eased = 1 - Math.pow(1 - p, 4);
      el.textContent = m[1] + Math.round(end * eased).toLocaleString("en-US") + m[3];
      if (p < 1) { requestAnimationFrame(frame); }
    }
    requestAnimationFrame(frame);
  }

  /* ---- Spotlight cards (pointer-follow glow) -------------- */
  document.addEventListener("pointermove", function (e) {
    var card = e.target.closest && e.target.closest(".card");
    if (!card) return;
    var r = card.getBoundingClientRect();
    card.style.setProperty("--mx", (e.clientX - r.left) + "px");
    card.style.setProperty("--my", (e.clientY - r.top) + "px");
  }, { passive: true });

  /* ---- Scroll Island -------------------------------------- */
  // Floating "On this page" pill for long pages: a conic ring
  // shows reading progress and it expands into a section index.
  var island = null, islandBackdrop = null;
  function closeIsland() {
    if (!island) return;
    island.classList.remove("open");
    islandBackdrop.classList.remove("show");
    $(".si-head", island).setAttribute("aria-expanded", "false");
  }
  (function buildIsland() {
    var sections = $$("main section[id]").filter(function (s) { return $("h2", s); });
    if (sections.length < 4) return;
    var chev = '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><polyline points="18 15 12 9 6 15"/></svg>';
    island = document.createElement("nav");
    island.className = "scroll-island";
    island.setAttribute("aria-label", "On this page");
    var links = sections.map(function (s) {
      return '<a href="#' + s.id + '" data-si="' + s.id + '">' + $("h2", s).textContent.replace(/</g, "&lt;") + "</a>";
    }).join("");
    island.innerHTML =
      '<div class="si-panel">' +
      '<div class="si-body"><div class="si-list"><div class="si-list-inner">' + links + "</div></div></div>" +
      '<button type="button" class="si-head" aria-expanded="false">' +
      '<span class="si-ring" aria-hidden="true"></span><span class="si-label">On this page</span>' + chev +
      '<span class="si-pct" aria-hidden="true">0%</span></button>' +
      "</div>";
    islandBackdrop = document.createElement("div");
    islandBackdrop.className = "si-backdrop";
    document.body.appendChild(islandBackdrop);
    document.body.appendChild(island);

    var head = $(".si-head", island), ring = $(".si-ring", island), pct = $(".si-pct", island);
    var anchors = $$("[data-si]", island);
    head.addEventListener("click", function () {
      var open = island.classList.toggle("open");
      islandBackdrop.classList.toggle("show", open);
      head.setAttribute("aria-expanded", open ? "true" : "false");
    });
    islandBackdrop.addEventListener("click", closeIsland);
    // Get out of the way while someone is filling in a form.
    document.addEventListener("focusin", function (e) {
      island.classList.toggle("typing", !!(e.target.closest && e.target.closest("form")));
    });
    anchors.forEach(function (a) {
      a.addEventListener("click", function (e) {
        var sec = document.getElementById(a.getAttribute("data-si"));
        if (!sec) return;
        e.preventDefault();
        closeIsland();
        sec.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" });
        history.replaceState(null, "", "#" + sec.id);
        var h2 = $("h2", sec);
        h2.classList.remove("si-flash"); void h2.offsetWidth; h2.classList.add("si-flash");
      });
    });

    var ticking = false;
    function update() {
      ticking = false;
      var max = document.documentElement.scrollHeight - window.innerHeight;
      var p = max > 0 ? Math.min(100, Math.max(0, (window.scrollY / max) * 100)) : 0;
      ring.style.setProperty("--p", p + "%");
      pct.textContent = Math.round(p) + "%";
      island.classList.toggle("show", window.scrollY > 420);
      var current = null;
      sections.forEach(function (s) { if (s.getBoundingClientRect().top < window.innerHeight * 0.4) { current = s.id; } });
      anchors.forEach(function (a) { a.classList.toggle("active", a.getAttribute("data-si") === current); });
    }
    window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
    window.addEventListener("resize", update);
    update();
  })();

  /* ---- Scroll reveal (progressive enhancement) ------------ */
  // The hidden state in CSS only applies under :root.js, which is
  // added at the top of this script — so if it never runs, all
  // content stays visible.
  var revealSel = ".hero-inner, .section-title, .section-subtitle, .info-box, .card, " +
    ".feature-media, .feature-body, .flow-step, .partner-cat, .t-card, .quote-card, " +
    ".timeline-item, .team-member, .event-card, .donate-way, .amount-box, .anchor-nav, .soon-panel";
  var revealEls = $$(revealSel);
  var counters = $$("[data-count]");
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
        if (!e.isIntersecting) return;
        if (e.target.hasAttribute("data-count")) { tick(e.target); } else { e.target.classList.add("in-view"); }
        io.unobserve(e.target);
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
    revealEls.concat(counters).forEach(function (el) { io.observe(el); });
    // Failsafe: if nothing was revealed shortly after load (unusual
    // environments where the observer never fires), reveal everything so
    // content is never stuck hidden.
    setTimeout(function () {
      if (revealEls.length && !$("[data-animate].in-view")) {
        revealEls.forEach(function (el) { el.classList.add("in-view"); });
      }
    }, 1800);
  } else {
    revealEls.forEach(function (el) { el.classList.add("in-view"); });
  }
})();
