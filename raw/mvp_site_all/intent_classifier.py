"""
Local Intent Classifier using FastEmbed.

This module provides a lightweight, local, in-memory classification system
to determine the appropriate agent mode based on user input.

It uses the `fastembed` library (ONNX Runtime) with `BAAI/bge-small-en-v1.5`
to generate embeddings for user input and compare them against pre-computed
anchor phrases for each agent mode.

## How It Works

### Classification Process

1. **Initialization** (async, background thread):
   - Loads FastEmbed model (`BAAI/bge-small-en-v1.5`, ~133MB)
   - Pre-computes anchor embeddings for each mode from ANCHOR_PHRASES
   - L2 normalizes all embeddings
   - Stores in `anchor_embeddings` dict

2. **Classification** (per request):
   - Embeds user input → 384-dim vector
   - L2 normalizes user embedding
   - Computes cosine similarity vs each anchor group
   - Takes max similarity per mode
   - Returns mode with highest similarity if ≥ SIMILARITY_THRESHOLD (0.65)
   - Otherwise defaults to MODE_CHARACTER (story mode)

### Integration with Agent Routing

The classifier is integrated into `get_agent_for_input()` routing logic with the
following priority order:

**Priority 5: Semantic Intent Classification** (this classifier runs here)

The classifier runs ONLY if:
- No "GOD MODE:" prefix detected (Priority 1)
- No character creation completion detected (Priority 2)
- Character creation not active (Priority 3)
- No "THINK:" prefix detected (Priority 4)

### Interaction with String Prefixes

**String prefixes take precedence over semantic classification:**

- `"GOD MODE:"` prefix (Priority 1): Returns immediately, classifier never runs
- `"THINK:"` prefix (Priority 4): Returns immediately, classifier never runs

**Example:**
- Input: `"THINK: What should I do?"` → PlanningAgent (prefix detected, classifier skipped)
- Input: `"What should I do?"` → Classifier runs → may return MODE_THINK → PlanningAgent

### Interaction with Mode Toggle (API Parameter)

**Mode toggle (`mode` parameter) is checked at different priorities:**

1. **Early check** (before classifier):
   - `mode="god"` → checked in Priority 1 (before classifier)
   - `mode="think"` → checked in Priority 4 (before classifier)

2. **Fallback check** (after classifier):
   - `mode="combat"` → checked in Priority 6 (after classifier)
   - `mode="rewards"` → checked in Priority 6 (after classifier)
   - `mode="info"` → checked in Priority 6 (after classifier)

**Example:**
- Input: `"attack"`, `mode="combat"`
- Flow: Classifier runs first → returns MODE_CHARACTER → Priority 6 checks mode="combat" → CombatAgent

### Interaction with State Validation

**State validation behavior varies by agent type:**

1. **CombatAgent** - Routes on semantic intent alone:
   - Can handle both active combat and initiating new combat
   - Example: User says "I attack the goblin" when not in combat → CombatAgent initiates combat

2. **RewardsAgent** - Routes on semantic intent alone:
   - Can handle both pending rewards and checking for missed rewards
   - Example: User says "claim my rewards" but LLM forgot to set rewards_pending → RewardsAgent checks for missed rewards

3. **CharacterCreationAgent** - Routes on semantic intent alone:
   - Can handle both active character creation and initiating level-up/recreation
   - Example: User says "level up" when not in character creation → CharacterCreationAgent handles level-up
   - Example: User wants to recreate character → CharacterCreationAgent handles recreation

**Example Scenarios:**

**Scenario 1: Combat Intent + Combat Active**
- Input: `"I attack the goblin!"`
- Classifier: Returns MODE_COMBAT (0.85 confidence)
- State: `game_state.is_in_combat() == True`
- Result: ✅ CombatAgent (handles active combat)

**Scenario 2: Combat Intent + Combat NOT Active (Valid Case)**
- Input: `"I attack the goblin!"`
- Classifier: Returns MODE_COMBAT (0.85 confidence)
- State: `game_state.is_in_combat() == False`
- Result: ✅ CombatAgent (can initiate combat - e.g., attacking non-hostile NPC starts combat)

**Scenario 3: Rewards Intent + Rewards Pending**
- Input: `"claim my rewards"`
- Classifier: Returns MODE_REWARDS (0.80 confidence)
- State: `RewardsAgent.matches_game_state() == True` (rewards pending)
- Result: ✅ RewardsAgent (processes pending rewards)

**Scenario 4: Rewards Intent + No Rewards Pending (Valid Case)**
- Input: `"claim my rewards"`
- Classifier: Returns MODE_REWARDS (0.80 confidence)
- State: `RewardsAgent.matches_game_state() == False` (no rewards pending)
- Result: ✅ RewardsAgent (can check for missed rewards - e.g., LLM forgot to set rewards_pending)

**Scenario 5: Character Creation Intent + Character Creation Active**
- Input: `"create a new character"`
- Classifier: Returns MODE_CHARACTER_CREATION (0.75 confidence)
- State: `CharacterCreationAgent.matches_game_state() == True` (character creation active)
- Result: ✅ CharacterCreationAgent (handles active character creation)

**Scenario 6: Level-Up Intent (Valid Case)**
- Input: `"level up my fighter"`
- Classifier: Returns MODE_LEVEL_UP (0.75 confidence)
- State: any
- Result: ✅ LevelUpAgent (handles level-up workflow)

**Scenario 7: Character Creation Intent + Character Recreation (Valid Case)**
- Input: `"I want to recreate my character"`
- Classifier: Returns MODE_CHARACTER_CREATION (0.70 confidence)
- State: `CharacterCreationAgent.matches_game_state() == False` (character creation not active)
- Result: ✅ CharacterCreationAgent (can handle character recreation)

### Supported Modes

The classifier supports the following modes:
- `MODE_THINK` → PlanningAgent (no state check)
- `MODE_INFO` → InfoAgent (no state check)
- `MODE_COMBAT` → CombatAgent (routes on intent, can initiate combat)
- `MODE_REWARDS` → RewardsAgent (routes on intent, can check for missed rewards)
- `MODE_DEFERRED_REWARDS` → DeferredRewardsAgent (explicit missed rewards check)
- `MODE_CHARACTER_CREATION` → CharacterCreationAgent (routes on intent, can initiate character creation/recreation)
- `MODE_LEVEL_UP` → LevelUpAgent (routes on intent, can initiate level-up workflows)
- `MODE_DIALOG` → DialogAgent (routes on intent, conversation-focused interactions)
- `MODE_DIALOG_HEAVY` → HeavyDialogAgent (routes on intent, major companion/high-stakes dialog)
- `MODE_FACTION` → FactionManagementAgent (routes on intent, can initiate faction management)
- `MODE_CAMPAIGN_UPGRADE` → CampaignUpgradeAgent (routes on intent, can guide toward divine ascension)
- `MODE_CHARACTER` → StoryModeAgent (default fallback)

**Security Note:** The classifier is explicitly blocked from returning `MODE_GOD`
(security safeguard - god mode must be explicitly requested via prefix or mode parameter).

### Confidence Threshold

`SIMILARITY_THRESHOLD = 0.65`

If the highest similarity score is below this threshold, the classifier defaults
to `MODE_CHARACTER` (story mode). This prevents false positives from low-confidence
classifications.

## Usage

    from mvp_site.intent_classifier import classify_intent

    mode, confidence = classify_intent("Check my inventory")
    if mode == constants.MODE_INFO:
        # Route to InfoAgent
        ...

## Thread Safety

The classifier uses thread-safe initialization with locks to prevent race conditions
during model loading and inference. Multiple threads can safely call `classify_intent()`
concurrently.

## Error Handling

If classification fails (model not ready, error during inference), the classifier
defaults to `MODE_CHARACTER` with 0.0 confidence, ensuring the system always has a
fallback agent.
"""

