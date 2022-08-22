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

init -900 python:

    # Holds the Inventory.
    from collections import OrderedDict

    ###########################################
    ###########################################
    #
    # InventoryObject Class
    #
    ###########################################
    ###########################################

    # InventoryObject uses Indexes. 
    # Indexes are counted from 0 rather than from 1.
    #
    # Index 0 in the inventory means 1st item, 
    # Index 1 second item, 2 third item and so on...
    # 
    # Same thing for pages. In here, page = 0 means the first page,
    # page 1 is the second, 2 is the third.
    # 
    # The ONLY time when this is not true is in the getPagesRepr method,
    # which gives you the "real" number rather than the index.
    # That is the one that should be used for printing purposes.

    class InventoryObject():

        "Inventory that holds all the items and manages them."

        def __init__(self):
 
            # Dictionary that notes the width and height of cells.
            # Doesn't have to be a dict, but I wanted to make it clear
            # when we want to get grid["width"] rather than grid[0].
            self.grid = {"width" : InventorySettings.grid[0], "height" : InventorySettings.grid[1]}

            # INDEX of the page that we're on.
            self.page = 0

            # OrderedDict. Keys are Item objects, Values are Ints representing a count.
            self.inventory = OrderedDict()

            # Currently selected Item (Key of self.inventory).
            self.selectedItem = None

            # Currently equipped Item (Key of self.inventory)
            self.equippedItem = None

        ##########################################
        ## Inventory - Add, Remove, Size Functions
        ##########################################

        # Adds an Item to inventory.
        def add(self, Item, count = 1):

            if Item.stackable:

                self.addItemCount(Item, count)

            self.inventory[Item] = count

        def addItemCount(self, Item, count = 1):

            if Item in self.inventory.keys():

                self.inventory[Item] += count

                if self.inventory[Item] >= Item.stackSize:
                    self.inventory[Item] = Item.stackSize

                return 

        # Removes an Item from the inventory.
        # If Item is not specified, it will remove the selected item.
        # If count is not 0 and the item is stackable, it will instead remove
        # the stacks, and only the Item if stacks go below 0.
        def remove(self, Item = None, count = 1):

            # Item not provided.
            # Attempting to use the SelectedItem instead.
            if Item == None:

                # Do nothing if nothing is selected
                if self.selectedItem == None:
                    return

                Item = self.selectedItem

            # Stackable Items
            if Item.stackable:

                self.removeItemCount(Item, count)

            # Unstackable Items
            else:

                # Unequip if this Item was equipped
                if Item == self.equippedItem:
                    self.unequip()

                # Unselect this item
                print("Unselected.")
                self.unselect()
                # Pop the noted Item index
                self.remove(Item)

                # If we try to remove it straight away before unselecting it,
                # the screen manages to render one more time, and throws
                # an error because it doesn't find the selected item
                # inside the inventory.

            # Check pages whether we don't have
            # (an) empty one(s) after the removal.
            self.checkPages()

        def removeItemCount(self, Item, count = 1):

            if not Item.stackable:
                raise Exception("Inventory.removeItemCount called with unstackable Item - {}".format(Item))

            print("Stackable")

            if Item in self.inventory.keys():

                print("Present")

                self.inventory[Item] -= count

                if self.inventory[Item] <= 0:

                    print("Went to 0")

                    # Make an exception, if the last item of the stack got removed.
                    if Item == self.equippedItem:
                        self.inventory[Item] = 1

                        print("Is Equippable")

                    else:

                        # Remove the Item from the inventory.
                        del self.inventory[Item]

                        # Unequip the Item if it's equipped.
                        if Item == self.getEquippedItem():

                            self.unequip()

                        # Unselect the Item if it's selected.
                        if Item == self.getSelectedItem():
                            self.unselect()

                # Check pages whether we don't have
                # (an) empty one(s) after the removal.
                self.checkPages()


        def getItemCount(self, Item):

            if not Item.stackable:

                return 1

            if Item in self.inventory.keys():

                return self.inventory[Item]

            return 0

        # Calculates how many cells on a page by doing
        # width * height of the grid.
        def getSize(self):

            return self.grid["width"] * self.grid["height"]

        # Clears the whole inventory.
        def clear(self):

            self.inventory = OrderedDict()
            self.equippedItem = None
            self.selectedItem = None
            self.page = 0

        ###################
        ## Page Functions
        ###################

        # Returns the index of the current page.
        def getCurrentPage(self):
            return self.page

        # Returns tuple of two ints - (Current Page INDEX, Final Page INDEX ).
        def getPages(self):

            # Calculate how many pages are there.
            lastPage = (len(self.inventory) - 1) // self.getSize()

            # A safe check. 
            if lastPage < 0:
                lastPage = 0

            # First is the current page index, second is the last page index.
            return ( self.page, lastPage )

        # Check pages whether we don't have (an) empty one(s)
        def checkPages(self):

            pages = self.getPages()

            if pages[0] > pages[1]:

                self.page = pages[1]

        # Moving up or down between pages. 1 goes up a page, -1 down a page.
        # You can move multiple pages, but it won't let you go to an empty one.
        def changePage(self, direction):

            # Check whether the move can be executed.
            if not self.canChangePage(direction):
                return None

            try:

                self.page += direction

            # Not given a number.
            except TypeError:
                raise Exception("changePage() got invalid direction.")


            # Finally, unselect whatever's selected.
            self.unselect()

        # Checks whether we can move between pages.
        # Moving is possible as long as we're not going past the first
        # or past the final page.
        def canChangePage(self, direction):

            # Only on one page - Cannot move anywhere.
            if self.getPages()[1] == 0:
                return False

            try:

                # Checks for going up.
                if direction > 0:

                    # Can move, unless it would lead us further than the last page.
                    if not (self.page + direction) > self.getPages()[1]:
                        return True

                # Checks for going down.
                elif direction < 0:

                    # Can move, unless we're on the first page.
                    if self.page > 0:
                        return True

            # Not given a number.
            except TypeError:
                raise Exception("changePage() got invalid direction.")

            # If we get here, it means the check did not pass.
            return False



        # Returns tuple of two ints - (Current Page, Final Page).
        # This shows the page indexes when counting from 1 rather than 0.
        def getPagesRepr(self):

            firstPage, lastPage = self.getPages()

            return (firstPage + 1, lastPage + 1)

        ####################################
        ## Calculation with Slots
        ####################################

        # Gets an index from a slot on a page, with the help of the page index.
        #
        # For example:
        # Giving it slot 5 while on page 1 will return index 14.
        # (With the default grid size of 9.)
        #
        # Converted from indexes to "real" numbers:
        # Giving it 6th item on 2nd page will return 15th item.
        def getFlattenedSlot(self, slot):

            # The last index in the whole Inventory.
            lastIndex = len( self.getAllItems() ) - 1

            # Check if the slot is valid.
            # For a slot to be valid, it has to be within one page,
            # and it must not point onto an empty slot.

            if slot > self.getSize() or slot > lastIndex:
                return None
            
            # Returns the slot index.
            return ( self.page * self.getSize() + slot )

        # # Compares whether slot from a page matches what is currently selected.
        # def compareFlattenedSlotToSelected(self, slot):
        #     return ( self.getFlattenedSlot(slot) == self.selectedSlot )

        # # Compares whether slot from a page matches what is currently equipped.
        # def compareFlattenedSlotToEquipped(self, slot):
        #     return ( self.getFlattenedSlot(slot) == self.equippedSlot )

        ####################################################################
        ## Selection of Items
        ####################################################################

        # Unselects selected item.
        def unselect(self):

            self.selectedItem = None

        # Handles selecting items.
        # This is the Function on Item Slot's button.
        def selectToggle(self, Item):

            # If clicked an already selected slot
            if self.selectedItem == Item:

                # Unselect it, and by that end this function.
                return self.unselect()

            # Any other slot clicked

            # Set it to the index gotten from the flattened slot.
            self.selectedItem = Item

        # Returns currently selected Item.
        def getSelectedItem(self):

            return self.selectedItem

        ###############################
        ## Calculations with Items
        ###############################

        # Returns Items from the current page.
        def getPageItems(self):

            # bottomLimitIndex is the Index of the first item on the page.
            # Simply put, it's 0 on page 0, 8 on page 1, 17 on page 2 etc...
            bottomLimitIndex = self.page * self.getSize()

            # topLimitIndex is the last possible index that can be included in the slice.
            # Slicing past the last index throws an IndexError.
            # Usually, the topLimitIndex is just the size of a page...
            topLimitIndex = self.page * self.getSize() + self.getSize()

            # ...Unless the page is not full, which can happen only on the last page.
            # That means it will only get the remaining items. 
            if topLimitIndex > len(self.inventory.keys()) - 1:
                topLimitIndex = len(self.inventory.keys()) - 1 + 1

            # Returns Items between bottomLimitIndex and topLimitIndex.
            #
            # For example:
            # On a full page with index 1, the slice is [9 : 18].
            # (Returns indexes 10 to 18 due to slice rules.)
            #
            # Another example:
            # On the last page with index 2 that has 4 items, 
            # the slice is [18 : 22], indexes 19, 20, 21 and 22.
            return self.inventory.keys()[ bottomLimitIndex : topLimitIndex ]

        # Returns ALL Items from the Inventory.
        def getAllItems(self):

            return self.inventory

        # Takes the amount of Items on the current page and calculates
        # how many slots on the page will be empty.
        def getEmptyCells(self):

            # Get the current and the last page.
            pages = self.getPages()

            # Unless this is the only page...
            if not pages[0] == 0:

                # ...only the last page can be not full.
                # As such, we can ignore other pages:
                if pages[0] != pages[1]:
                    return 0

            # Otherwise:
            return self.getSize() - len( self.getPageItems() )

        # Returns the Item object on the given slot.
        def getItemFromSlot(slot):

            # Checks whether index doesn't exceed the inventory.
            # -1 at the end because len() gives length, we need the last index.
            if not slot > len( self.getAllItems() ) - 1:

                return self.inventory[slot] 

            # Returns None otherwise.
            return None

        # Returns the Item object on the given flattened slot.
        def getItemFromFlattenedSlot(slot):

            # Get non-flatted version first
            slot = self.getFlattenedSlot(slot)

            # Check if the item exists.
            # Checks whether index doesn't exceed one page.
            if not slot > self.getSize():

                # Checks whether index doesn't exceed the inventory.
                # -1 at the end because len() gives length, we need the last index.
                if not slot > len( self.getAllItems() ) - 1:

                    return self.inventory[ slot ]

            # Returns None otherwise.
            return None

        ###############################
        ## Equipping and Using of Items
        ###############################

        # Equip currently selected item.
        # TODO: Add the Item argument, for specified Item rather than selected.
        def equip(self):

            # Do nothing if nothing is selected.
            if not self.selectedItem:
                return

            # Something was already equipped
            if self.equippedItem != None:

                # Unequip it first.
                self.unequip()

            # Call Item's equipped() method.
            self.selectedItem.equipped(self)

            self.equippedItem = self.selectedItem

        # Unequip currently equipped item.
        def unequip(self):

            # Do nothing if nothing is equipped.
            if self.equippedItem == None:
                return

            # Call Item's unequipped() method.
            self.equippedItem.unequipped(self)

            self.equippedItem = None

        # Returns currently equipped Item
        def getEquippedItem(self):
            return self.equippedItem

        # By default, use the currently selected item.
        #
        # Specified Item can be provided, in which case its effect is triggered
        # like if it was used by the player. For this, it doesn't even have to be in the Inventory.
        def use(self, specified = None):

            if specified:
                return specified.used(self)

            # Call Item's used() method.
            self.selectedItem.used(self)

            # An extra check whether an Item is still selected, in case
            # the Item changed it. Guava from the project is a great example.
            if self.selectedItem:

                # Remove the Item if it's supposed to be consumed.
                if self.selectedItem.consumedOnUse:

                    # Remove the Item from the Inventory.
                    self.remove()

        #####################################
        ## Checks
        #####################################

        # Whether currently normalized slot is the one selected.
        # Same functionality as compareFlattenedSlotToSelected but with friendly name.
        def isSelected(self, Item):
            
            return self.selectedItem == Item

        # Whether currently normalized slot is the one equipped.
        # Same functionality as compareFlattenedSlotToEquipped but with friendly name.
        def isEquipped(self, Item):
            
            return self.equippedItem == Item

        # Intended for a button on a screen.
        # Whether the Unequip button can be used.
        # It can be used only when the selectedSlot is the same as equippedSlot.
        def canUnequip(self):

            # There's an extra check for selectedSlot not None, because
            # when nothing is selected/equipped, selectedSlot/equippedSlot take the value of None.
            return ( self.selectedItem == self.equippedItem )

        # Intended for a button on a screen.
        # Whether the Equip button can be used.
        # It can be used if the selectedSlot Item is Equippable.
        def canEquip(self):

            # If an Item is selected.
            if self.selectedItem != None:
                return self.selectedItem.isEquippable()

            # If an Item isn't selected.
            return False 

        # Indended for a button on a screen.
        # Whether the Use button can be used.
        # It can be used if the selectedSlot Item is Usable.
        def canUse(self):

            # If an Item is selected.
            if self.selectedItem != None:
                return self.getSelectedItem().isUsable()

            # If an Item isn't selected.
            return False 

        #---------------------------------
        # Following Checks aren't used anywhere myself, but should prove useful to coders.
        #---------------------------------

        # Returns True if item is present somewhere in the Inventory, False otherwise.
        def isInInventory(self, item):

            return item in self.inventory

        # Returns True if the item is selected, False otherwise.
        # Checks for Item, rather than a Slot like .isSelected()  
        def isItemSelected(self, item):

            return item == self.getSelectedItem()

        # Returns True if item is equipped, False otherwise.
        # Checks for Item, rather than a Slot like .isEquipped()
        def isItemEquipped(self, item):

            return item == self.getEquippedItem()

init -850:

    # Default of the Inventory.
    default Inventory = InventoryObject()