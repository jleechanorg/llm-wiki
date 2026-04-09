/**
 * Settings page JavaScript functionality
 * Handles model selection with auto-save, debouncing, and error handling
 */
/* global firebase */

let settingsPageUnloading = false;
if (window && typeof window.addEventListener === "function") {
  window.addEventListener("beforeunload", () => {
    settingsPageUnloading = true;
  });
  document.addEventListener("visibilitychange", () => {
    if (document.visibilityState === "hidden") {
      settingsPageUnloading = true;
    } else {
      settingsPageUnloading = false;
    }
  });
}

// Consolidated settings initialization logic.
// This is used for both direct page load and SPA navigation.
window.initializeSettingsControls = function () {
  console.log("Initializing settings controls...");
  attachSettingsListeners();
  setup_byok_event_listeners();
  loadSettings();
};

document.addEventListener("DOMContentLoaded", function () {
  console.log("Settings page loaded");
  window.initializeSettingsControls();
});

// BYOK: Setup event listeners for API keys, toggle buttons, and clear buttons.
// This is extracted into a function so it can be called during SPA navigation.
function logByokBindingSnapshot(stage) {
  const providers = [
    { provider: "gemini", inputId: "geminiApiKey", toggleId: "toggleGeminiKey" },
    {
      provider: "openrouter",
      inputId: "openrouterApiKey",
      toggleId: "toggleOpenrouterKey",
    },
    {
      provider: "cerebras",
      inputId: "cerebrasApiKey",
      toggleId: "toggleCerebrasKey",
    },
    {
      provider: "openclaw",
      inputId: "openclawGatewayToken",
      toggleId: "toggleOpenclawGatewayToken",
    },
  ];

  const snapshot = providers.map(({ provider, inputId, toggleId }) => {
    const input = document.getElementById(inputId);
    const toggle = document.getElementById(toggleId);
    return {
      provider,
      inputExists: !!input,
      toggleExists: !!toggle,
      inputByokBound: input?.dataset?.byokBound || "",
      toggleByokBound: toggle?.dataset?.byokBound || "",
      inputDisabled: !!input?.disabled,
      inputType: input?.type || "",
      inputHasKey: input?.dataset?.hasKey || "",
      valueLen: (input?.value || "").length,
    };
  });

  console.log(`[BYOK_BINDING] ${stage}`, snapshot);
}

function setup_byok_event_listeners() {
  console.log("Setting up BYOK event listeners...");
  logByokBindingSnapshot("before_attach");

  // BYOK: API key input handlers - use blur for auto-save
  const inputs = [
    { id: "geminiApiKey", key: "gemini" },
    { id: "openrouterApiKey", key: "openrouter" },
    { id: "cerebrasApiKey", key: "cerebras" },
    { id: "openclawGatewayToken", key: "openclawGatewayToken" },
  ];

  inputs.forEach(({ id }) => {
    const input = document.getElementById(id);
    if (input) {
      if (input.dataset.byokBound === "true") {
        console.log(`[BYOK_BINDING] skip input already bound: ${id}`);
        return;
      }
      input.dataset.byokBound = "true";
      console.log(`[BYOK_BINDING] bound input listeners: ${id}`);

      let valueBeforeEdit = "";
      input.addEventListener("focus", () => {
        valueBeforeEdit = input.value;
        input.dataset.byokDirty = "false";

        if (
          input.dataset.hasKey === "true" &&
          input.value === MASKED_API_KEY_PLACEHOLDER
        ) {
          input.value = "";
        }
      });
      input.addEventListener("input", () => {
        input.dataset.byokDirty = "true";
      });
      input.addEventListener("blur", async (event) => {
        const val = event.target.value.trim();
        const wasDirty = input.dataset.byokDirty === "true";

        if (
          !wasDirty &&
          input.dataset.hasKey === "true" &&
          valueBeforeEdit === MASKED_API_KEY_PLACEHOLDER
        ) {
          input.value = MASKED_API_KEY_PLACEHOLDER;
          return;
        }

        // Only save if val is not empty (use clear button for that), and changed
        if (
          wasDirty &&
          val &&
          val !== valueBeforeEdit &&
          val !== MASKED_API_KEY_PLACEHOLDER
        ) {
          await saveSettings({ keyChanged: true });
        }
        // Note: byokDirty is reset by loadSettings() after successful save
      });
      input.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
          e.preventDefault();
          input.blur();
        }
      });
    }
  });

  // BYOK: Toggle visibility buttons
  const toggles = [
    {
      btnId: "toggleGeminiKey",
      inputId: "geminiApiKey",
      iconId: "geminiKeyIcon",
      provider: "gemini",
    },
    {
      btnId: "toggleOpenrouterKey",
      inputId: "openrouterApiKey",
      iconId: "openrouterKeyIcon",
      provider: "openrouter",
    },
    {
      btnId: "toggleCerebrasKey",
      inputId: "cerebrasApiKey",
      iconId: "cerebrasKeyIcon",
      provider: "cerebras",
    },
    {
      btnId: "toggleOpenclawGatewayToken",
      inputId: "openclawGatewayToken",
      iconId: "openclawGatewayTokenIcon",
      provider: "openclaw",
    },
  ];

  toggles.forEach(({ btnId, inputId, iconId, provider }) => {
    const btn = document.getElementById(btnId);
    if (btn) {
      if (btn.dataset.byokBound === "true") {
        console.log(`[BYOK_BINDING] skip toggle already bound: ${btnId}`);
        return;
      }
      btn.dataset.byokBound = "true";
      console.log(
        `[BYOK_BINDING] bound toggle listener: ${btnId} provider=${provider}`,
      );

      btn.addEventListener("click", async () => {
        const input = document.getElementById(inputId);
        console.log(
          `[BYOK_CLICK] toggle fired provider=${provider} btn=${btnId} input=${inputId} ` +
            `bound=${btn.dataset.byokBound} disabled=${!!input?.disabled} hasKey=${input?.dataset?.hasKey || ""} ` +
            `type=${input?.type || ""} valueLen=${(input?.value || "").length}`,
        );
        await toggle_api_key_visibility(inputId, iconId, provider);
        const afterInput = document.getElementById(inputId);
        console.log(
          `[BYOK_CLICK] toggle completed provider=${provider} input=${inputId} ` +
            `type=${afterInput?.type || ""} valueLen=${(afterInput?.value || "").length}`,
        );
      });
    }
  });

  // BYOK: Clear key buttons
  const clears = [
    {
      btnId: "clearGeminiKey",
      inputId: "geminiApiKey",
      setting: "gemini_api_key",
      status: "gemini-key-status",
    },
    {
      btnId: "clearOpenrouterKey",
      inputId: "openrouterApiKey",
      setting: "openrouter_api_key",
      status: "openrouter-key-status",
    },
    {
      btnId: "clearCerebrasKey",
      inputId: "cerebrasApiKey",
      setting: "cerebras_api_key",
      status: "cerebras-key-status",
    },
    {
      btnId: "clearOpenclawGatewayToken",
      inputId: "openclawGatewayToken",
      setting: "openclaw_gateway_token",
      status: "openclawGatewayTokenStatus",
    },
  ];

  clears.forEach(({ btnId, inputId, setting, status }) => {
    const btn = document.getElementById(btnId);
    if (btn) {
      if (btn.dataset.byokBound === "true") {
        console.log(`[BYOK_BINDING] skip clear already bound: ${btnId}`);
        return;
      }
      btn.dataset.byokBound = "true";
      console.log(`[BYOK_BINDING] bound clear listener: ${btnId}`);

      btn.addEventListener("click", () => {
        clear_api_key(inputId, setting, status);
      });
    }
  });

  const testButton = document.getElementById("testOpenclawConnection");
  if (testButton) {
    if (testButton.dataset.byokBound !== "true") {
      testButton.dataset.byokBound = "true";
      testButton.addEventListener("click", testOpenclawConnection);
    }
  }

  console.log("BYOK event listeners attached");
  logByokBindingSnapshot("after_attach");
  window.dumpByokBindings = () => logByokBindingSnapshot("manual_dump");
}

