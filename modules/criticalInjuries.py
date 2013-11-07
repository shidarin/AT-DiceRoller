#!/usr/bin/kivy
# Critical Injury Module
# By Sean Wallitsch, 2013/08/20

# Built in Modules

from random import randint
from time import strftime # For timestamping history log

# Kivy Modules

from kivy.app import App # Base App Class
from kivy.adapters.listadapter import ListAdapter # For History list
from kivy.uix.gridlayout import GridLayout # Only Using Grid Layouts
from kivy.uix.label import Label # Label Class for Returns
from kivy.uix.button import Button # Button Class for everything else
from kivy.uix.listview import ListItemButton, ListItemLabel, \
        CompositeListItem, ListView # For Right Side History
from kivy.uix.slider import Slider # For Controls
from kivy.uix.popup import Popup # For viewing description in History
from kivy.graphics import Canvas, Color, Rectangle # For backgrounds
from kivy.core.image import Image # For textures
from kivy.clock import Clock # For scheduling a deselect of the history list

# ==============================================================================
# AT GENERIC VARIABLES
# ==============================================================================

# Markup Shortcuts

SWF = "[font=fonts/sw_symbols.ttf]"
SWFC = "[/font]"
DC = "[color=873ead]"
CC = "[/color]"

# ==============================================================================
# APP SPECIFIC VARIABLES
# ==============================================================================

# For ResultDisplay
HEADER_TEXT = ('Roll', 'Severity', 'Result')
COL_SIZES = (20,20,60)

# DICTs

RESULTS ={
    "Minor Nick": "The target suffers 1 strain.",
    "Slowed Down": "The target can only act during the last allied initiative slot on his next turn.",
    "Sudden Jolt": "The target drops whatever is in hand.",
    "Distracted": "The target cannot perform a free maneuver during his next turn.",
    "Off-Balance": "Add (1) Setback Die to target's next skill check.",
    "Discouraging Wound": "Flip one light side Destiny point to the dark side (reverse if NPC).",
    "Stunned": "The target is staggered until the end of target's next turn.",
    "Stinger": "Increase difficulty of next check by (1).",
    "Bowled Over": "The target is knocked prone and suffers (1) strain.",
    "Head Ringer": "The target increases the difficulty of all Intellect and Cunning checks by (1) until the end of the encounter.",
    "Fearsome Wound": "The target increases the difficulty of all Presence and Willpower checks by (1) until the end of the encounter.",
    "Agonizing Wound": "The target increases the difficulty of all Brawn and Agility checks by (1) until the end of the encounter.",
    "Slightly Dazed": "The target is disoriented until the end of the encounter.",
    "Scattered Senses": "The target removes all Boost Die from skill checks until the end of the encounter.",
    "Hamstrung": "The target loses their free maneuver until the end of the encounter.",
    "Overpowered": "The target leaves himself open, and the attacker may immediately attempt another free attack against him, using the exact same pool as the original attack.",
    "Winded": "Until the end of the encounter, the target cannot voluntarily suffer strain to activate any abilities or gain additional maneuvers.",
    "Compromised": "Increase difficulty of all skill checks by (1) until the end of the encounter.",
    "At the Brink": "The target suffers (1) strain each time they perform an action",
    "Crippled": "One of the target's limbs (selected by the GM) is crippled until healed or replaced. Increase difficulty of all checks that require use of that limb by one.",
    "Maimed": "One of the target's limbs (selected by the GM) is permanently lost. Unless the target has a cybernetic replacement, the target cannot perform actions that would require the use of that limb. All other actions gain (1) Setback Die.",
    "Horrific Injury": "Randomly roll a 1d10 to determine one of the target's characteristics 1-3 for Brawn, 4-6 for Agility, 7 for Intellect, 8 for Cunning, 9 for Presence, 10 for Willpower. Until this Critical Injury is healed, treat that characteristic as (1) point lower.",
    "Temporarily Lame": "Until this Critical Injury is healed, the target cannot perform more than one maneuver during their turn.",
    "Blinded": "The target can no longer see. Upgrade the difficulty of all checks twice. Upgrade the difficulty of all Perception and Vigilance checks three times.",
    "Knocked Senseless": "The target is staggered for the remainder of the encounter.",
    "Gruesome Injury": "Randomly roll a 1d10 to determine one of the target's characteristics 1-3 for Brawn, 4-6 for Agility, 7 for Intellect, 8 for Cunning, 9 for Presence, 10 for Willpower. That characteristic is permanently reduced by (1), to a minimum of (1).",
    "Bleeding Out": "Every round, the target suffers (1) wound and (1) strain at the beginning of their turn. For every five wounds they suffer beyond their wound threshold, they suffer one additional Critical Injury (cannot suffer this one again).",
    "The End is Nigh": "The target will die after the last Initiative slot during the next round.",
    "Dead": "Complete, obliterated death"
    }

