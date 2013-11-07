#!/usr/bin/kivy
# Star Wars Dice Roller
# Basic Star Wars Dice Roller
#
# This script uses Kivy to build a GUI for setting up and rolling dice pools
# Provides functionality for setting pool from common pools
# Setting pools from the roll history
# Re-rolling the current pool
#
# By Sean Wallitsch, 2013/08/15

# ==============================================================================
# VERSION HISTORY
# ==============================================================================

# v1.0  Fully commented, fixed variable names, prepped for build

# ==============================================================================
# TO DO LIST
# ==============================================================================

# * Fix halfpool_to_markup() to not be incredibly dangerous
# * Rebuild so pool is a class, not global variables.

# ==============================================================================
# Imports
# ==============================================================================

from time import strftime # For timestamping history log
from sys import path # For getting textures in locally

# Kivy Imports

from kivy.app import App # Base App Class
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.gridlayout import GridLayout # Only Using Grid Layouts
from kivy.uix.label import Label # Label Class for Returns
from kivy.uix.button import Button # Button Class for everything else
from kivy.uix.accordion import Accordion, AccordionItem # For Right Side
from kivy.uix.listview import ListItemButton, ListItemLabel, \
        CompositeListItem, ListView # For Right Side History
from kivy.graphics import Canvas, Color, Rectangle # For backgrounds
from kivy.core.image import Image # For textures
from kivy.clock import Clock # For scheduling a deselect of the history list

# Custom Modules

from modules.sw_dice import add_dice # Star Wars Dice Rolls
from modules.color import rgb_to_linear, rgb_to_hex # Converts from 0-255


# ==============================================================================
# Variables
# ==============================================================================

# Colors

# 0-255 colors from Photoshop
COL_ABILITY = [70, 165, 52]
COL_PROFICIENCY = [255, 250, 20]
COL_BOOST = [169, 235, 255]
COL_DIFFICULTY = [135, 62, 173]
COL_CHALLENGE = [230, 56, 56]
COL_SETBACK = [80, 80, 80]

# Creates HTML ready hexes for markup
HEX_ABILITY = rgb_to_hex(COL_ABILITY)
HEX_PROFICIENCY = rgb_to_hex(COL_PROFICIENCY)
HEX_BOOST = rgb_to_hex(COL_BOOST)
HEX_DIFFICULTY = rgb_to_hex(COL_DIFFICULTY)
HEX_CHALLENGE = rgb_to_hex(COL_CHALLENGE)
HEX_SETBACK = rgb_to_hex(COL_SETBACK)

HEX_COLORS = [
    HEX_ABILITY,
    HEX_PROFICIENCY,
    HEX_BOOST,
    HEX_DIFFICULTY,
    HEX_CHALLENGE,
    HEX_SETBACK
    ]

# Creates 0-1 linear colors for Kivy. Conversion seemed dark, added mult
LIN_ABILITY = rgb_to_linear(COL_ABILITY, 2)
LIN_PROFICIENCY = rgb_to_linear(COL_PROFICIENCY, 2.45)
LIN_BOOST = rgb_to_linear(COL_BOOST, 2)
LIN_DIFFICULTY = rgb_to_linear(COL_DIFFICULTY, 2)
LIN_CHALLENGE = rgb_to_linear(COL_CHALLENGE, 2)
LIN_SETBACK = rgb_to_linear(COL_SETBACK, 2)

LIN_COLORS = [
    LIN_ABILITY,
    LIN_PROFICIENCY,
    LIN_BOOST,
    LIN_DIFFICULTY,
    LIN_CHALLENGE,
    LIN_SETBACK
    ]

# Dice Results
# [Number Rolled, S or F, A or T, Tri or D]

# GLOBAL vars edited by funcs
ability_rolls = [0,0,0]
proficiency_rolls = [0,0,0,0]
boost_rolls = [0,0,0]
difficulty_rolls = [0,0,0]
challenge_rolls = [0,0,0,0]
setback_rolls = [0,0,0]

# GLOBAL vars edited by funcs
all_rolls = [
    ability_rolls,
    proficiency_rolls,
    boost_rolls,
    difficulty_rolls,
    challenge_rolls,
    setback_rolls
    ]

DICE_TYPES = [
    "ability",
    "proficiency",
    "boost",
    "difficulty",
    "challenge",
    "setback"
    ]

RESULT_TYPES = [
    "success",
    "failure",
    "advantage",
    "threat",
    "triumph",
    "despair"
    ]

# Controls the Common Pools button grid
COMMON_POOLS = [
    "dddd",
    "ddddd",
    "dddddd",
    "cd",
    "cdd",
    "cddd",
    "cdddd",
    "cddddd",
    "ccd",
    "ccdd",
    "ccddd",
    "ccdddd",
    "cccd",
    "cccdd",
    "cccc",
    "ccccd",
    "ccccc",
    ]

# Pool Results
# GLOBAL vars edited by funcs

pool_success = 0
pool_advantage = 0
pool_triumph = 0
pool_despair = 0

roll_history = []

roll_history_strings = []

# Textures

# Larger textures for result backgrounds
TEX_SUCCESS = path[0] + "/tex/" + "success.png"
TEX_FAILURE = path[0] + "/tex/" + "failure.png"
TEX_ADVANTAGE = path[0] + "/tex/" + "advantage.png"
TEX_THREAT = path[0] + "/tex/" + "threat.png"
TEX_TRIUMPH = path[0] + "/tex/" + "triumph.png"
TEX_DESPAIR = path[0] + "/tex/" + "despair.png"

TEXTURE_LIST = [
    TEX_SUCCESS,
    TEX_FAILURE,
    TEX_ADVANTAGE,
    TEX_THREAT,
    TEX_TRIUMPH,
    TEX_DESPAIR
    ]


