AT-DiceRoller
=============

Dice roller for a sci fi tabletop RPG

AT-DR is a crossplatform, no bullshit dice pool building and result tabulating app. Meant to be a GM aid, so the focus was on building dice pools and seeing results as quickly as possible, as well as reviewing past results.

FeatureSet
==========

Features:

    Easily and quickly build dice pools
    No "roll" button, all results are tabulated on the fly
    Full history- see every roll and re-roll any pool from your history
    Interface scales down and up (within limits)
    Critical Injury Roller
    Force Dice Roller

Doesn't have:

    Any method of saving your dice pools

Currently For:

    OSX 10.6+ (64 bit only)
    Windows (32 or 64 bit) (Tested on Win 7, other compatibilities unknown)

Roadmap:

    Allow users to save their own dice pools?

Version History:
================

v1.0:

    Release Version
    Finished code commenting

Credits and Thanks:

    Fantasy Flight Games for a great Star Wars RPG
    Dice Font is by Aazlain
    App is written in Python
    GUI is written with Kivy
    App compiled with PyInstaller

Dice Font: http://community.fantasyflightgames.com/index.php?/topic/76059-can-we-make-the-swrpgicons-font-available/

How to use:
===========

Dice Section:
-------------

Add dice to the pool using either the single, double or triple buttons in the upper left, or select from the Common Pools to the right.

Once dice are added to the pool, you can Re-Roll those dice with the "Roll Again" button or "Reset All" the dice to clear the pool.

You can also clear individual types of dice from the pool by clicking on the dice color and amount in the pool area in the lower left. Be warned that this clears ONLY the type of dice you select, and does NOT re-roll the other types. 

If you want a new roll that's exactly the same without one type of dice (say removing a setback die), "Roll Again" and deselect the dice type. This has the advantage of saving your roll and generating a fresh new roll.

In the History view, you can see all of your previous rolls- the time, pool makeup, and results. Clicking on a pool makeup will save your current roll, change your pool makeup to the historical makeup you clicked on, and roll that makeup.

The app can be resized through normal means, but buttons and fonts get a little squishy if it gets too small, the basic layout will be modified if this is released for anything smaller than tablets.

Critical Injuries:
------------------

Slide the slider to select how many critical injuries the target is already suffering from.

Slide the second slider for modifications based on talents, etc.

Roll for a critical injury result, follow the rulebook for curing critical injuries based on severity.

Remember even if the ACTIVE component of a critical injury is no longer active, it still counts as a critical injury until healed!

Force Dice:
-----------

Select how many players are playing.

Roll the dice, view results.
