#!/usr/bin/python
# Star Wars Dice Module
# Contains a variety of dice related tools
# By Sean Wallitsch, 2013/08/18

# Imports

import random

# Functions

def dice_roll(sides=6, dice=1):
    """Rolls a (sides) die (dice) times and returns a list"""
    rolls = []
    for i in range(dice):
        rolls.append(random.randrange(sides) + 1)
    return rolls

def dice_boost(dice):
    """Rolls & interprets d6 dice according to Boost die"""
    rolls = dice_roll(6, dice)
    success = 0
    advantage = 0
    for i in rolls:
        if i == 3:
            success += 1
        elif i == 4:
            success += 1
            advantage += 1
        elif i == 5:
            advantage += 2
        elif i == 6:
            advantage += 1
    return success, advantage
    
def dice_setback(dice):
    """Rolls & interprets d6 dice according to Setback die"""
    rolls = dice_roll(6, dice)
    failure = 0
    threat = 0
    for i in rolls:
        if i in (3, 4):
            failure += 1
        elif i in (5, 6):
            threat += 1
    return failure, threat

def dice_ability(dice):
    """Rolls & interprets d8 dice according to Ability die"""
    rolls = dice_roll(8, dice)
    success = 0
    advantage = 0
    for i in rolls:
        if i in (2, 3):
            success += 1
        elif i == 4:
            success += 2
        elif i in (5, 6):
            advantage += 1
        elif i == 7:
            success += 1
            advantage += 1
        elif i == 8:
            advantage += 2
    return success, advantage

def dice_difficulty(dice):
    """Rolls & interprets d8 dice according to Difficulty die"""
    rolls = dice_roll(8, dice)
    failure = 0
    threat = 0
    for i in rolls:
        if i == 2:
            failure += 1
        elif i == 3:
            failure += 2
        elif i in (4, 5, 6):
            threat += 1
        elif i == 7:
            threat += 2
        elif i == 8:
            failure += 1
            threat += 1
    return failure, threat

def dice_proficiency(dice):
    """Rolls & interprets d12 dice according to Proficiency die"""
    rolls = dice_roll(12, dice)
    success = 0
    advantage = 0
    triumph = 0
    for i in rolls:
        if i in (2, 3):
            success += 1
        elif i in (4, 5):
            success += 2
        elif i == 6:
            advantage += 1
        elif i in (7, 8, 9):
            success += 1
            advantage += 1
        elif i in (10, 11):
            advantage += 2
        elif i == 12:
            success += 1
            triumph += 1
    return success, advantage, triumph

def dice_challenge(dice):
    """Rolls & interprets d12 dice according to Challenge die"""
    rolls = dice_roll(12, dice)
    failure = 0
    threat = 0
    despair = 0
    for i in rolls:
        if i in (2, 3):
            failure += 1
        elif i in (4, 5):
            failure += 2
        elif i in (6, 7):
            threat += 1
        elif i in (8, 9):
            failure += 1
            threat += 1
        elif i in (10, 11):
            threat += 2
        elif i == 12:
            failure += 1
            despair += 1
    return failure, threat, despair
    
def dice_force(dice):
    """Rolls & interprets d12 dice according to Force die"""
    rolls = dice_roll(12, dice)
    light = 0
    dark = 0
    for i in rolls:
        if i in (1, 2, 3, 4, 5, 6):
            dark += 1
        elif i == 7:
            dark += 2
        elif i in (8, 9):
            light += 1
        elif i in (10, 11, 12):
            light += 2
    return light, dark

def add_dice(number, type):
    """Sends roll commands and updates results"""
    success = 0
    advantage = 0
    failure = 0
    threat = 0
    triumph = 0
    despair = 0
    if type == "ability":
        success, advantage = dice_ability(number)
        return type, number, success, advantage
    elif type == "proficiency":
        success, advantage, triumph = dice_proficiency(number)
        return type, number, success, advantage, triumph
    elif type == "boost":
        success, advantage = dice_boost(number)
        return type, number, success, advantage
    elif type == "difficulty":
        failure, threat = dice_difficulty(number)
        return type, number, failure, threat
    elif type == "challenge":
        failure, threat, despair = dice_challenge(number)
        return type, number, failure, threat, despair
    elif type == "setback":
        failure, threat = dice_setback(number)
        return type, number, failure, threat
    else:
        print "Error, unknown dice type"