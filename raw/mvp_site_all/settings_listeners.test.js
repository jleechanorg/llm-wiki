const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

function makeElement(id) {
  return {
    id,
    handlers: {},
    value: '',
    textContent: '',
    type: 'text',
    checked: false,
    disabled: false,
    style: {},
    dataset: {},
    classList: {
      _set: new Set(),
      add(token) {
        this._set.add(token);
      },
      remove(token) {
        this._set.delete(token);
      },
      toggle(token, force) {
        if (force === true) {
          this._set.add(token);
          return true;
        }
        if (force === false) {
          this._set.delete(token);
          return false;
        }
        if (this._set.has(token)) {
          this._set.delete(token);
          return false;
        }
        this._set.add(token);
        return true;
      },
      contains(token) {
        return this._set.has(token);
      },
    },
    addEventListener(event, handler) {
      this.handlers[event] = handler;
    },
    removeEventListener(event) {
      delete this.handlers[event];
    },
    dispatchEvent(event) {
      const eventType = typeof event === 'string' ? event : event.type;
      const handler = this.handlers[eventType];
      if (typeof handler === 'function') {
        return handler({ target: this, type: eventType, ...event });
      }
      return undefined;
    },
    click() {
      return this.dispatchEvent({ type: 'click' });
    },
    focus() {
      return this.dispatchEvent({ type: 'focus' });
    },
    blur() {
      return this.dispatchEvent({ type: 'blur' });
    },
  };
}

function buildSettingsContext() {
  const documentHandlers = {};
  const windowHandlers = {};
  const elements = {
    geminiModel: makeElement('geminiModel'),
    openrouterModel: makeElement('openrouterModel'),
    cerebrasModel: makeElement('cerebrasModel'),
    openclawGatewayPort: makeElement('openclawGatewayPort'),
    openclawGatewayUrl: makeElement('openclawGatewayUrl'),
    openclawGatewayToken: makeElement('openclawGatewayToken'),
    'testOpenclawConnection': makeElement('testOpenclawConnection'),
    'openclaw-connection-status': makeElement('openclaw-connection-status'),
    'gemini-model-selection': makeElement('gemini-model-selection'),
    'openrouter-model-selection': makeElement('openrouter-model-selection'),
    'cerebras-model-selection': makeElement('cerebras-model-selection'),
    'openclaw-model-selection': makeElement('openclaw-model-selection'),
    debugModeSwitch: makeElement('debugModeSwitch'),
    factionMinigameSwitch: makeElement('factionMinigameSwitch'),
    'save-message': makeElement('save-message'),
    'error-message': makeElement('error-message'),
    geminiApiKey: makeElement('geminiApiKey'),
    openrouterApiKey: makeElement('openrouterApiKey'),
    cerebrasApiKey: makeElement('cerebrasApiKey'),
    toggleGeminiKey: makeElement('toggleGeminiKey'),
    toggleOpenrouterKey: makeElement('toggleOpenrouterKey'),
    toggleCerebrasKey: makeElement('toggleCerebrasKey'),
    geminiKeyIcon: makeElement('geminiKeyIcon'),
    openrouterKeyIcon: makeElement('openrouterKeyIcon'),
    cerebrasKeyIcon: makeElement('cerebrasKeyIcon'),
    clearGeminiKey: makeElement('clearGeminiKey'),
    clearOpenrouterKey: makeElement('clearOpenrouterKey'),
    clearCerebrasKey: makeElement('clearCerebrasKey'),
    clearOpenclawGatewayToken: makeElement('clearOpenclawGatewayToken'),
    'gemini-key-status': makeElement('gemini-key-status'),
    'openrouter-key-status': makeElement('openrouter-key-status'),
    'cerebras-key-status': makeElement('cerebras-key-status'),
    openclawGatewayTokenStatus: makeElement('openclawGatewayTokenStatus'),
    confirmationModal: makeElement('confirmationModal'),
    confirmationModalMessage: makeElement('confirmationModalMessage'),
    confirmationModalConfirm: makeElement('confirmationModalConfirm'),
    confirmationModalCancel: makeElement('confirmationModalCancel'),
  };

  const providerRadios = [
    makeElement('providerGemini'),
    makeElement('providerOpenrouter'),
    makeElement('providerOpenclaw'),
  ];
  providerRadios[0].value = 'gemini';
  providerRadios[0].checked = true;
  providerRadios[1].value = 'openrouter';
  providerRadios[2].value = 'openclaw';

  const documentStub = {
    visibilityState: 'visible',
    addEventListener(event, handler) {
      documentHandlers[event] = handler;
    },
    getElementById(id) {
      return elements[id] || null;
    },
    querySelectorAll(selector) {
      if (selector === 'input[name="llmProvider"]') {
        return providerRadios;
      }
      return [];
    },
    querySelector(selector) {
      if (selector === 'input[name="llmProvider"]:checked') {
        return providerRadios.find((radio) => radio.checked) || null;
      }
      return null;
    },
  };

  const context = {
    window: {
      addEventListener(event, handler) {
        windowHandlers[event] = handler;
      },
    },
    document: documentStub,
    console: {
      log() {},
      error() {},
      warn() {},
    },
    clearTimeout() {},
    setTimeout(fn) {
      const result = fn();
      context.__lastSavePromise = result;
      return 0;
    },
    fetch() {
      return Promise.resolve({
        ok: true,
        json: async () => ({ success: true }),
      });
    },
    __dispatchDocumentEvent(event) {
      const handler = documentHandlers[event];
      if (typeof handler === 'function') {
        handler();
      }
    },
    __dispatchWindowEvent(event) {
      const handler = windowHandlers[event];
      if (typeof handler === 'function') {
        handler();
      }
    },
  };

  return { context, elements, providerRadios };
}

