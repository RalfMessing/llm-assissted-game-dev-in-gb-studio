Task A4: Door/teleporter to a new scene
The player should be able to switch between two scenes via a specific object. A new scene has to be created for this. The starting scene contains a door/teleporter; when the player touches it, the new scene is loaded and the player appears there at a defined position. The new scene also contains an object to return to the previous scene.

Acceptance criteria
A4.1: A new scene has been created, is walkable and has working (wall) collision.
A4.2: Touching the door/teleporter field changes the scene; it does not trigger from a distance.
A4.3: The player appears at the defined position [OPEN: position], not inside a wall and not on the return object.
A4.4: In the new scene, a return object leads back. The player appears at the defined position in the starting scene, also not on the door trigger.
A4.5: Switching back and forth works at least 5 times in a row without a loop or re-triggering.
A4.6: After each switch, the player can be controlled immediately.
