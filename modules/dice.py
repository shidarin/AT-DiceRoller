#!/usr/bin/kivy
# Star Wars Dice Module
#
# By Sean Wallitsch, 2013/08/25

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

from submodules.sw_dice import add_dice # Star Wars Dice Rolls
from submodules.color import rgb_to_linear, rgb_to_hex, color_markup


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

# Markup Shortcuts

SWF = "[font=fonts/sw_symbols.ttf]"
SWFC = "[/font]"
COL = color_markup(HEX_COLORS)
CC = "[/color]"
B = "[b]"
BC = "[/b]"

# TYPES

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
    [4, 0, 0],
    [5, 0, 0],
    [6, 0, 0],
    [1, 1, 0],
    [2, 1, 0],
    [3, 1, 0],
    [4, 1, 0],
    [5, 1, 0],
    [1, 2, 0],
    [2, 2, 0],
    [3, 2, 0],
    [4, 2, 0],
    [1, 3, 0] ,
    [2, 3, 0],
    [0, 4, 0],
    [1, 4, 0],
    [0, 5, 0]
    ]

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

# ==============================================================================
# Classes
# ==============================================================================

# Special Buttons

class TypeButton(Button):
    def __init__(self, type=None, value=None, **kwargs):
        super(TypeButton, self).__init__(**kwargs)
        self.type = type
        self.value = value

# Function Classes

class RollHistory(object):
    def __init__(self, parent):
        
        # Parent Object
        self.parent = parent
        
        # Master History List
        self.history = []
    
    def add_roll(self, instance):
        """Saves roll_history"""
        current_roll = []
        current_time = strftime("%H:%M")
        current_roll.append(current_time)
        
        dice_amounts = []
        for i in self.parent.all_rolls:
            dice_amounts.append(i[0])
        current_roll.append(dice_amounts)
        
        results = []
        results.append(instance.pool_success)
        results.append(instance.pool_advantage)
        results.append(instance.pool_triumph)
        results.append(instance.pool_despair)
        current_roll.append(results)
        # We're left with the following:
        # ("HH:MM", [0,0,0,0,0,0], [0,0,0,0])
        #   Time     Dice Amounts   Results
        
        # Now we need to insert a string for Dice Amounts and Results
        current_roll = self._make_strings(current_roll)
        
        # Now our item looks like:
        # ("HH:MM", [0,0,0,0,0,0], "poolstring", [0,0,0,0], "resultstring")
        
        # Insert at top of rollHistory list.
        self.history.insert(0, current_roll)
        
        # Now we need to force the history list to update
        self.parent.parent.parent.uiRight.history.update_list()
    
    def _make_strings(self, history_item):
        """Takes a single history item and adds string conversions"""
        
        pool = history_item[1]
        results = history_item[2]
        
        pool_str = ""
        
        # If either pool side has more than 6 dice, we count by numbers
        if pool[0] + pool[1] + pool[2] > 6 or pool[3] + pool[4] + pool[5] > 6:
        
            # Good Side
            if pool[1]: # Proficiency
                pool_str += COL[1] + str(pool[1]) + SWF + "c" + SWFC + CC
            if pool[0]: # Ability
                pool_str += COL[0] + str(pool[0]) + SWF + "d" + SWFC + CC
            if pool[2]: # Boost
                pool_str += COL[2] + str(pool[2]) + SWF + "b" + SWFC + CC
                
            pool_str += " | "
            
            # Bad Side
            if pool[4]: # Challenge
                pool_str += COL[4] + str(pool[4]) + SWF + "c" + SWFC + CC
            if pool[3]: # Difficulty
                pool_str += COL[3] + str(pool[3]) + SWF + "c" + SWFC + CC
            if pool[5]: # Setback
                pool_str += COL[5] + str(pool[5]) + SWF + "b" + SWFC + CC
        
        # Numbers by visual:
        else:
            pool_str += SWF
            pool_str += COL[1] + ("c" * pool[1]) + CC # Proficiency
            pool_str += COL[0] + ("d" * pool[0]) + CC # Ability
            pool_str += COL[2] + ("b" * pool[2]) + CC # Boost
            pool_str += SWFC + " | " + SWF
            pool_str += COL[4] + ("c" * pool[4]) + CC # Challenge
            pool_str += COL[3] + ("d" * pool[3]) + CC # Difficulty
            pool_str += COL[5] + ("b" * pool[5]) + CC # Setback
            pool_str += SWFC

        result_str = ""
        result_str += B
        
        # Success vs Failure
        if results[0] > 0:
            result_str += COL[0] + str(results[0]) + SWF + "s" + CC + SWFC
        elif results[0] < 0:
            result_str += COL[3] + str(results[0]*-1) + SWF + "f" + CC + SWFC

        # Threat vs Advantage
        if results[1] > 0:
            result_str += COL[2] + "  " + str(results[1])\
                + SWF + "a" + CC + SWFC
        elif results[1] < 0:
            result_str += COL[5] + "  " + str(results[1]*-1)\
                + SWF + "t" + CC + SWFC
        
        
        if results[2]: # Triumph
            result_str += COL[1] + "  " + str(results[2])\
                + SWF + "x" + CC + SWFC
        
        if results[3]: # Despair
            result_str += COL[4] + "  " + str(results[3])\
                + SWF + "y" + CC + SWFC
        
        
        result_str += BC

        history_item.insert(3, result_str)
        history_item.insert(2, pool_str)
        
        return history_item

