# Karpathy LLM Wiki Gist - Comments
Source: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
Total comments: 30

--- [2026-04-04T16:49:23Z] @lisardo-iniesta ---
thank you Andrej!


--- [2026-04-04T16:50:19Z] @SagiPolaczek ---
Thank you for sharing!

now claude, pls read: `https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f`

--- [2026-04-04T16:50:55Z] @ANKIT0017 ---
how much time did it took from you?

--- [2026-04-04T16:53:11Z] @alinawab ---
Thank you. This is amazing. 

--- [2026-04-04T16:53:14Z] @AntonioCoppe ---
Thanks a lot, Andrej! Keep up the great work and thought-sharing for civilization's advancements!

--- [2026-04-04T16:53:40Z] @Shanks239 ---
Thanks for this, would put it to good use

--- [2026-04-04T16:55:06Z] @SoMaCoSF ---
I have my bot CONSTANTLY push gists... when in mid development - Ill often tell them "OK Great, now publish all this to a gist, give visuals, diagrams as SVGs - include mermaid and sankey logic as appropriate, give me the link" <-- Its a wonderful tool, then I just push Gists between frontiers, like having @grok read them, then publish a response for claude and my agents etc... USE MORE GISTS!!

--- [2026-04-04T16:55:40Z] @mexiter ---
good one, let me put it in motion! Thank you 

--- [2026-04-04T16:55:59Z] @wjlucc ---
Thanks for sharing! This is super helpful.

--- [2026-04-04T16:57:25Z] @alinawab ---
What's the failure mode? Where does it start fighting you? 

--- [2026-04-04T16:57:36Z] @alinawab ---
How do you decide when to create a new page vs edit an existing one?

--- [2026-04-04T16:59:30Z] @mingyue220 ---
thanks

--- [2026-04-04T16:59:56Z] @geetansharora ---
Great. Thanks for sharing.
One question: how can I share the knowledge base with my team? Currently we create a RAG and then a MCP server. Other users just connect to that MCP server and access it.
Should we follow a similar approach with this or something else? 

--- [2026-04-04T17:02:02Z] @samflipppy ---
.brain folder at the root of my project

it's a set of markdown files that act as persistent memory across sessions. every time an AI agent starts working on my project, it reads .brain/index.md first. no "here's what we did last time" back and forth. it just knows.

here's what's in mine:

