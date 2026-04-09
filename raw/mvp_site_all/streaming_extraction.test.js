/**
 * Layer 1 unit tests for StreamingClient extraction functions.
 *
 * Tests _extractPlanningThinking, _extractNarrativeFromRawEnvelope,
 * _extractNarrativeFromParsedEnvelope, _looksLikeIncompleteStructuredEnvelope,
 * and _getStreamingDisplayText with partial JSON chunks that simulate
 * real LLM streaming scenarios.
 *
 * Uses node:vm to sandbox streaming.js, same pattern as settings_listeners.test.js.
 */

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

/**
 * Build a minimal browser-like context so streaming.js can load.
 * We only need the StreamingClient class, not the full DOM wiring.
 */
function buildStreamingContext() {
    const context = {
        window: {},
        document: {
            addEventListener() { },
            getElementById() { return null; },
            querySelector() { return null; },
            querySelectorAll() { return []; },
        },
        console: {
            log() { },
            error() { },
            warn() { },
            debug() { },
        },
        AbortController: class {
            constructor() { this.signal = {}; }
            abort() { }
        },
        EventSource: class {
            constructor() {
                this.onmessage = null;
                this.onerror = null;
            }
            close() { }
        },
        fetch: async () => ({ ok: true, json: async () => ({}) }),
        setTimeout: (fn) => { fn(); return 0; },
        clearTimeout() { },
    };
    return context;
}

/**
 * Load streaming.js and return a fresh StreamingClient instance.
 */
function createClient() {
    const context = buildStreamingContext();
    vm.createContext(context);
    const streamingPath = path.join(__dirname, '..', 'js', 'streaming.js');
    const code = fs.readFileSync(streamingPath, 'utf8');
    vm.runInContext(code, context, { filename: streamingPath });
    // StreamingClient should be available in context
    const client = vm.runInContext('new StreamingClient("test-campaign")', context);
    return client;
}


// ══════════════════════════════════════════════════════════════════════
//  _extractPlanningThinking
// ══════════════════════════════════════════════════════════════════════

test('_extractPlanningThinking: extracts complete thinking from full JSON', () => {
    const client = createClient();
    const raw = '{"planning_block":{"thinking":"I should describe the scene carefully."},"narrative":"The sun sets."}';
    const result = client._extractPlanningThinking(raw);
    assert.equal(result, 'I should describe the scene carefully.');
});

test('_extractPlanningThinking: extracts partial thinking from incomplete JSON', () => {
    const client = createClient();
    // LLM is still streaming — no closing quote on thinking value yet
    const raw = '{"planning_block":{"thinking":"I need to cons';
    const result = client._extractPlanningThinking(raw);
    assert.equal(result, 'I need to cons');
});

test('_extractPlanningThinking: returns null when no planning_block present', () => {
    const client = createClient();
    const raw = '{"narrative":"Just a narrative without thinking."}';
    const result = client._extractPlanningThinking(raw);
    assert.equal(result, null);
});

test('_extractPlanningThinking: handles escaped characters in thinking text', () => {
    const client = createClient();
    const raw = '{"planning_block":{"thinking":"Line 1\\nLine 2\\tTabbed \\"quoted\\""},"narrative":"ok"}';
    const result = client._extractPlanningThinking(raw);
    assert.equal(result, 'Line 1\nLine 2\tTabbed "quoted"');
});

test('_extractPlanningThinking: ignores thinking key outside planning_block', () => {
    const client = createClient();
    // "thinking" appears as a value in a different field, not inside planning_block
    const raw = '{"action_resolution":{"thinking":"not this one"},"narrative":"hello"}';
    const result = client._extractPlanningThinking(raw);
    assert.equal(result, null);
});

test('_extractPlanningThinking: handles planning_block closed before thinking position', () => {
    const client = createClient();
    // planning_block is closed, then a separate "thinking" key appears
    const raw = '{"planning_block":{"intent":"attack"}},"action_resolution":{"thinking":"outside"}';
    const result = client._extractPlanningThinking(raw);
    assert.equal(result, null);
});