SEVERITY = [None, 'Easy', 'Average', 'Hard', 'Daunting', '-']

# ==============================================================================
# FUNCTIONS
# ==============================================================================

def crit_chart(roll):
    """Takes a roll value and interprets it according to the CI_chart"""
    
    if roll >= 151:
        severity = 5
    elif roll >= 126:
        severity = 4
    elif roll >= 91:
        severity = 3
    elif roll >= 41:
        severity = 2
    else:
        severity = 1
    
    if roll >= 151:
        name = "Dead"
    elif roll >= 141:
        name = "The End is Nigh"
    elif roll >= 131:
        name = "Bleeding Out"
    elif roll >= 126:
        name = "Gruesome Injury"
    elif roll >= 121:
        name = "Knocked Senseless"
    elif roll >= 116:
        name = "Blinded"
    elif roll >= 111:
        name = "Temporarily Lame"
    elif roll >= 106:
        name = "Horrific Injury"
    elif roll >= 101:
        name = "Maimed"
    elif roll >= 95:
        name = "Crippled"
    elif roll >= 91:
        name = "At the Brink"
    elif roll >= 86:
        name = "Compromised"
    elif roll >= 81:
        name = "Winded"
    elif roll >= 76:
        name = "Overpowered"
    elif roll >= 71:
        name = "Hamstrung"
    elif roll >= 66:
        name = "Scattered Senses"
    elif roll >= 61:
        name = "Slightly Dazed"
    elif roll >= 56:
        name = "Agonizing Wound"
    elif roll >= 51:
        name = "Fearsome Wound"
    elif roll >= 46:
        name = "Head Ringer"
    elif roll >= 41:
        name = "Bowled Over"
    elif roll >= 36:
        name = "Stinger"
    elif roll >= 31:
        name = "Stunned"
    elif roll >= 26:
        name = "Discouraging Wound"
    elif roll >= 21:
        name = "Off-Balance"
    elif roll >= 16:
        name = "Distracted"
    elif roll >= 11:
        name = "Sudden Jolt"
    elif roll >= 6:
        name = "Slowed Down"
    else:
        name = "Minor Nick"
    
    return severity, name

def new_pos(old_size = (1,1), new_size = (1,1), pos = (1,1), pos_mult = (0,0)):
    """Shortcut for adjusting a position based on widget size changes"""
    new_pos = (
        pos[0] + (old_size[0] - new_size[0]) * pos_mult[0],
        pos[1] + (old_size[1] - new_size[1]) * pos_mult[1]
        )
    return new_pos

# ==============================================================================
# GUI CLASSES
# ==============================================================================

# ==============================================================================
# RESULTBOX WIDGETS
# ==============================================================================

class crit_HeaderRoll(Label):
    """Header for Roll"""
    def __init__(self, **kwargs):
        super(crit_HeaderRoll, self).__init__(**kwargs)
        
        self.text = HEADER_TEXT[0]
        self.size_hint_x = COL_SIZES[0]

class crit_HeaderSeverity(Label):
    """Header for Severity"""
    def __init__(self, **kwargs):
        super(crit_HeaderSeverity, self).__init__(**kwargs)
        
        self.text = HEADER_TEXT[1]
        self.size_hint_x = COL_SIZES[1]

class crit_HeaderNameDesc(Label):
    """Header for the name and description"""
    def __init__(self, **kwargs):
        super(crit_HeaderNameDesc, self).__init__(**kwargs)
        
        self.text = HEADER_TEXT[2]
        self.size_hint_x = COL_SIZES[2]

class crit_HeaderDisplay(GridLayout):
    """All three headers together"""
    def __init__(self, **kwargs):
        super(crit_HeaderDisplay, self).__init__(**kwargs)
        
        self.cols = 3
        
        for widget in (
            crit_HeaderRoll(),
            crit_HeaderSeverity(),
            crit_HeaderNameDesc()
            ):
            self.add_widget(widget)