class DicePool(object):
    def __init__(self, parent):
        
        # Parent Object
        self.parent = parent
        
        # Roll Variables
        self.ability_rolls = [0,0,0]
        self.proficiency_rolls = [0,0,0,0]
        self.boost_rolls = [0,0,0]
        self.difficulty_rolls = [0,0,0]
        self.challenge_rolls = [0,0,0,0]
        self.setback_rolls = [0,0,0]
        
        
        # Totals
        self.pool_success = 0
        self.pool_advantage = 0
        self.pool_triumph = 0
        self.pool_despair = 0

        # History Object
        self.rollHistory = RollHistory(self)
        
    def save_roll(self):
        """Saves current roll to roll history"""
        
        save = False
        for roll in self.all_rolls: # Make sure we don't save an empty pool
            for dice in roll:
                if dice > 0:
                    save = True
        if save:
            self.rollHistory.add_roll(self)
            self.reset()
    
    def reset(self):
        
        # Roll Variables
        self.ability_rolls = [0,0,0]
        self.proficiency_rolls = [0,0,0,0]
        self.boost_rolls = [0,0,0]
        self.difficulty_rolls = [0,0,0]
        self.challenge_rolls = [0,0,0,0]
        self.setback_rolls = [0,0,0]
        
        self._update_all_rolls()
        
        # Totals
        self.pool_success = 0
        self.pool_advantage = 0
        self.pool_triumph = 0
        self.pool_despair = 0
        
        self.parent.parent.update_all()
    
    def reset_one(self, instance=None):
        """Zeroes and resets a single dice class"""
        str_type = instance.type
        type = DICE_TYPES.index(str_type)
        if type == 0:
            self.ability_rolls = [0,0,0]
        elif type == 1:
            self.proficiency_rolls = [0,0,0,0]
        elif type == 2:
            self.boost_rolls = [0,0,0]
        elif type == 3:
            self.difficulty_rolls = [0,0,0]
        elif type == 4:
            self.challenge_rolls = [0,0,0,0]
        elif type ==5:
            self.setback_rolls = [0,0,0]
        self._update_all_rolls()
        self.parent.parent.update_all()
    
    def add_dice(self, instance):
        full_pool = [0,0,0,0,0,0]
        type = DICE_TYPES.index(instance.type)
        full_pool[type] = instance.value
        self.set_pool(full_pool)
    
    def set_pool(self, pool=(0,0,0,0,0,0), reset="n"):
        """Sets the dice pool to a specific amount and rolls"""
        if reset == "y": # When getting a history pool, we want to reset
            self.save_roll()
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
            self._update_dice_results(
                result_list[0],
                result_list[1],
                result_list[2],
                result_list[3],
                result_list[4]
                )
    
    def _update_dice_results(self, type = "", number = 0, success = 0,\
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
    
        """
    
        if type == "boost":
            self.boost_rolls[0] += number
            self.boost_rolls[1] += success
            self.boost_rolls[2] += advantage
        elif type == "setback":
            self.setback_rolls[0] += number
            self.setback_rolls[1] -= success
            self.setback_rolls[2] -= advantage
        elif type == "ability":
            self.ability_rolls[0] += number
            self.ability_rolls[1] += success
            self.ability_rolls[2] += advantage
        elif type == "difficulty":
            self.difficulty_rolls[0] += number
            self.difficulty_rolls[1] -= success
            self.difficulty_rolls[2] -= advantage
        elif type == "proficiency":
            self.proficiency_rolls[0] += number
            self.proficiency_rolls[1] += success
            self.proficiency_rolls[2] += advantage
            self.proficiency_rolls[3] += special
        elif type == "challenge":
            self.challenge_rolls[0] += number
            self.challenge_rolls[1] -= success
            self.challenge_rolls[2] -= advantage
            self.challenge_rolls[3] += special
        # The else happens if the tuple isn't being received
        # from add_dice() correctly.
        else:
            print "Type not recognized during update_dice_results()"
        self._update_all_rolls()
        self.parent.parent.update_all()
    
    def _update_all_rolls(self):
        self.all_rolls = [
            self.ability_rolls,
            self.proficiency_rolls,
            self.boost_rolls,
            self.difficulty_rolls,
            self.challenge_rolls,
            self.setback_rolls
            ]
        self._update_pool_results()
    
    def _update_pool_results(self):
        """Forces an update to the master success, advantage, special counts"""
        success = 0
        advantage = 0
        triumph = 0
        despair = 0
        for i in self.all_rolls:
            success += i[1]
            advantage += i[2]
            if i == self.all_rolls[1]:
                triumph += i[3]
            elif i == self.all_rolls[4]:
                despair += i[3]
        self.pool_success = success
        self.pool_advantage = advantage
        self.pool_triumph = triumph
        self.pool_despair = despair
    
    def roll_again(self, instance=None):
        """Takes the current dice amounts and rolls the exact same roll"""
    
        pool = []
        for i in range(6):
            pool.append(self.all_rolls[i][0])
        
        self.set_pool(pool, "y")


# Interface Left - Top Half (Dice buttons)

class dice_DiceArray(GridLayout):
    """Array of buttons for each type, with different colors"""
    def __init__(self, type, color, **kwargs):
        super(dice_DiceArray, self).__init__(**kwargs)
        self.type = type
        self.color = color
        self.rows = 2
        self.make_array_buttons()
    
    def make_array_buttons(self):
        """Populates the bottom buttons of the ArrayDice class"""
        self.mainButton = TypeButton(
            text = B + self.type.title() + BC,
            type = self.type,
            background_color = self.color,
            markup = True,
            size_hint_y = .5,
            value = 1,
            on_press = self.pass_dice
            )
        
        self.lowerButtons = GridLayout(
            cols = 5,
            size_hint_y = .5
            )
        self.add_widget(self.mainButton)
        self.add_widget(self.lowerButtons)
        
        for i in range(2,4):
            self.lowerButtons.add_widget(TypeButton(
                text = B + str(i) + BC,
                size_hint_x = .5,
                size_hint_y = .5,
                background_color = self.color,
                on_press = self.pass_dice,
                markup = True,
                type = self.type,
                value = i
                ))
    
    def pass_dice(self, instance):
        self.parent.parent.dicePool.add_dice(instance)

class dice_DiceGrid(GridLayout):
    """Side of the window devoted to adding dice"""
    def __init__(self, **kwargs):
        super(dice_DiceGrid, self).__init__(**kwargs)
        self.cols = 3
        self.padding = 10
        self.spacing = 10
        for i in range(6):
            self.add_widget(dice_DiceArray(DICE_TYPES[i], LIN_COLORS[i]))

# Interface Left - Bottom Half (Results & Reset)

# Reset and Reroll Group

class dice_ResetArray(GridLayout):
    """Lists how many dice of each type are in the pool, reset individually"""
    def __init__(self, **kwargs):
        super(dice_ResetArray, self).__init__(**kwargs)
        self.cols = 3
        for i in range(6):
            self.add_widget(Label(
                size_hint_x = .15
                ))
    
    def update(self):
        all_rolls = self.parent.parent.parent.dicePool.all_rolls
        self.clear_widgets()
        for i in range(6):
            if all_rolls[i][0] != 0:
                self.add_widget(TypeButton(
                    text = B + str(all_rolls[i][0]) + BC,
                    size_hint_x = .15,
                    # Using padding_x as a type indicator is a shitty hack
                    # That I use because we can't resolve the type 
                    # from the text alone.
                    #
                    # I know now that I should create a list of custom funcs,
                    # One for each type, and assign that list_func[i] to
                    # each button The custom funcs would simply pass to a
                    # global func the type and amount.
                    markup = True,
                    background_color = LIN_COLORS[i],
                    type = DICE_TYPES[i],
                    on_press = self.parent.parent.parent.dicePool.reset_one
                    ))
            else:
                self.add_widget(Label(
                    size_hint_x = .15
                    ))

# Result Display

class dice_ResultLabel(GridLayout):
    """A single label to display a single result (success/failure, etc)"""
    def __init__(self, label, number, **kwargs):
        super(dice_ResultLabel, self).__init__(**kwargs)
        self.cols = 1
        # We need to get the type down to a string that matches the RESULT_TYPES
        self.type = label.lower()
        self.number = number
        
        if self.type != "":
            self.type = RESULT_TYPES.index(self.type)
            self.texture = Image(TEXTURE_LIST[self.type]).texture
            if str(number) != "":
                self.text = B + str(number) + BC
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
        
        if self.type != "": # If we're not empty, do texture binds
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

class dice_ResultGrid(GridLayout):
    """A 2x2 grid containing ResultLabel labels showing results"""
    def __init__(self, **kwargs):
        super(dice_ResultGrid, self).__init__(**kwargs)
        self.rows = 2
        self.cols = 2
        self.spacing = 10
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
        """Updates the result Labels"""
        self.clear_widgets() # Removes ALL ResultLabel objects
        dicePool = self.parent.parent.parent.dicePool
        
        # Check if there have been any results...
        dice = False
        for i in dicePool.all_rolls:
            if i[0] != 0:
                dice = True
        if dice:
            if dicePool.pool_success > 0:
                # We don't actually display the 'Success: ' text anymore, but
                # we still use the string itself for defining the type,
                # if the result is good or bad, and the texture to load.
                #
                # We could probably remove the trailing ': ', but this is taken 
                # care of at ResultLabel creation anyway.
                success_label = "Success"
                success_num = dicePool.pool_success
            elif dicePool.pool_success == 0:
                success_label = "Failure" # If no success, roll fails.
                success_num = ""
            else:
                success_label = "Failure"
                success_num = -1 * dicePool.pool_success
            if dicePool.pool_advantage > 0:
                advantage_label = "Advantage"
                advantage_num = dicePool.pool_advantage
            elif dicePool.pool_advantage < 0:
                advantage_label = "Threat"
                advantage_num = -1 * dicePool.pool_advantage
            else:
                advantage_label = ""
                advantage_num = ""
            # Triumph and Despair can only be zero or positive.
            if dicePool.pool_triumph > 0:
                triumph_label = "Triumph"
                triumph_num = dicePool.pool_triumph
            else:
                triumph_label = ""
                triumph_num = ""
            if dicePool.pool_despair > 0:
                despair_label = "Despair"
                despair_num = dicePool.pool_despair
            else:
                despair_label = ""
                despair_num = ""
            self.add_widget(dice_ResultLabel(success_label, success_num))
            self.add_widget(dice_ResultLabel(advantage_label, advantage_num))
            self.add_widget(dice_ResultLabel(triumph_label, triumph_num))
            self.add_widget(dice_ResultLabel(despair_label, despair_num))
         # Just in case, we reset the var.
        dice = False

class dice_ResultsByDice(Label):
    def __init__(self, **kwargs):
        super(dice_ResultsByDice, self).__init__(**kwargs)
        self.text = ''
        self.markup = True
    
    def update(self):
        """Updates the result Labels"""
        new_text = ''
        dicePool = self.parent.parent.parent.dicePool
        total_results = 0
        for i in range(3):
            total_results += dicePool.all_rolls[i][1]
            total_results += dicePool.all_rolls[i][2]
        total_results += dicePool.all_rolls[1][3]
        for i in range(3,6):
            total_results -= dicePool.all_rolls[i][1]
            total_results -= dicePool.all_rolls[i][2]
        total_results += dicePool.all_rolls[4][3]
        
        # Check if there have been any results...
        dice = False
        for i in dicePool.all_rolls:
            if i[0] != 0:
                dice = True
        if dice:
            if total_results <= 20:
                new_text += B + SWF
                new_text += COL[1] + 'a'*dicePool.all_rolls[1][2] + CC
                new_text += COL[0] + 'a'*dicePool.all_rolls[0][2] + CC
                new_text += COL[2] + 'a'*dicePool.all_rolls[2][2] + CC
                if new_text.count('a') > 0:
                    new_text += ' '
                    
                new_text += COL[1] + 's'*dicePool.all_rolls[1][1] + CC
                new_text += COL[0] + 's'*dicePool.all_rolls[0][1] + CC
                new_text += COL[2] + 's'*dicePool.all_rolls[2][1] + CC
                if new_text.count('s') > 0:
                    new_text += ' '
                    
                new_text += COL[1] + 'x'*dicePool.all_rolls[1][3] + CC
                
                new_text += SWFC + '  |  ' + SWF
                
                new_text += COL[4] + 'y'*dicePool.all_rolls[4][3] + CC
                if new_text.count('y') > 0:
                    new_text += ' '
                    
                new_text += COL[4] + 'f'*(dicePool.all_rolls[4][1]*-1) + CC
                new_text += COL[3] + 'f'*(dicePool.all_rolls[3][1]*-1) + CC
                new_text += COL[5] + 'f'*(dicePool.all_rolls[5][1]*-1) + CC
                if new_text.count('f') > 0:
                    new_text += ' '
                    
                new_text += COL[4] + 't'*(dicePool.all_rolls[4][2]*-1) + CC
                new_text += COL[3] + 't'*(dicePool.all_rolls[3][2]*-1) + CC
                new_text += COL[5] + 't'*(dicePool.all_rolls[5][2]*-1) + CC
                
            else:
                new_text += B
                if dicePool.all_rolls[1][2]:
                    new_text += COL[1] + str(dicePool.all_rolls[1][2])\
                        + SWF + 'a' + SWFC + CC + ' '
                if dicePool.all_rolls[0][2]:
                    new_text += COL[0] + str(dicePool.all_rolls[0][2])\
                        + SWF + 'a' + SWFC + CC + ' '
                if dicePool.all_rolls[2][2]:
                    new_text += COL[2] + str(dicePool.all_rolls[2][2])\
                        + SWF + 'a' + SWFC + CC + ' '
                if dicePool.all_rolls[1][1]:
                    new_text += COL[1] + str(dicePool.all_rolls[1][1])\
                        + SWF + 's' + SWFC + CC + ' '
                if dicePool.all_rolls[0][1]:
                    new_text += COL[0] + str(dicePool.all_rolls[0][1])\
                        + SWF + 's' + SWFC + CC + ' '
                if dicePool.all_rolls[2][1]:
                    new_text += COL[2] + str(dicePool.all_rolls[2][1])\
                        + SWF + 's' + SWFC + CC + ' '
                if dicePool.all_rolls[1][3]:
                    new_text += COL[1] + str(dicePool.all_rolls[1][3])\
                        + SWF + 'x' + SWFC + CC
                
                new_text += ' | '
                
                if dicePool.all_rolls[4][3]:
                    new_text += COL[4] + str(dicePool.all_rolls[4][3])\
                        + SWF + 'y' + SWFC + CC + ' '
                if dicePool.all_rolls[4][1]:
                    new_text += COL[4] + str(dicePool.all_rolls[4][1]*-1)\
                        + SWF + 'f' + SWFC + CC + ' '
                if dicePool.all_rolls[3][1]:
                    new_text += COL[3] + str(dicePool.all_rolls[3][1]*-1)\
                        + SWF + 'f' + SWFC + CC + ' '
                if dicePool.all_rolls[5][1]:
                    new_text += COL[5] + str(dicePool.all_rolls[5][1]*-1)\
                        + SWF + 'f' + SWFC + CC + ' '
                if dicePool.all_rolls[4][2]:
                    new_text += COL[4] + str(dicePool.all_rolls[4][2]*-1)\
                        + SWF + 't' + SWFC + CC + ' '
                if dicePool.all_rolls[3][2]:
                    new_text += COL[3] + str(dicePool.all_rolls[3][2]*-1)\
                        + SWF + 't' + SWFC + CC + ' '
                if dicePool.all_rolls[5][2]:
                    new_text += COL[5] + str(dicePool.all_rolls[5][2]*-1)\
                        + SWF + 't' + SWFC + CC
                
        dice = False
        self.text = new_text

class dice_ResultBottom(GridLayout):
    """Bottom half of the window devoted to displaying/resetting results"""
    def __init__(self, **kwargs):
        super(dice_ResultBottom, self).__init__(**kwargs)
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
            on_press = self.roll_again,
            markup = True
            )
        # dicePool represents the individual types of dice, and can clear
        # each. If no dice of a type are currently rolled, that dice
        # will be invisible. Otherwise it will read the current amount.
        self.resetArray = dice_ResetArray(
            size_hint_y = .5
            )
        # resetAllButton uses reset_all() to clear all individual dice results 
        # and amount of dice
        self.resetAllButton = Button(
            text = "[b]Reset All[/b]",
            size_hint_y = .25,
            on_press = self.save_roll,
            markup = True
            )
        # Some blank labels for shorthand reference
        self.blankLabel1 = Label(
            size_hint_y = .25
            )
        self.blankLabel2 = Label(
            size_hint_y = .25
            )
        self.resetGroup.add_widget(self.resetArray)
        self.resetGroup.add_widget(self.blankLabel1)
        # self.result_label_grid is where the results are displayed
        self.full_results_grid = GridLayout(
            rows = 2,
            size_hint_x = .66
            )
        self.results_by_dice = dice_ResultsByDice(
            size_hint_y = 10
            )
        self.result_label_grid = dice_ResultGrid(
            size_hint_y = 90
            )
        self.add_widget(self.resetGroup)
        self.full_results_grid.add_widget(self.result_label_grid)
        self.full_results_grid.add_widget(self.results_by_dice)
        self.add_widget(self.full_results_grid)
    
    def roll_again(self, instance=None):
        self.parent.dicePool.roll_again()
    
    def save_roll(self, ignore=''):
        self.parent.dicePool.save_roll()
        
    def update(self):
        """Updates the entire result side"""
        dice = False
        self.resetArray.update()
        for i in self.parent.dicePool.all_rolls: # Check if any dice exist
            if i[0] != 0:
                dice = True
        self.resetGroup.clear_widgets()
        if dice: # If dice exist, built the widgets
            self.resetGroup.add_widget(self.rollAgain)
            self.resetGroup.add_widget(self.resetArray)
            self.resetGroup.add_widget(self.resetAllButton)
        else: # If no dice rolled, build blanks.
            self.resetGroup.add_widget(self.blankLabel1)
            self.resetGroup.add_widget(self.resetArray)
            self.resetGroup.add_widget(self.blankLabel2)
        dice = False # Reset dice var just in case
        # Call a GUI update on the contained result_label_grid
        self.result_label_grid.update()
        self.results_by_dice.update()

# Top Layer Window

class dice_UILeft(GridLayout):
    """Left side of the interface, with dice and results"""
    def __init__(self, **kwargs):
        super(dice_UILeft, self).__init__(**kwargs)
        self.rows = 2
        self.size_hint_x = .65
        
        self.dicePool = DicePool(self)
        
        self.add_widget(dice_DiceGrid(
            size_hint_y = .5
            ))
        self.resultBottom = dice_ResultBottom(
            size_hint_y = .5
            )
        self.add_widget(self.resultBottom)

class ListItemTypeButton(ListItemButton):
    def __init__(self, type=None, value=None, **kwargs):
        super(ListItemTypeButton, self).__init__(**kwargs)
        self.type = type
        self.value = value

class dice_HistoryListView(GridLayout):
    """The list widget for viewing of the roll history, also let's you reroll"""
    def __init__(self, **kwargs):
        super(dice_HistoryListView, self).__init__(**kwargs)
        self.rows = 2
        # Top row is going to be our header
        self.header = GridLayout(
            cols = 3,
            size_hint_y = 3
            )
        # Header elements have the same size_hint_x as the list elements
        self.header_time = Label(
            text = "Time",
            size_hint_x = 12
            )
        self.header_pool = Label(
            text = "Pool",
            size_hint_x = 54
            )
        self.header_results = Label(
            text = "Results",
            size_hint_x = 34
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
                        'size_hint_x': 12
                        }
                    },
                {'cls': ListItemTypeButton,
                    'kwargs': {
                        'text': list[2],
                        'value': list[1],
                        'size_hint_x': 54,
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
                        'text': list[4],
                        'markup': True,
                        'size_hint_x': 34
                        }
                    }
            ]}

        self.list_adapter = ListAdapter(
            allow_empty_selection = True,
            selection_mode = 'single',
            data = [],
            args_converter = self.args_converter,
            cls=CompositeListItem
            )

        self.list_view = ListView(
            adapter=self.list_adapter,
            size_hint_y = 97
            )

        self.add_widget(self.list_view)
    
    def sch_clear_selection(self, ignore=''):
        """Schedules a rebuild of the list to clear selection."""
        Clock.schedule_once(self.update_list, .1)
    
    def update_list(self, ignore=''):
        """Totally rebuilds the entire list_view GUI"""
        # We remove and add ONLY the list_view, not touching the header.
        top = self.parent.parent.parent.parent.parent.parent.uiLeft.dicePool
        self.remove_widget(self.list_view)
        self.list_adapter = ListAdapter(
            allow_empty_selection = True,
            selection_mode = 'single',
            data = top.rollHistory.history,
            args_converter = self.args_converter,
            cls=CompositeListItem
            )
        self.list_view = ListView(
            adapter=self.list_adapter,
            size_hint_y = 97
            )
        self.add_widget(self.list_view)
    
    def pass_dice(self, instance):
        """Sets the pool with a save and reset"""
        top = self.parent.parent.parent.parent.parent.parent.uiLeft.dicePool
        new_pool = instance.value
        top.set_pool(new_pool, reset="y")

