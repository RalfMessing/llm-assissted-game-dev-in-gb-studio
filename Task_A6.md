Task A6: Simple inventory system
A simple inventory system in which the player can view collected items. The player can collect different item types (e.g. 3) that are placed somewhere in the game world. Collected items are stored in the inventory, which can be opened and closed with a defined button, and are displayed with their icon and the collected quantity. Item counts are kept after a scene change.

Regression task: Also show the collectible coins from A3 and the collectible key from the optional task in A5 in the inventory.

Acceptance criteria
A6.1: At least 3 different item types are placed at fixed positions in the game world; at least one type exists 2 or more times.
A6.2: Collecting an item makes it disappear and increases the count of exactly this type by 1. Initial counts are 0.
A6.3: The inventory opens and closes with the B button.
A6.4: It shows the icon and the count for each type.
A6.5: While the inventory is open, the game is paused and the player does not move. After closing, everything continues as before.
A6.6: The inventory cannot be opened during a dialogue.
A6.7: Counts are kept after a scene change.

Regression task
A6R.1: Coins from A3 and the key from A5 appear in the inventory with icon and count.
A6R.2: The inventory display and the counter or key status always match (one data source, no double bookkeeping).
A6R.3: The behavior of coins, chest, key and door remains unchanged.

