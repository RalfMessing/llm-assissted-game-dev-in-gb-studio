You are assisting me in developing a Game Boy game with GB Studio 4.3.2.

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
The game is still mostly GB Studio's stock top-down sample project. It has eight TOPDOWN scenes: Logo and Title Screen (UI), the 56-tile-wide Sample Town, two interiors (Music House and Top House), two cave scenes (Cave and Underground) and one teleporter room (which is reachable via an invisible trigger). These are connected by triggers, with 18 in Sample Town alone. The actors are the sample's own and some additional actors:
- Sample Town: an angry guy, a florist, a cat, a duck, a pet owner, a rock, a sign post, a (initially closed) chest which can be opened and yields one coin, and two other coins which can be collected by walking over them, a (initially closed) door with a switch next to it, which unlocks the door after interaction; another (initially closed) door which can be unlock by interacting with it after a key has been collected (variable Key State = 0 = door closed, key not yet collected; Key State = 1 = key collected, door can be opened; Key State = 2 = door unlocked, key permanently consumed).
- Music House: a DJ with a drumkit, a keyboard and machines.
- Top House: a radio and the radio guy.
- Caves: a sage, fires, a save point (also stored as the one actor prefab), plus pushable rocks, an ice block and hidden stairs in the Underground.

There's one shared script, "Init Menu", which the scenes call. The variables are mostly the sample's defaults: Quest1–12, Health, Defeated, Turnip Counter, Seen Cat/Duck, Used Radio, Pushed Ice Block, tile and menu/save helpers, and so on. The asset library is the standard bundle: about 40 sprites (NPCs, player variants, chest, portal, switch-like props, enemies and more), around 20 backgrounds, Rulz/Tronimal music tracks, emotes, two fonts and two animated tilesets. The project has no sound-effect assets at the moment.
- Implemented in previous tasks: Chest actor that can be opened and displays a text when opened (and retains an "opened" state); NPC that displays a dialogue when talked to; modification to the chest actor so that the player receives a coin when opening the chest for the first time; two other coin actors were added where walking over them triggers the collect coin script (the collect coin script increments the variable CoinCounter); Enemy that patrols normally and starts chasing the player once he gets too close, goes back to patrolling if player is far enough away (this is done by events in the OnInit and OnUpdate tabs of the enemy actor); 

## Task A6: Simple inventory system
A simple inventory system in which the player can view collected items. 
The player can collect different item types (coins, a key and a radio, all of which have their respective sprites) that are placed somewhere in the game world. 
Collected items are stored in the inventory, which can be opened and closed with a defined button, and are displayed with their icon and the collected quantity. 
Item counts are kept after a scene change.

## Regression task: 
Also show the collectible coins from A3 and the collectible key from the optional task in A5 in the inventory.

## Acceptance criteria
A6.1: At least 3 different item types are placed at fixed positions in the game world; at least one type exists 2 or more times.
A6.2: Collecting an item makes it disappear and increases the count of exactly this type by 1. Initial counts are 0.
A6.3: The inventory opens and closes with the B button.
A6.4: It shows the icon and the count for each type.
A6.5: While the inventory is open, the game is paused and the player does not move. After closing, everything continues as before.
A6.6: The inventory cannot be opened during a dialogue.
A6.7: Counts are kept after a scene change.

## Regression task
A6R.1: Coins from A3 and the key from A5 appear in the inventory with icon and count.
A6R.2: The inventory display and the counter or key status always match (one data source, no double bookkeeping).
A6R.3: The behavior of coins, chest, key and door remains unchanged.
