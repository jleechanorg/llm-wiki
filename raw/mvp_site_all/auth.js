/* global firebase */
// Initialize Firebase immediately to avoid race conditions
const firebaseConfig = {
  apiKey: 'AIzaSyARs7IekRptvhZIwtV7lwJh3axWFsn_4c8',
  authDomain: 'worldarchitecture-ai.firebaseapp.com',
  projectId: 'worldarchitecture-ai',
  storageBucket: 'worldarchitecture-ai.firebasestorage.app',
  messagingSenderId: '754683067800',
  appId: '1:754683067800:web:3b38787c69de301c147fed',
  measurementId: 'G-EFX5VFZ7CV',
};

try {
  if (!firebase.apps.length) {
    firebase.initializeApp(firebaseConfig);
  }
} catch (e) {
  console.error('Error initializing Firebase:', e);
}

// Initialize globals immediately
let scheduleTokenRefresh;
let clearTokenRefreshTimer;

// Helper to check environment
const canEnableTestMode = () =>
  ['localhost', '127.0.0.1', '[::1]'].includes(window.location.hostname) ||
  window.__ALLOW_TEST_MODE__ === true;

// Capture test params on load (dev-only)
const initialUrlParams = new URLSearchParams(window.location.search);
const testModeEnabled = initialUrlParams.get('test_mode') === 'true';
const testUserId = initialUrlParams.get('test_user_id') || 'test-user-123';
const testUserEmail = initialUrlParams.get('test_user_email') || 'test@example.com';
if (testModeEnabled && canEnableTestMode()) {
  console.log('🔒 Test Mode Params Captured:', {
    enabled: true,
    userId: testUserId,
    email: testUserEmail,
  });
  window._testModeParams = { enabled: true, userId: testUserId, email: testUserEmail };
  // Alias for api.js compatibility
  window.testAuthBypass = window._testModeParams;
} else if (testModeEnabled) {
  console.warn('Test mode requested but disabled in this environment');
}

// Define header getter shared logic
const getBaseAuthHeaders = async (forceRefresh = false) => {
  const user = firebase.auth().currentUser;
  let token;

  if (user) {
    token = await user.getIdToken(forceRefresh);
  }

  if (!user) throw new Error('User not currently signed in');
  if (!token) throw new Error('Failed to retrieve valid token');

  return {
    Authorization: `Bearer ${token}`,
  };
};

// Initialize auth readiness promise
let resolveAuthInit;
const authInitPromise = new Promise((resolve) => {
  resolveAuthInit = resolve;
});

const getTestModeParams = () => {
  const currentParams = new URLSearchParams(window.location.search);
  const enabled =
    (currentParams.get('test_mode') === 'true' || window._testModeParams?.enabled) &&
    canEnableTestMode();
  const userId = currentParams.get('test_user_id') || window._testModeParams?.userId || 'test-user-123';
  const email = currentParams.get('test_user_email') || window._testModeParams?.email || 'test@example.com';
  return { enabled, userId, email };
};

window.authTokenManager = {
  // These will be assigned real implementations when DOMContentLoaded runs/firebase inits
  scheduleTokenRefresh: (user) => scheduleTokenRefresh && scheduleTokenRefresh(user),
  clearTokenRefreshTimer: () => clearTokenRefreshTimer && clearTokenRefreshTimer(),

  // Public API for waiting for auth to be ready
  waitForAuthInit: () => authInitPromise,

  // Unified method to get the current "active" user (Real or Test)
  // Waits for initialization automatically
  getEffectiveUser: async () => {
    await authInitPromise;
    const firebaseUser = firebase.auth().currentUser;
    if (firebaseUser) return firebaseUser;

    // Fallback to test user if in dev mode
    const { enabled, userId, email } = getTestModeParams();
    if (enabled) {
      console.log('Using Test User identity');
      return { uid: userId, email: email || 'test@example.com', isAnonymous: true, isTestUser: true };
    }
    return null;
  },

  getAuthHeaders: async (forceRefresh = false) => {
    const { enabled, userId, email } = getTestModeParams();

    if (enabled) {
      console.log('🔐 Using Test Mode Auth Bypass for user:', userId);
      return {
        'X-Test-Bypass-Auth': 'true',
        'X-Test-User-ID': userId,
        'X-Test-User-Email': email || 'test@example.com',
      };
    }

    return getBaseAuthHeaders(forceRefresh);
  },
  getCurrentUser: () => firebase.auth().currentUser,
};

