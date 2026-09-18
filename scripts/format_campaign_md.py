#!/usr/bin/env python3
"""
format_campaign_md.py

Transforms raw WorldArchitect.AI exported campaign text logs into publication-ready,
human-readable Markdown chronicles with structured metadata, character dossiers,
collapsible world lore, clean HUD status bars, and formatted dialogue/combat cards.

Usage:
    python3 format_campaign_md.py <path_to_campaign.txt> [output_path.md]
"""

import sys
import os
import re
import json

def parse_dice_rolls(raw_block):
    formatted = []
    for line in raw_block.strip().split("\n"):
        line = line.strip().lstrip("- ")
        try:
            data = eval(line)
            roll = data.get("roll", "")
            res = data.get("result", "")
            label = data.get("label", "")
            formatted.append(f"> 🎲 **Check:** `{roll}` ➔ **{res}** &nbsp;*({label})*")
        except Exception:
            formatted.append(f"> 🎲 **Check:** {line}")
    return "\n".join(formatted)

def format_challenge(block):
    lines = block.strip().split("\n")
    header = lines[0].strip("[] ")
    details = []
    for l in lines[1:]:
        l = l.strip()
        if l.startswith("Objective:"):
            details.append(f"**Objective:** {l[len('Objective:'):].strip()}")
        elif l.startswith("Status:"):
            status_val = l[len("Status:"):].strip()
            details.append(f"**Status:** `{status_val}`")
        elif l.startswith("Resistance:"):
            details.append(f"**Resistance:** *{l[len('Resistance:'):].strip()}*")
        elif l:
            details.append(l)
    return "> [!NOTE] 🎯 **" + header + "**\n> " + "\n> ".join(details)

def format_companion_arc(block):
    lines = block.strip().split("\n")
    header = lines[0].strip("[] ")
    details = []
    for l in lines[1:]:
        l = l.strip()
        if l.startswith("Arc Type:"):
            details.append(f"**Arc Type:** {l[len('Arc Type:'):].strip()}")
        elif l.startswith("Event:"):
            details.append(f"**Event:** `{l[len('Event:'):].strip()}`")
        elif l.startswith("Description:"):
            details.append(f"**Description:** {l[len('Description:'):].strip()}")
        elif l:
            details.append(f"*{l}*")
    return "> [!IMPORTANT] 🌟 **" + header + "**\n> " + "\n> ".join(details)

def format_combat_status(block):
    lines = block.strip().split("\n")
    header = lines[0].strip("[] ")
    details = []
    for l in lines[1:]:
        l = l.strip()
        if l.startswith("•"):
            details.append(l)
        elif l:
            details.append(f"- {l}")
    return "> [!WARNING] ⚔️ **" + header + "**\n> " + "\n> ".join(details)

def format_timestamp(ts):
    ts = ts.strip("[] ")
    parts = [p.strip() for p in ts.split(",")]
    if len(parts) >= 3:
        year = parts[0]
        date = parts[1]
        time = parts[2]
        time_short = ":".join(time.split(":")[:2])
        return f"{date}, {year} ({time_short})"
    return ts

def get_scene_title(s):
    num = s["num"]
    loc = s["location"]
    titles = {
        1: "The King's Ribbon — The March on Winter-Mourn",
        2: "Calibration — The Argent Eaglets",
        3: "Winter-Mourn Keep in Sight — The First Command",
        4: "Debating the Mandate — The Threat of Chaos",
        5: "Approaching the Gates — Crossbows on the Wall",
        6: "Parley at the Gates — Lady Ashwood's Defiance",
        7: "The Ultimatum — Terms of the Empress",
        8: "The Refusal — Drawing the Battle Line",
        9: "Deploying the Argent Eaglets",
        10: "The First Volley — Shields Up",
        11: "Advancing to the Outer Barricade",
        12: "Breaching the Perimeter",
        13: "Assault on the Ramparts — Steel Meets Steel",
        14: "Melee on the Wallwalk",
        15: "Holding the Chokepoint",
        16: "The Garrison Breaks",
        17: "Securing the Wall",
        18: "Overlooking the Inner Ward",
        19: "Descent into the Keep",
        20: "Entering the Inner Ward",
        21: "Pacifying the Refugee Camp",
        22: "Establishing the Command Tent",
        23: "Interrogating the Camp Elders",
        24: "Inventory of the Settlement",
        25: "Noon Conference with Hektor and Liora",
        26: "Sudden Commotion in the Ward",
        27: "Ambush! The Hidden Threat",
        28: "Split-Second Reaction — Round 1",
        29: "Duel in the Mud — Round 2",
        30: "Felling the Infiltrator — Round 3",
        31: "Restoring Order",
        32: "Interrogating the Fallen",
        33: "Nightfall — The Camp Fires Burn",
        34: "Liora's Growing Doubt",
        35: "Finnian's Perimeter Report",
        36: "Hektor's Advice — Steel the Heart",
        37: "The Shadows of the Shattered Host",
        38: "A Restless Night in Winter-Mourn",
        39: "Midnight Watch — The Silent Threat",
        40: "Dawn Alarm — Torched Granaries & The Muster",
        41: "Breaching the High Hall",
        42: "The High Hall — Surrender of Lady Ashwood",
        43: "Departure South — Leaving the Garrison Behind",
        44: "The King's Road — Liora's Moral Reckoning",
        45: "March of the Silent Peace — Absolute Command",
    }
    return titles.get(num, f"Scene {num} — {loc}")