function loadSettingsScript(context) {
  vm.createContext(context);
  const settingsPath = path.join(__dirname, '..', 'js', 'settings.js');
  const code = fs.readFileSync(settingsPath, 'utf8');
  vm.runInContext(code, context, { filename: settingsPath });
  context.loadSettings = () => {};
  context.showLoadingIndicator = () => {};
  context.showSaveMessage = () => {};
  context.showErrorMessage = () => {};
  context.window.authTokenManager = {
    getAuthHeaders: async () => ({ Authorization: 'Bearer test' }),
  };
}

test('settings schema covers all known settings controls', () => {
  const { context, elements } = buildSettingsContext();
  loadSettingsScript(context);

  const schema = context.window.SETTINGS_SCHEMA;
  const schemaKeys = new Set(schema.map((entry) => entry.key));
  const schemaIds = new Set(
    schema.filter((entry) => entry.id).map((entry) => entry.id),
  );
  const schemaNames = new Set(
    schema.filter((entry) => entry.name).map((entry) => entry.name),
  );

  const expectedControls = [
    { key: 'llm_provider', name: 'llmProvider' },
    { key: 'gemini_model', id: 'geminiModel' },
    { key: 'openrouter_model', id: 'openrouterModel' },
    { key: 'cerebras_model', id: 'cerebrasModel' },
    { key: 'openclaw_gateway_port', id: 'openclawGatewayPort' },
    { key: 'openclaw_gateway_url', id: 'openclawGatewayUrl' },
    { key: 'openclaw_gateway_token', id: 'openclawGatewayToken' },
    { key: 'debug_mode', id: 'debugModeSwitch' },
    { key: 'faction_minigame_enabled', id: 'factionMinigameSwitch' },
  ];

  expectedControls.forEach((control) => {
    assert.ok(schemaKeys.has(control.key));
    if (control.id) {
      assert.ok(schemaIds.has(control.id));
    }
    if (control.name) {
      assert.ok(schemaNames.has(control.name));
    }
  });

  const expectedKeys = expectedControls.map((control) => control.key).sort();
  assert.deepEqual(Array.from(schemaKeys).sort(), expectedKeys);
});

test('settings controls attach listeners for all schema entries', () => {
  const { context, elements, providerRadios } = buildSettingsContext();
  loadSettingsScript(context);

  assert.equal(typeof context.window.initializeSettingsControls, 'function');
  context.window.initializeSettingsControls();

  assert.equal(context.window.settingsListenersAttached, true);
  context.window.SETTINGS_SCHEMA.forEach((entry) => {
    if (entry.type === 'radio') {
      providerRadios.forEach((radio) => {
        assert.ok(radio.handlers.change);
      });
      return;
    }
    const element = elements[entry.id];
    assert.ok(element);
    assert.ok(element.handlers.change);
  });
});

