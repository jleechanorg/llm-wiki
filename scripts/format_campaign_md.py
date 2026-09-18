#!/usr/bin/env python3
"""
format_campaign_md.py

Transforms raw WorldArchitect.AI exported campaign text logs into publication-ready,
human-readable Markdown chronicles with structured metadata, character dossiers,
collapsible world lore, clean HUD status bars, and formatted dialogue/combat cards.

Usage:
    python3 format_campaign_md.py <path_to_campaign.txt> [output_path.md]
    python3 format_campaign_md.py --shard <shard_idx> --total-shards <total_shards>
    python3 format_campaign_md.py --all
"""

import argparse
import ast
import glob
import os
import re
import sys

# Connect to centralized document_generator engine in worldarchitect.ai
try:
    for repo_path in ["/Users/jleechan/projects/worktree_exported_campaigns", "/Users/jleechan/worldarchitect.ai"]:
        if os.path.exists(repo_path) and repo_path not in sys.path:
            sys.path.insert(0, repo_path)
    from mvp_site.document_generator import story_text_to_markdown as _canonical_story_to_markdown
except ImportError:
    _canonical_story_to_markdown = None

def parse_dice_rolls(raw_block: str) -> str:
    formatted = []
    for raw_line in raw_block.strip().split("\n"):
        line = raw_line.strip().lstrip("- ")
        try:
            data = ast.literal_eval(line)
            roll = data.get("roll", "")
            res = data.get("result", "")
            label = data.get("label", "")
            formatted.append(f"> 🎲 **Check:** `{roll}` ➔ **{res}** &nbsp;*({label})*")
        except Exception:
            formatted.append(f"> 🎲 **Check:** {line}")
    return "\n".join(formatted)

def format_challenge(block: str) -> str:
    lines = block.strip().split("\n")
    header = lines[0].strip("[] ")
    details = []
    for line in lines[1:]:
        s = line.strip()
        if s.startswith("Objective:"):
            details.append(f"**Objective:** {s[len('Objective:'):].strip()}")
        elif s.startswith("Status:"):
            details.append(f"**Status:** `{s[len('Status:'):].strip()}`")
        elif s.startswith("Resistance:"):
            details.append(f"**Resistance:** *{s[len('Resistance:'):].strip()}*")
        elif s:
            details.append(s)
    return "> [!NOTE] 🎯 **" + header + "**\n> " + "\n> ".join(details)

def format_companion_arc(block: str) -> str:
    lines = block.strip().split("\n")
    header = lines[0].strip("[] ")
    details = []
    for line in lines[1:]:
        s = line.strip()
        if s.startswith("Arc Type:"):
            details.append(f"**Arc Type:** {s[len('Arc Type:'):].strip()}")
        elif s.startswith("Event:"):
            details.append(f"**Event:** `{s[len('Event:'):].strip()}`")
        elif s.startswith("Description:"):
            details.append(f"**Description:** {s[len('Description:'):].strip()}")
        elif s:
            details.append(f"*{s}*")
    return "> [!IMPORTANT] 🌟 **" + header + "**\n> " + "\n> ".join(details)

def format_combat_status(block: str) -> str:
    lines = block.strip().split("\n")
    header = lines[0].strip("[] ")
    details = []
    for line in lines[1:]:
        s = line.strip()
        if s.startswith("•"):
            details.append(s)
        elif s:
            details.append(f"- {s}")
    return "> [!WARNING] ⚔️ **" + header + "**\n> " + "\n> ".join(details)

def format_timestamp(ts: str) -> str:
    ts = ts.strip("[] ")
    parts = [p.strip() for p in ts.split(",")]
    if len(parts) >= 3:
        year = parts[0]
        date = parts[1]
        time = parts[2]
        time_short = ":".join(time.split(":")[:2])
        return f"{date}, {year} ({time_short})"
    return ts