def convert_campaign(input_path, output_path=None):
    if output_path is None:
        if input_path.endswith(".txt"):
            output_path = input_path[:-4] + ".md"
        else:
            output_path = input_path + ".md"

    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Split preamble vs scenes
    scenes_split = re.split(r"={10,}\s*SCENE (\d+)\s*={10,}", text)
    preamble = scenes_split[0].strip()

    # Clean God Mode header & internal instructions
    cleaned_preamble = re.sub(r"^God Mode:.*?\n\n", "", preamble, flags=re.DOTALL)
    cleaned_preamble = re.sub(r'Follow this protocol "[^"]+".*?\n', "", cleaned_preamble)
    cleaned_preamble = re.sub(
        r"See world history section below and then campaign details for more info on this scenario\.\s*",
        "",
        cleaned_preamble,
    )

    campaign_id = os.path.basename(os.path.dirname(os.path.abspath(input_path)))
    if not campaign_id or len(campaign_id) < 5:
        campaign_id = "Custom"

    frontmatter = f"""---
title: "The Knight of Two Suns"
campaign: "Dragon Knight"
campaign_id: "{campaign_id}"
protagonist: "Ser Arion val Valerion"
class: "Level 1 Paladin (Oath of the Crown)"
setting: "World of Assiah (Celestial Imperium)"
ruleset: "D&D 5E SRD / WorldArchitect.AI"
scenes_total: {len(scenes_split) // 2}
exported_from: "https://worldarchitect.ai"
---
"""

    header_md = """# ⚔️ The Knight of Two Suns
> *A WorldArchitect.AI Chronicle of Duty, Conscience, and the Silent Peace*

| **Protagonist** | **Sworn Allegiance** | **Setting** | **Ruleset** | **Status** |
| :--- | :--- | :--- | :--- | :--- |
| **Ser Arion val Valerion** (Age 16) | Empress Sariel / Celestial Imperium | Assiah (Winter-Mourn Province) | D&D 5E Paladin | 45 Scenes (Completed Act I–IV) |

---

## 📑 Table of Contents
1. [Campaign Dossier & Character Sheet](#-part-i-campaign-dossier--character-sheet)
2. [World History & Setting Lore](#-part-ii-world-history--setting-lore)
3. [Special Rules & Artifact Mechanics](#-part-iii-special-rules--artifact-mechanics)
4. [Scene Index & Timeline](#-scene-index--timeline)
5. [The Adventure Chronicle](#-part-iv-the-adventure-chronicle)
   - [Act I: The March to Winter-Mourn (Scenes 1–5)](#act-i-the-march-to-winter-mourn-scenes-15)
   - [Act II: The Siege & Breaching the Gates (Scenes 6–19)](#act-ii-the-siege--breaching-the-gates-scenes-619)
   - [Act III: Securing the Inner Ward & Skirmish (Scenes 20–39)](#act-iii-securing-the-inner-ward--skirmish-scenes-2039)
   - [Act IV: The High Hall & The Road South (Scenes 40–45)](#act-iv-the-high-hall--the-road-south-scenes-4045)

---
"""

    idx_world_history = cleaned_preamble.find("# World History")
    idx_campaign_details = cleaned_preamble.find("## V1 - Campaign Details")
    idx_dragon_favor = cleaned_preamble.find("## Dragon's Favor")

    premise_text = cleaned_preamble[:idx_world_history].strip()
    premise_text = premise_text.replace("# Campaign summary", "").strip()

    history_text = cleaned_preamble[idx_world_history:idx_campaign_details].strip()
    history_text = history_text.replace("# World History", "").strip()

    dossier_text = cleaned_preamble[idx_campaign_details:idx_dragon_favor].strip()
    dossier_text = dossier_text.replace("## V1 - Campaign Details", "").strip()

    mechanics_text = cleaned_preamble[idx_dragon_favor:].strip()

    part1_md = f"""## 🛡️ Part I: Campaign Dossier & Character Sheet

### 📖 Campaign Premise
{premise_text}

---

{dossier_text}
"""

    part2_md = f"""## 📜 Part II: World History & Setting Lore
<details open>
<summary><b>Click to collapse/expand Historical Canon of Assiah</b></summary>

{history_text}

</details>
"""

    part3_md = f"""## 🔮 Part III: Special Rules & Artifact Mechanics
<details>
<summary><b>Click to expand Dragon Patron Rules & Alexiel's Cache Rewards</b></summary>

{mechanics_text}

</details>
"""

    scene_records = []
    for i in range(1, len(scenes_split), 2):
        s_num = int(scenes_split[i])
        s_content = scenes_split[i + 1].strip()

        lines = s_content.split("\n")

        timestamp = ""
        location = ""
        status_line = ""
        resources_line = ""
        conditions_line = ""
        dice_raw = []
        in_dice = False
        in_header = True

        body_lines = []
        player_lines = []
        in_player = False
        player_type = "freeform"

        for l in lines:
            l_strip = l.strip()
            if in_header:
                if l_strip.startswith("[Timestamp:"):
                    timestamp = l_strip[len("[Timestamp:"):].rstrip("]")
                elif l_strip.startswith("Location:"):
                    location = l_strip[len("Location:"):].strip().rstrip("]")
                elif l_strip.startswith("Status:"):
                    status_line = l_strip[len("Status:"):].strip().rstrip("]")
                elif l_strip.startswith("Resources:"):
                    resources_line = l_strip[len("Resources:"):].strip().rstrip("]")
                elif l_strip.startswith("Conditions:"):
                    conditions_line = l_strip[len("Conditions:"):].strip().rstrip("]")
                elif l_strip.startswith("Dice Rolls:"):
                    in_dice = True
                elif in_dice and l_strip.startswith("- {"):
                    dice_raw.append(l_strip)
                elif l_strip.startswith("Game Master:"):
                    in_header = False
                    in_dice = False
            elif l_strip.startswith("Player ("):
                in_player = True
                m_ptype = re.search(r"Player \(([^)]+)\):", l_strip)
                if m_ptype:
                    player_type = m_ptype.group(1)
            elif in_player:
                player_lines.append(l)
            else:
                body_lines.append(l)

        gm_text = "\n".join(body_lines).strip()
        gm_text = re.sub(r"^Game Master:\s*", "", gm_text)
        gm_text = re.sub(r"\[CHARACTER CREATION - Review\]\s*", "", gm_text)

        def sub_challenge(m):
            return "\n\n" + format_challenge(m.group(0)) + "\n\n"

        gm_text = re.sub(
            r"\[SOCIAL SKILL CHALLENGE:[^\]]+\]\n(?:[^\n]+\n?)+",
            sub_challenge,
            gm_text,
        )

        def sub_arc(m):
            return "\n\n" + format_companion_arc(m.group(0)) + "\n\n"

        gm_text = re.sub(r"\[COMPANION ARC[^\]]+\]\n(?:[^\n]+\n?)+", sub_arc, gm_text)

        def sub_combat(m):
            return "\n\n" + format_combat_status(m.group(0)) + "\n\n"

        gm_text = re.sub(
            r"\[COMBAT (?:STATUS|INITIATIVE)[^\]]+\]\n(?:[^\n]+\n?)+",
            sub_combat,
            gm_text,
        )

        dice_md = ""
        if dice_raw:
            dice_md = "\n" + parse_dice_rolls("\n".join(dice_raw)) + "\n"

        player_text = "\n".join(player_lines).strip()

        scene_records.append(
            {
                "num": s_num,
                "timestamp": timestamp,
                "location": location,
                "status": status_line,
                "resources": resources_line,
                "conditions": conditions_line,
                "dice": dice_md,
                "gm_text": gm_text,
                "player_text": player_text,
                "player_type": player_type,
            }
        )

    index_md = """## 🗺️ Scene Index & Timeline

| Scene | Title | Location | In-Game Time | Focus / Event |
| :---: | :--- | :--- | :--- | :--- |
"""
    for s in scene_records:
        title = get_scene_title(s)
        anchor = f"#scene-{s['num']}-{re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')}"
        ts_formatted = format_timestamp(s["timestamp"])
        loc_short = s["location"].split(",")[0].strip()

        tag = "Roleplay"
        if s["dice"]:
            tag = "Skill Check / Combat"
        elif "SURRENDERED" in s["gm_text"]:
            tag = "Boss Surrender"
        elif "WAVERING" in s["gm_text"]:
            tag = "Social Challenge"
        elif "Liora" in s["gm_text"] and s["num"] in [44, 45]:
            tag = "Companion Climax"

        index_md += f"| **{s['num']:02d}** | [{title}]({anchor}) | {loc_short} | {ts_formatted} | {tag} |\n"

    index_md += "\n---\n"

    chronicle_md = "\n## 📖 Part IV: The Adventure Chronicle\n\n"

    for s in scene_records:
        num = s["num"]

        if num == 1:
            chronicle_md += """### Act I: The March to Winter-Mourn (Scenes 1–5)
> *The young paladin Ser Arion rides with the Argent Eaglets under orders from Prefect Gratian to disperse an unsanctioned refugee settlement.*

---
"""
        elif num == 6:
            chronicle_md += """### Act II: The Siege & Breaching the Gates (Scenes 6–19)
> *Arion arrives at the gates of Winter-Mourn Keep, parleys with Lady Annalise Ashwood, and leads the assault to secure the walls.*

---
"""
        elif num == 20:
            chronicle_md += """### Act III: Securing the Inner Ward & Skirmish (Scenes 20–39)
> *The Argent Eaglets secure the refugee encampment, confront hidden assassins, and endure a tense, watchful night.*

---
"""
        elif num == 40:
            chronicle_md += """### Act IV: The High Hall & The Road South (Scenes 40–45)
> *A dawn raid, the final breach of the High Hall, the arrest of Lady Ashwood, and the harrowing return march south.*

---
"""

        title = get_scene_title(s)
        anchor_id = f"scene-{num}-{re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')}"

        ts_disp = format_timestamp(s["timestamp"])

        hud_parts = []
        if s["location"]:
            hud_parts.append(f"📍 **{s['location']}**")
        if ts_disp:
            hud_parts.append(f"⏳ **{ts_disp}**")
        if s["status"]:
            hud_parts.append(f"🛡️ **{s['status']}**")
        if s["resources"]:
            hud_parts.append(f"✨ **{s['resources']}**")
        if s["conditions"]:
            hud_parts.append(f"⚠️ **{s['conditions']}**")

        hud_bar = " &nbsp;|&nbsp; ".join(hud_parts)

        chronicle_md += f'<a id="{anchor_id}"></a>\n\n#### Scene {num}: {title}\n\n'
        chronicle_md += f"> {hud_bar}\n"

        if s["dice"]:
            chronicle_md += s["dice"]

        chronicle_md += "\n" + s["gm_text"] + "\n\n"

        if s["player_text"]:
            p_content = s["player_text"]
            if p_content.startswith("OOC:"):
                chronicle_md += f"> [!TIP] 💡 **Out of Character (OOC) Query:**\n> {p_content[4:].strip()}\n\n"
            elif s["player_type"].startswith("choice:"):
                chronicle_md += f"> [!NOTE] ⚙️ **Player Choice:**\n> *{p_content}*\n\n"
            else:
                chronicle_md += f'> 👤 **Ser Arion:**\n> *"{p_content}"*\n\n'

        chronicle_md += "---\n\n"

    full_doc = (
        frontmatter
        + "\n"
        + header_md
        + "\n"
        + part1_md
        + "\n\n"
        + part2_md
        + "\n\n"
        + part3_md
        + "\n\n"
        + index_md
        + "\n"
        + chronicle_md
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_doc)

    print(f"Successfully converted {input_path} to {output_path} ({len(full_doc)} characters).")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 format_campaign_md.py <input.txt> [output.md]")
        sys.exit(1)
    inp = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else None
    convert_campaign(inp, out)
