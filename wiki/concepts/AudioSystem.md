---
title: "Audio System"
type: concept
tags: [game-development, audio, sound]
sources: ["animal-movement-web-game-technical-design-document"]
last_updated: 2026-04-07
---

Web Audio API-based audio system with four sound categories:

- **Footsteps**: Animal-specific movement sounds
- **Ambient**: Environment background audio (biome-based)
- **Actions**: Jump, swim, fly sound effects
- **UI**: Menu clicks, notifications

AudioManager class provides loadSounds(manifest), playSound(name, volume, loop), setEnvironmentalAudio(biome) methods.