# ==============================================================================
# Functions
# ==============================================================================

# History Functions

def convert_history(raw_list):
    """Converts a numbers based history to a string based history
    
    Args:
        raw_list: The list to have it's item's item's be replaced by strings.
            list[i][1] should be a dicepool (0,0,0,0,0,0)
            list[i][2] should be a results list (0,0,0,0)
    
    Raises:
        N/A
    
    Returns:
        A new list, with every entry having [i][1] and [i][2] replaced.
    
    """
    new_list = []
    for roll in raw_list:
        new_roll = []
        new_roll.append(roll[0])
        new_roll.append(dicepool_to_string(roll[1]))
        new_roll.append(results_to_string(roll[2]))
        new_list.append(new_roll)
    return new_list

def dicepool_to_string(pool = (0,0,0,0,0,0),\
    font_loc = "fonts/sw_symbols.ttf", color_list = HEX_COLORS):
    """Takes a single tuple and returns a string
    
    Args:
        pool: The length six list to be converted into a string with markup
        
        font_loc: The font used for markup.
        
        color_list: The color list used for markup.
    
    Raises:
        N/A
    
    Returns:
        A new string to be used in place of the inputted pool
    
    """
    font = "[font=" + font_loc + "]"
    cf = "[/font]"
    col = color_markup(color_list)
    cc = "[/color]"
    new_string = ""
    # If either pool side has more than 6 dice, we count by numbers
    if pool[0] + pool[1] + pool[2] > 6 or pool[3] + pool[4] + pool[5] > 6:
        if pool[1]: # Proficiency
            new_string += col[1] + str(pool[1]) + font + "c" + cf + cc
        else:
            # We add an empty color open and color close because when we
            # go from a string back to a dicepool, color close will
            # be used as a comma in a .split()
            new_string += col[1] + cc
        if pool[0]: # Ability
            new_string += col[0] + str(pool[0]) + font + "d" + cf + cc
        else:
            new_string += col[1] + cc
        if pool[2]: # Boost
            new_string += col[2] + str(pool[2]) + font + "b" + cf + cc
        else:
            new_string += col[1] + cc
        new_string += " | "
        if pool[4]: # Challenge
            new_string += col[4] + str(pool[4]) + font + "c" + cf + cc
        else:
            new_string += col[1] + cc
        if pool[3]: # Difficulty
            new_string += col[3] + str(pool[3]) + font + "c" + cf + cc
        else:
            new_string += col[1] + cc
        if pool[5]: # Setback
            new_string += col[5] + str(pool[5]) + font + "b" + cf + cc
        else:
            new_string += col[1] + cc
    # Numbers by visual:
    else:
        new_string += font
        new_string += col[1] + ("c" * pool[1]) + cc # Proficiency
        new_string += col[0] + ("d" * pool[0]) + cc # Ability
        new_string += col[2] + ("b" * pool[2]) + cc # Boost
        new_string += cf + " | " + font
        new_string += col[4] + ("c" * pool[4]) + cc # Challenge
        new_string += col[3] + ("d" * pool[3]) + cc # Difficulty
        new_string += col[5] + ("b" * pool[5]) + cc # Setback
        new_string += cf
    return new_string

def halfpool_markup(pool = "cd", bad = "n",\
    font_loc = "fonts/sw_symbols.ttf", color_list = HEX_COLORS):
    """Takes a single tuple and returns a string
    
    WARNING: THIS FUNCTION IS DANGEROUS AND ONLY WORKS FOR FONTS WITHOUT
        'c' OR 'd'. DEFAULT FONT WORKS FINE. FIX WHEN ABLE.
    
    Args:
        pool: A pool as represented by a string, for example 'ccddd'
        
        font_loc: The font used in markup (for replacement).
        
        color_list: The colors used in markup (for replacement).
    
    Raises:
        N/A
    
    Returns:
        N/A
    
    """
    font = "[font=" + font_loc + "]"
    cf = "[/font]"
    col = color_markup(color_list)
    cc = "[/color]"
    pool_string = pool
    # c = proficiency/challenge
    # b = boost/setback - BROKEN
    # d = ability/difficulty
    #
    # b doesn't work because it finds b in the font name. This func is super
    # dangerous and needs to be fixed ASAP.
    if bad == "n":
        pool_string = pool_string.replace("c", col[1] + font + "c" + cf + cc)
        pool_string = pool_string.replace("d", col[0] + font + "d" + cf + cc)
#         pool_string = pool_string.replace("b", col[2] + font + "b" + cf + cc)
    else:
        pool_string = pool_string.replace("c", col[4] + font + "c" + cf + cc)
        pool_string = pool_string.replace("d", col[3] + font + "d" + cf + cc)
#         pool_string = pool_string.replace("b", col[5] + font + "b" + cf + cc)
    return pool_string

def results_to_string(results = (0,0,0,0),\
    font_loc = "fonts/sw_symbols.ttf", color_list = HEX_COLORS):
    """Takes a single tuple and returns a string
    
    Args:
        results: A length 4 list representing the 4 possible results from SW 
            dice rolls- success/failure, advantage/threat, triumph, despair
        
        font_loc: The font to be added in via markup
        
        color_list: The list of colors to be added in via markup
    
    Raises:
        N/A
    
    Returns:
        A new string to be used instead of the inputted 'results' list.
        
    """
    font = "[font=" + font_loc + "]"
    cf = "[/font]"
    col = color_markup(color_list)
    cc = "[/color]"
    new_string = ""
    new_string += font + "[b]"
    if results[0] > 0: # Success vs Failure
        new_string += col[0] + cf + str(results[0]) + font + "s" + cc
    elif results[0] < 0:
        new_string += col[3] + cf + str(results[0]*-1) + font + "f" + cc
    if results[1] > 0: # Threat vs Advantage
        new_string += col[2] + cf + "  " + str(results[1]) + font + "a" + cc
    elif results[1] < 0:
        new_string += col[5] + cf + "  " + str(results[1]*-1) + font + "t" + cc
    if results[2]: # Triumph
        new_string += col[1] + cf + "  " + str(results[2]) + font + "x" + cc
    if results[3]: # Despair
        new_string += col[4] + cf + "  " + str(results[3]) + font + "y" + cc
    new_string += "[/b]" + cf
    return new_string

