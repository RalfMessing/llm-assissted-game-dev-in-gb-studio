Claude
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

# LLM answer
Task A2: Village Guard, step-by-step
Decisions I made
Scene: Sample Town. It is the only scene with enough entrances, and the village guard fits there.
Actor name: Village Guard.
Facing: Down. He is posted just beside the entrance and always looks south.
Dialogue: one text box with exactly Welcome to our village., no variables, no extra events.
Entrance: I can’t see your map, so you pick it in step 1. If you tell me which one you chose and where its free neighbouring fields are, I can check the placement before you test.
Steps
Pick the entrance.
Open World view and double-click Sample Town.
Pick one scene-change trigger that sits on open ground, ideally one with walkable fields on at least two sides. The door trigger to Top House or Music House is a good candidate.
Click the trigger once and note its position and size in the sidebar (X/Y, in tiles). One field is 2 tiles.
Add the actor.
In Sample Town, open the + menu in the toolbar and choose Add Actor (or right-click the map and choose Add Actor).
In the sidebar, rename it Village Guard in the name field at the top.
Place him.
Set X and Y in the sidebar so he stands exactly 1 field (2 tiles) away from the trigger, horizontally or vertically. Do not overlap the trigger.
Keep him on a field that is walkable ground, not on a collision tile, and not on any other actor or trigger.
Make sure the entrance is still reachable. At least one field next to the trigger must stay free of the guard, scenery and other actors. If the entrance only has two access fields, choose a position next to the trigger that leaves the main approach free.
Choose the sprite.
In the actor sidebar, click the Sprite Sheet field and pick a humanoid NPC sprite that has directional frames (for example a villager or guard-like sprite from the bundle). Don’t use the same sprite as the Angry Guy, so they are easy to tell apart.
Check the sprite’s Collision Bounds in the Sprites view if you are unsure. The box should cover the full 16x16 field. That is what makes him solid from all four sides (A2.3). You only need to look at it, not change it.
Set the actor properties.
Direction: set to Down.
Animation Speed: set to None (or the lowest static option) so he doesn’t animate.
If a Movement Type field is shown, set it to Static. Do not choose any option that includes facing the player, random walking or rotating.
Leave Collision Group at its default.
Write the interaction script.
With the guard selected, open the On Interact tab of the script editor.
Click Add Event, choose Dialogue → Display Dialogue.
In the text field, type exactly Welcome to our village. and nothing else. Don’t add a manual line break, because the editor wraps long text itself. Check that the preview shows the text in full and without errors.
Add no other events. In particular, do not add Actor Set Direction, Actor Face Toward Player or any movement event. The script stays a single event.
Leave the On Init, On Update and On Hit tabs empty.
Build and test.
Press Run (the Play button) and go to Sample Town. Test each criterion:
A2.1: walk through the entrance from the free side. The scene change must work.
A2.2 / A2.7: stand beside him and behind him, press A each time. He must stay facing down and not turn.
A2.3: try to walk into him from all four sides. You must be blocked every time.
A2.4: walk next to him without pressing A. Nothing must happen. Stand 2 fields away, face him and press A. Nothing must happen. Stand 1 field away, face him and press A. The text box opens.
A2.5: during the dialogue, press the D-pad. You must not move. After closing the box you must move normally.
A2.6: repeat the dialogue at least 5 times and compare it. It must be identical each time.
Also confirm after a dialogue, and after leaving and re-entering Sample Town, that he is still in the same place and facing down.
Check the build output.
Look at the build log after pressing Run. It must show no errors and no warnings. If anything appears, send me the exact text.
Things to report back
Which entrance you picked and the guard’s final X/Y.
Whether you saw a Movement Type field, and what it was set to.
Any warnings in the build output, plus a screenshot of the guard’s sidebar and of the dialogue in the running game if something looks off.

## 2nd Iteration
I followed your instructions. The build succeeded. Test result:

Works as expected:
- A2.1, A2.3, A2.4, A2.5, A2.6, A2.7

Does not work:
- A2.2: Observed: NPC turns toward the player when interacting with him standing 1 field next to him. Expected: NPC does not move or turn, even when interacted with.

## LLM answer
That one is on me. I assumed a single Display Dialogue event would leave him alone, but GB Studio turns an actor toward the player when the player interacts with it, before the On Interact script runs. It is an engine default, not something in your script, so it needs an explicit setting.

