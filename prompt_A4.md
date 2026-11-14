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

There's one shared script, "Init Menu", which the scenes call. The variables are mostly the sample's defaults: Quest1–12, Health, Defeated, Turnip Counter, Seen Cat/Duck, Used Radio, Pushed Ice Block, tile and menu/save helpers, and so on. The asset library is the standard bundle: about 40 sprites (NPCs, player variants, chest, portal, switch-like props, enemies and more), around 20 backgrounds, Rulz/Tronimal music tracks, emotes, two fonts and two animated tilesets. The project has no sound-effect assets at the moment.
- Implemented in previous tasks: Chest actor that can be opened and displays a text when opened (and retains an "opened" state); NPC that displays a dialogue when talked to; Enemy that patrols normally and starts chasing the player once he gets too close, goes back to patrolling if player is far enough away

## Task A4: Door/teleporter to a new scene
The player should be able to switch between two scenes via a specific object. A new scene has to be created for this. The starting scene contains a door/teleporter; when the player touches it, the new scene is loaded and the player appears there at a defined position. The new scene also contains an object to return to the previous scene.

### Acceptance criteria
A4.1: A new scene has been created, is walkable and has working (wall) collision.
A4.2: Touching the door/teleporter field changes the scene; it does not trigger from a distance.
A4.3: The player appears at the defined position [OPEN: position], not inside a wall and not on the return object.
A4.4: In the new scene, a return object leads back. The player appears at the defined position in the starting scene, also not on the door trigger.
A4.5: Switching back and forth works at least 5 times in a row without a loop or re-triggering.
A4.6: After each switch, the player can be controlled immediately.


Please start with the step-by-step instructions.
