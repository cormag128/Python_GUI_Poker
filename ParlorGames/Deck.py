# -*- coding: utf-8 -*-
"""
@author: tcw37
"""

#imports
from collections import deque
import random
import operator

#class that builds
class Card:

    #initialize a card when it is made
    def __init__(self, s, v):
        #card variables declarations
        self.suit = s
        self.value = v
        self.value = int(self.value)
        self.replaced = 0   #used only in terminal, obsoleted with GUI
        self.suitname = ""
        self.valuename = ""
        self.image = ""

        # give nicer suit
        if self.suit == 'c':
            self.suitname = "clubs"
        elif self.suit == 'd':
            self.suitname = "diamonds"
        elif self.suit == 'h':
            self.suitname = "hearts"
        elif self.suit == 's':
            self.suitname = "spades"
        else:
            self.suitname = "invalid"

        # give appropriate name
        if self.value == 1:
            self.valuename = "ace"
        elif self.value == 11:
            self.valuename = "jack"
        elif self.value == 12:
            self.valuename = "queen"
        elif self.value == 13:
            self.valuename = "king"
        else:
            self.valuename = self.value

        #set the cards image pathing
        self.image = "card/%s_of_%s.png" % (self.valuename, self.suitname)

#function to build the deck, takes in a deque
def builddeck(d):
    i = 1
    d.clear()

    # append hearts
    while i < 14:
        d.append(Card('h', i))
        i += 1

    i = 1

    # append diamonds
    while i < 14:
        d.append(Card('d', i))
        i += 1

    i = 1

    # append clubs
    while i < 14:
        d.append(Card('c', i))
        i += 1

    i = 1

    # append spades
    while i < 14:
        d.append(Card('s', i))
        i += 1


# function that shuffles the deck
def shuffledeck(d):
    random.shuffle(d)


# function that displays hand, used for terminal, obsolete for gui
def showhand(hand):
    g = 0
    while g < 5:
        print g, ": ", (hand[g].suitname, hand[g].valuename)
        g += 1


# function to replace a card
def replacecard(pos, hand, d):
    hand[pos] = d.pop()
    hand[pos].replaced = 1

#check for the handtype
def handtype(hand):
    g = 0
    h = 0
    j = 0
    k = 0
    l = 0
    found = 0
    count = 0
    str = ""

    #create a sorted version for checking straights
    temp = sorted(hand, key=operator.attrgetter('value'))

    #look for Royal flush
    if (hand[0].suit == hand[1].suit == hand[2].suit == hand[3].suit == hand[4].suit):
        if (temp[0].value == 1) & (temp[1].value == 10) & (temp[2].value == 11) & (temp[3].value == 12) & (temp[4].value == 13):
            return "Royal Flush"

    #look for straight flush
    if (hand[0].suit == hand[1].suit == hand[2].suit == hand[3].suit == hand[4].suit):
        if (temp[0].value == (temp[1].value - 1) == (temp[2].value - 2) == (temp[3].value - 3) == (temp[4].value - 4)):
            return "Straight Flush"


    #look for four of a kind
    g = 0
    while g < 5:
        h = 0
        while h < 5:
            j = 0
            while j < 5:
                k = 0
                while k < 5:
                    if (hand[g].value == hand[h].value == hand[j].value == hand[k].value) & (g != h) & (g != j) & (g != k) & (h != j) & (h != k) & (j != k):
                        return "4 of a kind"
                    k += 1
                j += 1
            h += 1
        g += 1
    #end of look for four of a kind

    #look for full house
    # look for 3 of a kind first (part of full house search)
    g = 0
    while g < 5:
        h = 0
        while h < 5:
            j = 0
            while j < 5:
                if (hand[g].value == hand[h].value) & (hand[h].value == hand[j].value) & (g != h) & (h != j) & (g != j):
                    found = hand[g].value
                j += 1
            h += 1
        g += 1

    # look for pair (part of full house search)
    if found != 0:
        g = 0
        while g < 5:
            h = 0
            while h < 5:
                if (hand[g].value == hand[h].value) & (g != h) & (hand[g].value != found):
                    return "Full House"
                h += 1
            g += 1
    #end of look for full house

    #look for flush
    if(hand[0].suit == hand[1].suit == hand[2].suit == hand[3].suit == hand[4].suit):
        return "Flush"
    #end of look for flush

    # look for straight
    if(temp[0].value == (temp[1].value - 1) == (temp[2].value - 2) == (temp[3].value - 3) == (temp[4].value - 4)):
        return "Straight"
    elif(temp[0].value == 1) & (temp[1].value == 10) & (temp[2].value == 11) & (temp[3].value == 12) & (temp[4].value == 13):
        return "Straight"
    # end of look for straight

    #look for 3 of a kind
    g = 0
    while g < 5:
        h=0
        while h < 5:
            j = 0
            while j < 5:
                if (hand[g].value == hand[h].value) & (hand[h].value == hand[j].value) & (g != h) & (h != j) & (g != j):
                    return "3 of a kind"
                j += 1
            h += 1
        g += 1
    #end of look for 3 of a kind

    #look for pair
    g = 0
    highval = 0
    count = 0
    while g < 5:
        h = 0
        while h < 5:
            if (hand[g].value == hand[h].value) & (g != h):
                count += 1
                if hand[g].value > highval:
                    highval = hand[g].value
                if hand[g].value == 1:
                    highval = 14
            h += 1
        g += 1

    #last if structure for returning remaining types
    if count == 4:
        return "2 Pair"
    elif ((count == 2) & (highval >= 11)):
        return "Pair Jacks+"
    else:
        return "High Card / Low Pair"
    #end of all looking