test('settings controls reattach listeners after SPA DOM replacement', async () => {
  const { context, elements } = buildSettingsContext();
  loadSettingsScript(context);

  context.window.initializeSettingsControls();

  const replacementProviderRadios = [
    makeElement('providerGeminiReplacement'),
    makeElement('providerOpenrouterReplacement'),
    makeElement('providerOpenclawReplacement'),
  ];
  replacementProviderRadios[0].value = 'gemini';
  replacementProviderRadios[0].checked = true;
  replacementProviderRadios[1].value = 'openrouter';
  replacementProviderRadios[2].value = 'openclaw';

  const replacementIds = [
    'geminiModel',
    'openrouterModel',
    'cerebrasModel',
    'openclawGatewayPort',
    'openclawGatewayUrl',
    'openclawGatewayToken',
    'testOpenclawConnection',
    'debugModeSwitch',
    'factionMinigameSwitch',
    'geminiApiKey',
    'openrouterApiKey',
    'cerebrasApiKey',
    'toggleGeminiKey',
    'toggleOpenrouterKey',
    'toggleCerebrasKey',
    'clearGeminiKey',
    'clearOpenrouterKey',
    'clearCerebrasKey',
  ];
  replacementIds.forEach((id) => {
    elements[id] = makeElement(id);
  });

  context.document.querySelectorAll = (selector) => {
    if (selector === 'input[name="llmProvider"]') {
      return replacementProviderRadios;
    }
    return [];
  };
  context.document.querySelector = (selector) => {
    if (selector === 'input[name="llmProvider"]:checked') {
      return replacementProviderRadios.find((radio) => radio.checked) || null;
    }
    return null;
  };

  context.window.initializeSettingsControls();

  replacementProviderRadios[0].checked = false;
  replacementProviderRadios[1].checked = true;
  replacementProviderRadios[2].checked = false;
  replacementProviderRadios[1].dispatchEvent({ type: 'change' });
  assert.equal(
    elements['gemini-model-selection'].classList.contains('d-none'),
    true,
  );
  assert.equal(
    elements['openrouter-model-selection'].classList.contains('d-none'),
    false,
  );

  elements.geminiApiKey.value = '********';
  elements.geminiApiKey.dataset.hasKey = 'true';
  elements.geminiApiKey.focus();
  assert.equal(elements.geminiApiKey.value, '');

  elements.geminiApiKey.value = 'new-key-value';
  elements.geminiApiKey.dispatchEvent({ type: 'input' });
  elements.geminiApiKey.blur();
  if (context.__lastSavePromise) {
    await context.__lastSavePromise;
  }
  assert.equal(elements.geminiApiKey.dataset.byokDirty, 'true');

  elements.geminiApiKey.dataset.hasKey = 'false';
  elements.geminiApiKey.value = 'visible-key';
  elements.toggleGeminiKey.click();
  assert.equal(elements.geminiApiKey.dataset.keyVisible, 'true');
  elements.toggleGeminiKey.click();
  assert.equal(elements.geminiApiKey.dataset.keyVisible, 'false');

  elements.geminiApiKey.value = 'clear-me';
  elements.geminiApiKey.dataset.hasKey = 'true';
  context.window.confirm = () => true;
  context.confirm = context.window.confirm;
  context.fetch = async () => ({
    ok: true,
    text: async () => JSON.stringify({ success: true }),
    json: async () => ({ success: true }),
  });
  assert.ok(elements.clearGeminiKey.handlers.click);
  const clearPromise = elements.clearGeminiKey.handlers.click();
  if (clearPromise && typeof clearPromise.then === 'function') {
    await clearPromise;
  }
  await new Promise((resolve) => globalThis.setTimeout(resolve, 0));
  assert.equal(elements.geminiApiKey.value, '');
  assert.equal(elements.geminiApiKey.dataset.hasKey, 'false');
});

test('saveSettings includes all settings keys', async () => {
  const { context, elements } = buildSettingsContext();
  loadSettingsScript(context);

  elements.geminiModel.value = 'gemini-3-flash-preview';
  elements.openrouterModel.value = 'x-ai/grok-4.1-fast';
  elements.cerebrasModel.value = 'zai-glm-4.6';
  elements.debugModeSwitch.checked = true;
  elements.factionMinigameSwitch.checked = false;

  let requestBody = null;
  context.fetch = async (_url, options) => {
    requestBody = JSON.parse(options.body);
    return { ok: true, json: async () => ({ success: true }) };
  };

  await context.saveSettings();
  if (context.__lastSavePromise) {
    await context.__lastSavePromise;
  }

  assert.ok(requestBody);
  const expectedKeys = [];
  for (const entry of context.window.SETTINGS_SCHEMA) {
    expectedKeys.push(entry.key);
  }
  expectedKeys.sort();
  const expectedKeysToSend = expectedKeys.filter(
    (key) => key !== 'openclaw_gateway_token',
  );
  assert.deepEqual(Object.keys(requestBody).sort(), expectedKeysToSend);
  assert.equal(requestBody.llm_provider, 'gemini');
  assert.equal(requestBody.debug_mode, true);
  assert.equal(requestBody.faction_minigame_enabled, false);
});

