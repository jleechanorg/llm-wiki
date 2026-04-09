#!/usr/bin/env node
/**
 * Tests for actual app.js implementation of structured fields
 */

const fs = require('fs');
const path = require('path');

// Read the actual app.js file
const appJsPath = path.join(__dirname, '../../frontend_v1/app.js');
const appJsContent = fs.readFileSync(appJsPath, 'utf8');

console.log("=== Testing Actual app.js Implementation ===\n");

// Test 1: Check if generateStructuredFieldsHTML exists
const hasGenerateFunction = appJsContent.includes('const generateStructuredFieldsHTML');
console.log(`generateStructuredFieldsHTML function exists: ${hasGenerateFunction ? '✅ PASS' : '❌ FAIL'}`);

// Test 2: Check if appendToStory has fullData parameter
const appendToStoryRegex = /const appendToStory = \([^)]*fullData[^)]*\)/;
const hasFullDataParam = appendToStoryRegex.test(appJsContent);
console.log(`appendToStory has fullData parameter: ${hasFullDataParam ? '✅ PASS' : '❌ FAIL'}`);

// Test 3: Check if dice_rolls is extracted from top-level fullData
const diceRollsFromFullData = appJsContent.includes('fullData.dice_rolls');
console.log(`Extracts dice_rolls from fullData: ${diceRollsFromFullData ? '✅ PASS' : '❌ FAIL'}`);

// Test 4: Check if resources is extracted from top-level fullData
const resourcesFromFullData = appJsContent.includes('fullData.resources');
console.log(`Extracts resources from fullData: ${resourcesFromFullData ? '✅ PASS' : '❌ FAIL'}`);