#define the function for giving a payout--
def payout(bet,handname):
    fpayout = 0
    bpayout = 0

    #set base payouts based on hand type
    if handname == "2 Pair":
        bpayout = 2
    elif handname == "Pair Jacks+":
        bpayout = 1
    elif handname == "3 of a kind":
        bpayout = 3
    elif handname == "Straight":
        bpayout = 4
    elif handname == "Flush":
        bpayout = 6
    elif handname == "Full House":
        bpayout = 9
    elif handname == "4 of a kind":
        bpayout = 25
    elif handname == "Straight Flush":
        bpayout = 50
    elif handname == "Royal Flush":
        bpayout = 250
    else:
        bpayout = -1

    #multiply payouts by the bet and return it
    fpayout = bpayout * bet
    fpayout = int(fpayout)
    return fpayout


# function for playing the game used only for terminal, does nothing in GUI
def playsingle(b):
    bank = b
    hand = []
    testhand = []
    d = deque('')
    handname = ""

    #build and shuffle deck
    builddeck(d)
    shuffledeck(d)

    while 1:
        bet = input("Enter an amount to bet (1-3): ")
        if bet <= 3:
            break

    #draw hand
    hand.append(d.pop())
    hand.append(d.pop())
    hand.append(d.pop())
    hand.append(d.pop())
    hand.append(d.pop())

    #show the player their hand
    showhand(hand)

    print "Handname: ",handtype(hand), " \n"

    #start replacing stuff, any number pushed is replaced, pushing 5 or higher ends replacing
    print("to mark a card for replacement, push that cards number,\nwhen done marking enter any other value\n")
    checker = 1
    while checker:
        decision = input("Enter Response: ")
        if decision < 5:
            if hand[decision].replaced == 0:
                replacecard(decision, hand, d)
            else:
                print "This card has already been replaced\n"
        else:
            #show new hand
            showhand(hand)
            print "Handname: ", handtype(hand), " \n"
            checker = 0

    #give payout here
    print "You won: %d \n" % (payout(bet, handtype(hand)))
    bank += payout(bet, handtype(hand))
    print "Your new bank is: %d \n" % (bank)

    return bank