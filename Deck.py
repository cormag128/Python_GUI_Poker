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
    size = len(hand)
    while g < size:
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
    size = len(hand)

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
    while g < size:
        h = 0
        while h < size:
            j = 0
            while j < size:
                k = 0
                while k < size:
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
    while g < size:
        h = 0
        while h < size:
            j = 0
            while j < size:
                if (hand[g].value == hand[h].value) & (hand[h].value == hand[j].value) & (g != h) & (h != j) & (g != j):
                    found = hand[g].value
                j += 1
            h += 1
        g += 1

    # look for pair (part of full house search)
    if found != 0:
        g = 0
        while g < size:
            h = 0
            while h < size:
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
    while g < size:
        h=0
        while h < size:
            j = 0
            while j < size:
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
    while g < size:
        h = 0
        while h < size:
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




#texas holdem specific stuff below
#                                #
#                                #
#                                #
#                                #
#                                #
#                                #
#                                #
#begin texas holdem specific code

#player class important to hold data
class player:
    def __init__(self):
        self.hand = []
        self.bank = 10000
        self.bet = 0
        self.turn = 0

class handvalue:
    def __init__(self):
        self.name = ''
        self.highvalue = 0
        self.handval = 0

#draw the starting hand for all players
def drawtexashand(d,human,ais):
    human.hand.append(d.pop())
    human.hand.append(d.pop())
    ais[0].hand.append(d.pop())
    ais[0].hand.append(d.pop())
    ais[1].hand.append(d.pop())
    ais[1].hand.append(d.pop())
    ais[2].hand.append(d.pop())
    ais[2].hand.append(d.pop())

# texas holdem starting bet, sets big and small starters
def startbidding(r,pot,human,ais):
    if r % 4 == 0:
        human.bank -= 100
        ais[0].bank -= 50
        human.bet = 100
        ais[0].bet = 50
        pot = 150
    elif r % 4 == 1:
        ais[0].bank -= 100
        ais[1].bank -= 50
        ais[0].bet = 100
        ais[1].bet = 50
        pot = 150
    elif r % 4 == 2:
        ais[1].bank -= 100
        ais[2].bank -= 50
        ais[1].bet = 100
        ais[2].bet = 50
        pot = 150
    elif r % 4 == 3:
        ais[2].bank -= 100
        human.bank -= 50
        ais[2].bet = 100
        human.bet = 50
        pot = 150
    return pot

# draw from the river and place the shadow cards in the players hands
def drawtoriver(d,river,human,ais):
    if len(river) == 0:
        river.append(d.pop())
        river.append(d.pop())
        river.append(d.pop())

        human.hand.append(river[0])
        human.hand.append(river[1])
        human.hand.append(river[2])

        ais[0].hand.append(river[0])
        ais[0].hand.append(river[1])
        ais[0].hand.append(river[2])

        ais[1].hand.append(river[0])
        ais[1].hand.append(river[1])
        ais[1].hand.append(river[2])

        ais[2].hand.append(river[0])
        ais[2].hand.append(river[1])
        ais[2].hand.append(river[2])

    elif len(river) == 3:
        river.append(d.pop())

        human.hand.append(river[3])
        ais[0].hand.append(river[3])
        ais[1].hand.append(river[3])
        ais[2].hand.append(river[3])
    else:
        river.append(d.pop())

        human.hand.append(river[4])
        ais[0].hand.append(river[4])
        ais[1].hand.append(river[4])
        ais[2].hand.append(river[4])

#function to set the values of aces to 14 when looking at high cards
def highaces(hand,handtype):
    if hand[0].value == 1:
        handtype.highcard = 14
    else:
        pass

