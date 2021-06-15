# Copyright 2021 - 2xxx Jan "Lezalith" Mašek <lezalith@gmail.com>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
##############################################################################
#
# Hi there! So glad to see you!
#
# Welcome to my LezInventory, Inventory framework. 
# This code's purpose is to let other creators code an Inventory into their game(s),
# an Inventory that I think is easy to set up, to use, to customize and relatively to understand.
#
# I've tried to comment every piece of code in these files, so while some knowledge of
# Python classes will prove useful, an amateur should be able to get as far as an expert will.
#
##############################################################################
#
# First, I will tell you some basic functionalities, and where to find all of them.
# 
# 95% of all the functionality is found in the inventory_class.rpy file. As there is
# only one object that handles the whole Inventory, all of the functions are tied to it.
#
# Inventory is defined once, at the bottom of that file. It requires a single argument,
# a tuple that says how the Inventory Slots grid will look. It is required in the
# format of (width, height), and is taken from the InventorySettings class.
# Default inventory uses (3, 3), which means a 3x3 grid.
#
# After the Inventory is defined, we can use all the different functions/methods. 
# While they are used mainly by the Inventory screen, some you'll be using yourself, like:
# Inventory.add(), which adds an Item to the Inventory.
# Inventory.remove(), which removes an Item from the Inventory.
# Inventory.use(), Inventory.equip() or Inventory.unequip() which interact with Items
# Inventory.isInInventory(Item), to check whether Item is in the Inventory
# Inventory.getEquippedItem() or Inventory.isEquipped(Item) to see which Item is currently equipped
#
# Inventory.use(Item) can also be used to trigger an Item's effect, like if it was used by the Inventory.
#
# I think you should only need more of them if you decide to do big changes to the Inventory screen,
# but if that's up your alley, go for it. All the functions are documented as well as can be, 
# all in the inventory_class.rpy file.
#
###############################################################################
#
# Second, you should learn how to define some Items to place into your Inventory.
#
# As might be expected, that's kind of a big topic in itself, so if you want to
# learn how to do that (And you probably should, Items are kinda an important part
# of an Inventory), jump over to lezInv_items.rpy, in the docs folder.
#
# It's the same folder as this doc file is in, so you should've
# encountered it already!
#
################################################################################
#
# Finally, for the basic customization, visit two more files:
#
# inventory_screen.rpy
# On top of that file (all the way up until about half of the file) are all the styles
# used in the screen. They are commented so you know exactly what style controls what,
# and once you change something in the style, it will change on the Inventory screen.
# 
# The names are written logically, as they go deeper.
# If we take one of the complex examples...
# 
# inventory_ is a prefix all styles here have
# side_menu is a frame containing everything on the right side.
# vbox_interaction is a name I chose for the vbox containing most buttons.
# throwaway_textbutton finally points at the textbutton of "Throw Away".
# style inventory_side_menu_vbox_interaction_throwaway_textbutton
#
# The second file is inventory_settings.rpy
# This file has a InventorySettings class.
# No functions here, you won't be using this one yourselves at all.
#
# It is there to control some of the most basic things about the Inventory,
# for example how the Slots grid looks.
# Just open the file, read what the variables inside the class do, change what you need.  
#
################################################################################
#
# There you go! If you go through all of this, you should understand the basics of LezInventory.
#
# Well... All of it, hopefully. 
# I really tried my best to write this Inventory to be as simple but at the same time
# as powerful as can be. Hopefully I've achieved this.
#
# Do let me know of your experience on my Discord, "Lezalith (LezCave.com)#2853".
# I will always be happy to hear from you.
#
# Godspeed, pilgrim.
# (I randomly remembered this when I was writing this file for the first time.
# In my world, that quote is said by Josh, at the beginning of Until Dawn.)