class dice_CommonPools(GridLayout):
    """A grid layout of buttons representing the common dice rolls as seen
    in COMMON_POOLS"""
    def __init__(self, **kwargs):
        super(dice_CommonPools, self).__init__(**kwargs)
        self.cols = 2
        
        # Create the good and bad pools
        self.good_pools = [] 
        for i in range(len(COMMON_POOLS)):
            self.good_pools.append(self.halfpool_markup(COMMON_POOLS[i]))
        self.bad_pools = []
        for i in range(len(COMMON_POOLS)):
            self.bad_pools.append(self.halfpool_markup(COMMON_POOLS[i],"y"))
            
        
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
            self.rightCol.add_widget(TypeButton(
                text = self.bad_pools[i],
                background_color = (.4,.4,.5,1),
                on_press = self.pass_bad,
                markup = True,
                value = COMMON_POOLS[i]
                ))
            self.leftCol.add_widget(TypeButton(
                text = self.good_pools[i],
                background_color = (.5,.5,.5,1),
                on_press = self.pass_good,
                markup = True,
                value = COMMON_POOLS[i]
                ))
        
        self.add_widget(self.leftCol)
        self.add_widget(self.rightCol)
    
    def pass_good(self, instance):
        """Takes a press_on signal from a button and passes it on to
        string_to_halfpool without bad set."""
        top = self.parent.parent.parent.parent.parent.parent
        back_pool = [0,0,0]
        pool = instance.value
        pool.extend(back_pool)
        top.uiLeft.dicePool.set_pool(pool)
    
    def pass_bad(self, instance):
        """Takes a press_on signal from a button and passes it on to
        string_to_halfpool with bad set."""
        top = self.parent.parent.parent.parent.parent.parent
        pool = [0,0,0]
        back_pool = instance.value
        pool.extend(back_pool)
        top.uiLeft.dicePool.set_pool(pool)

    def halfpool_markup(self, pool = (1, 1, 0), bad = "n"):
        """Takes a single tuple and returns a string"""
    
        pool_str = ''
        # c = proficiency/challenge
        # b = boost/setback
        # d = ability/difficulty
        if bad == "n":
            pool_str += COL[1] + SWF + "c"*pool[1] + SWFC + CC
            pool_str += COL[0] + SWF + "d"*pool[0] + SWFC + CC
            pool_str += COL[2] + SWF + "b"*pool[2] + SWFC + CC
        else:
            pool_str += COL[4] + SWF + "c"*pool[1] + SWFC + CC
            pool_str += COL[3] + SWF + "d"*pool[0] + SWFC + CC
            pool_str += COL[5] + SWF + "b"*pool[2] + SWFC + CC
        return pool_str

