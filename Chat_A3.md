
# LLM Answer
Task A3: Coins with counter (plus chest regression)
Decisions:

    Placement: 3 coins in Sample Town.
    Counter: a global variable Coin Counter.
    Per-coin flags: one global flag per coin, so collected coins stay gone after a scene change.
    Shared scripts: the pickup logic and the On Init check are each a shared script, so the logic exists only once.
    Debug output: after each pickup, a short dialogue shows the counter value.

1. Create the variables

    Open the Variables view in the left navigation.
    Rename four unused variables:
        Coin Counter
        Coin Town 1 Collected
        Coin Town 2 Collected
        Coin Town 3 Collected

Global variables start at 0 (false), so no extra initialization is needed.
2. Script “Collect Coin” (pickup logic)

    Open the Scripts section in the left navigation, click +, and name the script Collect Coin.
    Add the event If Variable Is ‘True’. Set the variable to Variable A, the script parameter.
    Leave the True branch empty. This blocks double counting.
    In the Else branch, add these events in this order:
        Variable Set To ‘True’, variable: Variable A
        Deactivate Actor, actor: Actor A
        Variable Increment By 1, variable: Coin Counter
        Display Dialogue, text: Coins: and then type $ and choose Coin Counter from the list.
    In the script’s sidebar under Parameters:
        Rename Variable A to Coin Flag and Actor A to Coin.
        If Coin Flag has a type option, set it to Variable (by reference), not Value. Otherwise the flag would not be saved.

If an event name doesn’t match exactly, search for its key word (e.g. “Deactivate”) in the Add Event search box.
3. Script “Hide Collected Coin” (restore after scene change)

    Create a new script named Hide Collected Coin.
    Add If Variable Is ‘True’ with Variable A.
    In the True branch, add Deactivate Actor with Actor A. Leave Else empty.
    Under Parameters, rename them to Coin Flag and Coin.

4. Place the coins

    Open Sample Town and add an actor.
        Name: Coin Town 1
        Sprite: the coin sprite (see the question below)
        Collision Group: leave at default
    Place it on a free, walkable field. It must not be on a trigger, an actor, or a collision tile.
    Open the actor’s On Hit tab, then the Player sub-tab, and add Call Script:
        Script: Collect Coin
        Coin Flag: Coin Town 1 Collected
        Coin: Coin Town 1
    Leave On Interact empty.
    Repeat for Coin Town 2 and Coin Town 3, each with its own flag. Keep at least one field between coins.

5. Update Sample Town’s On Init

    Select the scene Sample Town, then open the On Init tab.
    At the very top, before the existing events, add three Call Script events with Hide Collected Coin:
        Coin Town 1 Collected / Coin Town 1
        Coin Town 2 Collected / Coin Town 2
        Coin Town 3 Collected / Coin Town 3

Placing them at the top hides collected coins before the fade-in, so they never flash on screen.
6. Regression: the chest (A3R)

    Select the Treasure Chest actor and open On Interact.
    Find the branch that runs only when the chest is still closed (where Chest Town Opened gets set to true). Change only this branch:
        If it has a Display Dialogue, change its text to Coin found!.
        Add Variable Increment By 1 with Coin Counter right after Variable Set To ‘True’ (Chest Town Opened).
    Change nothing else, including the On Init check for the open sprite.

7. Test

    Build and check that there are no errors or warnings.
    In the game, check:
        A3.3: Touch a coin. It disappears and the dialogue shows “Coins: 1”.
        A3.4: Walk back and forth over the coin’s field. Nothing more happens.
        Deactivation holds: Walk far enough that the coin scrolls off screen, then come back. The coin stays gone.
        A3.5: Enter a house, come back out. Coins stay gone, and the next coin shows the correct total.
        A3R: Open the chest. You see “Coin found!”, and the next coin shows the total +1. Opening the chest again adds nothing.
        Title reset: Return to the title screen and start again. Coins are back and the counter is 0.

Question for you

Is there a coin sprite in the Sprites list, and what is it called? If there isn’t one, tell me which small item sprites exist (e.g. turnip, chest), and I’ll decide which to use.