test('saveSettings preserves server-loaded provider when radio selection is missing', async () => {
  const { context, providerRadios } = buildSettingsContext();
  loadSettingsScript(context);

  providerRadios[0].checked = false;
  providerRadios[1].checked = false;
  providerRadios[2].checked = false;
  context.window.__loadedSettings = { llm_provider: 'openclaw' };

  let requestBody = null;
  context.fetch = async (_url, options) => {
    requestBody = JSON.parse(options.body);
    return { ok: true, text: async () => JSON.stringify({ success: true }), json: async () => ({ success: true }) };
  };

  await context.saveSettings();
  if (context.__lastSavePromise) {
    await context.__lastSavePromise;
  }

  assert.ok(requestBody);
  assert.equal(requestBody.llm_provider, 'openclaw');
});

test('testOpenclawConnection sends provider settings payload', async () => {
  const { context, elements } = buildSettingsContext();
  loadSettingsScript(context);
  context.window.initializeSettingsControls();

  elements.openclawGatewayPort.value = '19999';
  elements.openclawGatewayUrl.value = 'https://gateway.example.test';
  elements.openclawGatewayToken.value = 'local-token-12345678';

  let requestBody = null;
  context.fetch = async (url, options) => {
    assert.equal(url, '/api/settings/test-openclaw-connection');
    requestBody = JSON.parse(options.body);
    return {
      ok: true,
      text: async () =>
        JSON.stringify({
          success: true,
          message: 'OpenClaw gateway connection succeeded',
          gateway_url: 'https://gateway.example.test',
          status_code: 200,
        }),
      json: async () => ({
        success: true,
        message: 'OpenClaw gateway connection succeeded',
        gateway_url: 'https://gateway.example.test',
        status_code: 200,
      }),
    };
  };

  assert.ok(elements.testOpenclawConnection.handlers.click);
  await elements.testOpenclawConnection.handlers.click();
  assert.ok(requestBody);
  assert.equal(requestBody.openclaw_gateway_port, '19999');
  assert.equal(requestBody.openclaw_gateway_url, 'https://gateway.example.test');
  assert.equal(requestBody.openclaw_gateway_token, 'local-token-12345678');
});

test('testOpenclawConnection omits masked token from payload', async () => {
  const { context, elements } = buildSettingsContext();
  loadSettingsScript(context);
  context.window.initializeSettingsControls();

  elements.openclawGatewayPort.value = '19999';
  elements.openclawGatewayUrl.value = 'https://gateway.example.test';
  elements.openclawGatewayToken.value = '********';

  let requestBody = null;
  let hasTokenField = false;
  context.fetch = async (url, options) => {
    assert.equal(url, '/api/settings/test-openclaw-connection');
    requestBody = JSON.parse(options.body);
    hasTokenField = Object.prototype.hasOwnProperty.call(
      requestBody,
      'openclaw_gateway_token',
    );
    return {
      ok: true,
      text: async () =>
        JSON.stringify({
          success: true,
          message: 'OpenClaw gateway connection succeeded',
          gateway_url: 'https://gateway.example.test',
          status_code: 200,
        }),
      json: async () => ({
        success: true,
        message: 'OpenClaw gateway connection succeeded',
        gateway_url: 'https://gateway.example.test',
        status_code: 200,
      }),
    };
  };

  assert.ok(elements.testOpenclawConnection.handlers.click);
  await elements.testOpenclawConnection.handlers.click();
  assert.ok(requestBody);
  assert.equal(hasTokenField, false);
  assert.equal(requestBody.openclaw_gateway_port, '19999');
  assert.equal(requestBody.openclaw_gateway_url, 'https://gateway.example.test');
});