document.addEventListener('DOMContentLoaded', () => {

  const auth = firebase.auth();
  const provider = new firebase.auth.GoogleAuthProvider();

  // Guard against missing elements on pages like settings.html
  const authContainer = document.getElementById('auth-container');

  let tokenRefreshTimeout = null;

  clearTokenRefreshTimer = () => {
    if (tokenRefreshTimeout) {
      clearTimeout(tokenRefreshTimeout);
      tokenRefreshTimeout = null;
    }
  };

  scheduleTokenRefresh = async (user) => {
    clearTokenRefreshTimer();
    if (!user) return;

    try {
      const tokenResult = await user.getIdTokenResult();
      const expirationTime = new Date(tokenResult.expirationTime).getTime();
      const now = Date.now();
      const refreshBufferMs = 5 * 60 * 1000; // Refresh 5 minutes before expiry
      const refreshIn = Math.max(0, expirationTime - now - refreshBufferMs);

      console.log(
        `🪙 Scheduling Firebase ID token refresh in ${Math.round(
          refreshIn / 1000,
        )}s (buffer ${refreshBufferMs / 60000}m)`,
      );

      tokenRefreshTimeout = setTimeout(async () => {
        try {
          console.log('🔄 Refreshing Firebase ID token before expiry');
          await user.getIdToken(true);
          await scheduleTokenRefresh(user); // Reschedule using new expiry
        } catch (error) {
          console.error('Failed to auto-refresh Firebase ID token:', error);
          // Retry in 1 minute to avoid leaving the user stranded
          tokenRefreshTimeout = setTimeout(() => scheduleTokenRefresh(user), 60000);
        }
      }, refreshIn);
    } catch (error) {
      console.error('Unable to schedule Firebase token refresh:', error);
      // Retry scheduling after a short delay in case of transient errors
      tokenRefreshTimeout = setTimeout(() => scheduleTokenRefresh(user), 60000);
    }
  };

  // getAuthHeaders removed from here as it's defined above

  const signIn = async () => {
    try {
      await auth.signInWithPopup(provider);
    } catch (e) {
      console.error('Sign-in error:', e);
    }
  };

  const getLoggedOutAuthMarkup = () => `
    <div class="welcome-screen">
      <div class="welcome-bg"></div>
      <div class="welcome-overlay"></div>
      <div class="welcome-vignette"></div>

      <div class="welcome-stars" aria-hidden="true">
        <div class="welcome-star" style="width:2px;height:2px;top:8%;left:12%;animation-delay:0s;animation-duration:2.8s"></div>
        <div class="welcome-star" style="width:1px;height:1px;top:15%;left:35%;animation-delay:0.5s;animation-duration:3.2s"></div>
        <div class="welcome-star" style="width:2px;height:2px;top:22%;left:68%;animation-delay:1s;animation-duration:2.5s"></div>
        <div class="welcome-star" style="width:1px;height:1px;top:6%;left:80%;animation-delay:0.2s;animation-duration:4s"></div>
        <div class="welcome-star" style="width:2px;height:2px;top:40%;left:5%;animation-delay:1.5s;animation-duration:3.5s"></div>
        <div class="welcome-star" style="width:1px;height:1px;top:55%;left:92%;animation-delay:0.8s;animation-duration:2.9s"></div>
        <div class="welcome-star" style="width:2px;height:2px;top:12%;left:55%;animation-delay:2s;animation-duration:3.1s"></div>
        <div class="welcome-star" style="width:1px;height:1px;top:30%;left:88%;animation-delay:0.3s;animation-duration:4.2s"></div>
      </div>

      <div class="welcome-card">
        <div class="welcome-logo">
          <span class="welcome-logo__icon" role="img" aria-label="Dragon">🐉</span>
          <h1 class="welcome-logo__name">WorldAI</h1>
        </div>

        <p class="welcome-tagline">Your AI-Powered Dungeon Master</p>

        <p class="welcome-desc">
          Epic AI-driven campaigns. Rich narrative. Infinite worlds.<br>
          Sign in to begin your adventure.
        </p>

        <button class="btn-google" id="signInBtn" type="button">
          <svg class="btn-google__icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
            <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
            <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
            <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.84z" fill="#FBBC05"/>
            <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
          </svg>
          Continue with Google
        </button>

        <p class="welcome-legal">
          By continuing you agree to our <a class="welcome-legal-link" href="/terms-of-use.html">Terms
            of Service</a> and <a class="welcome-legal-link" href="/privacy-policy.html">Privacy Policy</a>.
        </p>
      </div>
    </div>
  `;
  const signOut = async () => {
    try {
      await auth.signOut();
      window.location.href = '/';
    } catch (e) {
      console.error('Sign-out error:', e);
    }
  };

  // Attach the signOut function via delegation so it works when loaded via SPA
  document.addEventListener('click', (e) => {
    if (e.target && e.target.closest('#signOutBtnSettings')) {
      void signOut();
    }
  });

  auth.onAuthStateChanged(async (user) => {
    // Signal that auth has initialized (resolves the promise)
    if (resolveAuthInit) {
      resolveAuthInit();
      resolveAuthInit = null; // Only needs to be called once
    }

    const effectiveUser = user || await window.authTokenManager.getEffectiveUser();

    if (effectiveUser) {
      document.body.classList.remove('is-logged-out');
      document.body.classList.add('is-authenticated');
      // Just ensure we have a fresh token for internal state if needed
      if (user) {
        try {
          await user.getIdToken();
        } catch (e) {
          console.error('Failed to refresh token on auth state change:', e);
        }
      }

      if (user) {
        scheduleTokenRefresh(user);
      } else {
        clearTokenRefreshTimer();
      }
      // User is signed in, so the sign-in button should not be displayed.
      // We keep the container for layout purposes but ensure it's empty.
      if (authContainer) {
        authContainer.innerHTML = '';
      }
    } else {
      document.body.classList.remove('is-authenticated');
      document.body.classList.add('is-logged-out');
      // Cleanup auth-related storage
      localStorage.removeItem('redirect_after_login');
      clearTokenRefreshTimer();
      // User is signed out, show the splash page with sign-in button.
      if (authContainer) {
        authContainer.innerHTML = getLoggedOutAuthMarkup();
        const signInBtn = document.getElementById('signInBtn');
        if (signInBtn) signInBtn.onclick = signIn;
      }
    }
  });
});