from __future__ import annotations

import atexit
import inspect
import os
import shutil
import sys
import threading
import time
from pathlib import Path

from mvp_site import constants, logging_util

# NumPy is an optional accelerator. If it fails to import (including native
# linkage issues on some CI runners), semantic routing should disable gracefully
# rather than crashing module import.
try:
    import numpy as np

    NUMPY_AVAILABLE = True
except Exception as e:  # pragma: no cover - platform-specific failure modes
    np = None  # type: ignore[assignment]
    NUMPY_AVAILABLE = False
    logging_util.warning(
        "🧠 CLASSIFIER: numpy not available (%s) - semantic routing disabled",
        e,
    )

# Check for fastembed availability
try:
    from fastembed import TextEmbedding
    FASTEMBED_AVAILABLE = True
except Exception as e:
    # Keep symbol defined so tests can patch it when dependency is absent.
    TextEmbedding = None  # type: ignore[assignment]
    FASTEMBED_AVAILABLE = False
    logging_util.warning(
        "🧠 CLASSIFIER: fastembed not available (%s) - semantic routing disabled",
        e,
    )

# Check for ONNX Runtime (required by fastembed)
try:
    import onnxruntime  # noqa: F401
    ONNXRUNTIME_AVAILABLE = True
except Exception as e:
    ONNXRUNTIME_AVAILABLE = False
    logging_util.warning(
        "🧠 CLASSIFIER: onnxruntime not available (%s) - semantic routing disabled",
        e,
    )

# Model Configuration
# BAAI/bge-small-en-v1.5 is small (~133MB), fast, and effective for this task.
MODEL_NAME = "BAAI/bge-small-en-v1.5"  # slightly better than MiniLM, still small

