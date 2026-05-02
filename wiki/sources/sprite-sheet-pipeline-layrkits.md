---
title: "Game-Ready 2D Sprite Sheet Pipeline via AI"
type: source
tags: [game-dev, sprite-pipeline, ai-pipeline, computer-graphics]
date: 2026-05-01
source_file: ../raw/sprite-sheet-pipeline-layrkits.md
---

## Summary

A complete pipeline for creating game-ready 2D sprite sheets using AI image models (GPT Image 2, Nano Banana 2) for poses and AI video models (Kling) for motion, followed by local processing with Python/FFmpeg/Pillow. The core insight is that video models understand motion and leg mechanics in a way image models do not — extract frames from AI-generated video, then process into sprite sheets locally.

## Key Claims

- Image models cannot draw frame-perfect sprite sheets directly; they fail on mathematical frame ordering, character centering, and transparent backgrounds
- Video models (Kling) solve the leg/motion problem because they understand walking/running mechanics inherently
- The correct workflow is: AI image model → AI video model → FFmpeg frame extraction → Python/Pillow processing → sprite sheet
- Chroma key (#00FF00 exact green) background is the reliable approach — both image model and video model must avoid using green in the character
- Preserve-canvas mode scales the entire video canvas into each 256×256 cell rather than cropping per-frame (prevents fake camera movement)

## Key Quotes

> "Image models cannot follow strict layout rules. A sprite sheet requires: mathematical frame ordering (game engine accesses frames programmatically), character always centered in each frame (no jitter), transparent background." — Ronnie Stein (@LayrKits)

> "Kill a mosquito with a bazooka — use a video model (Kling) and extract frames." — Ronnie Stein (@LayrKits), on discovering the solution after two days of failed image model attempts

## Connections

- [[LayrKits]] — author, game dev who used Codex to one-shot a basic game
- [[Kling]] — video model used for animation; key to the pipeline
- [[GPTImage2]] — image model used for first animation-safe pose
- [[SpriteSheetPipeline]] — core concept; the 9-step pipeline from pose to final sheet
- [[ChromaKeyBackground]] — technique using exact #00FF00 green for background separation
- [[PreserveCanvasMode]] — critical pipeline setting that scales full video canvas per cell instead of per-frame cropping
- [[Codex]] — coding agent used by author to one-shot a basic game, then solve the sprite problem