function setApiKeyFieldVisible(input, icon, visible) {
  if (!input || !icon) {
    return;
  }
  input.dataset.keyVisible = visible ? "true" : "false";
  // Keep type=text to avoid browser password manager heuristics.
  input.style.webkitTextSecurity = visible ? "none" : "disc";
  if (visible) {
    icon.classList.remove("bi-eye");
    icon.classList.add("bi-eye-slash");
  } else {
    icon.classList.remove("bi-eye-slash");
    icon.classList.add("bi-eye");
  }
}

let saveTimeout = null;
let pendingKeyChange = false;
let lastKnownProvider = null;
const MASKED_API_KEY_PLACEHOLDER = "********";
const DEFAULT_OPENROUTER_MODEL = "meta-llama/llama-3.1-70b-instruct";
// Keep this aligned with backend `mvp_site/constants.py` DEFAULT_CEREBRAS_MODEL.
const DEFAULT_CEREBRAS_MODEL = "qwen-3-235b-a22b-instruct-2507";
const DEFAULT_GEMINI_MODEL = "gemini-3-flash-preview"; // Gemini 3 Flash (Dec 2025)
const DEFAULT_OPENCLAW_GATEWAY_PORT = 18789;

const GEMINI_MODEL_MAPPING = {
  "gemini-3-flash-preview": "gemini-3-flash-preview", // New default (Dec 2025)
  "gemini-2.0-flash": "gemini-2.0-flash",
  // Legacy compatibility - redirect 2.5 and Pro users to Gemini 3 Flash
  "gemini-3-pro-preview": "gemini-3-flash-preview",
  "gemini-2.5-flash": "gemini-3-flash-preview",
  "gemini-2.5-pro": "gemini-3-flash-preview",
  "pro-2.5": "gemini-3-flash-preview",
  "flash-2.5": "gemini-3-flash-preview",
};
let pendingAuthReload = false;

const SETTINGS_SCHEMA = [
  {
    key: "llm_provider",
    type: "radio",
    name: "llmProvider",
    allowed: ["gemini", "openrouter", "cerebras", "openclaw"],
    defaultValue: "gemini",
    required: true,
    onChange: (value) => toggleProviderSections(value),
  },
  {
    key: "gemini_model",
    type: "select",
    id: "geminiModel",
    defaultValue: DEFAULT_GEMINI_MODEL,
    normalize: (value) => GEMINI_MODEL_MAPPING[value] || DEFAULT_GEMINI_MODEL,
  },
  {
    key: "openrouter_model",
    type: "select",
    id: "openrouterModel",
    defaultValue: DEFAULT_OPENROUTER_MODEL,
  },
  {
    key: "cerebras_model",
    type: "select",
    id: "cerebrasModel",
    defaultValue: DEFAULT_CEREBRAS_MODEL,
  },
  {
    key: "openclaw_gateway_port",
    type: "number",
    id: "openclawGatewayPort",
    defaultValue: DEFAULT_OPENCLAW_GATEWAY_PORT,
    normalize: (value) => value,
  },
  {
    key: "openclaw_gateway_url",
    type: "text",
    id: "openclawGatewayUrl",
    defaultValue: "",
  },
  {
    key: "openclaw_gateway_token",
    type: "text",
    id: "openclawGatewayToken",
    defaultValue: "",
  },
  {
    key: "debug_mode",
    type: "switch",
    id: "debugModeSwitch",
    defaultValue: false,
  },
  {
    key: "faction_minigame_enabled",
    type: "switch",
    id: "factionMinigameSwitch",
    defaultValue: false,
  },
];
window.SETTINGS_SCHEMA = SETTINGS_SCHEMA;

