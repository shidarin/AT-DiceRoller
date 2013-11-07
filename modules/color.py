#!/usr/bin/python
# Color
# Some generic Color support Functions
# By Sean Wallitsch, 2013/08/18

# Functions

def rgb_to_linear(colorList, mult):
    """Takes a 0-255 rgb list or tuple and returns a 0-1 vec4"""
    new_colors = []
    for i in colorList:
        i = float(i)
        i = i / 255 * mult
        new_colors.append(i)
    new_colors.append(1)
    return new_colors

''' Below is from stack overflow: http://stackoverflow.com/questions/4296249/how-do-i-convert-a-hex-triplet-to-an-rgb-tuple-and-back '''

_NUMERALS = '0123456789abcdefABCDEF'
_HEXDEC = {v: int(v, 16) for v in (x+y for x in _NUMERALS for y in _NUMERALS)}
LOWERCASE, UPPERCASE = 'x', 'X'

def hex_to_rgb(triplet):
    """Takes a HEX and converts it to an RGB triplet tuple"""
    return (_HEXDEC[triplet[0:2]],\
            _HEXDEC[triplet[2:4]],\
            _HEXDEC[triplet[4:6]])

def rgb_to_hex(rgb, lettercase='x'):
    """Takes a RGB triplet tuple and converts it to a HEX"""
    return format((rgb[0]<<16 | rgb[1]<<8 | rgb[2]), '06'+lettercase)