You are assisting me in developing a Game Boy game with GB Studio 4.3.2.

## How we work
- You act as an advisor. I implement everything myself in the GB Studio editor.
- You cannot see or edit any project files, and I will not share project files or their contents.
- Give numbered step-by-step instructions for the editor: which view to open, which element to select, which event to add, and which values to set. Use the exact names of menus, events and fields as they appear in GB Studio 4.3.2.
- If GBVM code is needed, provide a complete snippet that I can paste unchanged into a "GBVM Script" event.
- I will follow your instructions literally and report what happens, including build output and screenshots of the editor or the running game.
- If information is missing, ask me. If something is not specified, decide yourself and state your decision.

## Global specification
- A "field" is 16x16 px (2x2 tiles), the size of the player sprite.
- Distances are measured in fields as Chebyshev distance: max(|x1 - x2|, |y1 - y2|).
- One second has 60 frames.
- Controls: D-pad = move, A = interact, B = open/close inventory. Start and Select are unused.
- Interaction: the player must be at most 1 field away from the object and face it.
- Returning to the title screen resets all variables and object states to their initial values. Scene changes do not reset states or variables.

## Quality requirements
- The game must build without errors or engine warnings and stay within Game Boy hardware limits.
- Use descriptive names for scenes, actors, triggers and variables. Reuse logic where it is required. Do not change anything the task does not require.

## Current project state
The game is still mostly GB Studio's stock top-down sample project. It has seven TOPDOWN scenes: Logo and Title Screen (UI), the 56-tile-wide Sample Town, two interiors (Music House and Top House), and two cave scenes (Cave and Underground). These are connected by triggers, with 14 in Sample Town alone. The actors are the sample's own:
- Sample Town: an angry guy, a florist, a cat, a duck, a pet owner, a rock and a sign post.
- Music House: a DJ with a drumkit, a keyboard and machines.
- Top House: a radio and the radio guy.
- Caves: a sage, fires, a save point (also stored as the one actor prefab), plus pushable rocks, an ice block and hidden stairs in the Underground.

The only custom addition is a Treasure Chest actor in Sample Town. Sample Town's On Init script now also checks that flag to restore the open sprite when you re-enter the scene. There's one shared script, "Init Menu", which the scenes call. The 34 variables are mostly the sample's defaults: Quest1–12, Health, Defeated, Turnip Counter, Seen Cat/Duck, Used Radio, Pushed Ice Block, tile and menu/save helpers, and so on. Chest Town Opened is the only new one. The asset library is the standard bundle: about 40 sprites (NPCs, player variants, chest, portal, switch-like props, enemies and more), around 20 backgrounds, Rulz/Tronimal music tracks, emotes, two fonts and two animated tilesets. The project has no sound-effect assets at the moment.

## Task A2: NPC with dialogue
An NPC (e.g. a "guard" in a village scene, about 1 field next to the "entrance" (scene-change field)) should be able to talk to the player. He always faces one direction and never moves. He is solid, so the player cannot walk through him. When the player interacts with him, a dialogue box with a text appears (e.g. "Welcome to our village."). The player cannot move during the dialogue. The dialogue can be repeated any number of times. The guard does not turn towards the player.

## Acceptance criteria
A2.1: The NPC stands about 1 field next to an entrance (scene-change field) and does not block it. The entrance remains reachable.
A2.2: He always faces the same direction and never moves, also not during or after a dialogue.
A2.3: He is solid from all four sides.
A2.4: Interaction only works at a distance of at most 1 field while facing the NPC. Merely approaching does not start a dialogue.
A2.5: The dialogue box shows exactly the specified text. The player cannot move during the dialogue and moves normally afterwards.
A2.6: The dialogue can be repeated any number of times with an identical sequence.
A2.7: The NPC does not turn towards the player, even when the player interacts from the side or from behind.

Please start with the step-by-step instructions.


