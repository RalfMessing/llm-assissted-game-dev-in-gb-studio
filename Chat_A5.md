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

# LLM Answer

I’m assuming GB Studio 4.x menu and event names; I can’t verify version “22.3.27”. If a name differs in your editor, tell me the name you see.

My decisions

Switch and door go in Sample Town. The door leads to a new small scene, Switch Door Room, which has a way back.
The switch state is stored in a global variable, so it survives scene changes.
The switch shows its state by direction: Left = off, Right = on.
The door is an actor. Deactivate Actor opens it: an inactive actor is invisible and doesn’t block the player.
The trigger behind the door also checks the variable. That way no scene change happens while the door is locked, even if the player somehow reaches the trigger.
The key logic uses one variable, Key State: 0 = in the world, 1 = carried, 2 = used. Because it has only one value at a time, the states can’t contradict each other.
1. Variables
Open the Variables view.
Rename two unused variables:
Switch Door On (0 = off, 1 = on)
Key State (0 / 1 / 2)
2. New scene “Switch Door Room”
In the Game World, right-click an empty area → Add Scene.
Set the name to Switch Door Room, Type Top Down 2D, and choose a small interior background (e.g. the one from Top House).
On Init: add Call Script → Init Menu, as the other scenes do.
Add a trigger at the bottom edge and name it Exit To Sample Town.
On Enter: Change Scene → Sample Town. Set X/Y to the field one field below the door (not on the door itself). Direction: Down.
3. Shared script “Update Switch Door”
Open Scripts → + → name it Update Switch Door.
Add If Variable Is ‘True’ → Variable Switch Door On.
True branch:
Set Actor Direction → Actor A (switch) → Right
Deactivate Actor → Actor B (door)
Else branch:
Set Actor Direction → Actor A → Left
Activate Actor → Actor B
If the editor doesn’t offer A/B, use the actor parameters your version offers. The first one is the switch, the second the door.
4. Actors in Sample Town

Door

Pick a field where the door is the only way through: there should be a wall or solid collision on both sides and behind it. If needed, use the Collisions tool to paint the neighboring fields solid.
Add an actor there, named Switch Door. Sprite: rock, or a door-like sprite if you have one. No scripts.

Switch

Add an actor Door Switch. Choose a switch-like sprite whose Left and Right frames look different (check this in the Sprite Editor). Initial direction: Left.
On Init: Call Script Update Switch Door with A = Door Switch, B = Switch Door.
On Interact:
If Variable Is ‘True’ Switch Door On
True: Set Variable To ‘False’ Switch Door On
Else: Set Variable To ‘True’ Switch Door On
After the If: Call Script Update Switch Door (A = Door Switch, B = Switch Door).
5. Door trigger
Place a 1x1-field trigger exactly on the door’s field and name it Switch Door Entrance.
On Enter: If Variable Is ‘True’ Switch Door On → Change Scene → Switch Door Room, spawn one field above the exit trigger, direction Up. Leave the Else branch empty.
6. Regression: key

I’m assuming A4 is a trigger with a Change Scene event. If not, describe your A4 object to me.

Key (Sample Town)

Add an actor Key with any key- or coin-like sprite.
On Init: If Variable Compare With Value Key State ≠ 0 → Deactivate Actor Key.
Use the same hit event your A3 coins use (e.g. On Hit → Player):
If Variable Compare With Value Key State = 0:
Set Variable To Value Key State = 1
Deactivate Actor Key
Display Dialogue: “You found a key!”

Key door (at the A4 object)

Place an actor Key Door directly on the A4 trigger’s field.
On Init: If Variable Compare With Value Key State = 2 → Deactivate Actor Key Door.
On Interact: If Variable Compare With Value Key State = 1
True:
Set Variable To Value Key State = 2
Deactivate Actor Key Door
Display Dialogue: “The key unlocks the door.”
Else: Display Dialogue: “Locked. You need a key.”
In the A4 trigger, wrap its existing Change Scene in If Variable Compare With Value Key State = 2. Change nothing else in it.
Test sequence
Start the game. The switch points left, the door blocks, and touching the area behind it does nothing (A5.1, A5.2).
Interact with the switch. It points right and the door disappears. Interact again: it points left and the door is back. Repeat several times (A5.3–A5.5).
With the switch on, go through the door, come back, and check that the switch and door are still on and open. Repeat with the switch off (A5.6, A5.7).
Without the key, the A4 door blocks and shows “Locked”. Pick up the key and leave and re-enter the scene: the key stays gone. Unlock the door, switch scenes back and forth, and check that the door stays open and the key is gone (A5R.1–A5R.4).

If the build shows a sprite or tile limit warning for Sample Town, send me the build output.

Question: What exactly is your A4 object (trigger or actor, and in which scene)? If it’s different from what I assumed, I’ll adjust step 6.

# 2nd Iteration
I followed your instructions. The build succeeded. Test result: 