test('saveSettings updates cached provider after successful save', async () => {
  const { context, providerRadios } = buildSettingsContext();
  loadSettingsScript(context);

  const requestBodies = [];
  providerRadios[0].checked = false;
  providerRadios[1].checked = true;
  context.window.__loadedSettings = { llm_provider: 'gemini' };

  context.fetch = async (_url, options) => {
    requestBodies.push(JSON.parse(options.body));
    return { ok: true, text: async () => JSON.stringify({ success: true }), json: async () => ({ success: true }) };
  };

  // First save should persist the currently selected provider.
  await context.saveSettings();
  if (context.__lastSavePromise) {
    await context.__lastSavePromise;
  }
  assert.equal(requestBodies[requestBodies.length - 1].llm_provider, 'openrouter');

  // Subsequent saves should reuse the cached provider when radios are unchecked.
  providerRadios[0].checked = false;
  providerRadios[1].checked = false;
  providerRadios[2].checked = false;

  await context.saveSettings();
  if (context.__lastSavePromise) {
    await context.__lastSavePromise;
  }

  assert.equal(requestBodies[requestBodies.length - 1].llm_provider, 'openrouter');
});

test('saveSettings falls back to default provider for invalid cached value', async () => {
  const { context, providerRadios } = buildSettingsContext();
  loadSettingsScript(context);

  let requestBody = null;
  providerRadios[0].checked = false;
  providerRadios[1].checked = false;
  providerRadios[2].checked = false;
  context.window.__loadedSettings = { llm_provider: 'not-a-provider' };

  context.fetch = async (_url, options) => {
    requestBody = JSON.parse(options.body);
    return { ok: true, text: async () => JSON.stringify({ success: true }), json: async () => ({ success: true }) };
  };

  await context.saveSettings();
  if (context.__lastSavePromise) {
    await context.__lastSavePromise;
  }

  assert.equal(requestBody.llm_provider, 'gemini');
});

test('saveSettings uses keepalive for navigation-safe persistence', async () => {
  const { context } = buildSettingsContext();
  loadSettingsScript(context);

  let requestOptions = null;
  context.fetch = async (_url, options) => {
    requestOptions = options;
    return { ok: true, json: async () => ({ success: true }) };
  };

  await context.saveSettings();
  if (context.__lastSavePromise) {
    await context.__lastSavePromise;
  }

  assert.ok(requestOptions);
  assert.equal(requestOptions.keepalive, true);
});

test('saveSettings suppresses unload-race fetch errors', async () => {
  const { context } = buildSettingsContext();
  loadSettingsScript(context);

  let showErrorCalls = 0;
  let consoleErrors = 0;
  context.showErrorMessage = () => {
    showErrorCalls += 1;
  };
  context.console.error = () => {
    consoleErrors += 1;
  };
  context.document.visibilityState = 'hidden';
  context.__dispatchDocumentEvent('visibilitychange');
  context.fetch = async () => {
    throw new TypeError('Failed to fetch');
  };

  await context.saveSettings();
  if (context.__lastSavePromise) {
    await context.__lastSavePromise;
  }

  assert.equal(showErrorCalls, 0);
  assert.equal(consoleErrors, 0);
});

test('extractErrorMessage supports nested error payloads', () => {
  const { context } = buildSettingsContext();
  loadSettingsScript(context);

  const response = { status: 400, statusText: 'Bad Request' };

  const nestedPayload = {
    error: { message: 'OpenRouter API key is invalid' },
  };
  assert.equal(
    context.extractErrorMessage(nestedPayload, response),
    'OpenRouter API key is invalid',
  );

  const objectPayload = { error: { detail: 'Missing key' } };
  assert.equal(context.extractErrorMessage(objectPayload, response), 'Missing key');
});

test('masked stored key reveal should fetch and enter visible text mode', async () => {
  const { context, elements } = buildSettingsContext();
  loadSettingsScript(context);
  context.setup_byok_event_listeners();
  context.fetch = async (url, options) => {
    if (url === '/api/settings/reveal-key') {
      const body = JSON.parse(options.body || '{}');
      assert.equal(body.provider, 'gemini');
      const payload = { success: true, provider: 'gemini', api_key: 'secret-gemini-key' };
      return {
        ok: true,
        text: async () => JSON.stringify(payload),
        json: async () => payload,
      };
    }
    return { ok: true, text: async () => JSON.stringify({ success: true }), json: async () => ({ success: true }) };
  };

  elements.geminiApiKey.type = 'text';
  elements.geminiApiKey.value = '********';
  elements.geminiApiKey.dataset.hasKey = 'true';
  elements.geminiApiKey.dataset.keyVisible = 'false';
  elements.geminiKeyIcon.classList.add('bi-eye');

  assert.ok(elements.toggleGeminiKey.handlers.click, 'toggle handler should be attached');
  await elements.toggleGeminiKey.handlers.click();
  assert.equal(elements.geminiApiKey.type, 'text');
  assert.equal(elements.geminiApiKey.dataset.keyVisible, 'true');
  assert.equal(elements.geminiApiKey.style.webkitTextSecurity, 'none');
  assert.equal(elements.geminiApiKey.value, 'secret-gemini-key');
  assert.equal(elements.geminiKeyIcon.classList.contains('bi-eye-slash'), true);
});

