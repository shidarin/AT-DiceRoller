#!/usr/bin/kivy
# Force Dice App Module
# By Sean Wallitsch, 2013/08/24

# Modules

from random import randrange

# Kivy Modules

from kivy.app import App # Base App Class
from kivy.uix.gridlayout import GridLayout # Only Using Grid Layouts
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.button import Button
from kivy.graphics import Canvas, Color, Rectangle # For backgrounds
from kivy.lang import Builder

#KV Style Section
Builder.load_string(
'''
<ForceSlider>:
    canvas:
        Clear:
        Color:
            rgb: 1, 1, 1
        BorderImage:
            border: (0, 18, 0, 18) if self.orientation == 'horizontal' else (18, 0, 18, 0)
            pos: (self.x + 7, self.center_y - 18) if self.orientation == 'horizontal' else (self.center_x - 18, self.y)
            size: (self.width*.92, 37) if self.orientation == 'horizontal' else (37, self.height)
            source: 'tex/slider%s_background.png' % self.orientation[0]
        Rectangle:
            pos: (self.value_pos[0] - 16, self.center_y - 15) if self.orientation == 'horizontal' else (self.center_x - 16, self.value_pos[1] - 16)
            size: (32, 32)
            source: 'tex/slider_cursor.png'

''')

# ==============================================================================
# AT GENERIC VARIABLES
# ==============================================================================

# Markup Shortcuts

SWF = "[font=fonts/sw_symbols.ttf]"
SWFC = "[/font]"


# ==============================================================================
# FUNCTIONS
# ==============================================================================

def force():
    """Rolls & interprets a d12 dice according to Force die"""
    roll = randrange(1,12)
    if roll in (1, 2, 3, 4, 5, 6):
        result = 'z'
    elif roll == 7:
        result = 'zz'
    elif roll in (8, 9):
        result = 'Z'
    elif roll in (10, 11, 12):
        result = 'ZZ'
    markup_result = '[b][size=32]' + SWF + result + SWFC + '[/size][/b]'
    return markup_result

# ==============================================================================
# GUI CLASSES
# ==============================================================================

class ForceSlider(Slider):
    def __init__(self, **kwargs):
        super(ForceSlider, self).__init__(**kwargs)
    pass

# ==============================================================================
# FORCE RESULTS
# ==============================================================================

class force_Results(GridLayout):
    """Result Display Area"""
    def __init__(self, **kwargs):
        super(force_Results, self).__init__(**kwargs)
        self.rows = 3
    
    def update(self):
        self.clear_widgets()
        for result in self.parent.controls.results:
            self.add_widget(Label(
                text = result,
                color = (0,0,0,1),
                markup = True,
                size_hint_x = 33,
                size_hint_y = 25
                ))

# ==============================================================================
# FORCE CONTROLS
# ==============================================================================