# Consistent cache dir so GitHub Actions can cache it between runs.
# FASTEMBED_CACHE_PATH env var overrides. When unset, prefer
# $HOME/.cache/fastembed if writable; otherwise fall back to /tmp/fastembed.
def _resolve_fastembed_cache_dir() -> str:
    explicit_cache_dir = os.environ.get("FASTEMBED_CACHE_PATH")
    if explicit_cache_dir:
        return explicit_cache_dir

    home_cache_dir = os.path.join(os.path.expanduser("~"), ".cache", "fastembed")
    try:
        os.makedirs(home_cache_dir, exist_ok=True)
        if os.access(home_cache_dir, os.W_OK):
            return home_cache_dir
    except OSError:
        pass

    return "/tmp/fastembed"


_FASTEMBED_CACHE_DIR: str | None = _resolve_fastembed_cache_dir()


def _is_hf_offline_mode() -> bool:
    """Return True when runtime should avoid all HuggingFace network access."""
    return os.environ.get("HF_HUB_OFFLINE", "").strip().lower() in {
        "1",
        "true",
        "yes",
    }


def _text_embedding_supports_local_files_only() -> bool:
    """Best-effort capability check for fastembed local-files-only init."""
    if TextEmbedding is None:
        return False

    try:
        signature = inspect.signature(TextEmbedding.__init__)
    except (TypeError, ValueError):
        return False

    return "local_files_only" in signature.parameters

# Classification Confidence Threshold
# If the highest similarity score is below this, default to MODE_CHARACTER (story mode).
SIMILARITY_THRESHOLD = 0.65
SPICY_BIAS_BOOST = 0.04  # Bias boost when spicy mode is enabled (slight prior)

# Anchor Phrases for each Mode
# These define the "centers of gravity" for each intent.
ANCHOR_PHRASES = {
    constants.MODE_THINK: [
        "what should i do?",
        "i need a plan",
        "let me think about this",
        "assess the situation",
        "what are my options?",
        "strategize",
        "analyze the threat",
        "consider the consequences",
        "review my objectives",
        "planning phase",
        "wait a minute",
        "hold on",
        "let's pause and think",
    ],
    constants.MODE_INFO: [
        "check my inventory",
        "what do i have?",
        "show my equipment",
        "list my items",
        "what am i wearing?",
        "check stats",
        "show character sheet",
        "view abilities",
        "inspect my gear",
        "open backpack",
        "how much gold do i have?",
        "check my spells",
        "what is my ac?",
        "do i have any potions?",
        "list my skills",
    ],
    constants.MODE_COMBAT: [
        "roll initiative",
        "start combat",
        "i attack",
        "attack the goblin",
        "draw weapon",
        "prepare for battle",
        "execute the prisoner",
        "coup de grace",
        "fight",
        "engage enemy",
        "cast offensive spell",
    ],
    constants.MODE_CHARACTER_CREATION: [
        "create character",
        "new character",
        "make a character",
        "character creation",
        "roll stats",
        "starting character",
        "build my character",
        "character builder",
    ],
    constants.MODE_REWARDS: [
        "claim my rewards",
        "what did i get?",
        "show me the loot",
        "distribute rewards",
        "process rewards",
        "claim xp",
        "what are my rewards?",
        "loot distribution",
        "collect rewards",
        "reward me",
    ],
    constants.MODE_LEVEL_UP: [
        "level up",
        "i want to level up",
        "apply my level up",
        "choose a feat",
        "ability score improvement",
        "increase my stats",
        "pick new spells",
        "gain class feature",
    ],
    constants.MODE_DEFERRED_REWARDS: [
        "check for missed rewards",
        "did i miss any xp?",
        "verify my rewards",
        "catch up on rewards",
        "check if i missed anything",
        "did the dm forget my loot?",
        "were any rewards missed?",
        "audit my rewards",
        "backtrack rewards",
        "review missed rewards",
    ],
    constants.MODE_DIALOG: [
        "talk to the bartender",
        "talk to the innkeeper",
        "speak with the merchant",
        "ask about rumors",
        "negotiate a deal",
        "have a conversation",
        "introduce myself to him",
        "tell her about",
        "ask them for information",
        "converse with the wizard",
        "chat with the innkeeper",
        "discuss the quest",
        "persuade the guard",
        "convince him to help",
        "threaten the bandit",
        "flatter the noble",
        "apologize to her",
        "confide in him",
        "bargain with the trader",
        "seek counsel from",
        "strike up a conversation",
        # Meeting/council scenarios
        "meet with my council",
        "meet with my advisors",
        "hold court with my allies",
        "summon my lieutenants",
        "convene a meeting",
        "gather my companions",
        # Check-in/status conversations
        "see how they're doing",
        "check on my party",
        "how are my companions",
        "ask astarion how he feels",
        "check in with shadowheart",
        # D&D social skill examples (Charisma-based)
        "deceive the guard about our intentions",
        "lie to the merchant about the item's value",
        "intimidate the bandit into surrendering",
        "interrogate the prisoner for information",
        "charm the noble at the party",
        "bribe the guard to look the other way",
        # Speaking manner examples
        "whisper to my ally about the plan",
        "plead with the king for mercy",
        "demand answers from the spy",
        "command my troops to stand down",
        # Information exchange examples
        "explain the situation to the captain",
        "inform the mayor about the threat",
        "respond to the ambassador's questions",
        # Emotional/relationship examples
        "comfort shadowheart after her loss",
        "thank the innkeeper for his hospitality",
        "welcome the new party member",
        "say goodbye to our fallen friend",
        # Argument/debate examples
        "press the argument",
        "argue that a more merciful dispersal",
        "make a point",
        "discuss with the commander",
        "reason with him",
        "debate the decision",
    ],
    constants.MODE_DIALOG_HEAVY: [
        "have a heart to heart with my companion",
        "confront my companion about betrayal",
        "help my companion through a crisis",
        "resolve a major relationship conflict",
        "have a high-stakes negotiation with the queen",
        "plead for mercy at a public tribunal",
        "deliver an emotional confession to my love interest",
        "talk down my ally from abandoning the party",
        "mediate peace between warring companions",
        "ask my companion to forgive me",
        "final companion arc confrontation",
        "major companion quest conversation",
    ],
    constants.MODE_FACTION: [
        "manage my faction",
        "faction management",
        "strategic faction system",
        "activate faction minigame",
        "show faction status",
        "check faction power",
        "what's my faction ranking?",
        "build farms",
        "recruit soldiers",
        "faction operations",
        "faction intel",
        "faction battle",
        "faction territory",
        "how many troops do i have?",
        "faction suggestions",
    ],
    constants.MODE_CAMPAIGN_UPGRADE: [
        "i wanna be a god",
        "i want to be a god",
        "accelerate my god",
        "let me be multiverse god",
        "become a deity",
        "ascend to godhood",
        "divine ascension",
        "become divine",
        "multiverse upgrade",
        "sovereign protocol",
        "transcend mortality",
        "tier upgrade",
        "upgrade my campaign",
        "go to next tier",
        "become more powerful",
        "reach godhood",
        "i want divine power",
        "skip to god tier",
        "multiverse god",
        "cosmic ascension",
    ],
    constants.MODE_SPICY: [
        # Romantic/intimate intent signals
        "seduce her",
        "seduce him",
        "kiss her",
        "kiss him",
        "embrace her",
        "embrace him",
        "flirt with",
        "make love",
        "get intimate",
        "romantic evening",
        "take things further",
        "invite her to my room",
        "invite him to my room",
        "spend the night together",
        "lean in for a kiss",
        "pull her close",
        "pull him close",
        "whisper seductively",
        "caress her",
        "caress him",
        "passionate embrace",
        "romantic moment",
        "bedroom",
        "undress",
        "get closer",
        "continue the night",
        "explore each other",
        "be with her",
        "be with him",
        "hold her close",
        "hold him close",
        # NOTE: UI toggle commands (enable/disable/exit spicy mode) are handled
        # by the toggle handler in world_logic.py and should NOT be here.
        # They are settings commands, not romantic/intimate content triggers.
    ],
    constants.MODE_CHARACTER: [
        "i look around",
        "go north",
        "open the door",
        "cast fireball",
        "sneak past the guard",
        "investigate the room",
        "i say hello",
        "draw my sword",
        "continue",
        "what happens next?",
        # Navigation and exploration anchors
        "walk down the path",
        "explore the forest",
        "search the room",
        "look around the room",
        "search for traps",
        "check the area",
        "move forward",
        "head down the corridor",
        "inspect the surroundings",
        "survey the landscape",
    ],
}