-index.md - current state of the project, what's deployed, what's broken, priorities
-architecture.md - stack, data flow, file map, key design patterns
-decisions.md - every architecture decision with the rationale and trade-offs
-changelog.md - what changed and when, with file namesbeen fixed
changelog.md - what changed and when, with file names
-deployment.md - URLs, env vars, secrets, how to deploy
-firestore-schema.md - every collection, field, and relationship
-pipeline.md - my real data (i'm building a job search tool and using it myself)

(stays local doesnt get commited)

the rules are simple: read .brain before making changes. update .brain after making changes. never commit it to git.

it solves the biggest problem with using AI for development - context loss. i can close a session, come back 3 days later with a completely new conversation, and the agent picks up exactly where the last one left off. it knows what's deployed, what broke last time, what decisions were made and why.

the changelog alone has saved me hours. instead of digging through git commits to figure out what changed, the agent reads the changelog and knows "oh, we switched from Genkit schema enforcement to manual JSON parsing because Gemini kept failing structured output. don't revert that."

it's not complicated. it's just markdown files. but it turns every AI session from "let me re-explain my entire project" into "read .brain and get to work."

--- [2026-04-04T17:06:40Z] @thelabvenice ---
legend 

--- [2026-04-04T17:09:29Z] @expectfun ---
Thank you! 

I think that the "append-and-review note" described in a [separate Andrej's blog post](https://karpathy.bearblog.dev/the-append-and-review-note) in 2025 is also a good idea which gets even better with agents, and it feels like such a note could be a part of such a wiki. 

But that note doesn't seem to be mentioned here (or am I missing?), so now I wonder whether combining those two ideas is a good idea. Guess there's only one way to find out...

--- [2026-04-04T17:14:00Z] @jshph ---
<img width="506" height="174" alt="Screenshot 2026-04-04 at 1 08 09 PM" src="https://gist.github.com/user-attachments/assets/4dc8041a-4337-4128-822d-f142b35481e3" />

this could be kindred thinking -- whether a workspace with tags that one's personally used for a long time, or one that an agent has been maintaining for a few weeks. CLAUDE.md can describe how the agent ought to construct new knowledge (with frontmatter `created: "[[2026-04-04]]"` fields etc), yet connections need to be drawn across the whole knowledge base. This design pattern allows the agent to continue building its working memory around its latest content but map core ideas over the entire vault

--- [2026-04-04T17:14:46Z] @bhagyeshsp ---
Thanks Andrej! Reading the idea in this format makes more sense now. I will try it.

On a related note, I'm maintaining a personal "learning" directory with different subdir with dedicated topics, a root progress.md etc. It is my 15-30 minute learning sprint with the help of the agent. The agent teaches me concepts as per my learner profile and preferences. Once one concept layer is complete, it ends the session, updates the relevant topic's progress file, marks notes and next session objectives for the next intance of the agent for the next day.

--- [2026-04-04T17:18:16Z] @lightningRalf ---
`Note that LLMs can't natively read markdown with inline images in one pass — the workaround is to have the LLM read the text first, then view some or all of the referenced images separately to gain additional context.`

Just tell pi to write an extension for that.

--- [2026-04-04T17:20:08Z] @logancautrell ---
This is amazing and I have already setup a similar inspired process using zed code + obsidian. Really appreciate your inspiration and this gist will help me refine. Kudos!

--- [2026-04-04T17:22:36Z] @function1st ---
Wonderful meta concept here. 

--- [2026-04-04T17:25:59Z] @ppeirce ---
you mention using the dataview plugin, but even better now is the first-party Bases plugin 

--- [2026-04-04T17:29:27Z] @EyderC ---
Que buena idea, a menudo me pierdo entre tantos campos que me interesan debido a que lo que sintetizo queda todo disperso en mis notas del iPad. 


--- [2026-04-04T17:29:49Z] @gkaria ---
Thank you, @karpathy ! So cool. Very helpful.

--- [2026-04-04T17:31:52Z] @jamesalmeida ---
`Note that LLMs can't natively read markdown with inline images in one pass — the workaround is to have the LLM read the text first, then view some or all of the referenced images separately to gain additional context.`

Instead of forcing separate passes for text and visuals, you can have the LLM pre-generate detailed descriptions for the images. Including these descriptions in the text could allow the LLM to process the entire context at once in future reads.

--- [2026-04-04T17:35:15Z] @Hosuke ---
Really appreciate the detailed writeup — the three-layer architecture (raw → wiki → schema) and the index.md + log.md navigation pattern are exactly what I was missing when I first tried implementing this from your tweet.

I ended up building an open source version: https://github.com/Hosuke/llmbase. Instead of relying on Obsidian as the frontend, it ships with a full React web UI, so the whole system is self-contained and deployable anywhere with one command. The "explorations add up" principle turned out to be the most powerful part — once Q&A answers file back into the wiki and linting suggests new connections, the knowledge base genuinely compounds.

One thing I found useful: model fallback chains. When the primary LLM times out mid-compilation, falling back to a secondary model keeps the wiki growing without manual intervention. Pairs well with an autonomous worker for continuous ingestion.

--- [2026-04-04T17:35:34Z] @tomicz ---
I use Plan mode in Cursor, it sounds similar to that? Might I be wrong?

--- [2026-04-04T17:37:24Z] @samjundi1 ---
Thanks Andrej!

--- [2026-04-04T17:39:23Z] @abodacs ---
Thank you for sharing! Andrej 

--- [2026-04-04T17:42:22Z] @AayushMathur7 ---
Awesome! Getting my OpenClaw to set this up right now
