class ThemeManager {
  getDefaultTheme() {
    if (window.__WORLDAI_FANTASY_THEME_ENABLED === false) {
      return 'default';
    }
    return 'fantasy';
  }

  isFantasyThemeEnabled() {
    return this.getDefaultTheme() === 'fantasy';
  }

  isAllowedTheme(theme) {
    if (theme === 'fantasy') {
      return this.isFantasyThemeEnabled() || theme === window.__WORLDAI_THEME_BOOTSTRAP_THEME;
    }
    return theme === 'default';
  }

  constructor() {
    this.themes = {
      default: { name: 'Default', icon: '☀️' },
      fantasy: { name: 'Fantasy', icon: '⚔️' },
    };
    this.currentTheme = this.getDefaultTheme();
    this._themeMenuEl = null;
    this._themeMenuClickHandler = null;
    this.init();
  }

  init() {
    this.loadSavedTheme();
    this.setupEventListeners();
    this.updateThemeIcon();
  }

  loadSavedTheme() {
    // Migration: check for old localStorage key
    const oldKey = localStorage.getItem('preferred-theme');
    if (oldKey) {
      // Migrate old preference to new key only if no newer preference exists
      if (!localStorage.getItem('theme')) {
        localStorage.setItem('theme', oldKey);
      }
      localStorage.removeItem('preferred-theme');
    }

    const bootstrapTheme = window.__WORLDAI_THEME_BOOTSTRAP_THEME || this.getDefaultTheme();

    // Migration: convert old 'light' theme to 'default'
    const stored = localStorage.getItem('theme');
    if (stored === 'light') {
      localStorage.setItem('theme', 'default');
    }

    // Respect test_theme URL parameter (set by theme-bootstrap.js for dev/test use)
    const params = new URLSearchParams(window.location.search);
    const urlTheme = params.get('test_theme');
    if (urlTheme && this.themes[urlTheme]) {
      this.setTheme(urlTheme);
      return;
    }

    const resolved = (localStorage.getItem('theme') || bootstrapTheme || this.getDefaultTheme()).toLowerCase();
    this.setTheme(this.isAllowedTheme(resolved) ? resolved : this.getDefaultTheme());
    if (!stored) {
      localStorage.setItem('theme', this.currentTheme);
    }
  }

  setTheme(theme) {
    if (!this.themes[theme] || !this.isAllowedTheme(theme)) {
      theme = this.getDefaultTheme();
    }
    this.currentTheme = theme;
    localStorage.setItem('theme', theme);

    if (theme === 'fantasy') {
      document.documentElement.setAttribute('data-theme', 'fantasy');
    } else {
      document.documentElement.removeAttribute('data-theme');
    }

    this.updateThemeIcon();

    // Dispatch event for other components (e.g., component-enhancer)
    window.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme: theme } }));
  }

  setupEventListeners() {
    const themeMenu = document.getElementById('theme-menu');
    if (!themeMenu) return;

    this._themeMenuEl = themeMenu;
    this._themeMenuClickHandler = (e) => {
      const item = e.target.closest('[data-theme-menu-item]');
      if (item) {
        e.preventDefault();
        this.setTheme(item.getAttribute('data-theme-menu-item'));
      }
    };

    themeMenu.addEventListener('click', this._themeMenuClickHandler);
  }

  updateThemeIcon() {
    const icon = document.getElementById('current-theme-icon');
    if (icon) {
      icon.textContent = this.themes[this.currentTheme]?.icon || '☀️';
    }
  }

  destroy() {
    if (this._themeMenuEl && this._themeMenuClickHandler) {
      this._themeMenuEl.removeEventListener('click', this._themeMenuClickHandler);
    }
    this._themeMenuEl = null;
    this._themeMenuClickHandler = null;
  }
}

// Initialize theme manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  window.themeManager = new ThemeManager();
});
