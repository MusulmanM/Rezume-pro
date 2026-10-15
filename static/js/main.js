/* My Rezume — progressive enhancement. The page works without this file. */
(function () {
  "use strict";

  var $ = function (sel, root) { return (root || document).querySelector(sel); };
  var $$ = function (sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); };
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var finePointer = window.matchMedia("(hover: hover) and (pointer: fine)").matches;

  /* ---------- Toast ---------- */
  var toast = $("#toast");
  var toastTimer = null;
  function showToast(text) {
    if (!toast) return;
    $(".toast__text", toast).textContent = text;
    toast.hidden = false;
    // restart the entry animation
    toast.style.animation = "none";
    void toast.offsetWidth;
    toast.style.animation = "";
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toast.hidden = true; }, 2400);
  }

  /* ---------- Clipboard ---------- */
  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text);
    }
    return new Promise(function (resolve, reject) {
      var area = document.createElement("textarea");
      area.value = text;
      area.setAttribute("readonly", "");
      area.style.position = "fixed";
      area.style.opacity = "0";
      document.body.appendChild(area);
      area.select();
      try {
        document.execCommand("copy") ? resolve() : reject(new Error("copy failed"));
      } catch (err) {
        reject(err);
      } finally {
        document.body.removeChild(area);
      }
    });
  }

  var copiedMsg = (document.documentElement.lang === "uz") ? "Xotiraga nusxalandi" : "Скопировано в буфер обмена";

  document.addEventListener("click", function (event) {
    var btn = event.target.closest("[data-copy], [data-copy-target]");
    if (!btn) return;
    var text = btn.getAttribute("data-copy");
    if (text === null) {
      var source = $(btn.getAttribute("data-copy-target"));
      text = source ? source.value : "";
    }
    if (!text) return;
    copyText(text).then(function () {
      btn.classList.add("is-copied");
      var label = $("span", btn);
      var original = label ? label.textContent : null;
      var copiedLabel = btn.getAttribute("data-copied-label");
      if (label && copiedLabel) label.textContent = copiedLabel;
      showToast(copiedMsg);
      setTimeout(function () {
        btn.classList.remove("is-copied");
        if (label && original !== null) label.textContent = original;
      }, 1800);
    }).catch(function () { /* clipboard blocked: nothing else to do */ });
  });

  /* ---------- Header: scrolled state, mobile menu, active link ---------- */
  var header = $("#site-header");
  var burger = $("#burger");
  var mobileNav = $("#mobile-nav");
  var toTop = $("#to-top");

  function onScroll() {
    var y = window.scrollY || window.pageYOffset;
    if (header) header.classList.toggle("is-scrolled", y > 8);
    if (toTop) toTop.hidden = y < 900;
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  function setMenu(open) {
    if (!burger || !mobileNav) return;
    burger.setAttribute("aria-expanded", String(open));
    mobileNav.hidden = !open;
    header.classList.toggle("is-open", open);
  }
  if (burger) {
    burger.addEventListener("click", function () {
      setMenu(burger.getAttribute("aria-expanded") !== "true");
    });
    $$("a", mobileNav).forEach(function (link) {
      link.addEventListener("click", function () { setMenu(false); });
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") setMenu(false);
    });
    window.addEventListener("resize", function () {
      if (window.innerWidth >= 1080) setMenu(false);
    });
  }

  if (toTop) {
    toTop.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: reduceMotion ? "auto" : "smooth" });
    });
  }

  // Keep the current section when switching language.
  $$("[data-lang-link]").forEach(function (link) {
    link.addEventListener("click", function () {
      if (window.location.hash) link.href = link.getAttribute("href").split("#")[0] + window.location.hash;
    });
  });

  var navLinks = $$(".nav a[data-nav]");
  if ("IntersectionObserver" in window && navLinks.length) {
    var sectionObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var id = entry.target.id;
        navLinks.forEach(function (a) {
          var active = a.getAttribute("data-nav") === id;
          a.classList.toggle("is-active", active);
          if (active) a.setAttribute("aria-current", "true"); else a.removeAttribute("aria-current");
        });
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    $$("[data-section]").forEach(function (s) { sectionObserver.observe(s); });
  }

  /* ---------- Reveal on scroll ---------- */
  var revealEls = $$("[data-reveal]");
  if (!("IntersectionObserver" in window) || reduceMotion) {
    revealEls.forEach(function (el) { el.classList.add("is-visible"); });
  } else {
    var revealObserver = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          obs.unobserve(entry.target);
        }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    revealEls.forEach(function (el) { revealObserver.observe(el); });
  }

  /* ---------- Metric count-up ---------- */
  function countUp(el) {
    var raw = el.getAttribute("data-count") || "";
    var match = raw.match(/^(\D*)(\d+(?:\.\d+)?)(.*)$/);
    if (!match || reduceMotion) return;
    var prefix = match[1], target = parseFloat(match[2]), suffix = match[3];
    var decimals = (match[2].split(".")[1] || "").length;
    var start = null, duration = 1400;
    function frame(ts) {
      if (start === null) start = ts;
      var p = Math.min((ts - start) / duration, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = prefix + (target * eased).toFixed(decimals) + suffix;
      if (p < 1) requestAnimationFrame(frame); else el.textContent = raw;
    }
    requestAnimationFrame(frame);
  }
  var counters = $$("[data-count]");
  if ("IntersectionObserver" in window && counters.length) {
    var countObserver = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { countUp(entry.target); obs.unobserve(entry.target); }
      });
    }, { threshold: 0.6 });
    counters.forEach(function (c) { countObserver.observe(c); });
  }

  /* ---------- Card spotlight ---------- */
  if (finePointer) {
    document.addEventListener("pointermove", function (e) {
      var card = e.target.closest && e.target.closest(".card--interactive");
      if (!card) return;
      var rect = card.getBoundingClientRect();
      card.style.setProperty("--mx", (e.clientX - rect.left) + "px");
      card.style.setProperty("--my", (e.clientY - rect.top) + "px");
    }, { passive: true });
  }

  /* ---------- Generic tabs (skills, architecture) ---------- */
  function setupTabs(tabs, onSelect) {
    if (!tabs.length) return;
    function select(tab, focus) {
      tabs.forEach(function (t) {
        var active = t === tab;
        t.classList.toggle("is-active", active);
        t.setAttribute("aria-selected", String(active));
        t.tabIndex = active ? 0 : -1;
        var panel = document.getElementById(t.getAttribute("aria-controls"));
        if (panel) panel.hidden = !active;
      });
      if (focus) tab.focus();
      if (onSelect) onSelect(tab);
    }
    tabs.forEach(function (tab, index) {
      tab.addEventListener("click", function () { select(tab, false); });
      tab.addEventListener("keydown", function (e) {
        var visible = tabs.filter(function (t) { return !t.classList.contains("is-filtered-out"); });
        var pos = visible.indexOf(tab);
        var next = null;
        if (e.key === "ArrowDown" || e.key === "ArrowRight") next = visible[(pos + 1) % visible.length];
        if (e.key === "ArrowUp" || e.key === "ArrowLeft") next = visible[(pos - 1 + visible.length) % visible.length];
        if (e.key === "Home") next = visible[0];
        if (e.key === "End") next = visible[visible.length - 1];
        if (next) { e.preventDefault(); select(next, true); }
      });
    });
    return select;
  }

  var skillTabs = $$(".skill-chip");
  var selectSkill = setupTabs(skillTabs);

  $$(".filter-tabs [data-filter]").forEach(function (btn, _, all) {
    btn.addEventListener("click", function () {
      var filter = btn.getAttribute("data-filter");
      all.forEach(function (b) {
        var active = b === btn;
        b.classList.toggle("is-active", active);
        b.setAttribute("aria-pressed", String(active));
      });
      var firstVisible = null;
      skillTabs.forEach(function (chip) {
        var show = filter === "all" || chip.getAttribute("data-category") === filter;
        chip.classList.toggle("is-filtered-out", !show);
        if (show && !firstVisible) firstVisible = chip;
      });
      var current = skillTabs.filter(function (c) { return c.classList.contains("is-active"); })[0];
      if (firstVisible && (!current || current.classList.contains("is-filtered-out"))) {
        selectSkill(firstVisible, false);
      }
    });
  });

  setupTabs($$(".layer"));

  /* ---------- Dialogs (project modals, video lightbox) ---------- */
  var lastTrigger = null;
  function openDialog(dialog) {
    if (!dialog || typeof dialog.showModal !== "function") return false;
    dialog.showModal();
    document.documentElement.classList.add("has-dialog");
    return true;
  }
  document.addEventListener("click", function (e) {
    var opener = e.target.closest("[data-open-dialog]");
    if (opener) {
      lastTrigger = opener;
      openDialog(document.getElementById(opener.getAttribute("data-open-dialog")));
      return;
    }
    var closer = e.target.closest("[data-close-dialog]");
    if (closer) {
      var dlg = closer.closest("dialog");
      if (dlg) dlg.close();
    }
  });
  $$("dialog").forEach(function (dialog) {
    // Click on the backdrop (outside the dialog box) closes it.
    dialog.addEventListener("click", function (e) {
      if (e.target !== dialog) return;
      var r = dialog.getBoundingClientRect();
      var inside = e.clientX >= r.left && e.clientX <= r.right && e.clientY >= r.top && e.clientY <= r.bottom;
      if (!inside) dialog.close();
    });
    dialog.addEventListener("close", function () {
      if (!$("dialog[open]")) document.documentElement.classList.remove("has-dialog");
      $$("video", dialog).forEach(function (v) { v.pause(); });
      if (lastTrigger && document.contains(lastTrigger)) lastTrigger.focus({ preventScroll: true });
    });
  });

  /* ---------- Hero video ---------- */
  var showcase = $("#showcase");
  var frame = $("#showcase-frame");
  var video = $("#hero-video");
  var fallback = $(".showcase__fallback");
  var playBtn = $("#video-play");
  var muteBtn = $("#video-mute");

  if (video) {
    var showFallback = function () {
      video.hidden = true;
      if (fallback) fallback.hidden = false;
      var controls = $(".showcase__controls");
      if (controls) controls.hidden = true;
    };
    video.addEventListener("error", showFallback);
    var source = video.currentSrc || video.src;
    if (!source) showFallback();

    var syncPlay = function () {
      if (!playBtn) return;
      var paused = video.paused;
      playBtn.classList.toggle("is-paused", paused);
      playBtn.setAttribute("aria-label", playBtn.getAttribute(paused ? "data-label-play" : "data-label-pause"));
    };
    video.addEventListener("play", syncPlay);
    video.addEventListener("playing", syncPlay);
    video.addEventListener("pause", syncPlay);
    if (reduceMotion) video.pause();
    var playPromise = video.paused || reduceMotion ? null : video.play();
    if (playPromise && playPromise.catch) playPromise.catch(syncPlay);
    syncPlay();

    if (playBtn) playBtn.addEventListener("click", function () {
      if (video.paused) video.play().catch(function () {}); else video.pause();
    });
    if (muteBtn) muteBtn.addEventListener("click", function () {
      video.muted = !video.muted;
      var on = !video.muted;
      muteBtn.setAttribute("aria-pressed", String(on));
      $(".ctrl__label", muteBtn).textContent = muteBtn.getAttribute(on ? "data-label-on" : "data-label-off");
      if (on && video.paused) video.play().catch(function () {});
    });

    var fsBtn = $("#video-fullscreen");
    var lightbox = $("#video-lightbox");
    var lightboxVideo = $("#lightbox-video");
    if (fsBtn && lightbox) fsBtn.addEventListener("click", function () {
      lastTrigger = fsBtn;
      if (!openDialog(lightbox)) return;
      if (lightboxVideo) {
        lightboxVideo.currentTime = video.currentTime || 0;
        lightboxVideo.muted = video.muted;
        lightboxVideo.play().catch(function () {});
      }
    });
  }

  $$("[data-shape-btn]").forEach(function (btn, _, all) {
    btn.addEventListener("click", function () {
      var shape = btn.getAttribute("data-shape-btn");
      if (showcase) showcase.setAttribute("data-shape", shape);
      all.forEach(function (b) {
        var active = b === btn;
        b.classList.toggle("is-active", active);
        b.setAttribute("aria-pressed", String(active));
      });
    });
  });

  if (frame && finePointer && !reduceMotion) {
    frame.addEventListener("mousemove", function (e) {
      var r = frame.getBoundingClientRect();
      var x = (e.clientX - r.left) / r.width - 0.5;
      var y = (e.clientY - r.top) / r.height - 0.5;
      frame.style.setProperty("--rx", (-y * 8).toFixed(2) + "deg");
      frame.style.setProperty("--ry", (x * 8).toFixed(2) + "deg");
    });
    frame.addEventListener("mouseleave", function () {
      frame.style.setProperty("--rx", "0deg");
      frame.style.setProperty("--ry", "0deg");
    });
  }

  /* ---------- Contact form ---------- */
  var form = $("#contact-form");
  if (form && window.fetch && window.FormData) {
    var statusBox = $("#form-status");
    var submitBtn = $(".contact-form__submit", form);
    var submitLabel = $(".btn__label", submitBtn);
    var defaultLabel = submitLabel.textContent;

    var setStatus = function (ok, text) {
      if (!statusBox) return;
      statusBox.hidden = false;
      statusBox.classList.toggle("form-status--success", ok);
      statusBox.classList.toggle("form-status--error", !ok);
      $(".form-status__text", statusBox).textContent = text;
    };
    var clearErrors = function () {
      $$(".field", form).forEach(function (f) { f.classList.remove("has-error"); });
      $$("[data-error-for]", form).forEach(function (p) { p.hidden = true; p.textContent = ""; });
      $$(".field__input", form).forEach(function (i) { i.removeAttribute("aria-invalid"); });
    };
    var showErrors = function (errors) {
      var first = null;
      Object.keys(errors || {}).forEach(function (name) {
        var input = form.elements[name];
        var box = $('[data-error-for="' + name + '"]', form);
        if (!input || !box) return;
        input.closest(".field").classList.add("has-error");
        input.setAttribute("aria-invalid", "true");
        box.textContent = errors[name][0];
        box.hidden = false;
        if (!first) first = input;
      });
      if (first) first.focus();
    };
    $$(".field__input", form).forEach(function (input) {
      input.addEventListener("input", function () {
        var field = input.closest(".field");
        if (!field.classList.contains("has-error")) return;
        field.classList.remove("has-error");
        input.removeAttribute("aria-invalid");
        var box = $('[data-error-for="' + input.name + '"]', form);
        if (box) box.hidden = true;
      });
    });

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (form.classList.contains("is-loading")) return;
      clearErrors();
      if (statusBox) statusBox.hidden = true;
      form.classList.add("is-loading");
      submitBtn.disabled = true;
      submitLabel.textContent = form.getAttribute("data-msg-sending");

      fetch(form.action, {
        method: "POST",
        body: new FormData(form),
        credentials: "same-origin",
        headers: { "X-Requested-With": "XMLHttpRequest", "Accept": "application/json" }
      })
        .then(function (res) {
          return res.json().catch(function () { return { ok: false }; }).then(function (data) {
            return { status: res.status, data: data };
          });
        })
        .then(function (result) {
          var data = result.data || {};
          if (data.ok) {
            form.reset();
            setStatus(true, data.message);
          } else {
            if (data.errors) showErrors(data.errors);
            setStatus(false, data.message || form.getAttribute("data-msg-error"));
          }
        })
        .catch(function () {
          setStatus(false, form.getAttribute("data-msg-error"));
        })
        .then(function () {
          form.classList.remove("is-loading");
          submitBtn.disabled = false;
          submitLabel.textContent = defaultLabel;
        });
    });
  }
})();
