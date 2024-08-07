transform my_size():
    size (240, 240)

image side lezalith = At("gui/myself.jpeg", my_size)
define lez = Character("Lezalith", image = "lezalith")

init -1 python:
    def copy_text(text, notice):

        import pygame.scrap
       
        pygame.scrap.put(pygame.scrap.SCRAP_TEXT, text.encode("utf-8"))

        renpy.notify(notice)

screen main_menu():

    use quick_menu

    tag main

    add gui.main_menu_background

    frame:
        align (0.5, 0.5)
        xysize (1800, 900)
        ypadding 75

        add "gui/myself.jpeg" xalign 1.0 size (200, 200) offset (-15, -60)

        vbox:
            xalign 0.5
            yoffset -40
            spacing 35

            vbox:
                xalign 0.5
                spacing 4

                text "LezInventory" xalign 0.5 size 72
                add Solid("000") size (700, 3) xalign 0.5
                text "Inventory Framework by Lezalith" xalign 0.5 

            vbox:
                
                spacing 40

                vbox:
                    xalign 0.5
                    spacing 2
                    text "Welcome to LezInventory!" xalign 0.5
                    text "An Inventory framework that I hope will be of use to many creators."

                hbox:
                    xalign 0.5
                    spacing 80

                    textbutton "What is LezInventory?" yalign 0.5 action Show("desc")

                    textbutton "How do I set it up?" yalign 0.5 action Show("info")

                text "You can try LezInventory by clicking one of the buttons below." xalign 0.5

                hbox:
                    spacing 150
                    xalign 0.5

                    textbutton "Enter from a screen.":
                        yalign 0.5
                        action Show("from_screen")

                    textbutton "Enter from a label.":
                        yalign 0.5
                        action Start("from_label")


                vbox:
                    xalign 0.5
                    spacing -5

                    text "What Example Items do you want in the preview?" size 26 xalign 0.5

                    textbutton "Basic ones, that show simplicity." xalign 0.5 action SetVariable("add_which_items", "basic") text_size 26 text_selected_color "ff6242"
                    textbutton "Advanced ones, that show off what LezInventory can do." xalign 0.5 action SetVariable("add_which_items", "advanced") text_size 26 text_selected_color "ff6242"
                    textbutton "ALL THE ITEMS!" xalign 0.5 action SetVariable("add_which_items", "both") text_size 26 text_selected_color "ff6242"

                vbox:
                    xalign 0.5
                    yalign 1.0
                    text "And here, you can click to copy my Discord, let me know how you've liked my work."

                    textbutton "Lezalith (LezCave.com)#2853" xalign 0.5 action Function(copy_text, text = "Lezalith (LezCave.com)#2853", notice = "Lez's Discord copied to clipboard!")

screen info():

    modal True

    add gui.main_menu_background

    frame:
        align (0.5, 0.5)
        xysize (1800, 800)
        ypadding 120

        add "gui/myself.jpeg" xalign 1.0 size (120, 120) offset (-10, -110)

        vbox:
            xalign 0.5
            spacing 50

            # text "Sorry, this is just a preview! The code will be out soon!"

            vbox:
                spacing 5
                text "To insert LezInventory into your project, all you need is to copy the \"lezInventory\" folder from one of this project's releases into your game folder." 
                text "You can find releases on the right side of the GitHub page, under \"Releases\"."

            vbox:
                spacing 5
                text "If you desire, you can delete the \"example_items\" folder inside, but they serve as amazing guidance. All of them are described in the documentation."

            vbox:
                spacing 5
                text "It is basically the clean canvas for you to grab if you want to use this inventory yourselves."
                text "If you do, be sure to check out the \"lezInv_startup.rpy\" file in the lezInventory/docs folder first."
                text "All of the code is commented as much as it can be, feel free to customize anything you want."

            text "Good luck!! :)"

        textbutton "Back to the menu!" align (0.5, 1.0) yoffset -10 action Hide("info")

style desc_style_text:
    size 28

screen desc():

    modal True

    add gui.main_menu_background

    frame:
        align (0.5, 0.5)
        xysize (1850, 800)
        ypadding 120

        add "gui/myself.jpeg" xalign 1.0 size (120, 120) offset (-10, -110)

        vbox:

            style_prefix "desc_style"

            xalign 0.5
            spacing 50

            vbox:
                spacing 3
                text "LezInventory is a framework that I've put together in about three weeks."
                text "In case you don't know me, my name is Lezalith, Lez for short, and I've been coding in Ren'Py for about 7 years."

            vbox:
                spacing 3
                text "Framework is a code that you can take and use yourselves. In my case it means a working Inventory."
                text "LezInventory is easy to use, customize and modify. It is flexible and does all the basics."
                text "It supports regular items, as well as equippable and usable ones. For the equippables, it has one equip slot."
                text "What's more, items are very easy to create."

            vbox:
                spacing 3
                text "There are defined styles for every piece of graphics in the Inventory."
                text "Styles are used to customize default Ren'Py projects, too, making things easier for those who use them."

            vbox:
                spacing 3
                text "The point of this Inventory is to provide game creators with a modern Inventory."
                text "An Inventory that let's them move forward with their projects, even better, help them make the whole game better."
                text "It is up to you to decide whether I've succeeded."


        textbutton "Back to the menu!" align (0.5, 1.0) yoffset 70 action Hide("desc")


screen from_screen():

    tag main
    modal True

    frame:
        align (0.5, 0.5)
        padding (100, 100)

        vbox:
            spacing 2
            first_spacing 20

            add "gui/myself.jpeg" xalign 0.5 size (250, 250) yoffset -50

            text "Sorry, didn't want to drop you into the Inventory straight away."
            text "Click the button below to enter it." xalign 0.5
            text "I sincerely hope you'll enjoy!" xalign 0.5
            text ""
            textbutton "Woosh!" action Function(reset_inventory), Show("quick_menu"), Show("inventory_screen", how_to_leave = "both"), Hide("from_screen") xalign 0.5

label from_label():

    $ reset_inventory()

    show screen quick_menu

    lez "This is a line of dialogue to show you we are inside a label.\nFeel free to play around with the Inventory, you'll end up back in this label when you click Return!"

    show screen quick_menu

    call screen inventory_screen

    lez "Welcome back to the label! I hope you've enjoyed :)"

    return