Works as expected: 
A5.1: Switch and door are in the same scene. Initial state: switch deactivated (sprite "off"), door locked.
A5.2: While the door is locked, it blocks the player and no scene change happens.
A5.5: Toggling works any number of times. The switch state and the door state never contradict each other.
A5.6: When the door is open, touching it leads to the other scene. There is a way back so that the test is possible.
A5.7: The state is kept after a scene change: switch on -> leave the scene and come back -> switch on, door open. The same applies to "off".
 A5R.1: The key behaves like a coin: collectible, disappears, permanently gone, no double counting.
A5R.2: Without the key, the scene-change object cannot be passed. With the key, it can be passed.
A5R.3: The key will be consumed and permanently gone after using the key to unlocking the scene-changing oject (from A4). The door will stay unlocked after consuming the key 
A5R.4: The function from A4 (switching scenes back and forth) remains unchanged when the door is open.

A5R.1: The key behaves like a coin: collectible, disappears, permanently gone, no double counting.
A5R.2: Without the key, the scene-change object cannot be passed. With the key, it can be passed.
A5R.3: The key will be consumed and permanently gone after using the key to unlocking the scene-changing oject (from A4). The door will stay unlocked after consuming the key 
A5R.4: The function from A4 (switching scenes back and forth) remains unchanged when the door is open.

Does not work: 

A5.3 and A5.4 Observed: The door switch does not change direction/sprite after interaction/locking/unlocking the switch door. Expected: The switch should change appearance/direction depending on its state (e.g. switch is left = door open, e.g. switch is right = door locked)

A5.3 and A5.4 Observed: In the closed door state, the switch door actor is visible. After unlocking the door, the switch door actor is no longer visible. However, the door/scene changes still works correctly. Expected: The switch door should change its apperance depending on its state open/closed
Regression task: Observed: In the closed key door state, the key door actor is visible. After unlocking the door, the key door actor is no longer visible. However, the door/scene changes still works correctly. Expected: The key door should change its apperance depending on its state locked/unlocked

# LLM Answer

Both problems come from the same thing: state is currently shown by actions that don’t change the sprite.

Switch: its sprite almost certainly has the animation type Fixed Direction. With that type, Set Actor Direction changes nothing visible.
Doors: Deactivate Actor removes the door completely, so you see it vanish instead of open.

My decisions

All three objects show their state by direction. Switch: Left = off, Right = on. Doors: Down = closed, Up = open.
An open door stays visible but no longer blocks the player. Actor Collisions Disable does that instead of Deactivate Actor.
Both doors use one new door sprite with two frames.
1. Fix the switch sprite
Open Sprites and select the sprite used by Door Switch.
Check that no other actor uses this sprite. If one does, duplicate the sprite and give the copy to the switch only.
Under Animation Settings, set Animation Type to Multiple Directions.
Select the Right animation and put the “lever right” frame in it.
Select the Left animation and tick Flip ‘Right’ Animation.
2. New door sprite
Create a 32x16 px PNG named door.png: left 16x16 frame = closed door, right 16x16 frame = open doorway. Use the same 4-color palette as the other sprites.
Put it in your project’s assets/sprites folder. It then appears in Sprites.
Set Animation Type to Multiple Directions.
Down animation: closed frame.
Up animation: open frame.
Left and Right animations: closed frame.
On both Switch Door and Key Door: set Sprite Sheet to door and Initial Direction to Down.
3. Script “Update Switch Door”

Replace the content of both branches:

True branch:
Set Actor Direction A → Right
Set Actor Direction B → Up
Actor Collisions Disable B
Else branch:
Set Actor Direction A → Left
Set Actor Direction B → Down
Actor Collisions Enable B

If the collision events have a different name, type “Collision” into the event search.

4. Key Door scripts

On Init, replace the existing If:

If Variable Compare With Value Key State = 2:
Set Actor Direction Self → Up
Actor Collisions Disable Self

On Interact, replace everything with three separate If events in this order:

If Key State = 0:
Set Actor Direction Self → Down
Display Dialogue “Locked. You need a key.”
If Key State = 1:
Set Variable To Value Key State = 2
Set Actor Direction Self → Up
Actor Collisions Disable Self
Display Dialogue “The key unlocks the door.”
If Key State = 2:
Set Actor Direction Self → Up

The extra direction events keep the door showing the right state if the engine turns the actor toward the player during interaction.

The triggers stay unchanged. They keep checking the variables, so no scene change can happen while a door is locked.

Retest
A5.3/A5.4: Interact with the switch. It turns right and the door shows open. Interact again: the switch turns left and the door shows closed and blocks again.
A5.5: Toggle several times; switch and door must always match.
A5.7: Leave and re-enter the scene with the switch on, then with it off.
Regression: Unlock the key door. It shows open and you can walk through. Leave and re-enter the scene: it still shows open.

If the switch still doesn’t change, send a screenshot of its sprite in the Sprite Editor with Animation Settings visible.

# Task finished 
53min 52sek