class dice_UIRight(Accordion):
    """The right side of the interface, an accordion group"""
    def __init__(self, **kwargs):
        super(dice_UIRight, self).__init__(**kwargs)
        self.size_hint_x = .35
        self.orientation = "vertical"
        
        # Accordion Items
        self.historyAcc = AccordionItem(
            title = "History"
            )
        self.commonPoolsAcc = AccordionItem(
            title = "Common Dice Pools"
            )
        
        # Things inside of the Accordion Items
        self.commonPools = dice_CommonPools()
        self.history = dice_HistoryListView()
        
        # Add interior items to Accordion Items
        self.commonPoolsAcc.add_widget(self.commonPools)
        self.historyAcc.add_widget(self.history)
        
        # Add Accordion Items
        self.add_widget(self.historyAcc)
        self.add_widget(self.commonPoolsAcc)

class dice_UI(GridLayout):
    """Main interface, additive dice to the left and results to the right"""
    def __init__(self, **kwargs):
        super(dice_UI, self).__init__(**kwargs)
        self.cols = 2
        
        self.uiLeft = dice_UILeft()
        self.uiRight = dice_UIRight()
        
        self.add_widget(self.uiLeft)
        self.add_widget(self.uiRight)
    
    def update_all(self):
        self.uiLeft.resultBottom.update()

if __name__ == "__main__":
    print "This module is not meant to be run directly"