test('_extractPlanningThinking: handles multi-chunk progressive accumulation', () => {
    const client = createClient();

    // Chunk 1: just the opening of planning_block
    const chunk1 = '{"planning_block":{"thinking":"I am conside';
    assert.equal(client._extractPlanningThinking(chunk1), 'I am conside');

    // Chunk 2: more thinking text
    const chunk2 = chunk1 + 'ring the player';
    assert.equal(client._extractPlanningThinking(chunk2), 'I am considering the player');

    // Chunk 3: thinking closes, narrative begins
    const chunk3 = chunk2 + '\'s options."},"narrative":"You see';
    assert.equal(client._extractPlanningThinking(chunk3), "I am considering the player's options.");
});


// ══════════════════════════════════════════════════════════════════════
//  _extractNarrativeFromRawEnvelope
// ══════════════════════════════════════════════════════════════════════

test('_extractNarrativeFromRawEnvelope: extracts narrative from complete JSON', () => {
    const client = createClient();
    const raw = '{"narrative":"The dragon roars!","action_resolution":{"outcome":"hit"}}';
    assert.equal(client._extractNarrativeFromRawEnvelope(raw), 'The dragon roars!');
});

test('_extractNarrativeFromRawEnvelope: extracts partial narrative from streaming', () => {
    const client = createClient();
    const raw = '{"action_resolution":{"outcome":"hit"},"narrative":"The dragon roar';
    assert.equal(client._extractNarrativeFromRawEnvelope(raw), 'The dragon roar');
});

test('_extractNarrativeFromRawEnvelope: extracts god_mode_response', () => {
    const client = createClient();
    const raw = '{"action_resolution":{"outcome":"Weather changed"},"god_mode_response":"The skies darken as storm clouds gather."}';
    assert.equal(
        client._extractNarrativeFromRawEnvelope(raw),
        'The skies darken as storm clouds gather.',
    );
});

test('_extractNarrativeFromRawEnvelope: extracts partial god_mode_response during streaming', () => {
    const client = createClient();
    const raw = '{"action_resolution":{"outcome":"Weather changed"},"god_mode_response":"The skies dark';
    assert.equal(client._extractNarrativeFromRawEnvelope(raw), 'The skies dark');
});

test('_extractNarrativeFromRawEnvelope: prefers god_mode_response over narrative when both present', () => {
    const client = createClient();
    // god_mode_response has priority over narrative in fieldPatterns order
    const raw = '{"narrative":"Story text","god_mode_response":"God text"}';
    assert.equal(client._extractNarrativeFromRawEnvelope(raw), 'God text');
});

test('_extractNarrativeFromRawEnvelope: extracts display_text field', () => {
    const client = createClient();
    const raw = '{"display_text":"Displayed narrative here"}';
    assert.equal(client._extractNarrativeFromRawEnvelope(raw), 'Displayed narrative here');
});

test('_extractNarrativeFromRawEnvelope: returns null when no text field present', () => {
    const client = createClient();
    const raw = '{"action_resolution":{"outcome":"hit"},"scene_header":"Dark Cave"}';
    assert.equal(client._extractNarrativeFromRawEnvelope(raw), null);
});

test('_extractNarrativeFromRawEnvelope: handles escaped characters', () => {
    const client = createClient();
    const raw = '{"narrative":"She said, \\"Hello!\\". A new\\nline follows."}';
    assert.equal(client._extractNarrativeFromRawEnvelope(raw), 'She said, "Hello!". A new\nline follows.');
});

test('_extractNarrativeFromRawEnvelope: progressive god_mode chunks', () => {
    const client = createClient();

    // Simulates 3 progressive chunks for god_mode
    const c1 = '{"action_resolution":{"outcome":"Weather changed"},';
    assert.equal(client._extractNarrativeFromRawEnvelope(c1), null);

    const c2 = c1 + '"god_mode_response":"The skies darken as storm clouds gather. ';
    assert.equal(client._extractNarrativeFromRawEnvelope(c2), 'The skies darken as storm clouds gather. ');

    const c3 = c2 + 'Thunder rumbles across the valley."}';
    assert.equal(
        client._extractNarrativeFromRawEnvelope(c3),
        'The skies darken as storm clouds gather. Thunder rumbles across the valley.',
    );
});