function getRadioGroup(name) {
  return Array.from(document.querySelectorAll(`input[name="${name}"]`));
}

function getSelectedRadioValue(name) {
  const selected = document.querySelector(`input[name="${name}"]:checked`);
  return selected ? selected.value : null;
}

function setRadioGroupValue(name, value) {
  const radios = getRadioGroup(name);
  radios.forEach((radio) => {
    radio.checked = radio.value === value;
  });
}

function setSelectValue(selectEl, value, fallback) {
  if (!selectEl) {
    return;
  }
  if (selectEl.options && selectEl.options.length > 0) {
    const hasOption = Array.from(selectEl.options).some(
      (opt) => opt.value === value,
    );
    selectEl.value = hasOption ? value : fallback;
    return;
  }
  selectEl.value = value ?? fallback;
}

function getElementsForEntry(entry) {
  if (entry.type === "radio") {
    return getRadioGroup(entry.name);
  }
  const element = document.getElementById(entry.id);
  return element ? [element] : [];
}

function setEntryDisabled(entry, disabled) {
  const elements = getElementsForEntry(entry);
  elements.forEach((element) => {
    element.disabled = disabled;
  });
}

function getOpenclawGatewayPayload() {
  const openclawPortInput = document.getElementById("openclawGatewayPort");
  const openclawUrlInput = document.getElementById("openclawGatewayUrl");
  const openclawTokenInput = document.getElementById("openclawGatewayToken");

  const rawToken = openclawTokenInput ? openclawTokenInput.value.trim() : "";
  const hasMaskedToken = rawToken === MASKED_API_KEY_PLACEHOLDER;

  const payload = {
    openclaw_gateway_port: openclawPortInput ? openclawPortInput.value : "",
    openclaw_gateway_url: openclawUrlInput ? openclawUrlInput.value.trim() : "",
    openclaw_gateway_token: hasMaskedToken ? "" : rawToken,
  };

  if (hasMaskedToken) {
    delete payload.openclaw_gateway_token;
  }

  return payload;
}

function setOpenclawConnectionStatus(message, isSuccess = null) {
  const statusElement = document.getElementById("openclaw-connection-status");
  if (!statusElement) {
    return;
  }

  if (!message) {
    statusElement.innerHTML = "";
    statusElement.style.display = "none";
    return;
  }

  // Try to extract a clean human-readable message from raw JSON blobs
  let displayMsg = message;
  if (typeof message === "string" && message.trim().startsWith("{")) {
    try {
      const parsed = JSON.parse(message);
      displayMsg =
        (parsed.error && parsed.error.message) ||
        parsed.message ||
        parsed.detail ||
        parsed.error ||
        message;
    } catch {
      // keep as-is
    }
  }

  const icon = isSuccess === true ? "bi-check-circle-fill" : isSuccess === false ? "bi-x-circle-fill" : "bi-info-circle";
  const badgeClass = isSuccess === true ? "bg-success" : isSuccess === false ? "bg-danger" : "bg-secondary";

  const span = document.createElement("span");
  span.className = `badge ${badgeClass} d-inline-flex align-items-center gap-1 py-2 px-3`;
  span.style.cssText = "font-size:0.82rem;font-weight:500;max-width:100%;white-space:normal;text-align:left;";
  span.innerHTML = `<i class="bi ${icon}"></i>`;
  span.appendChild(document.createTextNode(String(displayMsg)));
  statusElement.innerHTML = "";
  statusElement.appendChild(span);
  statusElement.style.display = "block";
}

async function testOpenclawConnection() {
  const testButton = document.getElementById("testOpenclawConnection");
  if (!testButton) {
    return;
  }

  const originalText = testButton.innerText;
  testButton.disabled = true;
  testButton.innerText = "Testing...";
  setOpenclawConnectionStatus("Testing OpenClaw connection...", null);

  try {
    const response = await fetch("/api/settings/test-openclaw-connection", {
      method: "POST",
      headers: {
        ...(await getAuthHeaders()),
        "Content-Type": "application/json",
      },
      body: JSON.stringify(getOpenclawGatewayPayload()),
      keepalive: false,
    });

    const payload = await readResponsePayload(response);
    if (response.ok && payload.success) {
      setOpenclawConnectionStatus(
        payload.message || "OpenClaw connection test passed.",
        true,
      );
      if (payload.status_code) {
        setOpenclawConnectionStatus(
          `${payload.message || "OpenClaw connection test passed."} (HTTP ${payload.status_code})`,
          true,
        );
      }
      return;
    }

    const message = extractErrorMessage(payload, response);
    console.error("OpenClaw connection test failed:", message);
    setOpenclawConnectionStatus(
      message || "OpenClaw connection test failed.",
      false,
    );
  } catch (error) {
    console.error("OpenClaw connection test request failed:", error);
    setOpenclawConnectionStatus(
      "OpenClaw connection test request failed. Check network and try again.",
      false,
    );
  } finally {
    testButton.disabled = false;
    testButton.innerText = originalText;
  }
}

function readEntryValue(entry) {
  if (entry.type === "radio") {
    return getSelectedRadioValue(entry.name) ?? entry.defaultValue;
  }
  const element = document.getElementById(entry.id);
  if (!element) {
    return entry.defaultValue;
  }
  if (entry.type === "switch") {
    return element.checked === true;
  }
  if (entry.type === "number") {
    return element.value || entry.defaultValue;
  }
  return element.value || entry.defaultValue;
}

