# -*- coding: utf-8 -*-
"""
@author: tcw37
"""

#This program was for testing and works with terminal, it is now obsolte


import os
import Deck

#clear terminal
os.system('cls' if os.name == 'nt' else 'clear')

#declarations
correct = "n"
correct2  = "n"

#build menu and set up basic playing
while correct == "n":
    print ('Games\n -----------------------------------\n')
    print ('1. Poker')
    print ('2. Texas Holdem')

    decision = input("Enter Response: ")

    if decision == 1:
        correct = "y"
        print('\nPoker selected, pick play style:')

        while correct2 == "n":
            print ("1. Play by yourself")
            print ("2. Let a bot play")

            decision = input("Enter Response: ")

            if decision == 1:
                bank = 100
                while 1:
                    bank = Deck.playsingle(bank)
                    correct2 = "y"

                    again = raw_input("Play another hand? (y or n)")
                    if again == "n":
                        break

            elif decision == 2:
               correct2 = "y"
            else:
                print ("invalid reponse, try again\n")


    elif decision == 2:
        correct = "y"
        print('\nTexas Holdem selected,')

        Deck.playholdem(1000)

    else:
        print('invalid button pressed, try again')