def story_text_to_markdown(story_text: str, campaign_title: str = "", campaign_id: str = "") -> str:
    if _canonical_story_to_markdown is not None:
        return _canonical_story_to_markdown(story_text, campaign_title=campaign_title, campaign_id=campaign_id)
    cleaned = story_text.replace("\\\\n", "\\n")
    title = campaign_title or "Untitled Campaign"
    scenes_split = re.split(r"={10,}\s*SCENE (\d+)\s*={10,}", cleaned)

    if len(scenes_split) <= 1:
        lines = [f"# ⚔️ {title}\n"]
        for p in cleaned.split("\n\n"):
            p_strip = p.strip()
            if not p_strip:
                continue
            if p_strip.startswith("Story:"):
                lines.append("### 📖 Story\n" + p_strip[len("Story:"):].strip() + "\n")
            elif p_strip.startswith("Main Character:"):
                lines.append("> 👤 **Main Character:**\n> " + p_strip[len("Main Character:"):].strip() + "\n")
            elif p_strip.startswith("God:"):
                lines.append("> ⚡ **God Mode:**\n> " + p_strip[len("God:"):].strip() + "\n")
            else:
                lines.append(p_strip + "\n")
        return "\n".join(lines)

    preamble = scenes_split[0].strip()
    cleaned_preamble = re.sub(r"^God Mode:.*?\n\n", "", preamble, flags=re.DOTALL)
    cleaned_preamble = re.sub(r'Follow this protocol "[^"]+".*?\n', "", cleaned_preamble)
    cleaned_preamble = re.sub(
        r"See world history section below and then campaign details for more info on this scenario\.\s*",
        "",
        cleaned_preamble,
    )

    total_scenes = len(scenes_split) // 2
    frontmatter = f"""---
title: "{title}"
campaign_id: "{campaign_id}"
scenes_total: {total_scenes}
exported_from: "https://worldarchitect.ai"
---
"""
    header_md = f"""# ⚔️ {title}
> *A WorldArchitect.AI Chronicle*

---
"""

    idx_history = cleaned_preamble.find("# World History")
    idx_details = cleaned_preamble.find("## V1 - Campaign Details")
    idx_rules = cleaned_preamble.find("## Dragon's Favor")

    body_sections = []
    if idx_history != -1 and idx_details != -1:
        premise = cleaned_preamble[:idx_history].replace("# Campaign summary", "").strip()
        history = cleaned_preamble[idx_history:idx_details].replace("# World History", "").strip()
        details = cleaned_preamble[idx_details:idx_rules if idx_rules != -1 else None].replace("## V1 - Campaign Details", "").strip()
        body_sections.append(f"## 🛡️ Part I: Campaign Dossier\n\n{premise}\n\n---\n\n{details}")
        body_sections.append(f"## 📜 Part II: World History & Lore\n<details open>\n<summary><b>Historical Lore</b></summary>\n\n{history}\n\n</details>")
        if idx_rules != -1:
            rules = cleaned_preamble[idx_rules:].strip()
            body_sections.append(f"## 🔮 Part III: Special Mechanics & Artifacts\n<details>\n<summary><b>Campaign Mechanics</b></summary>\n\n{rules}\n\n</details>")
    elif cleaned_preamble:
        body_sections.append(f"## 🛡️ Part I: Campaign Background\n\n{cleaned_preamble}")

    scene_records = []
    for i in range(1, len(scenes_split), 2):
        s_num = int(scenes_split[i])
        s_content = scenes_split[i + 1].strip()
        lines = s_content.split("\n")

        timestamp, location, status_line, resources_line, conditions_line = "", "", "", "", ""
        dice_raw, body_lines, player_lines = [], [], []
        in_dice, in_header, in_player = False, True, False
        player_type = "freeform"

        for line in lines:
            l_strip = line.strip()
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
                player_lines.append(line)
            else:
                body_lines.append(line)

        gm_text = "\n".join(body_lines).strip()
        gm_text = re.sub(r"^Game Master:\s*", "", gm_text)
        gm_text = re.sub(r"\[CHARACTER CREATION - Review\]\s*", "", gm_text)

        def sub_challenge(m):
            return "\n\n" + format_challenge(m.group(0)) + "\n\n"
        gm_text = re.sub(r"\[SOCIAL SKILL CHALLENGE:[^\]]+\]\n(?:[^\n]+\n?)+", sub_challenge, gm_text)

        def sub_arc(m):
            return "\n\n" + format_companion_arc(m.group(0)) + "\n\n"
        gm_text = re.sub(r"\[COMPANION ARC[^\]]+\]\n(?:[^\n]+\n?)+", sub_arc, gm_text)

        def sub_combat(m):
            return "\n\n" + format_combat_status(m.group(0)) + "\n\n"
        gm_text = re.sub(r"\[COMBAT (?:STATUS|INITIATIVE)[^\]]+\]\n(?:[^\n]+\n?)+", sub_combat, gm_text)

        dice_md = ""
        if dice_raw:
            dice_md = "\n" + parse_dice_rolls("\n".join(dice_raw)) + "\n"

        player_text = "\n".join(player_lines).strip()
        scene_records.append({
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
        })

    index_md = "## 🗺️ Scene Index & Timeline\n\n| Scene | Location | In-Game Time | Focus |\n| :---: | :--- | :--- | :--- |\n"
    for s in scene_records:
        ts_f = format_timestamp(s["timestamp"])
        loc_s = s["location"].split(",")[0].strip() or "Unknown"
        tag = "Roleplay"
        if s["dice"]:
            tag = "Skill Check / Combat"
        elif "SURRENDERED" in s["gm_text"]:
            tag = "Boss Surrender"
        elif "WAVERING" in s["gm_text"]:
            tag = "Social Challenge"
        index_md += f"| **{s['num']:02d}** | {loc_s} | {ts_f} | {tag} |\n"
    index_md += "\n---\n"

    chronicle_md = "## 📖 Part IV: The Adventure Chronicle\n\n"
    for s in scene_records:
        num = s["num"]
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

        chronicle_md += f"#### Scene {num}\n\n> {hud_bar}\n"
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
                chronicle_md += f'> 👤 **Player:**\n> *"{p_content}"*\n\n'
        chronicle_md += "---\n\n"

    full_md_parts = [frontmatter, header_md] + body_sections + [index_md, chronicle_md]
    return "\n\n".join(full_md_parts)