function applyEntryValue(entry, settings) {
  const rawValue = settings[entry.key];
  const value = entry.normalize
    ? entry.normalize(rawValue)
    : (rawValue ?? entry.defaultValue);

  if (entry.type === "radio") {
    const selectedValue =
      entry.allowed && entry.allowed.includes(value)
        ? value
        : entry.defaultValue;
    setRadioGroupValue(entry.name, selectedValue);
    if (entry.onChange) {
      entry.onChange(selectedValue);
    }
    return;
  }

  const element = document.getElementById(entry.id);
  if (!element) {
    return;
  }
  if (entry.type === "switch") {
    element.checked = value === true;
    return;
  }
  if (entry.type === "number") {
    element.value = String(value ?? entry.defaultValue);
    return;
  }
  setSelectValue(element, value, entry.defaultValue);
}

function attachSettingsListeners() {
  SETTINGS_SCHEMA.forEach((entry) => {
    const elements = getElementsForEntry(entry);
    if (!elements.length) {
      if (entry.type === "switch") {
        console.error(`DEBUG: ${entry.id} element NOT FOUND!`);
      }
      return;
    }

    elements.forEach((element) => {
      // Prevent duplicate listeners
      if (!element.dataset) {
        element.dataset = {};
      }
      if (element.dataset.settingsBound === "true") {
        return;
      }
      element.dataset.settingsBound = "true";

      element.addEventListener("change", (event) => {
        if (entry.onChange) {
          entry.onChange(event.target.value);
        }
        // Capture provider at change-time to avoid race with loadSettings()
        // (Firebase auth refresh can call loadSettings() during the debounce
        //  window, resetting the radio before the save fires).
        const providerAtChange =
          entry.key === "llm_provider" ? event.target.value : null;
        saveSettings({ providerAtChange });
      });
    });
  });
  window.settingsListenersAttached = true;
}

/**
 * Load user settings from the API and update the UI
 */