def color_markup(color_list):
    """A quick way of adding markup to a list of colors
    
    Args:
        color_list: A list of hex color values that will be placed inside of 
            markup
    
    Raises:
        N/A
    
    Returns:
        Returns a list with the given values in 'color_list' now marked up
    
    """
    new_color_list = []
    for i in color_list:
        new_string = "[color=#" + i + "]"
        new_color_list.append(new_string)
    return new_color_list

def string_to_pool(string="", font_loc = "fonts/sw_symbols.ttf",\
    color_list = HEX_COLORS):
    """Takes a pool in string form and makes a dice pool out of it

    Args:
        string: This is a string representing a six int list- which is
            the amount of dice. This list probably includes a lot of markup.
        
        font_loc: The location of the font that the string uses (used for
            replacement)
        
        color_list: The list of colors to be replaced inside of Kivy color
            markup.
    
    Raises:
        N/A
    
    Returns:
        Returns a new 6 int list in the form of (0,0,0,0,0,0)
    
    """
    string = string.replace("[font=" + font_loc + "]", "")
    for i in color_list:
        string = string.replace("[color=#" + str(i) + "]", "")
    string = string.replace("[/color]", ",")
    string = string.replace("[/font]","")
    string = string.replace(" | ", "")
    new_list = string.split(",")
    new_list = new_list[:6]
    largeList = False
    # We need to check large list vs short list.
    # Large history strings have a number followed by the designator
    # 1c, 2d, 1b
    # Small history strings write out a sequence of designators for each dice
    # c, dd, b
    # If the first character in a list item can be converted to an int,
    # it's a large list.
    for i in range(6):
        try:
            int(new_list[i][0])
            largeList = True
        except:
            print "",
    # If the above triggered the largeList Boolean, we'll convert the
    # largeList to a short style list. 
    if largeList:
        length_list = []
        for i in range(6):
            length_list.append(len(new_list[i]))
        for i in range(6):
            if length_list[i] > 0:
                dice_type = new_list[i][length_list[i]-1:]
                dice_num = new_list[i][:length_list[i]-1]
                new_list[i] = dice_type * int(dice_num)
    for i in range(6):
        new_list[i] = len(new_list[i])
    new_list = [
        new_list[1],
        new_list[0],
        new_list[2],
        new_list[4],
        new_list[3],
        new_list[5]
        ]
    return new_list

def string_to_halfpool(string="", bad="n",font_loc = "fonts/sw_symbols.ttf",\
    color_list = HEX_COLORS):
    """Takes a pool in string form and makes a half dice pool out of it
    
    Args:
        string: This is a string representing a three int list- which is
            the amount of dice. This list probably includes a lot of markup.
        
        bad: Indicates if the halfpool represents a light or dark pool
        
        font_loc: The location of the font that the string uses (used for
            replacement)
        
        color_list: The list of colors to be replaced inside of Kivy color
            markup.
    
    Raises:
        N/A
    
    Returns:
        Returns a new 6 int list in the form of (0,0,0,0,0,0)
    
    """
    string = string.replace("[font=" + font_loc + "]", "")
    for i in color_list: # Replace all the color markups at once
        string = string.replace("[color=#" + str(i) + "]", "")
    string = string.replace("[/color]", "")
    string = string.replace("[/font]","")
    new_list = [0, 0, 0, 0, 0, 0]
    # We're getting a three int list- [0,0,0] 'bad' tells us if we place
    # those three tuples on the left or right side
    if bad == "y":
        c, d, b = 4, 3, 5
    else:
        c, d, b = 1, 0, 2
    new_list[c] = string.count("c") # Proficiency/Challenge
    new_list[d] = string.count("d") # Ability/Difficulty
    new_list[b] = string.count("b") # Boost/Setback
    return new_list

def set_pool(pool=(0,0,0,0,0,0), reset="n"):
    """Sets the dice pool to a specific amount and rolls
    
    Args:
        pool: This is the amount of each type of dice to be added to the pool
        
        reset: If 'y', reset_all is run. In this case, the dice given in pool
            will be the ONLY dice in the pool at the end of the func.
    
    Raises:
        N/A
    
    Returns:
        Runs update_dice_results, which updates all GUIs."""
    if reset == "y": # When getting a full pool from history, we want to reset
        reset_all()
    for i in range(6):
        dice_num = pool[i]
        dice_type = DICE_TYPES[i]
        result_list = []
        for result in add_dice(dice_num, dice_type):
            result_list.append(result)
        if len(result_list) < 5: # Most dice only return 4 results
            result_list.append(0)
        # The result list now reads:
        # 0 - Type
        # 1 - Number of those dice rolled
        # 2 - Success or Fail
        # 3 - Advantage or Threat
        # 4 - Triumph or Despair
        # Update dice results takes each dice and, by type, updates
        # the type rolls, then calls for an update_all()
        # This way all the pool amounts and results get updated.
        update_dice_results(
            result_list[0],
            result_list[1],
            result_list[2],
            result_list[3],
            result_list[4]
            )
    

# GUI -> Program

def update_all():
    """Updates all relavant interfaces
    
    Args:
        N/A
    
    Raises:
        N/A
    
    Returns:
        Updates all GUIs
    
    """
    # First we tabulate the results
    update_pool_results()
    # Then we force an update to the button side, recreating the
    # Reset All, Roll Again, and Reset One buttons IF there are any dice
    # in the pool still.
    DiceApp.interface.interfaceLeft.resultBottom.update()

