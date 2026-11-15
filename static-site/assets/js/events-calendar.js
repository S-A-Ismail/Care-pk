/* ============================================================
   CARE: events calendar, upcoming/past split, event dialog
   Loaded (defer) on news-events.html only, after the vendored
   FullCalendar Standard bundle. Progressive enhancement: without
   JS every event is still listed as a plain card.

   Event status is never stored: it is computed here against
   today's date in Asia/Karachi, so the page cannot go stale.
   Dates in the data are inclusive; FullCalendar's all-day `end`
   is exclusive, so one day is added before handing it over.
   ============================================================ */
(function () {
  "use strict";

  var dataEl = document.getElementById("care-events-data");
  if (!dataEl) return;
  var EVENTS = [];
  try { EVENTS = JSON.parse(dataEl.textContent); } catch (e) { return; }
  var byId = {};
  EVENTS.forEach(function (ev) { byId[ev.id] = ev; });

  var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

  /* ---- Dates ---------------------------------------------- */
  function todayKarachi() {
    try {
      // en-CA formats as YYYY-MM-DD
      return new Intl.DateTimeFormat("en-CA", { timeZone: "Asia/Karachi", year: "numeric", month: "2-digit", day: "2-digit" }).format(new Date());
    } catch (e) {
      var d = new Date();
      return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate());
    }
  }
  function pad(n) { return (n < 10 ? "0" : "") + n; }
  function parts(iso) { var p = iso.split("-"); return { y: +p[0], m: +p[1], d: +p[2] }; }
  function addDay(iso) {
    var p = parts(iso), dt = new Date(Date.UTC(p.y, p.m - 1, p.d + 1));
    return dt.getUTCFullYear() + "-" + pad(dt.getUTCMonth() + 1) + "-" + pad(dt.getUTCDate());
  }
  function fmtDay(iso) { var p = parts(iso); return p.d + " " + MONTHS[p.m - 1] + " " + p.y; }
  function fmtRange(start, end) {   // en-GB, matches build.py
    end = end || start;
    var a = parts(start), b = parts(end);
    if (start === end) return fmtDay(start);
    if (a.y === b.y && a.m === b.m) return a.d + " to " + b.d + " " + MONTHS[a.m - 1] + " " + a.y;
    if (a.y === b.y) return a.d + " " + MONTHS[a.m - 1] + " to " + b.d + " " + MONTHS[b.m - 1] + " " + a.y;
    return fmtDay(start) + " to " + fmtDay(end);
  }

  var TODAY = todayKarachi();
  EVENTS.forEach(function (ev) { ev.status = (ev.end || ev.start) < TODAY ? "past" : "upcoming"; });
  var upcoming = EVENTS.filter(function (e) { return e.status === "upcoming"; })
    .sort(function (a, b) { return a.start < b.start ? -1 : a.start > b.start ? 1 : 0; });
  var past = EVENTS.filter(function (e) { return e.status === "past"; })
    .sort(function (a, b) { return (b.end || b.start) < (a.end || a.start) ? -1 : 1; });

  /* ---- Split the server-rendered cards into Upcoming / Past */
  var upList = document.querySelector("[data-events-upcoming]");
  var pastList = document.querySelector("[data-events-past]");
  var emptyMsg = document.querySelector("[data-events-empty]");
  var pastHeading = document.querySelector("[data-past-heading]");
  if (pastHeading) pastHeading.textContent = "Past Events";
  if (upList) {
    upcoming.forEach(function (ev) {
      var card = pastList && pastList.querySelector('[data-event-id="' + cssEsc(ev.id) + '"]');
      if (card) upList.appendChild(card);
    });
  }
  if (emptyMsg) emptyMsg.hidden = upcoming.length > 0;
  // Past events are grouped by year; hide a year whose events all moved to Upcoming.
  if (pastList) {
    pastList.querySelectorAll(".event-year-group").forEach(function (g) {
      g.hidden = !g.querySelector("[data-event-id]");
    });
  }
  if (pastList && !past.length) {
    var none = document.createElement("p");
    none.className = "events-empty";
    none.textContent = "No past events yet.";
    pastList.parentNode.insertBefore(none, pastList.nextSibling);
  }
  function cssEsc(s) { return String(s).replace(/["\\]/g, "\\$&"); }

  document.querySelectorAll("[data-event-open]").forEach(function (btn) {
    btn.hidden = false;
    btn.addEventListener("click", function () { openDialog(btn.getAttribute("data-event-open"), btn); });
  });

  /* ---- Default tab: Upcoming if any, else Past (unless the URL names a tab) */
  var tabsRoot = document.querySelector("[data-tabs]");
  function tabBtn(name) { return tabsRoot && tabsRoot.querySelector('.tab-btn[data-tab="' + name + '"]'); }
  var hash = (location.hash || "").replace("#", "");
  if (!(hash && tabBtn(hash))) {
    var def = tabBtn(upcoming.length ? "upcoming" : "past");
    if (def) def.click();
  }

  /* ---- Calendar (built lazily the first time its tab is shown) */
  var calEl = document.querySelector("[data-events-calendar]");
  var calPanel = calEl && calEl.closest(".tab-panel");
  var calendar = null, userChoseView = false;
  var mq = window.matchMedia ? window.matchMedia("(min-width: 720px)") : { matches: true };

  function initialDate() {
    if (upcoming.length) return upcoming[0].start;                // nearest upcoming
    if (past.length) return past[0].start;                        // most recent past
    return TODAY;
  }

  function buildCalendar() {
    if (calendar || !calEl || typeof FullCalendar === "undefined") return;
    calendar = new FullCalendar.Calendar(calEl, {
      locales: [{ code: "en-gb", week: { dow: 1, doy: 4 }, buttonText: { today: "Today", month: "Month", list: "List" } }],
      locale: "en-gb",
      initialView: mq.matches ? "dayGridMonth" : "listYear",
      initialDate: initialDate(),
      headerToolbar: { left: "prev,next today", center: "title", right: "dayGridMonth,listYear" },
      buttonText: { today: "Today", dayGridMonth: "Month", listYear: "List" },
      buttonHints: { prev: "Previous $0", next: "Next $0", today: "Go to today" },
      height: "auto",
      fixedWeekCount: false,
      dayMaxEvents: false,
      eventDisplay: "block",
      displayEventTime: false,          // all events are all-day; hides the "all-day" column in list view
      noEventsContent: "No events in this period.",
      events: EVENTS.map(function (ev) {
        return {
          id: ev.id, title: ev.title, start: ev.start, end: addDay(ev.end || ev.start), allDay: true,
          classNames: [ev.status === "past" ? "ev-past" : "ev-upcoming"],
          extendedProps: { status: ev.status }
        };
      }),
      eventContent: function (arg) {
        var nodes = [];
        if (arg.event.extendedProps.status === "past") {
          var tag = document.createElement("span");
          tag.className = "ev-tag"; tag.textContent = "Past";
          nodes.push(tag);
        }
        var t = document.createElement("span");
        t.className = "ev-title"; t.textContent = arg.event.title;
        nodes.push(t);
        return { domNodes: nodes };
      },
      eventDidMount: function (info) {
        // FullCalendar renders events without href, so make them keyboard operable.
        var ev = byId[info.event.id], el = info.el;
        el.setAttribute("tabindex", "0");
        el.setAttribute("role", "button");
        el.setAttribute("aria-label", ev.title + ", " + fmtRange(ev.start, ev.end) + (ev.status === "past" ? ", past event" : ", upcoming event") + ". Open details");
        el.addEventListener("keydown", function (e) {
          if (e.key === "Enter" || e.key === " ") { e.preventDefault(); openDialog(ev.id, el); }
        });
      },
      eventClick: function (info) {
        info.jsEvent.preventDefault();
        openDialog(info.event.id, info.el);
      },
      viewDidMount: function () {
        calEl.querySelectorAll(".fc-dayGridMonth-button, .fc-listYear-button").forEach(function (b) {
          if (!b._careBound) { b._careBound = true; b.addEventListener("click", function () { userChoseView = true; }); }
        });
      }
    });
    calendar.render();
    var onChange = function () {
      if (!userChoseView && calendar) calendar.changeView(mq.matches ? "dayGridMonth" : "listYear");
    };
    if (mq.addEventListener) mq.addEventListener("change", onChange);
    else if (mq.addListener) mq.addListener(onChange);
  }

  function maybeBuild() {
    if (calPanel && calPanel.classList.contains("active")) {
      buildCalendar();
      if (calendar) calendar.updateSize();
    }
  }
  if (calPanel && "MutationObserver" in window) {
    new MutationObserver(maybeBuild).observe(calPanel, { attributes: true, attributeFilter: ["class"] });
  }
  maybeBuild();

  /* ---- Dialog + gallery ----------------------------------- */
  var dlg = document.querySelector("[data-event-dialog]");
  if (!dlg) return;
  var $ = function (sel) { return dlg.querySelector(sel); };
  var stage = $("[data-gallery-stage]"), caption = $("[data-gallery-caption]"), counter = $("[data-gallery-counter]");
  var controls = $("[data-gallery-controls]"), prevBtn = $("[data-gallery-prev]"), nextBtn = $("[data-gallery-next]");
  var current = null, idx = 0, trigger = null;

  function icon(paths) {
    return '<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + paths + "</svg>";
  }
  var ICON = {
    calendar: '<rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>',
    clock: '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    pin: '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>'
  };
  function metaRow(ic, text) {
    var d = document.createElement("div");
    d.className = "event-meta";
    d.innerHTML = icon(ICON[ic]);
    d.appendChild(document.createTextNode(text));
    return d;
  }

  function openDialog(id, from) {
    var ev = byId[id];
    if (!ev) return;
    current = ev; idx = 0; trigger = from || document.activeElement;
    $("[data-dialog-status]").textContent = (ev.status === "past" ? "Past event" : "Upcoming event") + (ev.category ? " \u00b7 " + ev.category : "");
    $("[data-dialog-title]").textContent = ev.title;
    var meta = $("[data-dialog-meta]");
    meta.innerHTML = "";
    meta.appendChild(metaRow("calendar", fmtRange(ev.start, ev.end)));
    if (ev.time) meta.appendChild(metaRow("clock", ev.time));
    if (ev.location) meta.appendChild(metaRow("pin", ev.location));
    $("[data-dialog-summary]").textContent = ev.summary || "";
    renderSlide();
    if (typeof dlg.showModal === "function") dlg.showModal(); else dlg.setAttribute("open", "");
    $("[data-dialog-close]").focus();
  }

  function stopMedia() { stage.querySelectorAll("video").forEach(function (v) { try { v.pause(); } catch (e) {} }); }

  function renderSlide() {
    stopMedia();
    stage.innerHTML = "";
    var g = current.gallery || [];
    var galleryEl = $("[data-gallery]");
    if (galleryEl) galleryEl.hidden = !g.length;
    if (!g.length) {
      // No published photos for this event: show details only (no "coming soon" box).
      caption.textContent = "";
      controls.hidden = true;
      return;
    }
    var item = g[idx], node;
    if (item.type === "video") {
      node = document.createElement("video");
      node.controls = true; node.preload = "none"; node.playsInline = true;
      node.setAttribute("playsinline", "");
      node.poster = item.poster;
      node.width = item.width; node.height = item.height;
      node.setAttribute("aria-label", item.alt);
      var src = document.createElement("source");
      src.src = item.src; src.type = "video/mp4";
      node.appendChild(src);
    } else {
      node = document.createElement("img");
      node.src = item.src; node.alt = item.alt;
      node.width = item.width; node.height = item.height;
      node.decoding = "async";
    }
    stage.appendChild(node);
    caption.textContent = item.alt;
    controls.hidden = g.length < 2;
    counter.textContent = (idx + 1) + " / " + g.length;
    prevBtn.disabled = idx === 0;
    nextBtn.disabled = idx === g.length - 1;
  }

  function go(delta) {
    if (!current) return;
    var n = (current.gallery || []).length;
    var next = idx + delta;
    if (next < 0 || next >= n) return;
    idx = next;
    renderSlide();
  }
  prevBtn.addEventListener("click", function () { go(-1); });
  nextBtn.addEventListener("click", function () { go(1); });
  $("[data-dialog-close]").addEventListener("click", function () { dlg.close(); });

  // Click on the backdrop closes
  dlg.addEventListener("click", function (e) { if (e.target === dlg) dlg.close(); });

  dlg.addEventListener("close", function () {
    stopMedia();
    stage.innerHTML = "";
    if (trigger && document.contains(trigger)) { try { trigger.focus(); } catch (e) {} }
  });

  dlg.addEventListener("keydown", function (e) {
    if (e.key === "ArrowLeft" || e.key === "ArrowRight") {
      if (e.target && e.target.tagName === "VIDEO") return;   // let video controls seek
      e.preventDefault();
      go(e.key === "ArrowLeft" ? -1 : 1);
    } else if (e.key === "Tab") {
      // keep focus inside the dialog
      var f = Array.prototype.filter.call(
        dlg.querySelectorAll('button:not([disabled]), [href], video, [tabindex]:not([tabindex="-1"])'),
        function (el) { return !el.closest("[hidden]") && el.offsetParent !== null; });
      if (!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  });

  // Optional swipe on the gallery stage
  var sx = null;
  stage.addEventListener("pointerdown", function (e) { sx = e.clientX; });
  stage.addEventListener("pointerup", function (e) {
    if (sx === null) return;
    var dx = e.clientX - sx; sx = null;
    if (Math.abs(dx) > 50 && !(e.target && e.target.tagName === "VIDEO")) go(dx < 0 ? 1 : -1);
  });
})();
