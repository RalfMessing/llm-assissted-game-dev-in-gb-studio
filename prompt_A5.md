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
- Sample Town: an angry guy, a florist, a cat, a duck, a pet owner, a rock, a sign post, a (initially closed) chest which can be opened and yields one coin, and two other coins which can be collected by walking over them
- Music House: a DJ with a drumkit, a keyboard and machines.
- Top House: a radio and the radio guy.
- Caves: a sage, fires, a save point (also stored as the one actor prefab), plus pushable rocks, an ice block and hidden stairs in the Underground.

There's one shared script, "Init Menu", which the scenes call. The variables are mostly the sample's defaults: Quest1–12, Health, Defeated, Turnip Counter, Seen Cat/Duck, Used Radio, Pushed Ice Block, tile and menu/save helpers, and so on. The asset library is the standard bundle: about 40 sprites (NPCs, player variants, chest, portal, switch-like props, enemies and more), around 20 backgrounds, Rulz/Tronimal music tracks, emotes, two fonts and two animated tilesets. The project has no sound-effect assets at the moment.
- Implemented in previous tasks: Chest actor that can be opened and displays a text when opened (and retains an "opened" state); NPC that displays a dialogue when talked to; modification to the chest actor so that the player receives a coin when opening the chest for the first time; two other coin actors were added where walking over them triggers the collect coin script; Enemy that patrols normally and starts chasing the player once he gets too close, goes back to patrolling if player is far enough away

## Task A5: Switch with door mechanism
A locked door (leading to another scene) should be openable with a switch. Both objects are in the same scene. The player can activate and deactivate the switch by interacting with it (the switch starts deactivated). The switch changes its appearance depending on its state (e.g. its orientation from left to right). When the switch is activated, the door opens and stays open as long as the switch is activated. When the switch is deactivated again, the door is locked again and stays locked until the switch is activated. The state is kept after a scene change.

(Regression) task (optionally building on A3 and A4): An object for changing scenes (e.g. the one from A4) should be openable and lockable with a collectible key (same behavior as the coins from A3). Alternatively, all of A5 can be implemented for the object from A4.

### Acceptance criteria
A5.1: Switch and door are in the same scene. Initial state: switch deactivated (sprite "off"), door locked.
A5.2: While the door is locked, it blocks the player and no scene change happens.
A5.3: Interacting with the switch (at most 1 field away, facing the switch) activates it. The sprite changes and the door opens immediately.
A5.4: Interacting again deactivates it. The sprite changes back and the door closes immediately.
A5.5: Toggling works any number of times. The switch state and the door state never contradict each other.
A5.6: When the door is open, touching it leads to the other scene. There is a way back so that the test is possible.
A5.7: The state is kept after a scene change: switch on -> leave the scene and come back -> switch on, door open. The same applies to "off".

### Regression task
A5R.1: The key behaves like a coin: collectible, disappears, permanently gone, no double counting.
A5R.2: Without the key, the scene-change object cannot be passed. With the key, it can be passed.
A5R.3: The key will be consumed and permanently gone after using the key to unlocking the scene-changing oject (from A4). The door will stay unlocked after consuming the key 
A5R.4: The function from A4 (switching scenes back and forth) remains unchanged when the door is open.