def save_roll():
    """Saves current roll to roll history
    
    Args:
        Pulls all needed args from global vars, but only affects the 
            roll_history global var.
    
    Raises:
        N/A
    
    Returns:
        Calls the update_list() func on the history_view list
    
    """
    global roll_history
    current_roll = []
    dice_amounts = []
    results = []
    save = False
    for roll in all_rolls: # Make sure we don't save an empty pool
        for dice in roll:
            if dice > 0:
                save = True
    if save:
        current_time = strftime("%H:%M")
        current_roll.append(current_time)
        for i in all_rolls:
            dice_amounts.append(i[0])
        current_roll.append(dice_amounts)
        results.append(pool_success)
        results.append(pool_advantage)
        results.append(pool_triumph)
        results.append(pool_despair)
        current_roll.append(results)
        # We're left with the following:
        # ("HH:MM", [0,0,0,0,0,0], [0,0,0,0])
        #   Time     Dice Amounts   Results
        roll_history.insert(0, current_roll) # Put it at the head of the list
        # Now we need to create a list that for item 1 and 2, has
        # strings instead of numbers
        # A dice pool might be: "ccddb vs. ddb"
        # A result might be: "5s  3a  1x" (x is triumph)
        run_history_convert()
        # Now we need to force the history list to update
        DiceApp.interface.interfaceRight.history_view.update_list("")

def run_history_convert():
    """Grabs a global and runs convert_history to that global var
    
    Args:
        N/A
    
    Raises:
        N/A
    
    Returns:
        Recalculates all the string values in the roll_history list, uses
            global to save to roll_history_strings.
    
    """
    global roll_history_strings
    roll_history_strings = convert_history(roll_history)

# Pool Functions

def update_dice_results(type = "", number = 0, success = 0,\
    advantage = 0, special = 0):
    """Updates the global variables with dice results
    
    Args:
        type: One of the dice types from DICE_TYPES, used to determine
            what roll list to affect
        
        number: Amount of dice that were rolled
        
        success: Amount of Success/Failure that was generated. Based on
            the type, this might be subtracted from the overall number
        
        advantage: Amount of Advantage/Threat that was generated. Based
            on the type, this might be subtracted from the overall number
        
        special: Either Triumph or Despair, based on the type given. Will
            never be subtracted, as they do not cancel each other out.
    
    Raises:
        If type is not recognized, will print 'Type not recognized during
            update_dice_results()' to shell.'
    
    Returns:
        Changes global values for rolls and updates GUI
    
    """
    if type == "boost":
        global boost_rolls
        boost_rolls[0] += number
        boost_rolls[1] += success
        boost_rolls[2] += advantage
    elif type == "setback":
        global setback_rolls
        setback_rolls[0] += number
        setback_rolls[1] -= success
        setback_rolls[2] -= advantage
    elif type == "ability":
        global ability_rolls
        ability_rolls[0] += number
        ability_rolls[1] += success
        ability_rolls[2] += advantage
    elif type == "difficulty":
        global difficulty_rolls
        difficulty_rolls[0] += number
        difficulty_rolls[1] -= success
        difficulty_rolls[2] -= advantage
    elif type == "proficiency":
        global proficiency_rolls
        proficiency_rolls[0] += number
        proficiency_rolls[1] += success
        proficiency_rolls[2] += advantage
        proficiency_rolls[3] += special
    elif type == "challenge":
        global challenge_rolls
        challenge_rolls[0] += number
        challenge_rolls[1] -= success
        challenge_rolls[2] -= advantage
        challenge_rolls[3] += special
    # The else happens if the tuple isn't being received
    # from add_dice() correctly.
    else:
        print "Type not recognized during update_dice_results()"
    update_all()
    
def update_pool_results():
    """Forces an update to the master success, advantage, special counts
    
    Args:
        N/A
    
    Raises:
        N/A
    
    Returns:
        Updates the global pool counts
    
    """
    global pool_success
    global pool_advantage
    global pool_triumph
    global pool_despair
    success = 0
    advantage = 0
    triumph = 0
    despair = 0
    for i in all_rolls:
        success += i[1]
        advantage += i[2]
        if i == all_rolls[1]:
            triumph += i[3]
        elif i == all_rolls[4]:
            despair += i[3]
    pool_success = success
    pool_advantage = advantage
    pool_triumph = triumph
    pool_despair = despair

def reset_all(ignore=""):
    """Zeros all rolls and all dice
    
    Args:
        ignore: reset_all is called from both objects and other functions,
            ignore will toss the object if given.
    
    Raises:
        N/A
    
    Returns:
        Edits global roll values to 0 and updates all GUIs
    
    """
    global ability_rolls
    global proficiency_rolls
    global boost_rolls
    global difficulty_rolls
    global challenge_rolls
    global setback_rolls
    global all_rolls
    save_roll()
    ability_rolls = [0,0,0]
    proficiency_rolls = [0,0,0,0]
    boost_rolls = [0,0,0]
    difficulty_rolls = [0,0,0]
    challenge_rolls = [0,0,0,0]
    setback_rolls = [0,0,0]
    all_rolls = [
        ability_rolls,
        proficiency_rolls,
        boost_rolls,
        difficulty_rolls,
        challenge_rolls,
        setback_rolls
        ]
    update_all()

