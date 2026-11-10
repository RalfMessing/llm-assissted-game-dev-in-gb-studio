Task A5: Switch with door mechanism
A locked door (leading to another scene) should be openable with a switch. Both objects are in the same scene. The player can activate and deactivate the switch by interacting with it (the switch starts deactivated). The switch changes its appearance depending on its state (e.g. its orientation from left to right). When the switch is activated, the door opens and stays open as long as the switch is activated. When the switch is deactivated again, the door is locked again and stays locked until the switch is activated. The state is kept after a scene change.

(Regression) task (optionally building on A3 and A4): An object for changing scenes (e.g. the one from A4) should be openable and lockable with a collectible key (same behavior as the coins from A3). Alternatively, all of A5 can be implemented for the object from A4.

Acceptance criteria
A5.1: Switch and door are in the same scene. Initial state: switch deactivated (sprite "off"), door locked.
A5.2: While the door is locked, it blocks the player and no scene change happens.
A5.3: Interacting with the switch (at most 1 field away, facing the switch) activates it. The sprite changes and the door opens immediately.
A5.4: Interacting again deactivates it. The sprite changes back and the door closes immediately.
A5.5: Toggling works any number of times. The switch state and the door state never contradict each other.
A5.6: When the door is open, touching it leads to the other scene. There is a way back so that the test is possible.
A5.7: The state is kept after a scene change: switch on -> leave the scene and come back -> switch on, door open. The same applies to "off".

Regression task
A5R.1: The key behaves like a coin: collectible, disappears, permanently gone, no double counting.
A5R.2: Without the key, the scene-change object (e.g. from A4) cannot be passed. With the key, it can be passed.
A5R.3: [OPEN: is the key consumed? can the door be locked again?]
A5R.4: The function from A4 (switching scenes back and forth) remains unchanged when the door is open.
