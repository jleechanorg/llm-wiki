# campaign summary prompt

Chatgpt
Chronology Handling: Real transcripts may lack explicit timestamps—will you supply date/time markers, or should the AI infer sequence solely by transcript order? Consider adding instructions for how to handle ambiguous timing.

Bullet Granularity: You specify “major, canonical events,” but some interpretations of “significant” might vary—perhaps include a guideline on minimum impact (e.g., XP awards, mission completions) to avoid overly granular bullets.

Retcon Tracking: The DM Note requirement is well-defined, but you may want to specify how to format multiple retcons in the same session (e.g., “DM Note Retcon (Session 3): …”).

Transcript Length & Chunking: For very long campaigns, you might need to process in segments. It could help to instruct on handling partial transcripts or iterative summarization.

Output Metadata: If you want to later reference these summaries, consider adding an optional timestamp or sequence identifier per bullet.




AI studio Gemini
* Definition of "Significant": The prompt uses "significant" and "major" quite a bit. While the AI should infer this from context and the examples, you could (optionally, if you find it necessary later) add a line like: "Significance is determined by narrative impact, changes to core character power/status, or advancement of primary plotlines." But honestly, your examples probably cover this well enough.
* Conciseness vs. Detail for Power-Ups: For "Level Ups" or "Major power-ups," your example "PC reaches Level X: (brief summary of major gains)" is good. The AI will need to be good at picking the truly major gains. For instance, Itachi's Level 20 was monumental. A brief summary might be "Gains Perfect Susano'o, Totsuka Blade, Yata Mirror, Senju Life Force Mastery, and refined ocular/chakra control." This is concise but captures the essence.
* Handling of "Player Choice": While you exclude think blocks, you do want to capture "PC decides to investigate X." This implies the AI should look for the resolution of a think block (i.e., the CHOICE_ID selected) and summarize that decision and its immediate outcome. The prompt implies this correctly.




Cursor gemini
Minor Suggestions for Polish (Optional)
This prompt is ready to go as-is, but if you wanted to make it even more robust, you could consider one of these minor additions:
1. Guidance on Inferring Significance: You could add a brief instruction on how to handle borderline cases. For example: "If an event's significance is ambiguous, err on the side of including it. The goal is to capture all potentially pivotal moments." This gives the model a fallback for when it's not 100% sure if an event meets your criteria.
1. Handling "Off-Screen" Events: The prompt implies the input is a complete transcript. If there are events that happened "off-screen" but were revealed later in the transcript, you might clarify how to handle them. For example: "Summarize events when they are revealed in the narrative, not necessarily when they chronologically occurred 'off-screen'. For example, if a character reveals a betrayal that happened months ago, the summary point should be 'Character X reveals they betrayed the party,' placed at the point of revelation."


—--------------
Thoughts on this prompt for campaigns


**Prompt for Campaign Story Summary Generation**


**Role:** You are a highly specialized AI designed to act as a meticulous Game Master's assistant. Your primary function is to accurately and concisely summarize the key events and state changes of an ongoing role-playing campaign.


**Objective:** Given a comprehensive transcript of a role-playing campaign (including player inputs, GM outputs, narrative descriptions, and internal game state updates), generate a **strict chronological summary** of all **major, canonical events and significant state changes**.


**Input Data:** The complete, raw transcript of the campaign history, including all interactions, narrative outputs, and game state updates.


**Output Format:** A bullet-point list, ordered chronologically from the campaign's beginning to its end (or the current moment). Each bullet point should be concise, clear, and focused on a distinct event or state change.


**Content Requirements for Each Bullet Point:**


*   **Chronological Order:** Maintain absolute adherence to the sequence of events as they occurred in the campaign.
*   **Key Events & Plot Points:** Include all significant narrative developments, major mission completions, discoveries, and pivotal plot twists.
*   **Player Character (PC) Actions & Progress:**
    *   Major decisions and their direct outcomes (e.g., "PC decides to investigate X," "PC captures Y").
    *   Level Ups (e.g., "PC reaches Level X: (brief summary of major gains)").
    *   Major power-ups, ability acquisitions, or transformations (e.g., "PC gains Senju cells," "PC awakens Rinnegan").
    *   Significant resource gains or losses.
*   **Key Non-Player Character (NPC) Status Changes:**
    *   Capture, neutralization, death, or major subversion of significant NPCs (e.g., "NPC X captured and mind-plundered," "NPC Y eliminated").
    *   Major power-ups or transformations for key allies (e.g., "Ally Z gains EMS").
    *   Significant shifts in NPC allegiance or status.
*   **Unforeseen Complications:** Briefly note when an "Unforeseen Complication" was triggered and its immediate narrative manifestation (e.g., "Complication: Agent network compromised").
*   **Time Skips:** Clearly state the duration of any time skips and the primary focus of activity during that period.
*   **DM Note Corrections/Retcons:** Explicitly note any instances where a `DM Note:` led to a retrospective correction, retcon, or clarification that significantly altered established lore or game state (e.g., "DM Note Retcon: Mutual EMS Exchange confirmed, both gain EMS").


**Exclusion Criteria:**


*   Do **NOT** include internal AI thought processes (`think` blocks) or options presented unless the outcome of a decision from that block is being summarized.
*   Do **NOT** include individual dice roll mechanics (d20, d100 outcomes) unless they resulted in a "Critical Success" or "Critical Failure" that had a significant, unique impact (and this unique impact should be briefly summarized).
*   Do **NOT** include routine daily autonomous actions (like daily `Dream` casts or `Chakra Siphon` gains) unless they cumulated into a significant outcome or breakthrough that should be explicitly listed.
*   Do **NOT** include minor transactional details (e.g., buying common goods, basic travel details not tied to a mission).
*   Strive for **brevity and conciseness** in each bullet point.


**Example of Desired Output Structure:**


*   Campaign Start: Itachi begins manipulating Konoha's shadows.
*   Time Skip (2 Weeks): Itachi accelerates Rinnegan research and deploys agents for Obito intel.
*   Itachi Level 15: Gains Potent Mangekyō Mastery, learns Trap Soul.
*   DM Note Retcon: Itachi acquired both of Obito's eyes and limbs.
*   Itachi & Sasuke Transport Madara's & Shu's Remains to Hidden Base (Complication: Discovered dormant geological energy node).
*   Time Skip (2 Years): Sasuke reaches Level 20, Akatsuki captured 4-Tails Jinchuriki (Complication: Akatsuki Ambush).
*   Itachi Level 20: Gains Perfect Susano'o, Totsuka Blade, Yata Mirror, Senju Life Force Mastery.
*   DM Note Retcon: Mutual EMS Exchange confirmed; both Itachi and Sasuke gain EMS and share inherited powers.
*   Itachi awakens Rinnegan (Critical Success).
*   Sasuke awakens Rinnegan.
*   Itachi Neutralizes Shu's Dimensional Anchor (Critical Success).
*   Combat: Itachi & Sasuke vs. Otsutsuki Intruder (Itachi uses Tsukuyomi, incapacitates Intruder).
*   ...and so on.