Fix
In World view, open Sample Town and select Village Guard.
In the actor sidebar, look for a Face Interaction option (a checkbox or toggle near Direction and Animation Speed). If it is checked or enabled, uncheck it.
Keep Direction set to Down and leave On Interact with the single Display Dialogue event.
Press Run and repeat the A2.2 / A2.7 tests: interact from the left, the right and from behind, and check he stays facing down every time. Also check that the dialogue text and all your earlier passing tests still behave the same.
If you can’t find that option in 4.3.2

I can’t verify from here that the toggle has that exact name in your version. If you don’t see it, use this fallback:

Select Village Guard and open the On Interact tab.
Click Add Event, choose Actor → Set Direction, and set Actor to Self and Direction to Down.
Drag this event to the top of the script, above Display Dialogue. The script is then two events: Set Direction (Self, Down), then Display Dialogue.
Rebuild and retest. The engine’s turn and the reset happen before the next frame is drawn, so you should see no flicker. Tell me if you do see him twitch.
Please report back
Whether you found a Face Interaction option, and what it was set to before and after.
If you used the fallback, whether any flicker was visible.
The result of the A2.2 / A2.7 retest, plus any build warnings.

## 3rd Iteration
I cannot carry out step 4.3.2: Face Interaction option does not exist in GB Studio 22.3.27.
I followed your instructions.
The build succeeded. Test result:

Works as expected:
- A2.1, A2.3, A2.4, A2.5, A2.6, A2.7

Does not work:
- A2.2: Observed: even with new actor direction event, the actor flickers once into the direction you talk to him from. Expected: actor does not move under any circumstance.

## LLM answer
Your report shows the engine turns the actor toward the player before any script runs, so no event or actor property can stop it. My fallback could only reset the direction afterwards, and I was wrong to say it wouldn’t flicker, since I couldn’t verify that. Please also remove that Set Direction event, because it is no longer needed.

The turn only changes which sprite frame is drawn. If the sprite shows the same image in every direction, the turn is invisible, and that is the fix.

Fix: use a sprite that looks identical in all directions
Select Village Guard, open On Interact, and delete the Actor → Set Direction event. Only Display Dialogue with Welcome to our village. remains.
Open the Sprites view and look for a humanoid NPC sprite whose animation type is fixed, meaning it has one animation for all directions. In the sprite editor, check the Animation Type setting (or similarly named dropdown). Sprites of this kind don’t change their picture when the actor’s direction changes. Several sample NPCs are built this way.
If you find one, go back to the Village Guard sidebar, set it as the Sprite Sheet, set Direction to Down, and run the A2.2 / A2.7 tests again.
If no suitable sprite exists: make your own copy
Close the sprite in the editor. In your project’s assets/sprites folder, copy the sprite file you currently use, along with its matching .png, and give the copy a new name such as village_guard. This leaves the original untouched, so other actors are not affected.
In GB Studio, open the new sprite in the Sprites view.
Switch its Animation Type to the fixed-direction option if there is one. If there isn’t, edit the idle animation for Left, Right and Up so they use the same frame as Down. Do the same for the moving state if it is shown.
Select Village Guard, set its Sprite Sheet to the new copy, and keep Direction on Down.
Run it and retest.
Retest
A2.2 / A2.7: interact from the left, right and behind, and watch closely for any frame change.
Confirm that A2.1, A2.3 to A2.6 still pass. In particular, the collision box in the new sprite must still cover the full 16x16 field.
Check the build output for warnings.
Please report
Which option you used (an existing fixed sprite or your own copy), and the name of the sprite.
Whether any flicker remains.
The exact Animation Type options you see in the sprite editor, because I’m not certain of their wording. You wrote “GB Studio 22.3.27”, which doesn’t match 4.3.2. Please check Help → About and tell me which version you are on, in case the menus differ.

## Report back (still 3rd Iteration)
I followed your instructions. The build succeeded. Test result:

Works as expected:
- A2.1, A2.2, A2.3, A2.4, A2.5, A2.6, A2.7

## LLM Answer
All seven criteria pass, so Task A2 is done.

Here is where the project stands:

Village Guard in Sample Town has a single Display Dialogue event in On Interact with the text Welcome to our village.
His Direction is Down, and he uses a sprite that looks the same in every direction. That is why the engine’s turn on interaction is no longer visible.
The earlier Actor → Set Direction event is removed.

Two things are worth a quick check, since I didn’t get your answers last time:

Shared sprite: if you edited a copy, confirm that other actors still use the original. If you picked an existing fixed-direction sprite, any other actor using it will also look the same from every direction, which is harmless but worth knowing.
Version: your earlier message said “GB Studio 22.3.27”, which doesn’t match 4.3.2. If you are on a different version, tell me, because some menu names in my instructions may differ for later tasks.

When you’re ready, send me the next task.



# Task completed
in 18min57sec