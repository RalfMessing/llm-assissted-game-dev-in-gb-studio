Task A1: Interactive treasure chest
The player should be able to open a treasure chest by interacting with it. The chest is placed in the game world and can be opened by pressing a button. When the chest is opened, a short message may appear (optional, e.g. "The chest has been opened!") and its (visual) state changes permanently from "closed" to "open". The chest can only be opened once.

Acceptance criteria
A1.1: The chest is at the defined position [OPEN: position], is initially "closed" and blocks the player (solid).
A1.2: Pressing A only has an effect if the player is at most 1 field away and faces the chest. Otherwise nothing happens.
A1.3: When opened, the sprite changes to "open" immediately. If a message is implemented, it appears exactly once, and the player cannot move while it is shown.
A1.4: Pressing A rapidly several times does not open the chest twice and does not show the message twice.
A1.5: Interacting again triggers nothing (no message, the sprite does not switch back).
A1.6: The "open" state is permanent, also after leaving and re-entering the scene.