# 2nd iteration
I cannot carry out step 2.4.d: there is no list being displayed in GB Studio 4.3.2.

I cannot carry out step 4.3: the coin actor does not have an "On Hit" tab.

# LLM Answer
Checking how the coin trigger overlaps the player's bounds

Both issues have workarounds. For the dialogue, insert the variable by its number. For the pickup, use a trigger on each coin instead of On Hit.
Fix for 2.4.d: variable in the dialogue text

    Open the Variables view and find Coin Counter. Note the number GB Studio shows for it, e.g. in the sidebar or as its original name Variable NN.
    In the Display Dialogue of Collect Coin, enter the text Coins: $NN$. Replace NN with that number, without leading zeros.
    Click outside the text field. The editor should turn $NN$ into a variable token labeled Coin Counter.

If you can’t find the number, or no token appears, send me a screenshot of the Variables view with Coin Counter selected.
Fix for 4.3: trigger instead of On Hit

A trigger can’t be entered while the coin actor is solid, so each coin needs its collision disabled. This goes into the existing Hide Collected Coin script. I’m also renaming it, because it now does more than hide.
A. Adjust the script “Hide Collected Coin”

    Rename it to Init Coin.
    At the very top, before the If, add Actor Collisions Disable with actor Actor A. If the name differs, search for “Collisions”.
    Leave the rest unchanged (If Coin Flag is true → Deactivate Actor Actor A).

The three Call Script events in Sample Town’s On Init now call Init Coin automatically, because the rename keeps the reference.
B. A trigger for each coin

    In Sample Town, add a trigger and name it Coin Town 1 Pickup.
    Make it 2 tiles wide and 2 tiles high, positioned exactly over the coin sprite Coin Town 1.
    In the On Enter tab, add Call Script:
        Script: Collect Coin
        Coin Flag: Coin Town 1 Collected
        Coin: Coin Town 1
    Repeat for coins 2 and 3 with their own flags and actors.
    Leave the coin actors’ On Interact empty.

Walking back over a trigger after collecting does nothing more, because Collect Coin checks the flag first (A3.4).
Test

    Build and check that there are no warnings.
    Walk onto a coin. It disappears and “Coins: 1” appears.
    Walk back and forth over the spot. Nothing more happens.
    Approach each coin from all 4 directions. Each should trigger exactly when you step onto its field. If one only reacts from some directions, tell me which coin and direction, plus the coin’s X/Y and the trigger’s X/Y/size.

The coin-sprite question from my first answer is still open.

# 3rd iteration

I followed your instructions. The build succeeded. Test result:

Does not work:
- Acceptance criteria A3.4: Observed: repeatedly walking into the coin pickup triggers increments the coin counter every time and the dialog is displayed. Expected: walking over the coin pickup trigger repeatedly does nothing.
Checking how the flag's value gets passed into each call

# LLM Answer
The cause is almost certainly the Coin Flag parameter in Collect Coin: it’s being passed by value. The script then only changes a copy of the flag, the real flag Coin Town N Collected stays false, and the If check lets every visit through. This would also break A3.5, because collected coins would reappear after a scene change.
Fix: pass the parameter by reference

    In the left navigation under Scripts, select Collect Coin.
    In the sidebar under Parameters, find Coin Flag.
    Set the dropdown next to it to the by-reference option (Pass By Reference or Variable, not Pass By Value or Value).
    Don’t change anything else. The three triggers keep their settings.
    Build and test:
        Walk over each coin trigger several times. The counter should increase only on the first visit.
        A3.5: Collect a coin, go into a house and come back out. That coin stays gone, and the next coin shows the correct total.

If there is no such option

In that case, move the check and the flag into each trigger, and keep only the shared actions in the script.

    Change Collect Coin:
        Delete the If event and its contents.
        Add these events in this order:
            Deactivate Actor with Actor A
            Variable Increment By 1 with Coin Counter
            Display Dialogue with Coins: $NN$
        The Coin Flag parameter is no longer used. If it is still listed, ignore it.
    In the On Enter of each trigger Coin Town N Pickup:
        Add If Variable Is ‘True’ with Coin Town N Collected. Leave the True branch empty.
        In Else, add Variable Set To ‘True’ with Coin Town N Collected.
        Move the existing Call Script Collect Coin into Else, after the Set To True. Set Coin to Coin Town N.
    Init Coin only reads the flag, so by-value is fine there and it needs no change.