def reset_one(instance):
    """Zeroes and resets a single dice class
    
    Args:
        instance: The object that called this reset. This reset does
            not function if not called by an object
    Raises:
        N/A
    
    Returns:
        Edits globals rolls to 0 and updates GUI
    
    """
    global ability_rolls
    global proficiency_rolls
    global boost_rolls
    global difficulty_rolls
    global challenge_rolls
    global setback_rolls
    global all_rolls
    type = int(instance.padding_x * 1000)
    if type == 0:
        ability_rolls = [0,0,0]
    elif type == 1:
        proficiency_rolls = [0,0,0,0]
    elif type == 2:
        boost_rolls = [0,0,0]
    elif type == 3:
        difficulty_rolls = [0,0,0]
    elif type == 4:
        challenge_rolls = [0,0,0,0]
    elif type ==5:
        setback_rolls = [0,0,0]
    all_rolls = [
        ability_rolls,
        proficiency_rolls,
        boost_rolls,
        difficulty_rolls,
        challenge_rolls,
        setback_rolls
        ]
    update_all()

def roll_again(ignore=""):
    """Takes the current dice amounts and rolls the exact same roll
    
    Args:
        ignore: roll_again can be called from within objects, so we
            need a variable to ingest and ignore.
    
    Raises:
        N/A
    
    Returns:
        Rolls dice and adds them to the pools with update_dice_results()
    """
    roll_amounts = []
    for i in range(6):
        roll_amounts.append(all_rolls[i][0])
    reset_all() # Note that reset all will save the current roll to history
    for i in range(6):
        result_list = []
        for result in add_dice(roll_amounts[i], DICE_TYPES[i]):
            result_list.append(result)
        if len(result_list) < 5: # Most dice only return 4 results
            result_list.append(0)
        # The result list now reads:
        # 0 - Type
        # 1 - Number of those dice rolled
        # 2 - Success or Fail
        # 3 - Advantage or Threat
        # 4 - Triumph or Despair
        # Update dice results takes each dice and, by type, updates
        # the type rolls, then calls for an update_all()
        # This way all the pool amounts and results get updated.
        update_dice_results(
            result_list[0],
            result_list[1],
            result_list[2],
            result_list[3],
            result_list[4]
            )

# ==============================================================================
# Classes
# ==============================================================================

# Window Layouts

# Interface Left - Top Half (Dice buttons)

class DiceArray(GridLayout):
    """Array of buttons for each type, with different colors
    
    Args:
        type: A string that should match an item in DICE_TYPES
        
        color: A color tuple to be used for the background of the buttons
    
    Raises:
        N/A
    
    Returns:
        N/A
    
    """
    def __init__(self, type, color, **kwargs):
        super(DiceArray, self).__init__(**kwargs)
        self.type = type
        self.color = color
        self.rows = 2
        self.make_array_buttons()
    
    def pass_dice(self, instance):
        """Receives on_press from buttons, translates to int"""
        try:
            self.dice_num =\
                int(instance.text.replace("[b]", "").replace("[/b]", ""))
        except:
            self.dice_num = 1
        result_list = []
        for result in add_dice(self.dice_num, self.type):
            result_list.append(result)
        if len(result_list) < 5:
            result_list.append(0)
        update_dice_results(
            result_list[0],
            result_list[1],
            result_list[2],
            result_list[3],
            result_list[4]
            )
    
    
    def make_array_buttons(self):
        """Populates the bottom buttons of the ArrayDice class"""
        self.mainButton = Button(
            text = "[b]" + self.type.title() + "[/b]",
            background_color = self.color,
            markup = True,
            size_hint_y = .5,
            value = 1
            )
        self.mainButton.bind(on_press = self.pass_dice)
        self.lowerButtons = GridLayout(
            cols = 5,
            size_hint_y = .5
            )
        self.add_widget(self.mainButton)
        self.add_widget(self.lowerButtons)
        for i in range(2,4): # Used to create 2,3,4,5 buttons. Now only 2,3
            self.lowerButtons.add_widget(Button(
                text = "[b]" + str(i) + "[/b]",
                size_hint_x = .5,
                size_hint_y = .5,
                background_color = self.color,
                on_press = self.pass_dice,
                markup = True,
                ))

class AdditionalDiceGrid(GridLayout):
    """Side of the window devoted to adding dice
    
    Args:
        N/A
    
    Raises:
        N/A
    
    Returns:
        GUI
    
    """
    def __init__(self, **kwargs):
        super(AdditionalDiceGrid, self).__init__(**kwargs)
        self.cols = 3
        self.padding = 10
        self.spacing = 10
        for i in range(6):
            self.add_widget(DiceArray(DICE_TYPES[i], LIN_COLORS[i]))

# Interface Left - Bottom Half (Results & Reset)

# Reset and Reroll Group

class DicePoolReadoutAndReset(GridLayout):
    """Lists how many dice of each type are in the pool, reset individually
    
    Args:
        N/A
    
    Raises:
        N/A
    
    Returns:
        GUI
    
    """
    def __init__(self, **kwargs):
        super(DicePoolReadoutAndReset, self).__init__(**kwargs)
        self.cols = 3
        for i in range(6):
            self.add_widget(Label(
                size_hint_x = .15
                ))
    
    def update(self):
        self.clear_widgets()
        for i in range(6):
            if all_rolls[i][0] != 0:
                floati = float(i)
                self.add_widget(Button(
                    text = "[b]" + str(all_rolls[i][0]) + "[/b]",
                    size_hint_x = .15,
                    # Using padding_x as a type indicator is a shitty hack
                    # That I use because we can't resolve the type 
                    # from the text alone.
                    #
                    # I know now that I should create a list of custom funcs,
                    # One for each type, and assign that list_func[i] to
                    # each button The custom funcs would simply pass to a
                    # global func the type and amount.
                    padding_x = floati/1000,
                    markup = True,
                    background_color = LIN_COLORS[i],
                    on_press = reset_one
                    ))
            else:
                self.add_widget(Label(
                    size_hint_x = .15
                    ))

# Result Display

