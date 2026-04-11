---
title: "Animal Movement Web Game - Technical Design Document"
type: source
tags: [game-development, web-game, technical-design, html5-canvas, sprite-animation, physics]
date: 2026-04-07
source_file: raw/animal-movement-web-game-tdd.md
last_updated: 2026-04-07
---

## Summary
Technical Design Document (TDD) for an animal movement web game featuring four distinct animal types (Rabbit, Lion, Eagle, Dolphin) with unique movement mechanics, physics systems, and environmental interactions. Built on HTML5 Canvas with vanilla JavaScript, featuring tile-based world rendering, sprite animation, and a comprehensive game state management system.

## Key Claims
- **Movement Classes**: QuadrupedMovement, AerialMovement, AquaticMovement extend base AnimalMovement with specialized physics
- **Physics Implementation**: Velocity-based movement with acceleration curves, environmental resistance, and AABB collision detection
- **Sprite System**: 64x64px sprite sheets with 8-frame walk cycles, 4-directional movement, and performance optimizations (sprite atlasing, frame skipping, culling)
- **Tile-Based World**: 32x32px grid system with background, collision, foreground, and effects layers
- **Performance Target**: 60 FPS with fallback to 30 FPS, memory pooling, and object reuse
- **Audio Architecture**: Web Audio API with categorized sound effects (footsteps, ambient, actions, UI)
- **Save System**: JSON format with LocalStorage and IndexedDB, schema versioning for progress data

## Animal Specifications
| Animal | Speed | Agility | Special Ability |
|--------|-------|---------|----------------|
| Rabbit | 120px/s | High | Jump (3x height) |
| Lion | 180px/s | Medium | Pounce attack |
| Eagle | 200px/s | High | Flight mode |
| Dolphin | 150px/s | High | Underwater breathing |

## Architecture Components
- **InputManager**: Keyboard/mouse event handling with configurable key bindings and mobile touch joystick support
- **AnimationEngine**: Sprite management with playAnimation(), setDirection(), updateFrame() methods
- **PhysicsSystem**: Collision/movement calculations with environmental resistance and terrain effects
- **RenderEngine**: Canvas drawing with layer-based rendering pipeline
- **AudioManager**: Sound effects loading and environmental audio mixing
- **GameStateManager**: Scene transitions (menu, game, settings) with transition effects

## Environmental Systems
- **Water zones**: Slow land animals, speed aquatic
- **Elevation**: Affects movement speed uphill/downhill
- **Weather**: Rain reduces visibility, affects sounds
- **Day/night**: Changes animal behavior patterns

## Connections
- [[GameDevelopment]] — the broader development methodology
- [[HTML5Canvas]] — the rendering technology
- [[WebAudioAPI]] — the audio implementation
- [[SpriteAnimation]] — the animation system
- [[PhysicsEngine]] — the movement and collision system

## Contradictions
- None identified — first technical design document for a web game in the wiki