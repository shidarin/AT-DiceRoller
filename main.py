#!/usr/bin/kivy
# AT Dice Roller
# Dice Roller with Critical Injuries and Force Die
#
# This script uses Kivy to build a GUI for setting up and rolling dice pools
# Provides functionality for setting pool from common pools
# Setting pools from the roll history
# Re-rolling the current pool
# Rolling critical injuries
# Rolling force pool
#
# By Sean Wallitsch, 2013/08/25

# ==============================================================================
# VERSION HISTORY
# ==============================================================================

# v1.0  Fully commented, fixed variable names, prepped for build
# v1.1  Rebuilt core dice section to use a class for dicePool
#       Added Critical Injuries
#       Added Force Dice
#       Offloaded everything into contained modules
#       Added dice by dice results
#       Slight Resolution Change

# ==============================================================================
# TO DO LIST
# ==============================================================================

# Allow users to save their own pools?
# Add About screen
# Two types of icon, one for App one for desktop?

# ==============================================================================
# Imports
# ==============================================================================

# Kivy Imports

from kivy.app import App # Base App Class
from kivy.graphics import Canvas, Color, Rectangle # For backgrounds
from kivy.uix.gridlayout import GridLayout
from kivy.uix.accordion import Accordion, AccordionItem

# Custom Modules

from modules.dice import dice_UI
from modules.criticalInjuries import crit_UI
from modules.forceDice import force_UI

# ==============================================================================
# Accordion Switcher
# ==============================================================================

class InjuryAndForceUI(GridLayout):
    """Top level UI"""
    def __init__(self, **kwargs):
        super(InjuryAndForceUI, self).__init__(**kwargs)
        self.cols = 2
        
        self.injury = crit_UI(
            size_hint_x = 70
            )
        self.force_dice = force_UI(
            size_hint_x = 30
            )
        
        self.add_widget(self.injury)
        self.add_widget(self.force_dice)

class ATDR(Accordion):
    def __init__(self, **kwargs):
        super(ATDR, self).__init__(**kwargs)
        self.orientation = "horizontal"
        
        # Accordion Items
        self.diceAcc = AccordionItem(
            title = "Dice Pools"
            )
        self.crit_forceAcc = AccordionItem(
            title = "Critical Injuries and Force Dice"
            )
        
        # Things inside of the Accordion Items
        self.dice = dice_UI()
        self.crit_force = InjuryAndForceUI()
        
        # Add interior items to Accordion Items
        self.diceAcc.add_widget(self.dice)
        self.crit_forceAcc.add_widget(self.crit_force)
        
        # Add Accordion Items
        self.add_widget(self.crit_forceAcc)
        self.add_widget(self.diceAcc)
    

# ==============================================================================
# App
# ==============================================================================

class ATDiceApp(App):
    """Main App, sets icon, name, and window size"""
    # These are high level variables
    icon = 'tex/diceIcon.png' # Set the App Icon
    title = 'AT-Dice Roller' # Set the Window Title
    
    def __init__(self, **kwargs):
        super(ATDiceApp, self).__init__(**kwargs)
        self.ui = ATDR()
    
    def on_start(self):
        # This is an undocumented way to set the window size on startup
        # Found at github: https://github.com/kivy/kivy/pull/577
        # Seems the Kivy team gave in over Tito's strong objections.
        # Thank God.
        self._app_window.size = 1200, 600
    
    def build(self):
        self.ui.bind(
            size = self._update_rect,
            pos = self._update_rect
            )
            
        # Set Canvas BG Color
        with self.ui.canvas.before:
            Color(.07,.07,.1)
            self.rect = Rectangle(
                size = self.ui.size,
                pos = self.ui.pos
                )
        return self.ui
    
    # Updates Canvas BG size and Pos
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
DiceApp = ATDiceApp()

if __name__ == "__main__":
    DiceApp.run()