# check for the handtype, returns more info
def texhandtype(hand):
    g = 0
    h = 0
    j = 0
    k = 0
    l = 0
    handdata = handvalue()
    found = 0
    count = 0
    str = ""
    size = len(hand)

    # create a sorted version for checking straights
    temp = sorted(hand, key=operator.attrgetter('value'))
    handdata.highcard = temp[len(hand)-1].value
    highaces(temp,handdata)

    if(len(hand) > 2):
        # look for Royal flush
        if (temp[0].suit == temp[len(hand) - 4].suit == temp[len(hand) - 3].suit == temp[len(hand) - 2].suit == temp[len(hand) - 1].suit):
            if (temp[0].value == 1) & (temp[len(hand) - 4].value == 10) & (temp[len(hand) - 3].value == 11) & (temp[len(hand) - 2].value == 12) & (
                temp[len(hand) - 1].value == 13):
                handdata.name = "Royal Flush"
                handdata.handval = 13
                return handdata

        # look for straight flush
        g=0
        while g < len(hand) % 4:
            if (temp[g].suit == temp[g+1].suit == temp[g+2].suit == temp[g+3].suit == temp[g+4].suit):
                if (temp[g].value == (temp[g+1].value - 1) == (temp[g+2].value - 2) == (temp[g+3].value - 3) == (
                    temp[g+4].value - 4)):
                    handdata.name = "Straight Flush"
                    handdata.handval = temp[4].value
                    return handdata
            g += 1

        # look for four of a kind
        g = 0
        while g < size:
            h = 0
            while h < size:
                j = 0
                while j < size:
                    k = 0
                    while k < size:
                        if (hand[g].value == hand[h].value == hand[j].value == hand[k].value) & (g != h) & (g != j) & (
                            g != k) & (h != j) & (h != k) & (j != k):
                            handdata.name = "4 of a kind"
                            handdata.handval = hand[h].value
                            return handdata
                        k += 1
                    j += 1
                h += 1
            g += 1
        # end of look for four of a kind

        # look for full house
        # look for 3 of a kind first (part of full house search)
        g = 0
        while g < size:
            h = 0
            while h < size:
                j = 0
                while j < size:
                    if (hand[g].value == hand[h].value) & (hand[h].value == hand[j].value) & (g != h) & (h != j) & (
                        g != j):
                        handdata.handval = hand[g].value
                        found = hand[g].value
                    j += 1
                h += 1
            g += 1

        # look for pair (part of full house search)
        if found != 0:
            g = 0
            while g < size:
                h = 0
                while h < size:
                    if (hand[g].value == hand[h].value) & (g != h) & (hand[g].value != found):
                        handdata.name = "Full House"
                        return handdata
                    h += 1
                g += 1
        # end of look for full house

        # look for flush
        g = 0
        numc = 0
        numh = 0
        numd = 0
        nums = 0
        while g < size:
            if hand[g].suit == 'c':
                numc += 1
            elif hand[g].suit == 's':
                nums += 1
            elif hand[g].suit == 'h':
                numh += 1
            elif hand[g].suit == 'd':
                numd += 1

            if numc >= 5 or numd >= 5 or nums >= 5 or numh >= 5:
                handdata.name = "Flush"
                handdata.handval = temp[size-1].value
                return handdata
            g += 1
            # end of look for flush

        # look for straight

        g = 0
        while g < len(hand) % 4:
            if (temp[g].value == (temp[g+1].value - 1) == (temp[g+2].value - 2) == (temp[g+3].value - 3) == (temp[g+4].value - 4)):
                handdata.name = "Straight"
                handdata.handval = temp[4].value
                return handdata
            elif ((temp[0].value == 1) & (temp[g].value == 10) & (temp[g+1].value == 11) & (temp[g+2].value == 12) & (temp[g+3].value == 13)):
                handdata.name = "Straight"
                handdata.handval = temp[4].value
                return handdata
            g += 1
        # end of look for straight

        # look for 3 of a kind
        g = 0
        while g < size:
            h = 0
            while h < size:
                j = 0
                while j < size:
                    if (hand[g].value == hand[h].value) & (hand[h].value == hand[j].value) & (g != h) & (h != j) & (
                        g != j):
                        handdata.name = "3 of a kind"
                        handdata.handval = hand[g].value
                        return handdata
                    j += 1
                h += 1
            g += 1
        # end of look for 3 of a kind

        # look for pair
        g = 0
        highval = 0
        count = 0
        while g < size:
            h = 0
            while h < size:
                if (hand[g].value == hand[h].value) & (g != h):
                    count += 1
                    if hand[g].value > highval:
                        handdata.handval = hand[g].value
                        highval = hand[g].value
                    if hand[g].value == 1:
                        highval = 14
                h += 1
            g += 1

        # last if structure for returning remaining types
        if count == 4:
            handdata.name = "2 Pair"
            return handdata
        elif (count == 2):
            handdata.name = "Pair"
            return handdata
        else:
            handdata.name = "High Card"
            return handdata
            # end of all looking

    #otherwise we have 2 cards so look only for pair
    else:
        if temp[0].value == temp[1].value:
            handdata.name = "Pair"
            return handdata
        else:
            handdata.name = "High Card"
        return handdata

def humanbet(human, roundpot, pot):
    while 1:
        print("Press 1 to call/check or 2 to raise, if you call/check you will bet %d" % (roundpot-human.bet))
        print("Current pot: %d" % (pot))

        decision = input("Response: ")

        if decision == 1:
            if human.bet == roundpot:
                humancheck()
                return
            else:
                humancall()
                return

def humancheck(human,roundpot,pot):
    pass

def humancall(human,roundpot,pot):
    human.bank -= (roundpot - human.bet)
    human.bet = roundpot

def humanraise(human,roundpot,pot):
    pass

# function for playing holdem
def playholdem(b):
    human = player()
    river = []
    d = deque('')
    ais = []
    handtypes = []
    ais.append(player())
    ais.append(player())
    ais.append(player())

    round = 3
    pot = 0
    roundpot = 100

    builddeck(d)
    shuffledeck(d)

    pot = startbidding(round,pot,human,ais)

    drawtexashand(d,human,ais)

    while (human.bet < roundpot or ais[0].bet < roundpot or ais[1].bet < roundpot or ais[2].bet < roundpot):
        humanbet(human,roundpot,pot)
    drawtoriver(d,river,human,ais)

    handtypes.append(texhandtype(human.hand))
    handtypes.append(texhandtype(ais[0].hand))
    handtypes.append(texhandtype(ais[1].hand))
    handtypes.append(texhandtype(ais[2].hand))

    showhand(human.hand)
    print(handtypes[0].name)
    print"---------------------\n"