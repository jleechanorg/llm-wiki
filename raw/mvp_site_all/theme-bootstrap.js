(function () {
  // Supported themes - add new themes here
  var THEMES = ['fantasy', 'default'];

  function toBoolean(value) {
    if (value === null || value === undefined) {
      return null;
    }
    var normalized = String(value).toLowerCase();
    if (normalized === '1' || normalized === 'true' || normalized === 'yes' || normalized === 'on') {
      return true;
    }
    if (normalized === '0' || normalized === 'false' || normalized === 'no' || normalized === 'off') {
      return false;
    }
    return null;
  }

  function isFantasyThemeEnabled() {
    var params = new URLSearchParams(window.location.search);
    var queryValue = toBoolean(params.get('fantasy_theme'));
    if (queryValue !== null) {
      return queryValue;
    }

    queryValue = toBoolean(params.get('enable_fantasy_theme'));
    if (queryValue !== null) {
      return queryValue;
    }

    queryValue = toBoolean(localStorage.getItem('worldai_fantasy_theme_enabled'));
    if (queryValue !== null) {
      return queryValue;
    }

    // Default to enabled so current PR behavior remains visible by default.
    return true;
  }

  // First check URL parameter (for dev/test use)
  var params = new URLSearchParams(window.location.search);
  var testTheme = params.get('test_theme');
  var fantasyEnabled = isFantasyThemeEnabled();
  window.__WORLDAI_FANTASY_THEME_ENABLED = fantasyEnabled;

  // Handle async CSS loading (CSP-compliant alternative to inline onload handlers)
  function activateAsyncCSS() {
    var asyncLinks = document.querySelectorAll('link[data-async-css]');
    for (var i = 0; i < asyncLinks.length; i++) {
      asyncLinks[i].media = 'all';
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', activateAsyncCSS);
  } else {
    activateAsyncCSS();
  }

  if (testTheme && THEMES.indexOf(testTheme) !== -1) {
    if (testTheme === 'fantasy') {
      document.documentElement.setAttribute('data-theme', 'fantasy');
    } else {
      document.documentElement.removeAttribute('data-theme');
    }
    window.__WORLDAI_THEME_BOOTSTRAP_THEME = testTheme;
    return;
  }

  // Then check localStorage
  var storedTheme = localStorage.getItem('theme') || localStorage.getItem('preferred-theme');
  if (storedTheme === 'fantasy' && fantasyEnabled) {
    document.documentElement.setAttribute('data-theme', 'fantasy');
  } else if (storedTheme === 'default') {
    // Keep explicit default (light) preference as non-fantasy.
    document.documentElement.removeAttribute('data-theme');
  } else if (storedTheme === 'light') {
    // Legacy "light" preference preserved for compatibility with older sessions.
    document.documentElement.removeAttribute('data-theme');
    localStorage.removeItem('theme');
    localStorage.setItem('theme', 'default');
  } else if (storedTheme && storedTheme !== 'fantasy') {
    localStorage.removeItem('theme');
    storedTheme = null;
  } else {
    // First-time users and migration edge cases use the rollout-controlled default.
    if (fantasyEnabled) {
      document.documentElement.setAttribute('data-theme', 'fantasy');
    } else {
      document.documentElement.removeAttribute('data-theme');
    }
  }

  window.__WORLDAI_FANTASY_THEME_ENABLED = fantasyEnabled;
  window.__WORLDAI_THEME_BOOTSTRAP_THEME = document.documentElement.getAttribute('data-theme') === 'fantasy' ? 'fantasy' : 'default';
})();