// Test 5: Check if interaction handler passes full data
const interactionPassesData = /appendToStory\(\s*['"]gemini['"][\s\S]*?,\s*data\s*,\s*\)/.test(appJsContent);
console.log(`Interaction handler passes full data: ${interactionPassesData ? '✅ PASS' : '❌ FAIL'}`);

// Test 6: Check if story loading passes entry data
const storyLoadingPassesEntry = /appendToStory\(\s*entry\.actor,\s*entry\.text,\s*entry\.mode,\s*debugMode,\s*entry\.user_scene_number,\s*entry\b/.test(appJsContent);
console.log(`Story loading passes entry data: ${storyLoadingPassesEntry ? '✅ PASS' : '❌ FAIL'}`);

// Test 7: Check for spicy toggle choice routing to settings endpoint
const hasSpicyEnableChoiceRouting = /choiceId\s*===\s*['"]enable_spicy_mode['"]/.test(appJsContent);
console.log(
  `Choice handler detects enable_spicy_mode: ${
    hasSpicyEnableChoiceRouting ? '✅ PASS' : '❌ FAIL'
  }`
);

// Test 8: Check for spicy disable choice routing to settings endpoint
const hasSpicyDisableChoiceRouting = /choiceId\s*===\s*['"]disable_spicy_mode['"]/.test(appJsContent);
console.log(
  `Choice handler detects disable_spicy_mode: ${
    hasSpicyDisableChoiceRouting ? '✅ PASS' : '❌ FAIL'
  }`
);

// Test 9: Ensure settings endpoint is used for spicy choice routing
const usesSettingsEndpointForSpicyChoice = /\/api\/settings/.test(appJsContent);
console.log(
  `Choice handler references /api/settings: ${
    usesSettingsEndpointForSpicyChoice ? '✅ PASS' : '❌ FAIL'
  }`
);

// Test 10: Ensure streaming path has explicit fallback to regular interaction
const hasStreamingClientFallback = /StreamingClient is unavailable; falling back to regular interaction flow\./.test(
  appJsContent,
);
console.log(
  `Streaming path has non-streaming fallback: ${
    hasStreamingClientFallback ? '✅ PASS' : '❌ FAIL'
  }`
);

// Test 11: Ensure fallback calls regular interaction handler
const fallbackCallsRegularHandler = /await handleRegularInteraction\(userInput, mode\);/.test(
  appJsContent,
);
console.log(
  `Streaming fallback calls handleRegularInteraction: ${
    fallbackCallsRegularHandler ? '✅ PASS' : '❌ FAIL'
  }`
);

// Test 12: Streaming client waits for auth initialization before requesting headers
const streamingJsPath = path.join(__dirname, '../../frontend_v1/js/streaming.js');
const streamingJsContent = fs.readFileSync(streamingJsPath, 'utf8');
const hasAuthInitWait = /waitForAuthInit\(\)/.test(streamingJsContent);
console.log(
  `Streaming client waits for auth init: ${hasAuthInitWait ? '✅ PASS' : '❌ FAIL'}`
);

// Test 13: Streaming client has firebase token fallback on auth header failure
const hasStreamingAuthFallback = /fallback path for transient auth races before headers are available/i.test(
  streamingJsContent,
);
console.log(
  `Streaming client has auth fallback: ${
    hasStreamingAuthFallback ? '✅ PASS' : '❌ FAIL'
  }`
);

// Test 14: app.js declares streaming state variables (prevents ReferenceError)
const hasStreamingStateDeclarations =
  /let streamingClient = null;/.test(appJsContent) &&
  /let streamingElement = null;/.test(appJsContent);
console.log(
  `Streaming state variables declared: ${
    hasStreamingStateDeclarations ? '✅ PASS' : '❌ FAIL'
  }`
);

// Test 15: Streaming client transforms raw JSON chunks into narrative display text
const hasStreamingDisplayExtractor =
  /_getStreamingDisplayText\(/.test(streamingJsContent) &&
  /_extractNarrativeFromParsedEnvelope\(/.test(streamingJsContent) &&
  /_extractNarrativeFromRawEnvelope\(/.test(streamingJsContent) &&
  /_looksLikeIncompleteStructuredEnvelope\(/.test(streamingJsContent);
console.log(
  `Streaming client extracts narrative from JSON chunks: ${
    hasStreamingDisplayExtractor ? '✅ PASS' : '❌ FAIL'
  }`
);

// Test 16: Chunk handler uses display-text transformer instead of raw fullText
const chunkUsesDisplayText =
  /const displayText = this\._getStreamingDisplayText\(this\.fullText\);/.test(
    streamingJsContent
  ) && /this\.onChunk\(payload\.text, displayText\);/.test(streamingJsContent);
console.log(
  `Chunk handler renders transformed display text: ${
    chunkUsesDisplayText ? '✅ PASS' : '❌ FAIL'
  }`
);

// Test 16b: Envelope-like raw JSON is not shown to the user; we render a safe placeholder instead
const suppressesEarlyEnvelopeJson =
  /if \(this\._looksLikeIncompleteStructuredEnvelope\(rawText\)\)\s*\{[\s\S]*return this\._getStructuredEnvelopePlaceholder\(rawText\);\s*\}/.test(
    streamingJsContent
  );
console.log(
  `Streaming client suppresses early raw JSON envelope display: ${
    suppressesEarlyEnvelopeJson ? '✅ PASS' : '❌ FAIL'
  }`
);

// Test 16c: Suppression logic handles markdown-fenced JSON or schema-key-first chunks
const suppressesFencedOrSchemaKeyEnvelope =
  /\^```(?:json)?/i.test(streamingJsContent) &&
  /"action_resolution"\|"scene_header"\|"resources"\|"rolls"/.test(streamingJsContent);
console.log(
  `Streaming suppression handles fenced/schema-key envelope chunks: ${
    suppressesFencedOrSchemaKeyEnvelope ? '✅ PASS' : '❌ FAIL'
  }`
);

// Test 17: Two-phase streaming resets buffer before phase-2 chunks
const hasPhaseTransitionReset =
  /case 'phase_transition':/.test(streamingJsContent) &&
  /payload && payload\.reset_text/.test(streamingJsContent) &&
  /this\.fullText = ''/.test(streamingJsContent);
console.log(
  `Streaming client resets text on phase transition: ${
    hasPhaseTransitionReset ? '✅ PASS' : '❌ FAIL'
  }`
);

// Test 18: Streaming placeholder shows explicit loading text before first chunk
const hasStreamingLoadingText =
  /<span class="streaming-text">Loading story\.\.\.<\/span>/.test(appJsContent);
console.log(
  `Streaming pre-chunk loading text exists: ${
    hasStreamingLoadingText ? '✅ PASS' : '❌ FAIL'
  }`
);

// Test 19: Streaming completion finalizes in-place (no remove-and-reappend)
const hasInPlaceStreamingFinalize =
  /renderStoryEntryElement\(\s*streamingElement,/.test(appJsContent) &&
  !/parentNode\.removeChild\(streamingElement\)/.test(appJsContent);
console.log(
  `Streaming completion renders in-place: ${
    hasInPlaceStreamingFinalize ? '✅ PASS' : '❌ FAIL'
  }`
);

// Test 20: onChunk handler does not force auto-scroll each chunk
const onChunkHandlerMatch = appJsContent.match(
  /streamingClient\.onChunk\s*=\s*\([^)]*\)\s*=>\s*\{[\s\S]*?\n\s*\};/
);
const chunkHandlerAvoidsAutoScroll =
  !!onChunkHandlerMatch && !/scrollToBottom\(/.test(onChunkHandlerMatch[0]);
console.log(
  `Streaming chunk updates avoid forced auto-scroll: ${
    chunkHandlerAvoidsAutoScroll ? '✅ PASS' : '❌ FAIL'
  }`
);

// Test 21: createStreamingHandler in streaming.js uses explicit loading placeholder
const createHandlerHasLoadingText = /createStreamingHandler[\s\S]*Loading story\.\.\./.test(
  streamingJsContent
);
console.log(
  `createStreamingHandler has loading placeholder: ${
    createHandlerHasLoadingText ? '✅ PASS' : '❌ FAIL'
  }`
);

// Test 22: createStreamingHandler does not force scrollTop on chunk updates
const createHandlerNoForcedScroll = !/storyContainer\.scrollTop\s*=/.test(streamingJsContent);
console.log(
  `createStreamingHandler avoids forced scrollTop: ${
    createHandlerNoForcedScroll ? '✅ PASS' : '❌ FAIL'
  }`
);

// Test 23: createStreamingHandler completion does not remove and reappend entry
const createHandlerNoRemoveReappend =
  !/removeChild\(streamingElement\)/.test(streamingJsContent) &&
  /_renderFinalEntryInPlace\(/.test(streamingJsContent);
console.log(
  `createStreamingHandler finalizes in-place: ${
    createHandlerNoRemoveReappend ? '✅ PASS' : '❌ FAIL'
  }`
);

// Summary
const allTests = [
    hasGenerateFunction,
    hasFullDataParam,
    diceRollsFromFullData,
    resourcesFromFullData,
    interactionPassesData,
    storyLoadingPassesEntry,
    hasSpicyEnableChoiceRouting,
    hasSpicyDisableChoiceRouting,
    usesSettingsEndpointForSpicyChoice,
    hasStreamingClientFallback,
    fallbackCallsRegularHandler,
    hasAuthInitWait,
    hasStreamingAuthFallback,
    hasStreamingStateDeclarations,
    hasStreamingDisplayExtractor,
    chunkUsesDisplayText,
    suppressesEarlyEnvelopeJson,
    suppressesFencedOrSchemaKeyEnvelope,
    hasPhaseTransitionReset,
    hasStreamingLoadingText,
    hasInPlaceStreamingFinalize,
    chunkHandlerAvoidsAutoScroll,
    createHandlerHasLoadingText,
    createHandlerNoForcedScroll,
    createHandlerNoRemoveReappend
];

const passed = allTests.filter(t => t).length;
const total = allTests.length;

console.log(`\n=== Summary: ${passed}/${total} tests passed ===`);

if (passed < total) {
    console.log("\n❌ Implementation incomplete - some tests failed");
    process.exit(1);
} else {
    console.log("\n✅ All implementation tests passed!");
}