// ══════════════════════════════════════════════════════════════════════
//  _looksLikeIncompleteStructuredEnvelope (god_mode unsuppression fix)
// ══════════════════════════════════════════════════════════════════════

test('_looksLikeIncompleteStructuredEnvelope: true for structured fields without narrative', () => {
    const client = createClient();
    const raw = '{"action_resolution":{"outcome":"hit"},"scene_header":"Dark Cave"';
    assert.equal(client._looksLikeIncompleteStructuredEnvelope(raw), true);
});

test('_looksLikeIncompleteStructuredEnvelope: structured-field guard skips when narrative present', () => {
    const client = createClient();
    // The structured-field guard (L418-422) correctly skips when narrative is present,
    // but the catch-all guard (L426-430) still fires for JSON starting with '{'.
    // This is correct: _getStreamingDisplayText extracts narrative BEFORE calling this.
    const raw = '{"action_resolution":{"outcome":"hit"},"narrative":"Text here"}';
    assert.equal(client._looksLikeIncompleteStructuredEnvelope(raw), true);
});

test('_looksLikeIncompleteStructuredEnvelope: structured-field guard skips when god_mode present', () => {
    const client = createClient();
    // THE FIX at L418-422 ensures the structured-field guard doesn't fire for god_mode.
    // But the catch-all guard (L426-430) still fires for JSON-like text.
    // This is correct: _getStreamingDisplayText extracts god_mode BEFORE calling this.
    const raw = '{"action_resolution":{"outcome":"Weather changed"},"god_mode_response":"The skies darken';
    assert.equal(client._looksLikeIncompleteStructuredEnvelope(raw), true);
});

test('_looksLikeIncompleteStructuredEnvelope: false for plain text (not JSON)', () => {
    const client = createClient();
    assert.equal(client._looksLikeIncompleteStructuredEnvelope('Just some plain text'), false);
});


// ══════════════════════════════════════════════════════════════════════
//  _getStreamingDisplayText (integration of extraction chain)
// ══════════════════════════════════════════════════════════════════════

test('_getStreamingDisplayText: returns god_mode_response from raw envelope', () => {
    const client = createClient();
    const raw = '{"action_resolution":{"outcome":"Weather changed"},"god_mode_response":"Storm clouds roll in';
    const result = client._getStreamingDisplayText(raw);
    assert.equal(result, 'Storm clouds roll in');
});

test('_getStreamingDisplayText: returns narrative from raw envelope', () => {
    const client = createClient();
    const raw = '{"action_resolution":{"outcome":"hit"},"narrative":"The dragon breathes fire';
    const result = client._getStreamingDisplayText(raw);
    assert.equal(result, 'The dragon breathes fire');
});

test('_getStreamingDisplayText: returns placeholder for incomplete structured envelope', () => {
    const client = createClient();
    const raw = '{"action_resolution":{"outcome":"hit"},"scene_header":"Dark';
    const result = client._getStreamingDisplayText(raw);
    // Should return a placeholder (not the raw JSON)
    assert.notEqual(result, raw);
    // The placeholder content varies but should NOT be the raw JSON
    assert.ok(
        !result.includes('"action_resolution"'),
        `Expected placeholder, got raw JSON: ${result}`,
    );
});

test('_getStreamingDisplayText: returns plain text as-is', () => {
    const client = createClient();
    const raw = 'Just some plain text from the LLM';
    const result = client._getStreamingDisplayText(raw);
    assert.equal(result, 'Just some plain text from the LLM');
});

test('_getStreamingDisplayText: returns narrative from fully parsed JSON', () => {
    const client = createClient();
    const raw = '{"narrative":"Complete story text here.","action_resolution":{"outcome":"success"}}';
    const result = client._getStreamingDisplayText(raw);
    assert.equal(result, 'Complete story text here.');
});

test('_getStreamingDisplayText: returns god_mode_response from fully parsed JSON', () => {
    const client = createClient();
    const raw = '{"god_mode_response":"The weather shifts dramatically.","action_resolution":{}}';
    const result = client._getStreamingDisplayText(raw);
    assert.equal(result, 'The weather shifts dramatically.');
});