class ResultLabel(GridLayout):
    """A single label to display a single result (success/failure, etc)
    
    Args:
        label: The type of result. Will lower() and remove any trailing
            ': '
        
        number: The amount of each result
    
    Raises:
        N/A
    
    Returns
        GUI
    """
    def __init__(self, label, number, **kwargs):
        super(ResultLabel, self).__init__(**kwargs)
        self.cols = 1
        # We need to get the type down to a string that matches the RESULT_TYPES
        self.type = label.replace(": ", "").lower()
        self.number = number
        
        if self.type != "":
            self.type = RESULT_TYPES.index(self.type)
            self.texture = Image(TEXTURE_LIST[self.type]).texture
            if str(number) != "":
                self.text =\
                    "[b]" + str(number) + "[/b]"
            else:
                self.text = ""
        else: # I shouldn't need this. But it's here.
            self.type = ""
        
        if self.type == "": # If we have no type, we're empty
            self.resultDisplay = Label(
                text = "",
                size_hint_x = .5,
                size_hint_y = .5
                )
        else:
            self.resultDisplay = Label(
                text = self.text,
                size_hint_x = .5,
                size_hint_y = .5,
                font_size = 36,
                markup = True
                )
        
        if self.type in (0,2,4): # Good types
            self.Color = (.6,.9,.7)
        elif self.type in (1,3,5): # Bad types
            self.Color = (.9,.6,.7)
        else:
            self.Color = (.75,.75,.75)
        
        if self.type != "": # If we're not empty do texture binds
            self.resultDisplay.bind(
                size = self._update_tex,
                pos = self._update_tex
                )
            with self.resultDisplay.canvas.before:
                Color(self.Color[0],self.Color[1],self.Color[2])
                self.tex = Rectangle(
                    texture = self.texture,
                    size = (
                        self.resultDisplay.size[1],
                        self.resultDisplay.size[1]
                        ),
                    pos = self.resultDisplay.pos
                    )
                    
        self.add_widget(self.resultDisplay)
    
    def _update_tex(self, instance, value):
        """Updates texture on resize"""
        self.tex.pos = (\
            instance.pos[0] + (instance.size[0] - instance.size[1])/2,             
            instance.pos[1]
            )
        self.tex.size = (instance.size[1], instance.size[1]) 

class ResultGrid(GridLayout):
    """A 2x2 grid containing ResultLabel labels showing results
    
    Args:
        N/A
    
    Raises:
        N/A
    
    Returns:
        GUI
    
    """
    def __init__(self, **kwargs):
        super(ResultGrid, self).__init__(**kwargs)
        self.rows = 2
        self.cols = 2
        self.spacing = 10
        self.size_hint_x = .66
        # When first created, all labels should be empty.
        self.add_widget(Label(
            size_hint_y = .5,
            size_hint_x = .5
            ))
        self.add_widget(Label(
            size_hint_y = .5,
            size_hint_x = .5
            ))
        self.add_widget(Label(
            size_hint_y = .5,
            size_hint_x = .5
            ))
        self.add_widget(Label(
            size_hint_y = .5,
            size_hint_x = .5
            ))
    
    def update(self):
        """Updates the result Labels
        
        Args:
            self: The object to be affected
        
        Raises:
            N/A
        
        Returns:
            Removes and Recreates all Dice Labels under the ResultGrid object
        
        """
        self.clear_widgets() # Removes ALL ResultLabel objects
        dice = False
        for i in all_rolls: # Checks if there have been any results...
            if i[0] != 0:
                dice = True
        if dice:
            if pool_success > 0:
                # We don't actually display the 'Success: ' text anymore, but
                # we still use the string itself for defining the type,
                # if the result is good or bad, and the texture to load.
                #
                # We could probably remove the trailing ': ', but this is taken 
                # care of at ResultLabel creation anyway.
                success_label = "Success: "
                success_num = pool_success
            elif pool_success == 0:
                success_label = "Failure" # If no success, roll fails.
                success_num = ""
            else:
                success_label = "Failure: "
                success_num = -1 * pool_success
            if pool_advantage > 0:
                advantage_label = "Advantage: "
                advantage_num = pool_advantage
            elif pool_advantage < 0:
                advantage_label = "Threat: "
                advantage_num = -1 * pool_advantage
            else:
                advantage_label = ""
                advantage_num = ""
            # Triumph and Despair can only be zero or positive.
            if pool_triumph > 0:
                triumph_label = "Triumph: "
                triumph_num = pool_triumph
            else:
                triumph_label = ""
                triumph_num = ""
            if pool_despair > 0:
                despair_label = "Despair: "
                despair_num = pool_despair
            else:
                despair_label = ""
                despair_num = ""
            self.add_widget(ResultLabel(success_label, success_num))
            self.add_widget(ResultLabel(advantage_label, advantage_num))
            self.add_widget(ResultLabel(triumph_label, triumph_num))
            self.add_widget(ResultLabel(despair_label, despair_num))
         # Just in case, we reset the var.
        dice = False

