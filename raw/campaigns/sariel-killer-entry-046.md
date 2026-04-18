---
title: "Sariel Killer — Scene 046"
type: source
tags: [campaign, scene, sariel-killer]
last_updated: 2026-04-12
scene_number: 46
scene_total: 685
source_file: /tmp/campaign_downloads_v2/
---

## Scene 046 Summary

============================================================ [Timestamp: 2025 July 5, 08:25 Location: Blackwood Academy - Main Hall Status: Lvl 1 Master Profiler | HP: 9/9 | XP: 125/300 | Gold: 150gp Conditions: None | Exhaustion: 0 | Inspiration: No] Resources: HD: 1/1, Class Features: Expertise (Investigation, Deception), Sneak Attack (1d6), Thieves' Cant Dice Rolls:   - Intelligence (Investigation) check (to probe for technical specifics): 1d20+9 = 19+9 = 28 (Exceptional Success)  Game Master

## Key Details

- **Location:** Blackwood Academy - Main Hall
- **Level hint:** 1
- **Word count:** 574
- **Campaign:** [[Sariel Killer]]
- **Entry:** [[sariel-killer-entry-046]]

---

## Full Scene Content

============================================================
[Timestamp: 2025 July 5, 08:25
Location: Blackwood Academy - Main Hall
Status: Lvl 1 Master Profiler | HP: 9/9 | XP: 125/300 | Gold: 150gp
Conditions: None | Exhaustion: 0 | Inspiration: No]
Resources: HD: 1/1, Class Features: Expertise (Investigation, Deception), Sneak Attack (1d6), Thieves' Cant
Dice Rolls:
  - Intelligence (Investigation) check (to probe for technical specifics): 1d20+9 = 19+9 = 28 (Exceptional Success)

Game Master:
Sariel's analytical gaze intensifies, her 20 Intelligence already processing the initial outline Ethan has provided. The nuances, the underlying architecture, the specific choices made by the system's designers – these are the true vulnerabilities. She needs a deeper dive, more raw data.

"The biometric system," Sariel states, her voice precise, cutting through the last lingering echoes of the bell. "Tell me more about its architecture. Is it a multimodal system, fusing different biometrics, or single-factor? What specific biometric data does it collect – fingerprint, facial recognition, iris scan, gait analysis, voiceprint? What is the underlying authentication protocol? Is it local, or does it push data to a centralized cloud server? What are the known failure rates, and what are the system's fallback authentication methods? Details, Ethan. The more granular the data, the faster I can dissect its inherent flaws."

Ethan blinks, momentarily taken aback by the sheer depth and breadth of Sariel's questioning. His initial excitement, already high, now spikes with a profound intellectual satisfaction. This isn't just someone offering a quick fix; this is someone who speaks his language, but with a terrifyingly advanced lexicon. He pulls out his tablet, his fingers flying across the holographic interface with renewed purpose, already pulling up schematic diagrams and data streams.

"Right. Okay. It's primarily a facial recognition and gait analysis system, backed by a neural network for pattern matching," he begins, a rapid-fire torrent of technical jargon now flowing freely. "Local processing on each access point, but aggregated to a central, hardened server in the admin wing for redundancy and, we suspect, for 'behavioral anomaly detection.' It uses a modified zero-knowledge proof for initial authentication, then a proprietary hash function for ongoing verification. Known failure rates are under 0.01% for false negatives, but we've seen spikes in false positives... The fallback is a standard alphanumeric password, but it requires admin override after too many failed biometrics. The real headache is the anti-spoofing; it incorporates a live liveness detection module that's proving incredibly robust. We've tried several deepfake injections, but the AI detects them before they can initiate a handshake..."

He gestures animatedly at the glowing diagrams on his tablet, his tired eyes alight with the thrill of genuine intellectual engagement. "The data packets are encrypted with a rotating quantum-resistant cipher, changed daily. Our biggest lead is an occasional transient lag in the gait analysis module when processing high-volume traffic, which suggests a potential buffer overflow vulnerability under specific conditions. But we haven't been able to trigger it consistently without setting off alarms. As for the Legacy Scions' algorithms... that's a whole other beast. They're definitely piggybacking on the school's comms, but how they're correlating social data without admin access is what's really baffling us."

He looks up, a silent question in his gaze, eager for your next move, clearly having found his intellectual equal, and perhaps, his strategic superior.

Player (choice: propose_targeted_biometric_exploit):
Propose Targeted Biometric Exploit - Suggest a specific strategy to exploit the potential buffer overflow vulnerability in the biometric system, leveraging the new technical details.

============================================================