class crit_ResultRoll(Label):
    """Display are for resulting roll"""
    def __init__(self, previous, mod, roll, **kwargs):
        super(crit_ResultRoll, self).__init__(**kwargs)
        
        # Check to see if anything has been rolled
        if roll:
            self.text = "[size=12](" + str(previous) +  "*10" + ") + "\
                + str(mod) + " + " + str(roll) + "[/size]\n[b][size=36]"\
                + str(previous*10 + mod + roll) + "[/b][/size]"
        # Else label text will be empty
        self.size_hint_x = COL_SIZES[0]
        self.halign = 'center'
        self.markup = True

class crit_ResultSeverity(Label):
    """Display are for severity"""
    def __init__(self, severity, **kwargs):
        super(crit_ResultSeverity, self).__init__(**kwargs)
        
        # Check to see if anything has been rolled
        if severity:
            if severity < 5:
                self.text = '[b]' + SEVERITY[severity] + '[/b]\n&bl;' +\
                    SWF + DC + 'd'*severity + CC + SWFC + '&br;'
            else:
                self.text = "[b]" + SEVERITY[severity] + "[/b]"
        # Else label will be empty
        self.size_hint_x = COL_SIZES[1]
        self.halign = 'center'
        self.markup = True

class crit_ResultNameDesc(Label):
    """Display are for the Name and Description of injury"""
    def __init__(self, name, **kwargs):
        super(crit_ResultNameDesc, self).__init__(**kwargs)
        
        # If this widget size changes, we need the text to stay within
        self.bind(
            size = self._update_text
            )
        
        # Check for roll
        if name:
            self.text = "[b]" + name + "[/b]: " + RESULTS[name]
        # Else label will be blank
        # This forces a soft wrap
        self.text_size = (self.size[0]*.96, None)
        self.size_hint_x = COL_SIZES[2]
        self.markup = True
    
    def _update_text(self, instance, value):
        """Updates the softwrap values on widget size change"""
        self.text_size = (instance.size[0]*.96, None)

class crit_ResultDisplay(GridLayout):
    """All three results in a grid"""
    def __init__(self, previous, mod, roll, severity, name, **kwargs):
        super(crit_ResultDisplay, self).__init__(**kwargs)
        
        self.cols = 3
        
        for widget in (
            crit_ResultRoll(previous, mod, roll),
            crit_ResultSeverity(severity),
            crit_ResultNameDesc(name)
            ):
            self.add_widget(widget)

# ==============================================================================
# History_UI WIDGETS
# ==============================================================================

class crit_PopupLabel(Label):
    """This is the text display inside the results history popup"""
    def __init__(self, severity, name, **kwargs):
        super(crit_PopupLabel, self).__init__(**kwargs)
        self.severity = severity
        self.name = name
        self.text = RESULTS[self.name] + "\n\n" + SEVERITY[severity]\
            + "  &bl;" + SWF + DC + "d"*self.severity + SWFC + CC + "&br;"
        
        # Forces a softwrap
        self.text_size = (self.size[0]*.96, None)
        self.size_hint_y = 80
        self.markup = True
        
        # Update softwrap if widget size changes
        self.bind(
            size = self._update_text
            )
    
    def _update_text(self, instance, value):
        """This updates the text wrap"""
        self.text_size = (self.size[0]*.96, None)

class crit_ListItemButton(ListItemButton):
    """The button for the HistoryUI list. Clicking this creates a popup"""
    def __init__(self, severity, name, **kwargs):
        super(crit_ListItemButton, self).__init__(**kwargs)
        self.severity = severity
        self.name = name
        self.text = self.name
        self.on_press = self.pop_up_descript
        
        self.popup_content = GridLayout(
            rows = 2
            )
        
        self.popup = Popup(
            size_hint_x = .6,
            size_hint_y = .4,
            title = self.name,
            title_size = 18,
            content = self.popup_content,
            )
        
        # Popup and Child Widgets
        self.popup_button = Button(
            text = "Dismiss",
            size_hint_y = 20,
            on_press = self.popup.dismiss
            )
        
        self.popup_content.add_widget(crit_PopupLabel(
            severity = self.severity,
            name = self.name
            ))
        
        self.popup_content.add_widget(self.popup_button)

    def pop_up_descript(self):
        self.popup.open()