class ResultBottom(GridLayout):
    """Side of the window devoted to displaying/resetting results
    
    Args:
        N/A
    
    Raises:
        N/A
    
    Returns:
        GUI
    
    """
    def __init__(self, **kwargs):
        super(ResultBottom, self).__init__(**kwargs)
        self.cols = 3
        self.padding = 10
        self.spacing = 10
        # resetGroup is the leftmost group, with the resetAll button, the
        # dice pool count and the reroll button.
        self.resetGroup = GridLayout(
            rows = 3,
            size_hint_x = .34,
            spacing =10
            )
        # rollAgain uses roll_again() to reset results and roll the same pool 
        # over again.
        self.rollAgain = Button(
            text = "[b]Roll Again[/b]",
            size_hint_y = .25,
            on_press = roll_again,
            markup = True
            )
        # dicePool represents the individual types of dice, and can clear
        # each. If no dice of a type are currently rolled, that dice
        # will be invisible. Otherwise it will read the current amount.
        self.dicePool = DicePoolReadoutAndReset(
            size_hint_y = .5
            )
        # resetAllButton uses reset_all() to clear all individual dice results 
        # and amount of dice
        self.resetAllButton = Button(
            text = "[b]Reset All[/b]",
            size_hint_y = .25,
            on_press = reset_all,
            markup = True
            )
        # Some blank labels for shorthand reference
        self.blankLabel1 = Label(
            size_hint_y = .25
            )
        self.blankLabel2 = Label(
            size_hint_y = .25
            )
        self.resetGroup.add_widget(self.dicePool)
        self.resetGroup.add_widget(self.blankLabel1)
        # self.result_label_grid is where the results are displayed
        self.result_label_grid = ResultGrid()
        self.add_widget(self.resetGroup)
        self.add_widget(self.result_label_grid)
        
    def update(self):
        """Updates the entire result side
        
        Args:
            self: the object to be affected.
        
        Raises:
            N/A
        
        Returns:
            Calls a gui update of the result_label_grid
        
        """
        dice = False
        self.dicePool.update()
        for i in all_rolls: # Check if any dice exist
            if i[0] != 0:
                dice = True
        self.resetGroup.clear_widgets()
        if dice: # If dice exist, built the widgets
            self.resetGroup.add_widget(self.rollAgain)
            self.resetGroup.add_widget(self.dicePool)
            self.resetGroup.add_widget(self.resetAllButton)
        else: # If no dice rolled, build blanks.
            self.resetGroup.add_widget(self.blankLabel1)
            self.resetGroup.add_widget(self.dicePool)
            self.resetGroup.add_widget(self.blankLabel2)
        dice = False # Reset dice var just in case
        # Call a GUI update on the contained result_label_grid
        self.result_label_grid.update()

# Top Layer Window

class InterfaceLeft(GridLayout):
    """Left side of the interface, with dice and results
    
    Args:
        N/A
    
    Raises:
        N/A
    
    Returns:
        GUI elements
    
    """
    def __init__(self, **kwargs):
        super(InterfaceLeft, self).__init__(**kwargs)
        self.rows = 2
        self.size_hint_x = .65
        self.add_widget(AdditionalDiceGrid(
            size_hint_y = .5
            ))
        self.resultBottom = ResultBottom(
            size_hint_y = .5
            )
        self.add_widget(self.resultBottom)

class HistoryView(GridLayout):
    """The list widget for viewing of the roll history, also let's you reroll
    
    Args:
        N/A
    
    Raises:
        N/A
    
    Returns:
        GUI
    
    """
    def __init__(self, **kwargs):
        super(HistoryView, self).__init__(**kwargs)
        self.rows = 2
        # Top row is going to be our header
        self.header = GridLayout(
            cols = 3,
            size_hint_y = 3
            )
        # Header elements have the same size_hint_x as the list elements
        self.header_time = Label(
            text = "Time",
            size_hint_x = 10
            )
        self.header_pool = Label(
            text = "Pool",
            size_hint_x = 55
            )
        self.header_results = Label(
            text = "Results",
            size_hint_x = 35
            )
        self.header.add_widget(self.header_time)
        self.header.add_widget(self.header_pool)
        self.header.add_widget(self.header_results)
        self.add_widget(self.header)
        # End Header Section
        
        # This is an args based on the 'list_composite' kivy example
        # I really don't understand it terribly well, but it's working correctly
        #
        # list = the 'data' list given to the list_adapter below
        
        self.args_converter = lambda row_index, list: {
            'text': list,
            'size_hint_y': None,
            'height': 25, # this is the height of the rows
            'cls_dicts': [ # Each cls entry is an item in the row
                {'cls': ListItemLabel,
                    'kwargs': { # the keywords used during item creation
                        'text': list[0],
                        'size_hint_x': 10
                        }
                    },
                {'cls': ListItemButton,
                    'kwargs': {
                        'text': list[1],
                        'size_hint_x': 55,
                        'deselected_color': [.3,.3,.3,1],
                        'selected_color': [.6,.6,.6,1],
                        'on_press': self.pass_dice,
                        # ListItemButton will always stay selected, and doesn't
                        # provide an API for deselecting.
                        # Therefore, we rebuild the entire list after
                        # the user touches one button.
                        #
                        # Sloppy, but seems to be the only way.
                        'on_release': self.sch_clear_selection,
                        'markup': True
                        }
                    },
                {'cls': ListItemLabel,
                    'kwargs': {
                        'text': list[2],
                        'markup': True,
                        'size_hint_x': 35
                        }
                    }
            ]}

        self.list_adapter = ListAdapter(
            allow_empty_selection = True,
            selection_mode = 'single',
            data = roll_history_strings,
            args_converter = self.args_converter,
            cls=CompositeListItem
            )

        self.list_view = ListView(
            adapter=self.list_adapter,
            size_hint_y = 97
            )

        self.add_widget(self.list_view)
    
    def sch_clear_selection(self, ignore):
        """Schedules a rebuild of the list to clear selection.
        
        Args:
            self: The current object to affect
            
            ignore: Called from a nested object, we don't need to reference
                back to this.
        
        Raises:
            N/A
        
        Returns:
            Rebuilds the list GUI in .1 seconds
        
        """
        Clock.schedule_once(self.update_list, .1)
    
    def update_list(self, ignore):
        """Totally rebuilds the entire list_view GUI
        
        Args:
            self: The object to be affected
            
            ignore: The object that calls this, which is actually the same
        
        Raises:
            N/A
        
        Returns:
            N/A
        
        """
        # We remove and add ONLY the list_view, not touching the header.
        self.remove_widget(self.list_view)
        self.list_adapter = ListAdapter(
            allow_empty_selection = True,
            selection_mode = 'single',
            data = roll_history_strings,
            args_converter = self.args_converter,
            cls=CompositeListItem
            )
        self.list_view = ListView(
            adapter=self.list_adapter,
            size_hint_y = 97
            )
        self.add_widget(self.list_view)
    
    def pass_dice(self, object):
        """Passes the button press to the set_pool() function with reset enabled
        
        Args:
            self: The object containing this (not used)
            
            object: The object calling this (we use this to grab the text)
            
        Raises:
            N/A
        
        Returns:
            N/A
        
        """
        new_pool = string_to_pool(object.text)
        set_pool(new_pool, reset="y")