class LocalIntentClassifier:
    _instance = None
    _lock = threading.Lock()
    _init_lock = threading.Lock()  # Separate lock for initialization

    def __init__(self):
        self.model = None
        self.anchor_embeddings: dict[str, np.ndarray] = {}
        self.ready = False
        self._load_error = None
        self._initializing = False  # Flag to track initialization state
        self._cleaned_up = False  # Flag to prevent double cleanup
        self._retry_count = 0
        self._max_retries = 3  # Maximum retry attempts

        # Register cleanup handler for graceful shutdown
        atexit.register(self._cleanup)

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    @staticmethod
    def _cache_candidates() -> list[Path]:
        # Fastembed uses HuggingFace cache format: models--{org}--{model_name}
        # The ONNX variant appends '-onnx' suffix
        model_cache_name = f"models--{MODEL_NAME.replace('/', '--')}"
        candidates = []
        if _FASTEMBED_CACHE_DIR:
            candidates.append(Path(_FASTEMBED_CACHE_DIR) / model_cache_name)
            candidates.append(Path(_FASTEMBED_CACHE_DIR) / f"{model_cache_name}-onnx")
        return candidates

    # Minimum blob size threshold (~60MB) - quantized ONNX cache is ~67MB.
    # This catches truncated downloads while avoiding false negatives.
    _MIN_BLOBS_TOTAL_SIZE_BYTES = 60_000_000

    @staticmethod
    def _is_corrupted_cache_dir(cache_dir: Path) -> bool:
        # Check for dangling ONNX symlinks (broken model files)
        # Wrap in try-except to handle filesystem errors gracefully
        try:
            for onnx_file in cache_dir.rglob("*.onnx"):
                try:
                    if onnx_file.is_symlink() and not onnx_file.exists():
                        return True
                except OSError:
                    # Treat filesystem errors on individual files as potential corruption
                    return True
        except OSError as e:
            # Treat filesystem errors (permission, broken mount, etc.) as corruption indicator
            logging_util.debug(
                "🧠 CLASSIFIER: Filesystem error checking ONNX files in %s: %s",
                cache_dir,
                e,
            )
            return True

        blobs_dir = cache_dir / "blobs"
        if not blobs_dir.exists():
            # Check if cache dir has any content - if completely empty, it's not corruption,
            # just a fresh/uninitialized cache. If it has other files but no blobs, that's
            # suspicious and should be treated as corrupted.
            try:
                has_content = any(cache_dir.iterdir())
            except OSError:
                # If we can't read the directory, treat as corrupted
                return True
            if not has_content:
                # Empty cache dir - not corrupted, just uninitialized
                return False
            # Has other content but no blobs - likely corrupted
            return True

        # Check if blobs directory is empty or too small (incomplete download)
        # Wrap in try-except to handle filesystem errors gracefully
        total_bytes = 0
        try:
            for blob_file in blobs_dir.rglob("*"):
                try:
                    if blob_file.is_file():
                        total_bytes += blob_file.stat().st_size
                except OSError:
                    # Skip files we can't stat - don't fail the whole check
                    continue
        except OSError as e:
            logging_util.debug(
                "🧠 CLASSIFIER: Filesystem error checking blobs in %s: %s",
                blobs_dir,
                e,
            )
            # If we can't read the blobs directory, treat as corrupted
            return True

        return total_bytes < LocalIntentClassifier._MIN_BLOBS_TOTAL_SIZE_BYTES

    @staticmethod
    def _has_active_download_lock(cache_dir: Path) -> bool:
        """Return True when lock markers suggest another process is actively downloading."""
        lock_patterns = ("*.lock", "*.lck", "*.part")
        for pattern in lock_patterns:
            try:
                if any(cache_dir.rglob(pattern)):
                    return True
            except OSError:
                # If lock scan fails, be conservative and avoid destructive deletion.
                return True
        return False

    def _validate_and_repair_cache(self) -> None:
        """Detect and repair corrupted FastEmbed cache state before model load."""
        for cache_dir in self._cache_candidates():
            # Keep broken symlinks eligible for repair; Path.exists() is False for them.
            if not cache_dir.exists() and not cache_dir.is_symlink():
                continue

            if not self._is_corrupted_cache_dir(cache_dir):
                continue

            # Skip destructive repair while another process appears to be downloading.
            if self._has_active_download_lock(cache_dir):
                logging_util.warning(
                    "🧠 CLASSIFIER: Corrupted cache detected at %s but active download lock markers are present; skipping purge this attempt.",
                    cache_dir,
                )
                continue

            logging_util.warning(
                "🧠 CLASSIFIER: Corrupted cache detected at %s. Rebuilding cache directory.",
                cache_dir,
            )
            # Handle race condition: another process may have already deleted this directory.
            # Also handle permission errors gracefully to avoid failing init.
            try:
                if cache_dir.is_symlink() or cache_dir.is_file():
                    cache_dir.unlink()
                else:
                    shutil.rmtree(cache_dir)
            except FileNotFoundError:
                # Already deleted by another process - this is fine, racing is expected
                logging_util.debug(
                    "🧠 CLASSIFIER: Cache directory already removed by another process: %s",
                    cache_dir,
                )
            except (PermissionError, OSError) as e:
                # Permission denied or other OS error - log and continue, don't abort init
                logging_util.error(
                    "🧠 CLASSIFIER: Failed to remove corrupted cache %s: %s. Proceeding anyway.",
                    cache_dir,
                    e,
                )

    def initialize_async(self):
        """Start initialization in a background thread."""
        # Check dependencies first
        if not NUMPY_AVAILABLE or not FASTEMBED_AVAILABLE or not ONNXRUNTIME_AVAILABLE:
            logging_util.warning(
                f"🧠 CLASSIFIER: Dependencies not available (numpy={NUMPY_AVAILABLE}, fastembed={FASTEMBED_AVAILABLE}, onnxruntime={ONNXRUNTIME_AVAILABLE}). "
                "Semantic routing disabled."
            )
            self._load_error = "Dependencies not available"
            return

        with self._init_lock:
            if self.ready or self._initializing:
                return
            self._initializing = True
        # Use daemon=False to ensure thread completes before interpreter shutdown,
        # preventing core dumps from abrupt termination of ONNX/FastEmbed native libraries.
        threading.Thread(target=self._initialize_model, daemon=False).start()

    def _initialize_model(self):
        """Load model and compute anchor embeddings (heavy operation) with retry logic."""
        max_retries = self._max_retries
        retry_delay = 2.0  # Start with 2 seconds

        try:
            # Validate and repair cache before attempting model load
            try:
                self._validate_and_repair_cache()
            except Exception as e:
                self._load_error = str(e)
                logging_util.error(
                    "🧠 CLASSIFIER: Cache preflight failed before retries: %s", e
                )
                return

            for attempt in range(max_retries):
                try:
                    if attempt > 0:
                        logging_util.info(
                            f"🧠 CLASSIFIER: Retry attempt {attempt}/{max_retries - 1} "
                            f"after {retry_delay:.1f}s delay..."
                        )
                        time.sleep(retry_delay)
                        retry_delay *= 2  # Exponential backoff

                    logging_util.info(f"🧠 CLASSIFIER: Loading embedding model {MODEL_NAME}...")
                    self._validate_and_repair_cache()
                    # threads=1 to avoid hogging CPU during startup.
                    # cache_dir uses a consistent path (not /tmp) so CI can cache it.
                    model_kwargs = {
                        "model_name": MODEL_NAME,
                        "threads": 1,
                        "cache_dir": _FASTEMBED_CACHE_DIR,
                    }
                    if _is_hf_offline_mode():
                        if _text_embedding_supports_local_files_only():
                            model_kwargs["local_files_only"] = True
                        logging_util.info(
                            "🧠 CLASSIFIER: HF_HUB_OFFLINE enabled; startup will use local cache only."
                        )
                    model = TextEmbedding(**model_kwargs)

                    # Only assign to self.model after successful creation
                    # This prevents partial initialization state
                    self.model = model

                    logging_util.info("🧠 CLASSIFIER: Computing anchor embeddings...")
                    for mode, phrases in ANCHOR_PHRASES.items():
                        # fastembed returns a generator, convert to list then array
                        embeddings_list = list(self.model.embed(phrases))
                        # Stack to create (N, D) matrix
                        matrix = np.array(embeddings_list)

                        # L2 Normalization (required because BGE-Small returns unnormalized vectors)
                        norms = np.linalg.norm(matrix, axis=1, keepdims=True)
                        # Avoid division by zero
                        norms[norms == 0] = 1.0
                        self.anchor_embeddings[mode] = matrix / norms

                    self.ready = True
                    self._retry_count = attempt
                    logging_util.info(
                        f"🧠 CLASSIFIER: Ready for inference (succeeded on attempt {attempt + 1})."
                    )
                    return  # Success - exit retry loop

                except Exception as e:
                    # Reset model to None on failure to allow retry
                    self.model = None
                    self._load_error = str(e)
                    if _is_hf_offline_mode() and (
                        "local file" in str(e).lower() or "offline" in str(e).lower()
                    ):
                        logging_util.warning(
                            "🧠 CLASSIFIER: Offline cache load failed; skipping retries and falling back to MODE_CHARACTER."
                        )
                        self._retry_count = attempt
                        return

                    if attempt < max_retries - 1:
                        logging_util.warning(
                            f"🧠 CLASSIFIER: Initialization attempt {attempt + 1} failed: {e}. "
                            f"Will retry in {retry_delay:.1f}s..."
                        )
                    else:
                        # Final attempt failed
                        logging_util.error(
                            f"🧠 CLASSIFIER: Initialization failed after {max_retries} attempts: {e}. "
                            f"Semantic routing disabled - all requests will default to MODE_CHARACTER."
                        )
                        self._retry_count = attempt
        finally:
            with self._init_lock:
                self._initializing = False

    def _validate_and_repair_model_cache(self) -> None:
        """
        Validate and repair the FastEmbed model cache.

        This method ensures the cache directory exists and is writable,
        and removes any corrupted cache entries to force re-download.
        """
        cache_dir = _FASTEMBED_CACHE_DIR
        if cache_dir is None:
            return

        # Ensure cache directory exists
        os.makedirs(cache_dir, exist_ok=True)

        # Check if cache is writable - fail fast if not
        if not os.access(cache_dir, os.W_OK):
            error_msg = f"Cache directory {cache_dir} is not writable"
            logging_util.error(f"🧠 CLASSIFIER: {error_msg}")
            raise RuntimeError(f"CLASSIFIER: {error_msg}")

        # Check for model files in the cache and repair if corrupted.
        # FastEmbed stores model directories directly under cache_dir.
        # A valid cache entry should have model files (onnx files, config.json, etc.)
        try:
            entries = os.listdir(cache_dir)
            valid_entries = []
            corrupted_entries = []

            for entry in entries:
                entry_path = os.path.join(cache_dir, entry)
                if os.path.isdir(entry_path):
                    # Check if this looks like a valid FastEmbed cache entry
                    # Valid entries typically have onnx files, config.json, tokenizer files
                    has_onnx = any(f.endswith(('.onnx', '.onnx_data')) for f in os.listdir(entry_path) if os.path.isfile(os.path.join(entry_path, f)))
                    has_config = os.path.exists(os.path.join(entry_path, "config.json"))
                    has_tokenizer = os.path.exists(os.path.join(entry_path, "tokenizer.json")) or os.path.exists(os.path.join(entry_path, "tokenizer_config.json"))

                    if has_onnx or has_config or has_tokenizer:
                        valid_entries.append(entry)
                    else:
                        # Empty or corrupted - mark for removal
                        corrupted_entries.append(entry)

            # Remove corrupted entries to force re-download
            if corrupted_entries:
                logging_util.warning(
                    f"🧠 CLASSIFIER: Removing {len(corrupted_entries)} corrupted cache entries: {corrupted_entries}"
                )
                for entry in corrupted_entries:
                    try:
                        entry_path = os.path.join(cache_dir, entry)
                        shutil.rmtree(entry_path)
                        logging_util.info(f"🧠 CLASSIFIER: Removed corrupted cache entry: {entry}")
                    except Exception as e:
                        logging_util.warning(f"🧠 CLASSIFIER: Failed to remove {entry}: {e}")

            if valid_entries:
                logging_util.info(
                    f"🧠 CLASSIFIER: Found {len(valid_entries)} valid cached model entries"
                )
        except OSError as e:
            logging_util.warning(
                f"🧠 CLASSIFIER: Error checking cache: {e}"
            )

        logging_util.info("🧠 CLASSIFIER: Cache validation complete")

    def predict(
        self,
        text: str,
        context: str | None = None,
        spicy_bias: bool = False,
    ) -> tuple[str, float]:
        """
        Predict the agent mode for the given text.

        Returns:
            Tuple[str, float]: (Selected Mode, Confidence Score)

        If model is not ready or confidence is low, returns (MODE_CHARACTER, 0.0).
        """
        if not NUMPY_AVAILABLE:
            return constants.MODE_CHARACTER, 0.0

        # Input validation: handle edge cases
        if not text or not text.strip():
            logging_util.debug("🧠 CLASSIFIER: Empty or whitespace-only input. Defaulting.")
            return constants.MODE_CHARACTER, 0.0

        if len(text.strip()) < 2:
            logging_util.debug("🧠 CLASSIFIER: Input too short (< 2 chars). Defaulting.")
            return constants.MODE_CHARACTER, 0.0

        # Combine text with context if available
        # We use a clear separator and limit context length to maintain focus
        classification_input = text
        if context and context.strip():
            # Use last 500 chars of context to keep it concise
            trimmed_context = context.strip()[-500:]
            classification_input = f"{trimmed_context}\n\nUSER ACTION: {text}"

        # Use lock to ensure atomic read of ready/model/anchor_embeddings state
        # This prevents race conditions where initialization is in progress
        retry_needed = False
        with self._lock:
            if not self.ready:
                if self._load_error:
                    # If initialization failed, try to recover by retrying initialization
                    if self.model is None:
                        logging_util.warning(
                            f"🧠 CLASSIFIER: Model not ready (failed: {self._load_error}). Retrying initialization..."
                        )
                        retry_needed = True
                    else:
                        logging_util.warning(
                            f"🧠 CLASSIFIER: Model not ready (failed: {self._load_error}). Defaulting."
                        )
                else:
                    logging_util.debug("🧠 CLASSIFIER: Model still loading. Defaulting.")

        # Retry initialization if needed (outside lock to avoid deadlock)
        # initialize_async uses _init_lock, not _lock, so this is safe
        if retry_needed:
            self.initialize_async()
            return constants.MODE_CHARACTER, 0.0

        # Re-check ready state after potential retry (without lock for quick check)
        if not self.ready:
            return constants.MODE_CHARACTER, 0.0

        # Re-acquire lock to read model state atomically
        with self._lock:
            # Defensive check: ensure model exists even if ready flag is set
            if self.model is None:
                logging_util.warning("🧠 CLASSIFIER: Model is None despite ready=True. Defaulting.")
                return constants.MODE_CHARACTER, 0.0

            # Copy references to local variables while holding lock
            # This ensures we use a consistent snapshot of the model state
            model = self.model
            anchor_embeddings = self.anchor_embeddings.copy()  # Shallow copy for safety

        # Now we can use model and anchor_embeddings without holding the lock
        # This prevents blocking other threads during the potentially slow embedding computation
        try:
            start_time = time.time()

            # Embed combined classification input
            # fastembed returns generator
            user_embedding = list(model.embed([classification_input]))[0]  # Shape (D,)

            # L2 Normalization (required because BGE-Small returns unnormalized vectors)
            norm = np.linalg.norm(user_embedding)
            if norm > 0:
                user_embedding = user_embedding / norm

            best_mode = constants.MODE_CHARACTER
            best_score = -1.0

            # Compare against all anchor groups
            for mode, anchors in anchor_embeddings.items():
                # anchors is (N, D), user_embedding is (D,)
                # fastembed vectors are normalized, so dot product is cosine similarity
                scores = np.dot(anchors, user_embedding)
                max_score = np.max(scores)
                if spicy_bias and mode == constants.MODE_SPICY:
                    max_score = min(1.0, max_score + SPICY_BIAS_BOOST)

                if max_score > best_score:
                    best_score = max_score
                    best_mode = mode

            elapsed_time = time.time() - start_time
            truncated_text = text[:30] + ("..." if len(text) > 30 else "")
            ctx_flag = " [WITH_CONTEXT]" if context else ""
            bias_flag = " [SPICY_BIAS]" if spicy_bias else ""
            logging_util.info(
                f"🧠 CLASSIFIER: Input='{truncated_text}'{ctx_flag}{bias_flag} -> {best_mode} (score={best_score:.3f}) | ⏱️ Latency: {elapsed_time*1000:.2f}ms"
            )

            if best_score >= SIMILARITY_THRESHOLD:
                return best_mode, float(best_score)

            return constants.MODE_CHARACTER, float(best_score)

        except Exception as e:
            logging_util.error(f"🧠 CLASSIFIER: Prediction error: {e}")
            return constants.MODE_CHARACTER, 0.0

    def _cleanup(self):
        """Clean up resources to prevent native library crashes during shutdown."""
        if self._cleaned_up:
            return

        self._cleaned_up = True

        # Clear model reference before Python exits to prevent FastEmbed/ONNX Runtime
        # native library cleanup crashes. The model will be garbage collected, but
        # clearing the reference explicitly helps avoid termination issues.
        if self.model is not None:
            try:
                # FastEmbed doesn't have explicit cleanup, but clearing the reference
                # helps prevent crashes during Python exit
                self.model = None
                self.anchor_embeddings.clear()
                self.ready = False
            except Exception:
                # Ignore errors during cleanup - we're shutting down anyway
                pass


