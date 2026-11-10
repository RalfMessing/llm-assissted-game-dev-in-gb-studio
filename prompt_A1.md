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
- Base project: top-down adventure with a title screen ("Start Game"), five scenes (Top House, Underground, Cave, Sample Town and Music House) connected by a working transition, a player character with sprite, animations, movement and wall collision, and a basic interaction setup.

## Task Task A1: Interactive treasure chest
The player should be able to open a treasure chest by interacting with it. The chest is placed in the game world and can be opened by pressing a button. When the chest is opened, a short message may appear (optional, e.g. "The chest has been opened!") and its (visual) state changes permanently from "closed" to "open". The chest can only be opened once.

## Acceptance criteria
A1.1: The chest is at the defined position [OPEN: position], is initially "closed" and blocks the player (solid).
A1.2: Pressing A only has an effect if the player is at most 1 field away and faces the chest. Otherwise nothing happens.
A1.3: When opened, the sprite changes to "open" immediately. If a message is implemented, it appears exactly once, and the player cannot move while it is shown.
A1.4: Pressing A rapidly several times does not open the chest twice and does not show the message twice.
A1.5: Interacting again triggers nothing (no message, the sprite does not switch back).
A1.6: The "open" state is permanent, also after leaving and re-entering the scene.

Please start with the step-by-step instructions.