test('confirmation modal uses non-dimming backdrop options', async () => {
  const { context, elements } = buildSettingsContext();
  loadSettingsScript(context);

  let capturedOptions = null;
  context.window.bootstrap = {
    Modal: function Modal(_el, options) {
      capturedOptions = options || {};
      this.show = () => {};
      this.hide = () => {};
    },
  };

  const pending = context.show_confirmation_modal('Confirm key removal?');
  assert.ok(capturedOptions);
  assert.equal(capturedOptions.backdrop, false);
  assert.equal(elements.confirmationModal.style.backgroundColor, 'transparent');
  assert.equal(elements.confirmationModal.style.backdropFilter, 'none');

  assert.ok(elements.confirmationModalConfirm.handlers.click);
  elements.confirmationModalConfirm.handlers.click();
  const result = await pending;
  assert.equal(result, true);
});

function buildAuthContext({ search = '', effectiveUser = null } = {}) {
  const documentHandlers = {};
  const bodyClasses = new Set();
  const authContainer = { innerHTML: '' };
  const signOutBtnDashboard = {};
  let authStateHandler = null;

  const authObject = {
    currentUser: null,
    onAuthStateChanged(handler) {
      authStateHandler = handler;
    },
    signInWithPopup: async () => {},
    signOut: async () => {},
  };

  const context = {
    console: { log() {}, warn() {}, error() {} },
    URLSearchParams,
    localStorage: { removeItem() {} },
    setTimeout() { return 1; },
    clearTimeout() {},
    window: {
      location: { hostname: 'localhost', search },
      __ALLOW_TEST_MODE__: true,
    },
    document: {
      body: {
        classList: {
          add(token) { bodyClasses.add(token); },
          remove(token) { bodyClasses.delete(token); },
          contains(token) { return bodyClasses.has(token); },
        },
      },
      addEventListener(event, handler) {
        documentHandlers[event] = handler;
      },
      getElementById(id) {
        if (id === 'auth-container') return authContainer;
        if (id === 'signOutBtnDashboard') return signOutBtnDashboard;
        if (id === 'signInBtn') return { onclick: null };
        return null;
      },
    },
    firebase: {
      apps: [],
      initializeApp() {
        this.apps.push({});
      },
      auth() {
        return authObject;
      },
    },
  };

  context.firebase.auth.GoogleAuthProvider = function GoogleAuthProvider() {};
  vm.createContext(context);
  const authPath = path.join(__dirname, '..', 'auth.js');
  const code = fs.readFileSync(authPath, 'utf8');
  vm.runInContext(code, context, { filename: authPath });
  context.window.authTokenManager.getEffectiveUser = async () => effectiveUser;
  documentHandlers.DOMContentLoaded();

  return {
    bodyClasses,
    authContainer,
    triggerAuthState: async (user) => {
      await authStateHandler(user);
    },
  };
}

test('auth applies authenticated class for test-mode effective user without firebase user', async () => {
  const { bodyClasses, authContainer, triggerAuthState } = buildAuthContext({
    search: '?test_mode=true&test_user_id=test-user-42',
    effectiveUser: { uid: 'test-user-42', isTestUser: true },
  });

  await triggerAuthState(null);

  assert.equal(bodyClasses.has('is-authenticated'), true);
  assert.equal(bodyClasses.has('is-logged-out'), false);
  assert.equal(authContainer.innerHTML, '');
});

test('auth applies logged-out class when no effective user exists', async () => {
  const { bodyClasses, authContainer, triggerAuthState } = buildAuthContext({
    search: '',
    effectiveUser: null,
  });

  await triggerAuthState(null);

  assert.equal(bodyClasses.has('is-logged-out'), true);
  assert.equal(bodyClasses.has('is-authenticated'), false);
  assert.match(authContainer.innerHTML, /Welcome to WorldAI/);
});