# Global helper
def classify_intent(
    text: str,
    context: str | None = None,
    spicy_bias: bool = False,
) -> tuple[str, float]:
    """Public API to classify intent.

    Args:
        text: Input text to classify.
        context: Optional prior turn context for improved accuracy.
        spicy_bias: When True, applies a small prior boost toward spicy intent.
    """
    return LocalIntentClassifier.get_instance().predict(
        text, context=context, spicy_bias=spicy_bias
    )


def initialize():
    """Public API to trigger initialization."""
    semantic_setting = os.environ.get("ENABLE_SEMANTIC_ROUTING", "").lower()

    if semantic_setting == "false":
        logging_util.info(
            "🔧 SEMANTIC_ROUTING_DISABLED: Skipping classifier initialization (ENABLE_SEMANTIC_ROUTING=false)"
        )
        return

    if semantic_setting == "true":
        # Explicit opt-in should work even under TESTING=true.
        LocalIntentClassifier.get_instance().initialize_async()
        return

    # Default behavior in tests: skip unless the test is explicitly about the classifier.
    # This avoids background threads logging after pytest has closed its capture streams,
    # and reduces non-deterministic startup cost in unrelated test suites.
    if os.environ.get("TESTING", "").lower() == "true":
        argv = " ".join(sys.argv).lower()
        allow_in_tests = os.environ.get("ENABLE_SEMANTIC_ROUTING_IN_TESTS", "").lower() == "true"
        if not allow_in_tests and "test_intent_classifier" not in argv:
            logging_util.info(
                "🧪 TESTING_MODE: Skipping classifier initialization for non-classifier tests"
            )
            return

    LocalIntentClassifier.get_instance().initialize_async()


