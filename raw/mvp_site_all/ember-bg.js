/* Ember particle background — ported from worldai_claw AmbientBackground */
(function () {
  var EMBER_COLORS = ['#ff6820', '#ff9500', '#ffc000', '#ff4000', '#e05000', '#ff7c10'];
  var EMBER_COUNT = 160;
  var ALPHA_MULTIPLIER = 0.55;
  var TARGET_FPS = 30;
  var FRAME_INTERVAL = 1000 / TARGET_FPS;

  function spawnParticle(w, h) {
    return {
      x:  Math.random() * w,
      y:  h + 5,
      r:  Math.random() * 1.8 + 0.3,
      vx: (Math.random() - 0.5) * 0.5,
      vy: -(Math.random() * 1.2 + 0.3),
      a:  Math.random() * 0.5 + 0.2,
      da: Math.random() * 0.003 + 0.001,
      c:  EMBER_COLORS[Math.floor(Math.random() * EMBER_COLORS.length)],
    };
  }

  function initParticles(w, h) {
    var particles = [];
    for (var i = 0; i < EMBER_COUNT; i++) {
      var p = spawnParticle(w, h);
      p.x = Math.random() * w;
      p.y = Math.random() * h;
      p.a = Math.random();
      particles.push(p);
    }
    return particles;
  }

  var canvas = document.getElementById('ember-bg-canvas');
  if (!canvas) return;

  // Guard: canvas 2D context may be unavailable (e.g. disabled GPU, privacy settings)
  var ctx = canvas.getContext('2d');
  if (!ctx) return;

  var particles = [];
  var animationId = null;
  var cachedGradient = null;
  var lastFrameTime = 0;

  function prefersReducedMotion() {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  function buildGradient() {
    var g = ctx.createLinearGradient(0, 0, 0, canvas.height);
    g.addColorStop(0, '#0a0a12');
    g.addColorStop(1, '#1a1520');
    cachedGradient = g;
  }

  // One-time static gradient draw for prefers-reduced-motion users.
  // No animation, no RAF — just a single fill to provide a themed background.
  function drawStatic() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    buildGradient();
    ctx.fillStyle = cachedGradient;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
  }

  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    buildGradient();
    particles = initParticles(canvas.width, canvas.height);
  }

  function draw() {
    var w = canvas.width;
    var h = canvas.height;

    // Use cached gradient — rebuilt only on resize
    ctx.fillStyle = cachedGradient;
    ctx.fillRect(0, 0, w, h);

    for (var i = 0; i < particles.length; i++) {
      var p = particles[i];
      p.x += p.vx;
      p.y += p.vy;
      p.a -= p.da;
      if (p.a <= 0 || p.y < -5) {
        particles[i] = spawnParticle(w, h);
        continue;
      }
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = p.c;
      ctx.globalAlpha = p.a * ALPHA_MULTIPLIER;
      ctx.fill();
    }
    ctx.globalAlpha = 1;
  }

  function animate(timestamp) {
    animationId = requestAnimationFrame(animate);
    if (timestamp - lastFrameTime < FRAME_INTERVAL) return;
    lastFrameTime = timestamp;
    draw();
  }

  function isFantasyTheme() {
    return document.documentElement.getAttribute('data-theme') === 'fantasy';
  }

  function start() {
    if (!isFantasyTheme()) return;
    if (prefersReducedMotion()) {
      drawStatic();
      return;
    }
    resize();
    if (!animationId) animationId = requestAnimationFrame(animate);
  }

  function stop() {
    if (animationId) {
      cancelAnimationFrame(animationId);
      animationId = null;
    }
    ctx.clearRect(0, 0, canvas.width, canvas.height);
  }

  window.addEventListener('resize', function () {
    if (!isFantasyTheme()) return;
    // Resize even if animationId is null (e.g., tab was hidden) to keep canvas dimensions correct.
    // When reduced-motion is active, redraw the static gradient at the new dimensions.
    if (prefersReducedMotion()) {
      drawStatic();
    } else {
      resize();
    }
  });

  // Respect dynamic changes to prefers-reduced-motion
  var motionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
  // addEventListener not supported in older Safari/WebKit; fallback to addListener
  function onMotionChange() {
    if (motionQuery.matches) {
      // Reduced motion turned ON: cancel animation and draw static gradient instead of blank canvas.
      if (animationId) {
        cancelAnimationFrame(animationId);
        animationId = null;
      }
      if (isFantasyTheme()) drawStatic();
    } else if (isFantasyTheme()) {
      start();
    }
  }

  if (motionQuery.addEventListener) {
    motionQuery.addEventListener('change', onMotionChange);
  } else if (motionQuery.addListener) {
    // Legacy fallback for older browsers
    motionQuery.addListener(onMotionChange);
  }

  // Pause animation when tab is not visible (performance optimization)
  // Also resize canvas in case window was resized while tab was hidden
  document.addEventListener('visibilitychange', function () {
    if (document.hidden) {
      if (animationId) {
        cancelAnimationFrame(animationId);
        animationId = null;
      }
    } else if (isFantasyTheme() && !prefersReducedMotion()) {
      resize(); // Resize in case window changed while tab was hidden
      lastFrameTime = 0; // Reset to allow immediate draw on visibility change
      if (!animationId) animationId = requestAnimationFrame(animate);
    }
  });

  var observer = new MutationObserver(function () {
    if (isFantasyTheme()) {
      if (!animationId) start();
    } else {
      stop();
    }
  });
  observer.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }
})();