class crit_HistoryList(object):
    """History list object"""
    def __init__(self, parent):
        self.parent = parent
        self.history = []
    
    def update_history(self, historySet):
        """Updates the history list and forces a HistoryUI update"""
        self.history.insert(0, historySet)
        self.parent.update_list()

# ==============================================================================
# CRITICAL INJURY TOP LEVEL
# ==============================================================================

class crit_HistoryUI(GridLayout):
    """Displays a header and the main history list"""
    def __init__(self, **kwargs):
        super(crit_HistoryUI, self).__init__(**kwargs)
        self.rows = 2
        
        self.historyList = crit_HistoryList(self)
        
        self.bind(
            size = self._update_lines,
            pos = self._update_lines
            )
        
        # Top row is going to be our header
        self.header = GridLayout(
            cols = 4,
            size_hint_y = 15
            )
        # Header elements have the same size_hint_x as the list elements
        self.header_time = Label(
            text = "Time",
            size_hint_x = 10
            )
        self.header_roll = Label(
            text = "Roll",
            size_hint_x = 25
            )
        self.header_severity = Label(
            text = "Severity",
            size_hint_x = 25
            )
        self.header_results = Label(
            text = "Results",
            size_hint_x = 30
            )
        self.header.add_widget(self.header_time)
        self.header.add_widget(self.header_roll)
        self.header.add_widget(self.header_severity)
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
            'height': 35, # this is the height of the rows
            'cls_dicts': [ # Each cls entry is an item in the row
                {'cls': ListItemLabel,
                    'kwargs': { # the keywords used during item creation
                        'text': list[0],
                        'size_hint_x': self.header_time.size_hint_x
                        }
                    },
                {'cls': ListItemLabel,
                    'kwargs': {
                        'text': "[size=12](" + str(list[1][0]) +  "*10"\
                            + ") + " + str(list[1][1]) + " + "\
                            + str(list[1][2]) + "[b] = [/size][size=24]"\
                            + str(sum(list[1])) + "[/b][/size]",
                        'size_hint_x': self.header_roll.size_hint_x,
                        'markup': True,
                        'valign': 'middle'
                        }
                    },
                {'cls': ListItemLabel,
                    'kwargs': {
                        'text': "[size=12]" + SEVERITY[list[2]] + "  &bl;"\
                            + SWF + DC + "d"*list[2] + SWFC + CC\
                            + "&br;[/size]",
                        'size_hint_x': self.header_severity.size_hint_x,
                        'markup': True
                        }
                    },
                {'cls': crit_ListItemButton,
                    'kwargs': {
                        'severity': list[2],
                        'name': list[3],
                        'text': '',
                        'size_hint_x': self.header_results.size_hint_x,
                        'deselected_color': [.6,.6,.6,1],
                        'selected_color': [.9,.9,.9,1],
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
            ]}

        self.list_adapter = ListAdapter(
            allow_empty_selection = True,
            selection_mode = 'single',
            data = self.historyList.history,
            args_converter = self.args_converter,
            cls=CompositeListItem
            )

        self.list_view = ListView(
            adapter=self.list_adapter,
            size_hint_y = 85
            )

        self.add_widget(self.list_view)
        
        with self.canvas.before:
            Color(.1843, .655, .831)
            self.horz_spacer = Rectangle(
                size = (self.size[0]*.98, 1),
                pos = new_pos(self.size, (self.size[0]*.98, 1),\
                    self.pos, (.5, .87))
                )
    
    def sch_clear_selection(self, ignore):
        """Schedules the list to be updated"""
        Clock.schedule_once(self.update_list, .1)
    
    def update_list(self, ignore=''):
        """Causes the list to be rebuilt"""
        # We remove and add ONLY the list_view, not touching the header.
        self.remove_widget(self.list_view)
        self.list_adapter = ListAdapter(
            allow_empty_selection = True,
            selection_mode = 'single',
            data = self.historyList.history,
            args_converter = self.args_converter,
            cls=CompositeListItem
            )
        self.list_view = ListView(
            adapter=self.list_adapter,
            size_hint_y = 97
            )
        self.add_widget(self.list_view)
    
    def _update_lines(self, instance, value):
        horz1_new_size = (instance.size[0]*.98, 1)
        self.horz_spacer.size = horz1_new_size
        self.horz_spacer.pos = new_pos(instance.size, horz1_new_size,\
            instance.pos, (.5, .87))

class crit_ResultBox(GridLayout):
    """Main readout for injury results"""
    def __init__(self, **kwargs):
        super(crit_ResultBox, self).__init__(**kwargs)
        self.rows = 2
        
        # Initialize all of our variables
        self._clear_result()
        
        # Display Widgets
        self.resultDisplay = crit_ResultDisplay(
            self._previousInjuries,
            self._rollMod,
            self._roll,
            self._severity,
            self._resultKey,
            size_hint_y = 80
            )
        
        self.headerDisplay = crit_HeaderDisplay(
            size_hint_y = 20
            )
        
        self.add_widget(self.headerDisplay)
        self.update() # Will add our resultDisplay
        
        self.bind(
            size = self._update_lines,
            pos = self._update_lines
            )
        
        with self.canvas.before:
            Color(.1843, .655, .831)
            self.horz1_spacer = Rectangle(
                size = (self.size[0]*.98, 1),
                pos = new_pos(self.size, (self.size[0]*.98, 1),\
                    self.pos, (.5, .755))
                    )
            self.horz2_spacer = Rectangle(
                size = (self.size[0]*.98, 1),
                pos = new_pos(self.size, (self.size[0]*.98, 1),\
                    self.pos, (.5, 0))
                    )
    
    def _clear_result(self):
        """Inits and clears all results"""
        self._previousInjuries = 0
        self._rollMod = 0
        self._roll = 0
        self._severity = 0
        self._resultKey = ''
    
    def roll(self, ignore=''):
        """Saves current, grabs the slider values, randint()s, _set_result()"""
        if self._roll:
            self._save_roll()
            self._clear_result()
        previous = int(self.parent.controls.prevInjuriesSlider.value)
        mod = int(self.parent.controls.modSlider.value)
        roll = randint(1,100)
        severity, resultKey = crit_chart(previous*10 + mod + roll)
        
        self._set_result(previous, mod, roll, severity, resultKey)
        self.update()
    
    def _save_roll(self):
        """Takes the current roll and adds it to history"""
        time = strftime("%H:%M")
        roll_set = (self._previousInjuries, self._rollMod, self._roll)
        history = (time, roll_set, self._severity, self._resultKey)
        self.parent.historyUI.historyList.update_history(history)
    
    def _set_result(self, previous, mod, roll, severity, resultKey):
        """Sets the result variables"""
        self._previousInjuries = previous
        self._rollMod = mod
        self._roll = roll
        self._severity = severity
        self._resultKey = resultKey
    
    def update(self):
        """Rebuilds widgets"""
        if self.resultDisplay in self.children:
            self.remove_widget(self.resultDisplay)
            self.resultDisplay = crit_ResultDisplay(
                self._previousInjuries,
                self._rollMod,
                self._roll,
                self._severity,
                self._resultKey,
                size_hint_y = 80
                )
        self.add_widget(self.resultDisplay)
    
    def _update_lines(self, instance, value):
        horz1_new_size = (instance.size[0]*.98, 1)
        self.horz1_spacer.size = horz1_new_size
        self.horz2_spacer.size = horz1_new_size
        self.horz1_spacer.pos = new_pos(instance.size, horz1_new_size,\
            instance.pos, (.5, .755))
        self.horz2_spacer.pos = new_pos(instance.size, horz1_new_size,\
            instance.pos, (.5, 0))

class crit_Controls(GridLayout):
    """Area for sliders"""
    def __init__(self, **kwargs):
        super(crit_Controls, self).__init__(**kwargs)
        self.cols = 2
        
        # Left Half is a 6 row slider grid
        self.sliders = GridLayout(
            rows = 6,
            size_hint_x = 75,
            spacing = 20,
            padding = 20
            )
        
        # Previous Injuries
        self.prevInjuriesLabel = Label(
            text = "Previous Critical Injuries"
            )
        self.prevInjuriesSlider = Slider(
            range = (0,15),
            step = 1,
            value = 0,
            size_hint_x = 90
            )
        self.prevInjuriesReadout = Label(
            text = "[b]" + str(int(self.prevInjuriesSlider.value)) + "[/b]",
            markup = True
            )
        
        self.prevInjuriesSliderGrid = GridLayout(
            cols = 3,
            spacing = 12
            )
        
        self.prevInjuriesSliderGrid.add_widget(Label(
            text = '0',
            size_hint_x = 5
            ))
        self.prevInjuriesSliderGrid.add_widget(self.prevInjuriesSlider)
        self.prevInjuriesSliderGrid.add_widget(Label(
            text = '15',
            size_hint_x = 5
            ))
        
        # Roll Modifier
        self.modLabel = Label(
            text = "Roll Modifier"
            )
        self.modSlider = Slider(
            range = (-150,150),
            step = 5,
            value = 0,
            size_hint_x = 90
            )
        self.modReadout = Label(
            text = "[b]" + str(int(self.modSlider.value)) + "[/b]",
            markup = True
            )
            
        self.modSliderGrid = GridLayout(
            cols = 3,
            spacing = 12
            )
        
        self.modSliderGrid.add_widget(Label(
            text = '-150',
            size_hint_x = 5
            ))
        self.modSliderGrid.add_widget(self.modSlider)
        self.modSliderGrid.add_widget(Label(
            text = '150',
            size_hint_x = 5
            ))
        
        # Right Half is Reset and Roll Buttons
        self.buttonContainer = GridLayout(
            cols = 1,
            padding = 20,
            spacing = 20,
            size_hint_x = 25
            )
        
        self.resetButton = Button(
            text = "Reset",
            on_press = self.reset,
            size_hint_y = 30
            )
        
        self.rollButton = Button(
            text = "Roll",
            on_press = self.roll,
            size_hint_y = 70
            )
        
        # Add all widgets
        for widget in (
            self.prevInjuriesLabel,
            self.prevInjuriesSliderGrid,
            self.prevInjuriesReadout,
            self.modLabel,
            self.modSliderGrid,
            self.modReadout
            ):
            self.sliders.add_widget(widget)
        
        self.add_widget(self.sliders)
        self.add_widget(self.buttonContainer)
        self.buttonContainer.add_widget(self.resetButton)
        self.buttonContainer.add_widget(self.rollButton)
        
        # Binds for Bg Color
        self.bind(
            size = self._update_bg,
            pos = self._update_bg
            )
        
        # Binds for Slide values
        self.prevInjuriesSlider.bind(
            value = self._update_slider_readouts
            )
        
        self.modSlider.bind(
            value = self._update_slider_readouts
            )
        
        # BG Color
        with self.canvas.before:
            Color(.033, .149, .202)
            self.bg = Rectangle(
                size = self.size,
                pos = self.pos
                )
    
    def roll(self, ignore=''):
        self.parent.resultBox.roll()
    
    def reset(self, ignore=''):
        self.prevInjuriesSlider.value = 0
        self.modSlider.value = 0
        self._update_slider_readouts()
    
    def _update_bg(self, instance, value):
        self.bg.size = instance.size
        self.bg.pos = instance.pos
    
    def _update_slider_readouts(self, instance='', value=''):
        self.sliders.remove_widget(self.prevInjuriesReadout)
        self.prevInjuriesReadout = Label(
            text = "[b]" + str(int(self.prevInjuriesSlider.value)) + "[/b]",
            markup = True
            )
        self.sliders.add_widget(self.prevInjuriesReadout, index = 3)
        self.sliders.remove_widget(self.modReadout)
        self.modReadout = Label(
            text = "[b]" + str(int(self.modSlider.value)) + "[/b]",
            markup = True
            )
        self.sliders.add_widget(self.modReadout, index = 0)
        

# ==============================================================================
# CRITICAL INJURY GUI
# ==============================================================================

class crit_UI(GridLayout):
    """Contains both the result box and the history view"""
    def __init__(self, **kwargs):
        super(crit_UI, self).__init__(**kwargs)
        self.rows = 3
        self.spacing = 10
        
        self.resultBox = crit_ResultBox(
            size_hint_y = 20
            )
        self.controls = crit_Controls(
            size_hint_y = 40
            )
        self.historyUI_Grid = GridLayout(
            cols = 3,
            size_hint_y = 40,
            )
        self.historyUI = crit_HistoryUI(
            size_hint_x = 96
            )
        self.historyUI_Grid.add_widget(Label(
            size_hint_x = 2
            ))
        self.historyUI_Grid.add_widget(self.historyUI)
        self.historyUI_Grid.add_widget(Label(
            size_hint_x = 2
            ))
        
        self.add_widget(self.controls)
        self.add_widget(self.resultBox)
        self.add_widget(self.historyUI_Grid)


if __name__ == '__main__':
    print "This module shoudl only be called from within another program"