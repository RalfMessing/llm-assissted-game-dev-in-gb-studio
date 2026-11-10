Task A7: Enemy with chasing behavior
There should be enemies that patrol a small area and chase the player as soon as and as long as the player is within a defined detection radius (e.g. 2 [OPEN: tiles or fields] by Chebyshev distance, i.e. max(|x1 - x2|, |y1 - y2|)). When the player leaves the detection radius, the enemy stops chasing. The enemy cannot move through walls or other solid objects. On contact with the player, a message is displayed (optionally, the player can also be sent back to the start scene or even to the title screen).

Acceptance criteria
A7.1: At least 1 enemy patrols deterministically on a fixed, small route (back and forth in a 1x3 area, e.g. from the starting field two fields to the right, then from there two fields to the left, and so on).
A7.2: When the scene is entered, the enemy always starts at its patrol start.
A7.3: If the Chebyshev distance is at most 2, the enemy chases the player.
A7.4: If the distance becomes greater than 2, the chase ends immediately and the enemy returns to patrolling (its new starting field is the field it is on when the chase stops). It does not stand still and does not chase permanently.
A7.5: The enemy does not move through walls or solid objects, does not get stuck permanently and does not leave the scene.
A7.6: The enemy is slower than the player (the player can escape).
A7.7: On contact (fields overlap), the player is sent to the title screen and has to restart.