class CommonPools(GridLayout):
    """A grid layout of buttons representing the common dice rolls as seen
    in COMMON_POOLS
    
    Args:
        N/A
    
    Raises:
        N/A
    
    Returns:
        GUI
    
    """
    def __init__(self, **kwargs):
        super(CommonPools, self).__init__(**kwargs)
        self.cols = 2
        
        # Create the good and bad pools
        self.good_pools = [] 
        for i in range(len(COMMON_POOLS)):
            self.good_pools.append(halfpool_markup(COMMON_POOLS[i]))
        self.bad_pools = []
        for i in range(len(COMMON_POOLS)):
            self.bad_pools.append(halfpool_markup(COMMON_POOLS[i],"y"))
            
        
        self.rightCol = GridLayout(
            cols = 1,
            size_hint_x = 50
            )
        self.leftCol = GridLayout(
            cols = 1,
            size_hint_x = 50
            )
        
        # Creates a button for each item in COMMON_POOLS
        # Links the right col to pass_bad() and the left col to pass_good()
        
        for i in range(len(COMMON_POOLS)):
            self.rightCol.add_widget(Button(
                text = self.bad_pools[i],
                background_color = (.4,.4,.5,1),
                on_press = self.pass_bad,
                markup = True
                ))
            self.leftCol.add_widget(Button(
                text = self.good_pools[i],
                background_color = (.5,.5,.5,1),
                on_press = self.pass_good,
                markup = True
                ))
        
        self.add_widget(self.leftCol)
        self.add_widget(self.rightCol)
    
    def pass_good(self, object):
        """Takes a press_on signal from a button and passes it on to
        string_to_halfpool without bad set.
        
        Args:
            self: parent object, not used.
            
            object: the object that called this function, we need it's text.
        
        Raises:
            N/A
        
        Returns:
            Sets the dice pool with set_pool()
        
        """
        pool = string_to_halfpool(object.text)
        set_pool(pool)
    
    def pass_bad(self, object):
        """Takes a press_on signal from a button and passes it on to
        string_to_halfpool with bad set.
        
        Args:
            self: parent object, not used.
            
            object: the object that called this function, we need it's text.
        
        Raises:
            N/A
        
        Returns:
            Sets the dice pool with set_pool()
        
        """
        pool = string_to_halfpool(object.text, bad="y")
        set_pool(pool)

class InterfaceRight(Accordion):
    """The right side of the interface, an accordion group
    
    Args:
        N/A
    
    Raises:
        N/A
    
    Returns:
        GUI
    
    """
    def __init__(self, **kwargs):
        super(InterfaceRight, self).__init__(**kwargs)
        self.size_hint_x = .35
        self.orientation = "vertical"
        
        # Accordion Items
        self.history = AccordionItem(
            title = "History"
            )
        self.commonPools = AccordionItem(
            title = "Common Dice Pools"
            )
        
        # Things inside of the Accordion Items
        self.commonPoolsButtons = CommonPools()
        self.history_view = HistoryView()
        
        # Add interior items to Accordion Items
        self.commonPools.add_widget(self.commonPoolsButtons)
        self.history.add_widget(self.history_view)
        
        # Add Accordion Items
        self.add_widget(self.history)
        self.add_widget(self.commonPools)

class InterfaceUI(GridLayout):
    """Main interface, additive dice to the left and results to the right.
    
    Args:
        N/A
    
    Raises:
        N/A
    
    Returns:
        GUI
    
    """
    def __init__(self, **kwargs):
        super(InterfaceUI, self).__init__(**kwargs)
        self.cols = 2
        
        self.interfaceLeft = InterfaceLeft()
        self.interfaceRight = InterfaceRight()
        
        self.add_widget(self.interfaceLeft)
        self.add_widget(self.interfaceRight)

# ==============================================================================
# App
# ==============================================================================

class SWDApp(App):
    """Main App, sets icon, name, and window size
    
    Args:
        N/A
    
    Raises:
        N/A
    
    Returns:
        App
    
    """
    # These are high level variables
    icon = 'tex/diceIcon.png' # Set the App Icon
    title = 'Unoffocial SWD (by Shidarin)' # Set the Window Title
    
    def __init__(self, **kwargs):
        super(SWDApp, self).__init__(**kwargs)
        self.interface = InterfaceUI()
    
    def on_start(self):
        # This is an undocumented way to set the window size on startup
        # Found at github: https://github.com/kivy/kivy/pull/577
        # Seems the Kivy team gave in over Tito's strong objections.
        # Thank God.
        self._app_window.size = 1136, 640
    
    def build(self):
        self.interface.bind(
            size = self._update_rect,
            pos = self._update_rect
            )
        # Set Canvas BG Color
        with self.interface.canvas.before:
            Color(.07,.07,.1)
            self.rect = Rectangle(
                size = self.interface.size,
                pos = self.interface.pos
                )
        return self.interface
    
    # Updates Canvas BG size and Pos
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
DiceApp = SWDApp()

if __name__ == "__main__":
    DiceApp.run()