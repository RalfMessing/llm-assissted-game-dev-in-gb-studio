Task A3: Collectible with counter
The player should be able to pick up a collectible (coin). The coins lie on the ground in the game world, are collected when the player touches them and disappear after being collected (so they cannot be collected again). When a coin is collected, a (predefined) counter is increased by one.

Regression task (if A1 has already been solved): Modify the chest from A1 so that, when opened, it shows the text "Coin found!" (if a text was implemented) and increases the coin counter by 1.

Acceptance criteria
A3.1: At least 3 coins are placed at defined positions [OPEN: positions].
A3.2: The counter is a variable with the initial value 0, and its value can be checked during testing (debug output).
A3.3: On touch, the coin disappears immediately and the counter increases by exactly 1.
A3.4: Each coin counts only once. Standing on the field for a longer time or walking back and forth does not count twice.
A3.5: Collected coins stay gone after a scene change, and the counter value is kept.

Regression task
A3R.1: When the chest is opened, the same coin counter increases by exactly 1, not a second variable.
A3R.2: If A1 has a text, it now reads "Coin found!".
A3R.3: All criteria of A1 still apply unchanged.