def convert_single_file(input_path: str, output_path: str = None) -> bool:
    if output_path is None:
        output_path = os.path.splitext(input_path)[0] + ".md"
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            raw_text = f.read()
        title = os.path.splitext(os.path.basename(input_path))[0]
        cid = os.path.basename(os.path.dirname(os.path.abspath(input_path)))
        md_text = story_text_to_markdown(raw_text, campaign_title=title, campaign_id=cid)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md_text)
        print(f"Converted: {os.path.basename(input_path)} -> {os.path.basename(output_path)} ({len(md_text)} chars)")
        return True
    except Exception as e:
        print(f"Error converting {input_path}: {e}", file=sys.stderr)
        return False

def get_all_campaign_txts(base_dir: str = "/Users/jleechan/llm_wiki/raw/campaigns") -> list[str]:
    pattern = os.path.join(base_dir, "*", "*.txt")
    files = sorted(glob.glob(pattern))
    return files

def main():
    parser = argparse.ArgumentParser(description="Convert WorldArchitect campaign TXT to readable Markdown")
    parser.add_argument("input_file", nargs="?", help="Specific input TXT file to convert")
    parser.add_argument("output_file", nargs="?", help="Optional output MD file path")
    parser.add_argument("--shard", type=int, default=None, help="Shard index (0-based)")
    parser.add_argument("--total-shards", type=int, default=None, help="Total number of shards")
    parser.add_argument("--all", action="store_true", help="Process all campaigns in raw/campaigns/*/*.txt")

    args = parser.parse_args()

    if args.input_file:
        success = convert_single_file(args.input_file, args.output_file)
        sys.exit(0 if success else 1)

    all_files = get_all_campaign_txts()
    print(f"Total campaign TXT files found: {len(all_files)}")

    if args.shard is not None and args.total_shards is not None:
        shard_size = (len(all_files) + args.total_shards - 1) // args.total_shards
        start_idx = args.shard * shard_size
        end_idx = min(start_idx + shard_size, len(all_files))
        shard_files = all_files[start_idx:end_idx]
        print(f"Processing shard {args.shard + 1}/{args.total_shards}: items [{start_idx}:{end_idx}] ({len(shard_files)} files)...")
        success_count = sum(1 for f in shard_files if convert_single_file(f))
        print(f"Shard {args.shard + 1} completed: {success_count}/{len(shard_files)} converted successfully.")
        sys.exit(0 if success_count == len(shard_files) else 1)

    if args.all:
        print(f"Processing all {len(all_files)} files...")
        success_count = sum(1 for f in all_files if convert_single_file(f))
        print(f"All completed: {success_count}/{len(all_files)} converted successfully.")
        sys.exit(0 if success_count == len(all_files) else 1)

    parser.print_help()

if __name__ == "__main__":
    main()