def check_classifier_startup(
    classifier_instance: LocalIntentClassifier,
    startup_timeout_seconds: int = 60,
) -> None:
    """Wait for classifier initialization and handle failures gracefully.

    Called by create_app() after initialize(). If the classifier fails to load
    (e.g. HuggingFace 429 rate-limiting), this logs a warning and continues
    rather than crashing the server. Semantic routing degrades to the default
    MODE_CHARACTER fallback automatically.
    """
    import time as _time

    deadline = _time.time() + startup_timeout_seconds
    timed_out = False
    while not classifier_instance.ready and _time.time() < deadline:
        if not classifier_instance._initializing:
            break
        _time.sleep(0.5)
    else:
        if not classifier_instance.ready:
            timed_out = True

    if not classifier_instance.ready:
        if (
            classifier_instance._load_error
            and not classifier_instance._initializing
            and not timed_out
        ):
            logging_util.warning(
                "CLASSIFIER_DEGRADED: Model load failed: %s. "
                "Semantic routing disabled — requests will use MODE_CHARACTER fallback.",
                classifier_instance._load_error,
            )
            return

        if timed_out:
            logging_util.warning(
                "CLASSIFIER: Startup wait timed out after %ss; "
                "continuing server startup without semantic routing readiness.",
                startup_timeout_seconds,
            )