Then test as in step 5 above. If it still counts more than once, send me a screenshot of a trigger’s On Enter script and of the Collect Coin sidebar.

# 4th iteration
The Coin Flag parameter in the Collect Coin script was already set to "By Ref"

# LLM Answer
Weighing a possible compiler bug in the If branch

Then I won’t keep debugging the parameter. Instead, we’ll take the flag out of the script entirely: each trigger checks and sets its own global flag directly, and Collect Coin only performs the shared actions. That way, no flag access depends on how a script parameter is handled.
1. Simplify Collect Coin

    Select Collect Coin under Scripts.
    Delete the If Variable Is ‘True’ event together with its contents.
    Add these events, in this order:
        Deactivate Actor with Actor A
        Variable Increment By 1 with Coin Counter
        Display Dialogue with Coins: $NN$, exactly as before
    If Coin Flag is still listed under Parameters, ignore it.

2. Change each trigger

Do these steps for each trigger Coin Town N Pickup (N = 1, 2, 3):

    Open its On Enter tab.
    Add If Variable Is ‘True’ with Coin Town N Collected. Leave the True branch empty.
    In the Else branch, add Variable Set To ‘True’ with Coin Town N Collected.
    Move the existing Call Script Collect Coin into the Else branch, below Variable Set To ‘True’. Set Coin to Coin Town N.

3. Test

    Build.
    A3.4: Walk over each coin’s field several times. Only the first visit counts.
    A3.5: Collect a coin, enter a house and come back out. The coin is still gone, and the next coin shows the correct total.

If a collected coin reappears after the scene change, Init Coin has the same parameter problem. Tell me, and I’ll move that check into On Init with direct variables as well.

# 5th iteration

I followed your instructions. The build succeeded. Test result:

Does not work:
- Acceptance criteria A3.4: Observed: repeatedly walking into the coin pickup triggers doesnt trigger an incrementation of the coin counter repeatedly. However when walking into a coin pickup trigger, the incrementation of the coin counter as well as the dialogue display happens twice instead of once
  Expected: walking over the coin pickup trigger repeatedly does nothing. Only one coin should be added when collecting a coin

# LLM Answer

If the counter goes up only on the first visit, the flag check works. If it then goes up twice, the coin actions are running twice within that one pickup. Since the flag is set before `Collect Coin` is called, a second firing of the same trigger can't cause this. The most likely cause is a duplicated event left over from moving the **Call Script** (moving in the editor works by copy + delete, and the delete can get missed).

## 1. Check `Collect Coin`

1. Select `Collect Coin` under **Scripts**.
2. The script must contain exactly these 3 events, each exactly once, with no **If** and nothing else:
    1. **Deactivate Actor** – **Actor A**
    2. **Variable Increment By 1** – `Coin Counter`
    3. **Display Dialogue** – `Coins: $NN$`
3. Delete any extra events.

## 2. Check every trigger's On Enter

1. Select each trigger `Coin Town N Pickup` and open **On Enter**.
2. The script must look exactly like this:
    - **If Variable Is 'True'** – `Coin Town N Collected`
        - **True:** empty
        - **Else:**
            1. **Variable Set To 'True'** – `Coin Town N Collected`
            2. **Call Script** – `Collect Coin`, **Coin** = `Coin Town N`
3. There must be exactly **one** **Call Script**, inside **Else**.
4. Nothing may come after the **If**, including no second **Call Script**.

## 3. Check for overlapping triggers

1. In the **Sample Town** sidebar, open the list of triggers.
2. Each coin must have exactly one trigger. Look for leftovers such as an extra pickup trigger or a duplicated trigger lying on the same position.
3. Delete any extras.

## 4. Test

1. **Build**.
2. On a new game, collect a coin. The dialogue appears once and shows "Coins: 1".
3. Walk over the field again. Nothing happens.

If everything matches and it still counts twice, send me screenshots of `Collect Coin` and of one trigger's **On Enter**.