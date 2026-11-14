You are assisting me in developing a Game Boy game with GB Studio 22.3.27.

## How we work
- You act as an advisor. I implement everything myself in the GB Studio editor.
- You cannot see or edit any project files, and I will not share project files or their contents.
- Give numbered step-by-step instructions for the editor: which view to open, which element to select, which event to add, and which values to set. Use the exact names of menus, events and fields as they appear in GB Studio 22.3.27.
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

The only two custom additions are a Treasure Chest actor in Sample Town and a Village Guard NPC actor in Sample Town. Sample Town's On Init script now also checks that flag to restore the open sprite when you re-enter the scene. There's one shared script, "Init Menu", which the scenes call. The 34 variables are mostly the sample's defaults: Quest1–12, Health, Defeated, Turnip Counter, Seen Cat/Duck, Used Radio, Pushed Ice Block, tile and menu/save helpers, and so on. Chest Town Opened is the only new one. The asset library is the standard bundle: about 40 sprites (NPCs, player variants, chest, portal, switch-like props, enemies and more), around 20 backgrounds, Rulz/Tronimal music tracks, emotes, two fonts and two animated tilesets. The project has no sound-effect assets at the moment.

Task A7: Enemy with chasing behavior
There should be enemies that patrol a small area and chase the player as soon as and as long as the player is within a defined detection radius (e.g. 2 [OPEN: tiles or fields] by Chebyshev distance, i.e. max(|x1 - x2|, |y1 - y2|)). When the player leaves the detection radius, the enemy stops chasing. The enemy cannot move through walls or other solid objects. On contact with the player, a message is displayed (optionally, the player can also be sent back to the start scene or even to the title screen).

Acceptance criteria
A7.1: At least 1 enemy patrols deterministically on a fixed, small route (back and forth in a 1x3 area, e.g. from the starting field two fields to the right, then from there two fields to the left, and so on).
A7.2: When the scene is entered, the enemy always starts at its patrol start.
A7.3: If the Chebyshev distance is at most 2, the enemy chases the player.
A7.4: If the distance becomes greater than 2, the chase ends immediately and the enemy returns to patrolling (its new starting field is the field it is on when the chase stops). It does not stand still and does not chase permanently.
A7.5: The enemy does not move through walls or solid objects, does not get stuck permanently and does not leave the scene.
A7.6: The enemy is slower than the player (the player can escape).
A7.7: On contact (fields overlap), the player is sent to the title screen and has to restart.

Please start with the step-by-step instructions.