# Game-Ready 2D Sprite Sheet Pipeline via AI
**Source:** [Ronnie Stein @LayrKits — X thread](https://x.com/layrkits/status/2050277473116619240)
**Date:** May 1, 2026
**Views:** 127.2K
**Author context:** Game dev enthusiast who used Codex to one-shot a basic game, then solved the animation/sprite problem.

---

## Summary

A complete pipeline for creating game-ready 2D sprite sheets using AI image models (GPT Image 2, Nano Banana 2) for poses + AI video models (Kling) for motion, then local processing with Python/FFmpeg/Pillow. Replaces broken approaches of trying to get image models to draw frame-perfect sprite sheets directly.

**Core insight:** Video models understand motion and leg mechanics in a way image models don't. Extract frames from AI-generated video → process into sprite sheets locally.

---

## The Problem (Why Image Models Fail for Sprite Sheets)

Image models cannot follow strict layout rules. A sprite sheet requires:
- Mathematical frame ordering (game engine accesses frames programmatically)
- Character always centered in each frame (no jitter)
- Transparent background

Additionally, image models don't understand walking/running mechanics — they mess up legs even when given exact instructions.

Two days of prompt variations + AI wrapper tools failed. Even pixel art styles were problematic (only top-down 2-frame walks worked reliably).

**The solution:** Kill a mosquito with a bazooka — use a video model (Kling) and extract frames.

---

## The Pipeline

### Step 1 — Create First Animation-Safe Pose (Image Model)

Use GPT Image 2 or Nano Banana 2. Requirements:
- Background: **exact #00FF00 chroma green** (flat, no shadows/floor/gradients)
- Character must NOT use green anywhere (clothing, gems, magic, outlines, antialiasing, glow)
- Full body: head to feet, full weapon/cape/hair/accessories visible
- Character centered, no cropping
- Character height ~40-50% of canvas (video models animate wider than first pose suggests)
- Generous empty margin on all sides (outer 20-30% border area stays empty)
- One character only, no text/watermark/border/shadow/props/gradients

**For non-idle animations:** Create a transition pose first (small move away from idle), not the extreme action pose. This helps attacks, runs, jumps, casts, hits, and landings flow naturally.

### Step 2 — Animate in Kling (Video Model)

Use the image-model result as Kling's first frame. Single prompt field — include everything:
- Motion description
- Preservation rules
- Camera rules
- Background rules
- Avoid constraints

**For simple pixel sprites:** Use short literal prompts. Long direction-lock prompts can cause Kling to reinterpret and cause travel/rotation/redesign.

**Locked camera prompt (critical):**
```
Use the uploaded image as the exact first frame.
Animate a tiny retro RPG sprite marching in place.
Keep the character pinned to the center of the screen.
Keep the same front-facing view for the entire clip.
The character must not turn, rotate, face diagonally, face sideways,
move forward, move backward, or move across the screen.
Only animate a simple two-step pose cycle:
the feet alternate a few pixels, the knees bend slightly,
and the weapon arm and off-hand/shield arm bob slightly.
Keep the head, chest, body angle, equipment sides, size, colors,
and pixel-art design the same.
Locked camera.
Flat #00FF00 green background stays unchanged.
No shadows, no floor, no effects, no blur, no new details, no redesign.
```

**For complex animations:** Describe exact body-motion language:
```
Bad: fast overhead sword slash
Good:
Use the uploaded image as the exact first frame.
Create an overhead sword attack.
The character makes a small weight shift,
raises the sword overhead,
pauses briefly in anticipation,
steps forward slightly,
strikes downward,
follows through,
then returns toward the ready stance.
```

**Tips:**
- Don't use same image as both first AND final frame (can produce still video)
- For isometric walks: use "walk in place" + explicit cardinal direction, forbid diagonal drift
- For vertical animations (jump/fall/landing): generate body motion cleanly first; add landing dust/takeoff wind as separate overlay animations
- If motion is good but ending doesn't connect: use image model for bridge frames (cheaper than re-running video)

### Step 3 — Extract Full-Resolution Frames (FFmpeg)

Script: `tools/extract_frames_ffmpeg.py`
- Uses system ffmpeg/ffprobe (no APIs, no paid services)
- Output: numbered PNG frames in directory
- Generates extraction report with metadata

### Step 4 — Visual Review + Frame Selection

Two scripts:
- `tools/make_contact_sheet.py` — visual review of all frames
- `tools/select_frames.py` — create 12-frame and/or 24-frame exports

**Frame selection rules:**
1. Choose frame 1 first: playable start pose (ready stance or transition away from idle)
2. Choose final frame second: clean recovery/landing/handoff back to idle
3. Choose key action beats between them (anticipation, lift-off, windup, contact, apex, impact, follow-through, recoil, recovery)
4. Fill gaps with evenly spaced in-betweens
5. Remove: blurry, malformed, duplicate-looking, missing limbs/weapons, visually out-of-order frames
6. Preserve VFX frames (takeoff wind, landing dust, magic arcs, impact plumes)
7. Keep original canvas for every selected frame — no per-frame cropping/recentering/alignment

### Step 5 — Matte Background (Fallback Only)

Script: `tools/matte_light_background.py`
- Only for off-white/gray/lightly-tinted backgrounds when regeneration isn't possible
- NOT for clean chroma green (Step 6 handles that better/faster)

### Step 6 — Remove Green + Build Sprite Sheet

Script: `tools/animation_pipeline.py`
- Removes exact/near #00FF00 chroma green, despills green edges
- **Preserve-canvas mode (default):** scales entire source video canvas into each 256×256 cell
- Does NOT crop/recenter per-frame (that creates fake camera movement)
- Output: 12 frames at 256×256 → sheet is 3072×256; 24 frames → 6144×256
- Generates validation report with warnings

**Critical:** preserve-canvas uses the fixed video camera as the cell boundary. If source video drifts, fix the video prompt (regenerate with locked camera) — do NOT repair by shifting individual cells.

### Step 7 — Review Before Shipping

Validation checklist:
- [ ] Report status is pass
- [ ] Sheet size is exactly `frame_count × 256` by 256
- [ ] Source canvas is stable across frames
- [ ] No per-frame bottom/ground-line/bounding-box alignment was applied
- [ ] No weapon, limb, cloth, hair, cape, or effect is accidentally clipped
- [ ] Lower-right watermark/logo removed if present

### Step 8 — Rebuild Preview Gallery

Script: `tools/build_sprite_gallery_manifest.py`
- Generates JavaScript manifest for static HTML sprite viewer
- Viewer shows newest sheets first, plays animation at selectable FPS, checker background

### Step 9 — Stage Temp Files for Cleanup

Move bulky extracted-frame folders to cleanup staging after review. Keep final promoted sheets, contact sheets, and JSON reports.

**Folder structure after promotion:**
```
final_sprites/
  <character>/
    <animation>/
      sheets/
        <character>_<animation>_12f_256.png
        <character>_<animation>_24f_256.png
      frames/
        12f_256/
        24f_256/
```

---

## Tips and Tricks

- Frame first pose for animation (full body + weapon + cape + hair), not portrait framing
- Video models animate wider than first pose suggests — keep margins generous
- Start from transition pose for non-idle animations (small move away from idle)
- For jump/fall/landing: body motion first, then add vertical effects separately
- If last frames look too similar to first (animation seems "stuck"): remove the worst duplicative last frames
- For end-frame to idle transition: use image model to generate bridge frames (cheap)
- **Money-saving tip:** Most animations can be made with just an image model + reference grid + sprite sheet extraction — more frustrating but possible
- Some video tools add lower-right watermark: clear it with a fixed transparent rectangle (x0=200, y0=236, x1=256, y1=256) per cell after processing

---

## Key Tools Summary

| Script | Purpose |
|--------|---------|
| `tools/extract_frames_ffmpeg.py` | Extract full-res PNG frames from video |
| `tools/make_contact_sheet.py` | Visual review of all frames |
| `tools/select_frames.py` | Select specific frames for sprite sheet |
| `tools/matte_light_background.py` | Fallback matting for non-green backgrounds |
| `tools/animation_pipeline.py` | Chroma removal + sprite sheet assembly |
| `tools/build_sprite_gallery_manifest.py` | Generate JS manifest for sprite viewer |
| `sprite_viewer.html` | Static local sprite animation viewer |

---

## Author's Context

- Tried Unity years ago, multiple game ideas, abandoned due to graphics limitations
- Could sculpt in Blender (150 hours on a character) but couldn't animate for game use
- Codex one-shotted a working game from one paragraph prompt
- Sprite sheet problem seemed like a dead end until discovering Kling video model
- Pipeline now works well; even experimented with stitching animations together

---

## Related / Source

- Original post: https://x.com/layrkits/status/2050277473116619240
- Author: Ronnie Stein [@LayrKits](https://x.com/LayrKits)
- Author originally dismissed video approach as "killing mosquito with an axe"
- Saved by a short X reply suggesting "use kling and just extract frames"
- Tools referenced: GPT Image 2, Nano Banana 2, Kling, Codex, FFmpeg, Pillow