async function loadSettings() {
  try {
    // Wait for authentication (centralized logic)
    // getEffectiveUser() handles waitForAuthInit automatically
    let currentUser;
    if (window.authTokenManager) {
      currentUser = await window.authTokenManager.getEffectiveUser();
    } else {
      currentUser = null;
    }

    // If no user found, wait for sign-in.
    if (!currentUser) {
      console.log("Guest user on settings page - waiting for sign-in.");
      if (!pendingAuthReload && window.firebase?.auth) {
        pendingAuthReload = true;
        try {
          window.firebase?.auth()?.onAuthStateChanged((user) => {
            if (user) {
              pendingAuthReload = false;
              loadSettings();
            }
          });
        } catch (error) {
          pendingAuthReload = false;
          console.warn("Firebase auth listener failed:", error);
        }
      }
      return;
    }

    console.log("Loading user settings...");
    const geminiApiKeyInput = document.getElementById("geminiApiKey");
    const openrouterApiKeyInput = document.getElementById("openrouterApiKey");
    const cerebrasApiKeyInput = document.getElementById("cerebrasApiKey");
    const openclawGatewayTokenInput = document.getElementById("openclawGatewayToken");
    if (geminiApiKeyInput) geminiApiKeyInput.value = "";
    if (openrouterApiKeyInput) openrouterApiKeyInput.value = "";
    if (cerebrasApiKeyInput) cerebrasApiKeyInput.value = "";
    if (openclawGatewayTokenInput) openclawGatewayTokenInput.value = "";
    const response = await fetch("/api/settings", {
      headers: await getAuthHeaders(),
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const settings = await response.json();
    console.log("Loaded settings:", settings);
    lastKnownProvider =
      typeof settings?.llm_provider === "string"
        ? settings.llm_provider
        : lastKnownProvider;
    window.__loadedSettings = settings;

    // Get current user email from Firebase Auth (skip in test mode)
    const _testMode =
      new URLSearchParams(window.location.search).get("test_mode") === "true";
    let userEmail = "";
    if (!_testMode) {
      try {
        userEmail = window.firebase?.auth()?.currentUser?.email || "";
      } catch (error) {
        console.warn("Firebase auth unavailable while loading settings email:", error);
      }
      if (!userEmail && window.firebase?.auth && !pendingAuthReload) {
        pendingAuthReload = true;
        try {
          window.firebase.auth().onAuthStateChanged((user) => {
            if (user?.email) {
              pendingAuthReload = false;
              loadSettings();
            }
          });
        } catch (error) {
          pendingAuthReload = false;
          console.warn("Failed to subscribe to Firebase auth state changes:", error);
        }
      }
    }

    SETTINGS_SCHEMA.forEach((entry) => {
      applyEntryValue(entry, settings);
    });

    // BYOK: Load API key values and status indicators.

    // Get API key inputs (using different variable names to avoid conflicts with DOMContentLoaded scope)
    const geminiKeyInput = document.getElementById("geminiApiKey");
    const geminiKeyStatus = document.getElementById("gemini-key-status");
    if (geminiKeyInput && geminiKeyStatus) {
      if (settings.has_custom_gemini_key) {
        const geminiKeyValue = (settings.gemini_api_key || "").trim();
        geminiKeyInput.value = geminiKeyValue || MASKED_API_KEY_PLACEHOLDER;
        geminiKeyStatus.style.display = "block";
        console.log("Custom Gemini API key is configured");
        geminiKeyInput.dataset.hasKey = "true";
        geminiKeyInput.dataset.byokDirty = "false";
        setApiKeyFieldVisible(geminiKeyInput, document.getElementById("geminiKeyIcon"), false);
      } else {
        geminiKeyInput.value = "";
        geminiKeyInput.placeholder = "Enter your Gemini API key";
        geminiKeyStatus.style.display = "none";
        geminiKeyInput.dataset.hasKey = "false";
        geminiKeyInput.dataset.byokDirty = "false";
        setApiKeyFieldVisible(geminiKeyInput, document.getElementById("geminiKeyIcon"), false);
      }
    }

    const openrouterKeyInput = document.getElementById("openrouterApiKey");
    const openrouterKeyStatus = document.getElementById(
      "openrouter-key-status",
    );
    if (openrouterKeyInput && openrouterKeyStatus) {
      if (settings.has_custom_openrouter_key) {
        const openrouterKeyValue = (settings.openrouter_api_key || "").trim();
        openrouterKeyInput.value =
          openrouterKeyValue || MASKED_API_KEY_PLACEHOLDER;
        openrouterKeyStatus.style.display = "block";
        console.log("Custom OpenRouter API key is configured");
        openrouterKeyInput.dataset.hasKey = "true";
        openrouterKeyInput.dataset.byokDirty = "false";
        setApiKeyFieldVisible(
          openrouterKeyInput,
          document.getElementById("openrouterKeyIcon"),
          false,
        );
      } else {
        openrouterKeyInput.value = "";
        openrouterKeyInput.placeholder = "Enter your OpenRouter API key";
        openrouterKeyStatus.style.display = "none";
        openrouterKeyInput.dataset.hasKey = "false";
        openrouterKeyInput.dataset.byokDirty = "false";
        setApiKeyFieldVisible(
          openrouterKeyInput,
          document.getElementById("openrouterKeyIcon"),
          false,
        );
      }
    }

    const cerebrasKeyInput = document.getElementById("cerebrasApiKey");
    const cerebrasKeyStatus = document.getElementById("cerebras-key-status");
    if (cerebrasKeyInput && cerebrasKeyStatus) {
      if (settings.has_custom_cerebras_key) {
        const cerebrasKeyValue = (settings.cerebras_api_key || "").trim();
        cerebrasKeyInput.value = cerebrasKeyValue || MASKED_API_KEY_PLACEHOLDER;
        cerebrasKeyStatus.style.display = "block";
        console.log("Custom Cerebras API key is configured");
        cerebrasKeyInput.dataset.hasKey = "true";
        cerebrasKeyInput.dataset.byokDirty = "false";
        setApiKeyFieldVisible(
          cerebrasKeyInput,
          document.getElementById("cerebrasKeyIcon"),
          false,
        );
      } else {
        cerebrasKeyInput.value = "";
        cerebrasKeyInput.placeholder = "Enter your Cerebras API key";
        cerebrasKeyStatus.style.display = "none";
        cerebrasKeyInput.dataset.hasKey = "false";
        cerebrasKeyInput.dataset.byokDirty = "false";
        setApiKeyFieldVisible(
          cerebrasKeyInput,
          document.getElementById("cerebrasKeyIcon"),
          false,
        );
      }
    }

    const openclawGatewayTokenStatus = document.getElementById(
      "openclawGatewayTokenStatus",
    );
    if (openclawGatewayTokenInput && openclawGatewayTokenStatus) {
      if (settings.has_custom_openclaw_gateway_token) {
        const openclawGatewayTokenValue = (
          settings.openclaw_gateway_token || ""
        ).trim();
        openclawGatewayTokenInput.value =
          openclawGatewayTokenValue || MASKED_API_KEY_PLACEHOLDER;
        openclawGatewayTokenStatus.style.display = "block";
        console.log("Custom OpenClaw gateway token is configured");
        openclawGatewayTokenInput.dataset.hasKey = "true";
        openclawGatewayTokenInput.dataset.byokDirty = "false";
        setApiKeyFieldVisible(
          openclawGatewayTokenInput,
          document.getElementById("openclawGatewayTokenIcon"),
          false,
        );
      } else {
        openclawGatewayTokenInput.value = "";
        openclawGatewayTokenInput.placeholder =
          "Enter your OpenClaw gateway Bearer token";
        openclawGatewayTokenStatus.style.display = "none";
        openclawGatewayTokenInput.dataset.hasKey = "false";
        openclawGatewayTokenInput.dataset.byokDirty = "false";
        setApiKeyFieldVisible(
          openclawGatewayTokenInput,
          document.getElementById("openclawGatewayTokenIcon"),
          false,
        );
      }
    }
  } catch (error) {
    console.error("Failed to load settings:", error);
    showErrorMessage("Failed to load settings. Please refresh the page.");
  }
}

/**
 * Show a non-blocking confirmation modal. Falls back to window.confirm if Bootstrap is unavailable.
 */
function show_confirmation_modal(message) {
  const modalElement = document.getElementById("confirmationModal");
  const messageElement = document.getElementById("confirmationModalMessage");
  const confirmButton = document.getElementById("confirmationModalConfirm");
  const cancelButton = document.getElementById("confirmationModalCancel");

  if (!modalElement || !window.bootstrap) {
    return Promise.resolve(window.confirm(message));
  }

  return new Promise((resolve) => {
    // Keep the confirm modal non-dimming even if global modal styles drift.
    modalElement.style.backgroundColor = "transparent";
    modalElement.style.backdropFilter = "none";
    modalElement.style.filter = "none";
    document
      .querySelectorAll(".modal-backdrop")
      .forEach((backdrop) => backdrop.remove());

    if (messageElement) {
      messageElement.textContent = message;
    }

    const modalInstance = new window.bootstrap.Modal(modalElement, {
      // Do not dim the entire settings page when confirming key removal.
      backdrop: false,
      focus: true,
      keyboard: true,
    });

    const cleanup = () => {
      confirmButton?.removeEventListener("click", onConfirm);
      cancelButton?.removeEventListener("click", onCancel);
      modalElement.removeEventListener("hidden.bs.modal", onCancel);
    };

    const onConfirm = () => {
      cleanup();
      resolve(true);
      modalInstance.hide();
    };

    const onCancel = () => {
      cleanup();
      resolve(false);
    };

    confirmButton?.addEventListener("click", onConfirm, { once: true });
    cancelButton?.addEventListener("click", onCancel, { once: true });
    modalElement.addEventListener("hidden.bs.modal", onCancel, { once: true });

    modalInstance.show();
  });
}

async function readResponsePayload(response) {
  try {
    const text = await response.text();
    if (!text) {
      return {};
    }
    try {
      return JSON.parse(text);
    } catch {
      return { _raw: text };
    }
  } catch (error) {
    console.error("Failed to read response body:", error);
    return { _raw: "" };
  }
}

function extractErrorMessage(payload, response) {
  if (payload && typeof payload === "object") {
    if (typeof payload.error === "object" && payload.error !== null) {
      if (
        typeof payload.error.message === "string" &&
        payload.error.message.trim()
      ) {
        return payload.error.message.trim();
      }
      if (
        typeof payload.error.detail === "string" &&
        payload.error.detail.trim()
      ) {
        return payload.error.detail.trim();
      }
    }

    if (typeof payload.error === "string" && payload.error.trim()) {
      return payload.error.trim();
    }
    if (typeof payload.message === "string" && payload.message.trim()) {
      return payload.message.trim();
    }
    if (typeof payload.detail === "string" && payload.detail.trim()) {
      return payload.detail.trim();
    }
    if (typeof payload.reason === "string" && payload.reason.trim()) {
      return payload.reason.trim();
    }
  }

  if (payload && typeof payload === "string" && payload.trim()) {
    return payload.trim();
  }

  const raw = payload && payload._raw ? String(payload._raw).trim() : "";
  if (raw) {
    return raw.slice(0, 200);
  }

  return `Request failed (${response.status} ${response.statusText})`;
}

/**
 * Save settings with debouncing and visual feedback
 */
async function saveSettings(options = {}) {
  const { keyChanged = false, providerAtChange = null } = options;
  if (keyChanged) {
    pendingKeyChange = true;
  }
  // Track the most recent intentional provider selection across debounce resets
  if (providerAtChange) {
    saveSettings._pendingProvider = providerAtChange;
  }
  // Debounce rapid changes
  if (saveTimeout) {
    clearTimeout(saveTimeout);
  }

  saveTimeout = setTimeout(async () => {
    const keyChangedForThisSave = pendingKeyChange;
    pendingKeyChange = false;
    // Use the captured provider (if set) to avoid race with loadSettings()
    const capturedProvider = saveSettings._pendingProvider || null;
    saveSettings._pendingProvider = null;
    const selectedProvider = getSelectedRadioValue("llmProvider");
    const providerEntry = SETTINGS_SCHEMA.find((entry) => entry.key === "llm_provider");
    const allowedProviders = providerEntry?.allowed ?? [];
    const loadedProvider =
      typeof window.__loadedSettings?.llm_provider === "string"
        ? window.__loadedSettings.llm_provider
        : lastKnownProvider;
    const candidateProvider =
      capturedProvider || selectedProvider || loadedProvider || "gemini";
    const resolvedProvider =
      typeof candidateProvider === "string" &&
      allowedProviders.includes(candidateProvider)
        ? candidateProvider
        : "gemini";
    if (!selectedProvider && !loadedProvider) {
      console.warn(
        "No provider is selected. Falling back to default provider:",
        resolvedProvider,
      );
    }

    const settingsToSave = {};
    SETTINGS_SCHEMA.forEach((entry) => {
      if (entry.key === "llm_provider") {
        return;
      }
      settingsToSave[entry.key] = readEntryValue(entry);
    });
    settingsToSave.llm_provider = resolvedProvider;

    // BYOK: Only include API keys if user entered a new value
    const geminiApiKeyInput = document.getElementById("geminiApiKey");
    if (
      geminiApiKeyInput &&
      geminiApiKeyInput.dataset.byokDirty === "true" &&
      geminiApiKeyInput.value.trim() &&
      geminiApiKeyInput.value.trim() !== MASKED_API_KEY_PLACEHOLDER
    ) {
      settingsToSave.gemini_api_key = geminiApiKeyInput.value.trim();
    }

    const openrouterApiKeyInput = document.getElementById("openrouterApiKey");
    if (
      openrouterApiKeyInput &&
      openrouterApiKeyInput.dataset.byokDirty === "true" &&
      openrouterApiKeyInput.value.trim() &&
      openrouterApiKeyInput.value.trim() !== MASKED_API_KEY_PLACEHOLDER
    ) {
      settingsToSave.openrouter_api_key = openrouterApiKeyInput.value.trim();
    }

    const cerebrasApiKeyInput = document.getElementById("cerebrasApiKey");
    if (
      cerebrasApiKeyInput &&
      cerebrasApiKeyInput.dataset.byokDirty === "true" &&
      cerebrasApiKeyInput.value.trim() &&
      cerebrasApiKeyInput.value.trim() !== MASKED_API_KEY_PLACEHOLDER
    ) {
      settingsToSave.cerebras_api_key = cerebrasApiKeyInput.value.trim();
    }

    const openclawGatewayTokenInput = document.getElementById(
      "openclawGatewayToken",
    );
    if (
      openclawGatewayTokenInput &&
      openclawGatewayTokenInput.dataset.byokDirty === "true" &&
      openclawGatewayTokenInput.value.trim() &&
      openclawGatewayTokenInput.value.trim() !== MASKED_API_KEY_PLACEHOLDER
    ) {
      settingsToSave.openclaw_gateway_token = openclawGatewayTokenInput.value.trim();
    } else {
      delete settingsToSave.openclaw_gateway_token;
    }

    const safeSettingsToLog = { ...settingsToSave };
    for (const keyField of [
      "gemini_api_key",
      "openrouter_api_key",
      "cerebras_api_key",
      "openclaw_gateway_token",
    ]) {
      const value = safeSettingsToLog[keyField];
      if (typeof value === "string" && value) {
        safeSettingsToLog[keyField] =
          value.length <= 4 ? "***" : `***${value.slice(-4)}`;
      }
    }
    console.log("Saving settings:", safeSettingsToLog);

    // Show loading indicator
    showLoadingIndicator(true);

    // Disable inputs during save
    SETTINGS_SCHEMA.forEach((entry) => setEntryDisabled(entry, true));
    // BYOK: Disable API key inputs during save
    if (geminiApiKeyInput) geminiApiKeyInput.disabled = true;
    if (openrouterApiKeyInput) openrouterApiKeyInput.disabled = true;
    if (cerebrasApiKeyInput) cerebrasApiKeyInput.disabled = true;
    if (openclawGatewayTokenInput) openclawGatewayTokenInput.disabled = true;

    try {
      const response = await fetch("/api/settings", {
        method: "POST",
        keepalive: true,
        headers: {
          ...(await getAuthHeaders()),
          "Content-Type": "application/json",
        },
        body: JSON.stringify(settingsToSave),
      });

      const result = await readResponsePayload(response);

      if (response.ok && result.success) {
        console.log("Settings saved successfully");
        lastKnownProvider = resolvedProvider;
        window.__loadedSettings = {
          ...(window.__loadedSettings || {}),
          llm_provider: resolvedProvider,
        };
        // Show green toast notification for API key saves
        if (keyChangedForThisSave) {
          showSaveMessage("Your API key has been saved.");
          // Reload settings to update UI state
          await loadSettings();
        } else {
          showSaveMessage();
        }
      } else {
        const message = extractErrorMessage(result, response);
        console.error("Failed to save settings:", message);
        showErrorMessage(
          message || "Failed to save settings. Please try again.",
        );
        if (keyChangedForThisSave) {
          pendingKeyChange = true;
        }
      }
    } catch (error) {
      if (isBenignSettingsFetchAbort(error)) {
        return;
      }
      console.error("Failed to save settings:", error);
      showErrorMessage(
        "An error occurred while saving settings. Please try again.",
      );
      if (keyChangedForThisSave) {
        pendingKeyChange = true;
      }
    } finally {
      // Re-enable inputs and hide loading
      SETTINGS_SCHEMA.forEach((entry) => setEntryDisabled(entry, false));
      // BYOK: Re-enable API key inputs
      if (geminiApiKeyInput) geminiApiKeyInput.disabled = false;
      if (openrouterApiKeyInput) openrouterApiKeyInput.disabled = false;
      if (cerebrasApiKeyInput) cerebrasApiKeyInput.disabled = false;
      if (openclawGatewayTokenInput) openclawGatewayTokenInput.disabled = false;
      showLoadingIndicator(false);
    }
  }, 300); // 300ms debounce
}

function isBenignSettingsFetchAbort(error) {
  const message = String(error || "");
  if (!message.includes("Failed to fetch")) {
    return false;
  }
  return settingsPageUnloading;
}

function toggleProviderSections(provider) {
  const geminiSection = document.getElementById("gemini-model-selection");
  const openrouterSection = document.getElementById(
    "openrouter-model-selection",
  );
  const cerebrasSection = document.getElementById("cerebras-model-selection");
  const openclawSection = document.getElementById("openclaw-model-selection");

  if (geminiSection) {
    geminiSection.classList.toggle("d-none", provider !== "gemini");
  }
  if (openrouterSection) {
    openrouterSection.classList.toggle("d-none", provider !== "openrouter");
  }
  if (cerebrasSection) {
    cerebrasSection.classList.toggle("d-none", provider !== "cerebras");
  }
  if (openclawSection) {
    openclawSection.classList.toggle("d-none", provider !== "openclaw");
  }
}

/**
 * Get authentication headers for API requests
 */
async function getAuthHeaders() {
  if (window.authTokenManager) {
    return window.authTokenManager.getAuthHeaders();
  }

  const headers = {};

  // In test mode (URL param), inject test bypass headers only in allowed environments.
  const _urlParams = new URLSearchParams(window.location.search);
  const canEnableTestMode =
    ["localhost", "127.0.0.1", "[::1]"].includes(window.location.hostname) ||
    window.__ALLOW_TEST_MODE__ === true;
  if (_urlParams.get("test_mode") === "true" && canEnableTestMode) {
    headers["X-Test-Bypass-Auth"] = "true";
    headers["X-Test-User-ID"] =
      _urlParams.get("test_user_id") || "test-user-123";
    return headers;
  }

  // Include Firebase auth token
  try {
    const user = firebase.auth().currentUser;
    if (user) {
      const token = await user.getIdToken();
      headers["Authorization"] = `Bearer ${token}`;
    }
  } catch (error) {
    console.error("Failed to get auth token:", error);
  }

  return headers;
}

/**
 * Show success message with auto-hide
 */
function showSaveMessage(customText) {
  const messageDiv = document.getElementById("save-message");
  const messageText = document.getElementById("save-message-text");
  const errorDiv = document.getElementById("error-message");

  if (!messageDiv) return;

  if (messageText && !messageText.dataset.defaultText) {
    messageText.dataset.defaultText =
      messageText.textContent || "Settings saved successfully!";
  }

  // Hide error message
  if (errorDiv) {
    errorDiv.style.display = "none";
  }

  // Show success message
  if (messageText) {
    const fallbackText =
      messageText.dataset.defaultText || "Settings saved successfully!";
    messageText.textContent = customText ?? fallbackText;
  }
  messageDiv.style.display = "block";
  messageDiv.style.opacity = "1";

  // Fade out after 3 seconds
  setTimeout(() => {
    messageDiv.style.opacity = "0";
    messageDiv.style.transition = "opacity 0.5s";

    setTimeout(() => {
      messageDiv.style.display = "none";
      messageDiv.style.opacity = "1";
    }, 500);
  }, 3000);
}

/**
 * Show error message with auto-hide
 */
function showErrorMessage(message) {
  const errorDiv = document.getElementById("error-message");
  const errorText = document.getElementById("error-text");
  const messageDiv = document.getElementById("save-message");

  // Hide success message
  if (messageDiv) {
    messageDiv.style.display = "none";
  }

  // Show error message
  if (errorText) {
    errorText.textContent = message;
  } else {
    errorDiv.innerHTML = `<i class="bi bi-exclamation-triangle me-2"></i>${message}`;
  }

  errorDiv.style.display = "block";
  errorDiv.style.opacity = "1";

  // Auto-hide after 5 seconds
  setTimeout(() => {
    errorDiv.style.opacity = "0";
    errorDiv.style.transition = "opacity 0.5s";

    setTimeout(() => {
      errorDiv.style.display = "none";
      errorDiv.style.opacity = "1";
    }, 500);
  }, 5000);
}

/**
 * Show/hide loading indicator
 */
function showLoadingIndicator(show) {
  const loadingDiv = document.getElementById("loading-indicator");

  if (show) {
    loadingDiv.style.display = "block";
  } else {
    loadingDiv.style.display = "none";
  }
}

/**
 * BYOK: Toggle API key visibility between password and text
 * Simplified to just toggle input type - no placeholder manipulation
 */
async function reveal_stored_api_key(provider) {
  const response = await fetch("/api/settings/reveal-key", {
    method: "POST",
    keepalive: false,
    headers: {
      ...(await getAuthHeaders()),
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ provider }),
  });

  const payload = await readResponsePayload(response);
  if (!response.ok || !payload.success) {
    const message = extractErrorMessage(payload, response);
    throw new Error(message || "Failed to reveal API key");
  }

  return String(payload.api_key || "").trim();
}

async function toggle_api_key_visibility(inputId, iconId, provider) {
  const input = document.getElementById(inputId);
  const icon = document.getElementById(iconId);

  if (!input || !icon) {
    console.warn(
      `toggleApiKeyVisibility: Could not find input ${inputId} or icon ${iconId}`,
    );
    return;
  }

  // Guard: Don't allow toggling if input is disabled (e.g. during save or load)
  if (input.disabled) {
    console.warn(
      `toggleApiKeyVisibility: Input ${inputId} is disabled, ignoring toggle request`,
    );
    return;
  }

  const isMaskedStoredKey =
    input.dataset?.hasKey === "true" &&
    (input.value || "").trim() === MASKED_API_KEY_PLACEHOLDER;
  if (isMaskedStoredKey) {
    try {
      const revealedKey = await reveal_stored_api_key(provider);
      if (!revealedKey) {
        throw new Error("Stored key is empty");
      }
      input.value = revealedKey;
      setApiKeyFieldVisible(input, icon, true);
      return;
    } catch (error) {
      console.error(`Failed to reveal ${provider} key:`, error);
      showErrorMessage("Failed to reveal API key. Please try again.");
      setApiKeyFieldVisible(input, icon, false);
      return;
    }
  }

  const currentlyVisible = input.dataset.keyVisible === "true";
  setApiKeyFieldVisible(input, icon, !currentlyVisible);
  console.log(`Toggled ${inputId} visibility -> ${!currentlyVisible}`);
}

/**
 * BYOK: Clear an API key and save the change
 */
async function clear_api_key(inputId, settingKey, statusId) {
  const input = document.getElementById(inputId);
  const statusDiv = document.getElementById(statusId);

  if (!input) return;

  const confirmed = await show_confirmation_modal(
    "Are you sure you want to remove this API key? This will disable your custom key until you add a new one.",
  );
  if (!confirmed) return;

  // Save the empty key to clear it in Firestore
  showLoadingIndicator(true);
  try {
    const response = await fetch("/api/settings", {
      method: "POST",
      keepalive: true,
      headers: {
        ...(await getAuthHeaders()),
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ [settingKey]: "" }),
    });

    const result = await readResponsePayload(response);

    if (response.ok && result.success) {
      console.log(`${settingKey} cleared successfully`);
      showSaveMessage("Your API key has been cleared.");

      // Update UI state directly without reload
      input.value = "";
      const providerName = settingKey.includes("gemini")
        ? "Gemini"
        : settingKey.includes("openrouter")
          ? "OpenRouter"
          : settingKey.includes("openclaw_gateway_token")
            ? "OpenClaw gateway"
            : "Cerebras";
      const placeholderSuffix =
        settingKey.includes("openclaw_gateway_token") ? "token" : "API key";
      input.placeholder = `Enter your ${providerName} ${placeholderSuffix}`;
      input.dataset.hasKey = "false";
      input.dataset.byokDirty = "false";
      if (statusDiv) {
        statusDiv.style.display = "none";
      }
      const icon = document.getElementById(
        inputId === "openclawGatewayToken"
          ? "openclawGatewayTokenIcon"
          : inputId === "geminiApiKey"
            ? "geminiKeyIcon"
            : inputId === "openrouterApiKey"
              ? "openrouterKeyIcon"
              : "cerebrasKeyIcon",
      );
      setApiKeyFieldVisible(input, icon, false);

      // Also reload settings to ensure full sync
      await loadSettings();
    } else {
      const message = extractErrorMessage(result, response);
      console.error(`Failed to clear ${settingKey}:`, message);
      showErrorMessage(message || "Failed to clear API key. Please try again.");
    }
  } catch (error) {
    console.error(`Failed to clear ${settingKey}:`, error);
    showErrorMessage(
      "An error occurred while clearing the API key. Please try again.",
    );
  } finally {
    showLoadingIndicator(false);
  }
}