class force_Controls(GridLayout):
    """Controls for Force Dice"""
    def __init__(self, **kwargs):
        super(force_Controls, self).__init__(**kwargs)
        self.rows = 6
        self.spacing = 20
        self.padding = 20
        self.text_color = (.05, .05, .05, 1) # Need to invert due to light
        
        self.results = []
        
        self.forceDiceLabel = Label(
            text = '[size=20][color=222222][b]Force Dice[/b][/color][/size]',
            size_hint_y = 13,
            markup = True
            )
            
        # Slider Segment
        self.forceDiceSliderGrid = GridLayout(
            cols = 3,
            spacing = 4,
            size_hint_y = 15
            )
        self.forceDiceSlider = ForceSlider(
            range = (1,9),
            step = 1,
            value = 1,
            size_hint_x = 86
            )
        self.forceDiceMin = Label(
            text = '1',
            size_hint_x = 8,
            color = self.text_color
            )
        self.forceDiceMax = Label(
            text = '9',
            size_hint_x = 8,
            color = self.text_color
            )
        for widget in (
            self.forceDiceMin,
            self.forceDiceSlider,
            self.forceDiceMax
            ):
            self.forceDiceSliderGrid.add_widget(widget)
        
        self.forceDiceSlider.bind(
            value = self._update_value
            )
        
        # Readout
        self.forceDiceReadout = Label(
            text = "[b][size=18][color=222222]"\
                + str(int(self.forceDiceSlider.value))\
                + "[/color][/size][/b]",
            size_hint_y = 7,
            color = self.text_color,
            markup = True
            )
        
        # Blank Spacer
        self.forceDiceSpacer = Label(
            size_hint_y = 10
            )
        
        # Buttons
        self.forceDiceButtonGrid = GridLayout(
            cols = 2,
            size_hint_y = 30,
            spacing = 15,
            )
        self.forceDiceReset = Button(
            text = "Reset",
            size_hint_x = .25,
            on_press = self._reset
            )
        self.forceDiceRoll = Button(
            text = "Roll",
            size_hint_x = .75,
            on_press = self._roll
            )
        self.forceDiceButtonGrid.add_widget(self.forceDiceReset)
        self.forceDiceButtonGrid.add_widget(self.forceDiceRoll)
        
        self.resultTotal = Label(
            size_hint_y = 20
            )
        
        # Main Build
        for widget in (
            self.forceDiceLabel,
            self.forceDiceSliderGrid,
            self.forceDiceReadout,
            self.forceDiceSpacer,
            self.forceDiceButtonGrid,
            self.resultTotal
            ):
            
            self.add_widget(widget)
        
    def _update_value(self, instance='', value=''):
        self.remove_widget(self.forceDiceReadout)
        self.forceDiceReadout = Label(
            text = "[b][size=18]" + str(int(self.forceDiceSlider.value))\
                + "[/size][/b]",
            size_hint_y = 7,
            color = self.text_color,
            markup = True
            )
        self.add_widget(self.forceDiceReadout, index = 3)
    
    def _reset(self, instance):
        self.results = []
        self.forceDiceSlider.value = 1
        self._update_value()
        self._update_total()
        self.parent.results.update()
    
    def _roll(self, instance):
        self.results = []
        for dice in range(int(self.forceDiceSlider.value)):
            self.results.append(force())
        self.parent.results.update()
        self._update_total()
    
    def _update_total(self):
        self.remove_widget(self.resultTotal)
        if self.results:
            self.resultTotal = Label(
                text = self._get_total(),
                size_hint_y = 20,
                color = (0,0,0,1),
                markup = True
                )
        else:
            self.resultTotal = Label(
                size_hint_y = 20
                )
        self.add_widget(self.resultTotal)
    
    def _get_total(self):
        result_count = ''
        for result in self.results:
            result_count += result
        result_count = result_count.replace('[b][size=32]' + SWF, '')
        result_count = result_count.replace(SWFC + '[/size][/b]', '')
        light = result_count.count('Z')
        dark = result_count.count('z')
        if light > 0:
            lightstring = str(light) + SWF + 'Z' + SWFC
        else:
            lightstring = ''
        if dark > 0:
            darkstring = str(dark) + SWF + 'z' + SWFC
        else:
            darkstring = ''
        if dark > 0 and light > 0:
            connector = '     '
        else:
            connector = ''
        final_string = "[b][size=28]" + lightstring + connector\
            + darkstring + "[/size][/b]"
        return final_string

# ==============================================================================
# Force GUI
# ==============================================================================

class force_UI(GridLayout):
    def __init__(self, **kwargs):
        super(force_UI, self).__init__(**kwargs)
        self.rows = 2
        
        self.controls = force_Controls(
            size_hint_y = 50
            )
        self.results = force_Results(
            size_hint_y = 50
            )
        
        self.bind(
            size = self._update_bg,
            pos = self._update_bg
            )
        
        self.add_widget(self.controls)
        self.add_widget(self.results)
        
        with self.canvas.before:
            Color(.89, .87, .852)
            self.bg = Rectangle(
                size = self.size,
                pos = self.pos
                )
    
    def _update_bg(self, instance, value):
        self.bg.size = instance.size
        self.bg.pos = instance.pos

if __name__ == '__main__':
    print "Do not run this module directly!"