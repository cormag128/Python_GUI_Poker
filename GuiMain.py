# -*- coding: utf-8 -*-
"""
@author: tcw37
"""

#imports
import Deck
from collections import deque
from Tkinter import *
from PIL import ImageTk
import operator


#class for the gui
class parlorapp(Tk):

    #import variables
    bank = 100
    alreadybet = 0
    alreadyrep = 0
    hand = []
    testhand = []
    d = deque('')
    handname = ""

    #init function
    def __init__(self,parent):
        Tk.__init__(self,parent,)
        self.parent = parent
        self.initialize()

    #initialization of the game
    def initialize(self):

        #build a grid and make it un resizable
        self.grid()
        self.resizable(False,False)

        #entry box for betting
        self.entry = Entry(self)
        self.entry.grid(column=2,row=0,sticky='EW')

        # display the hand
        def displayhand():
            #canvases to place card on
            canvas0 = Canvas(self, bg="#228B22", width=300, height=400, bd=1, highlightbackground="black")
            canvas0.grid(column=0, row=1)

            canvas1 = Canvas(self, bg="#228B22", width=300, height=400, bd=1, highlightbackground="black")
            canvas1.grid(column=1, row=1)

            canvas2 = Canvas(self, bg="#228B22", width=300, height=400, bd=1, highlightbackground="black")
            canvas2.grid(column=2, row=1)

            canvas3 = Canvas(self, bg="#228B22", width=300, height=400, bd=1, highlightbackground="black")
            canvas3.grid(column=3, row=1)

            canvas4 = Canvas(self, bg="#228B22", width=300, height=400, bd=1, highlightbackground="black")
            canvas4.grid(column=4, row=1)

            #place card images onto the canvases
            cimage0 = ImageTk.PhotoImage(file=self.hand[0].image)
            canvas0.image = cimage0
            canvas0.create_image(150, 200, image=cimage0, )

            cimage1 = ImageTk.PhotoImage(file=self.hand[1].image)
            canvas1.image = cimage1
            canvas1.create_image(150, 200, image=cimage1)

            cimage2 = ImageTk.PhotoImage(file=self.hand[2].image)
            canvas2.image = cimage2
            canvas2.create_image(150, 200, image=cimage2)

            cimage3 = ImageTk.PhotoImage(file=self.hand[3].image)
            canvas3.image = cimage3
            canvas3.create_image(150, 200, image=cimage3)

            cimage4 = ImageTk.PhotoImage(file=self.hand[4].image)
            canvas4.image = cimage4
            canvas4.create_image(150, 200, image=cimage4)

        #funtion for the ai playing the game
        def aiplay():
            self.hand = []
            self.handname = ""

            #build and shuffle tghe deck
            Deck.builddeck(self.d)
            Deck.shuffledeck(self.d)

            #we'll just have the bot always bet 1 for now
            self.bet = 1
            self.bet = int(self.bet)

            #draw the bots hand
            self.hand.append(self.d.pop())
            self.hand.append(self.d.pop())
            self.hand.append(self.d.pop())
            self.hand.append(self.d.pop())
            self.hand.append(self.d.pop())

            #display the bank and make it possible to update
            self.bankvariable = StringVar()
            bankdisplay = Label(self, textvariable=self.bankvariable)
            self.bankvariable.set("Bank: %s" % (self.bank))
            bankdisplay.grid(column=0, row=0)

            #display the bots hand
            displayhand()

            #Tell the player what the bot's hand is
            self.labelvariable = StringVar()
            handlabel = Label(self, textvariable=self.labelvariable, bg="#228B22", width=35)
            handlabel.grid(column=1, row=0)
            self.labelvariable.set("Current Hand: %s" % (Deck.handtype(self.hand)))
            self.handname = Deck.handtype(self.hand)

            #make the AI do stuff
            holdval1 = 0
            holdval2 = 0
            hcount = 0
            scount = 0
            dcount = 0
            ccount = 0

            #begin checking hands for the ai, and decide what it should replace
            #all of the ifs then pass are for hands its not advantageous to change
            if self.handname == "Royal Flush":
                pass
            elif self.handname == "Straight Flush":
                pass
            elif self.handname == "4 of a kind":
                pass
            elif self.handname == "Full House":
                pass
            elif self.handname == "Flush":
                pass
            elif self.handname == "Straight":
                pass
            #beginning of replacing stuff for 3 of a kind
            elif self.handname == "3 of a kind":
                g = 0
                while g < 5:
                    h = 0
                    while h < 5:
                        j = 0
                        while j < 5:
                            #this will check if we have 3 cards of the same, and if we do set the value for checking later
                            if (self.hand[g].value == self.hand[h].value) & (self.hand[h].value == self.hand[j].value) & (g != h) & (h != j) & (g != j):
                                holdval1 = self.hand[g].value
                            j += 1
                        h += 1
                    g += 1

                g = 0

                #find any card that doesn't make up the 3 of a kind and replace it
                while g < 5:
                    if self.hand[g].value != holdval1:
                        Deck.replacecard(g,self.hand,self.d)
                    g += 1
            #end of replacing stuff for 3 of a kind

            #replace for 2 pair
            elif self.handname == "2 Pair":
                g = 0
                while g < 5:
                    h = 0
                    while h < 5:
                        #get the values of the two pairs, if we have no pair, set the first, then set the second
                        if (self.hand[g].value == self.hand[h].value) & (g != h):
                            if holdval1 == 0:
                                holdval1 = self.hand[g].value
                            elif holdval1 == self.hand[g].value:
                                pass
                            else:
                                holdval2 = self.hand[g].value
                        h += 1
                    g += 1

                g=0

                #replace the card that isn't a part of the 2 pair
                while g < 5:
                    if (self.hand[g].value != holdval1) & (self.hand[g].value != holdval2):
                        Deck.replacecard(g,self.hand,self.d)
                    g += 1
            #end replace for 2 pair

            #replace for pair
            elif self.handname == "Pair Jacks+":
                g = 0
                while g < 5:
                    h = 0
                    while h < 5:
                        #find the value of the pair
                        if (self.hand[g].value == self.hand[h].value) & (g != h):
                            holdval1 = self.hand[g].value
                        h += 1
                    g += 1

                g = 0

                #replace any cards that aren't part of the pair
                while g < 5:
                    if (self.hand[g].value != holdval1):
                        Deck.replacecard(g, self.hand, self.d)
                    g += 1
            #end replace for pair

            #replace for high card
            else:
                k = 0
                #count how many of each suit of card we have
                while k < 5:
                    if self.hand[k].suit == 'c':
                        ccount += 1
                        k+=1
                    elif self.hand[k].suit == 'd':
                        dcount += 1
                        k += 1
                    elif self.hand[k].suit == 's':
                        scount += 1
                        k += 1
                    else:
                        hcount += 1
                        k += 1

                #attempts to look for a flush chance
                #if we have 4 of a suit, then replace the last card, else skip
                if(ccount == 4):
                    g = 0
                    while g < 5:
                        if self.hand[g].suit != 'c':
                            Deck.replacecard(g,self.hand,self.d)
                        g += 1
                elif(dcount == 4):
                    g = 0
                    while g < 5:
                        if self.hand[g].suit != 'd':
                            Deck.replacecard(g, self.hand, self.d)
                        g += 1
                elif(scount == 4):
                    g = 0
                    while g < 5:
                        if self.hand[g].suit != 's':
                            Deck.replacecard(g, self.hand, self.d)
                        g += 1
                elif(hcount == 4):
                    g = 0
                    while g < 5:
                        if self.hand[g].suit != 'h':
                            Deck.replacecard(g, self.hand, self.d)
                        g += 1
                else:
                    #now the program will start looking for a straight chance
                    #sort a temp hand
                    temp = sorted(self.hand, key=operator.attrgetter('value'))

                    #if we have 4 cards in a row then replace the last card
                    if (temp[0].value == (temp[1].value - 1) == (temp[2].value - 2) == (temp[3].value - 3)):
                        Deck.replacecard(4, self.hand, self.d)
                    else:
                        #look for cards that are tens or lower, toss those
                        g = 0
                        while g < 5:
                            #find any cards Jacks or above, those give a chance to win, replace others
                            if self.hand[g].value <= 10:
                                Deck.replacecard(g, self.hand, self.d)
                            else:
                                pass
                            g += 1
                        #end of looking for cards 10 and lower
                    #end of looking for a straight
                #end of looking for a flush chance
            #end replace for high card

            #display new hand and display the new hand type
            displayhand()
            self.labelvariable.set("Current Hand: %s" % (Deck.handtype(self.hand)))

            #award payout
            payout = Deck.payout(self.bet, Deck.handtype(self.hand))
            self.bank += payout

            #display if the bot won or lost
            self.labelvariable2 = StringVar()
            if payout > 0:
                self.labelvariable2.set("Last Result: You Won: %d" % (payout))
                handlabel = Label(self, textvariable=self.labelvariable2, bg="#228B22", width=25)
            elif payout <= 0:
                self.labelvariable2.set("Last Result: You lost: %d" % (0 - payout))
                handlabel = Label(self, textvariable=self.labelvariable2, bg="red", width=25)

            #update the bank
            self.bankvariable.set("Bank: %s" % (self.bank))
            handlabel.grid(column=4, row=3)


        #the function that actually runs the game for a human player
        def begingame():

            #remove the texas holdem butotn if it exists
            if texasbutton.winfo_exists():
                texasbutton.destroy()

            #if structure stops player from betting multiple times per hand
            if self.alreadybet == 0:
                #some variables
                self.alreadybet = 1
                self.alreadyrep = 0
                self.hand = []
                self.handname = ""
                Deck.builddeck(self.d)
                Deck.shuffledeck(self.d)

                #set bet from the bar
                self.bet = self.entry.get()
                self.bet = int(self.bet)

                #draw player hand
                self.hand.append(self.d.pop())
                self.hand.append(self.d.pop())
                self.hand.append(self.d.pop())
                self.hand.append(self.d.pop())
                self.hand.append(self.d.pop())

                #build the bank display
                self.bankvariable = StringVar()
                bankdisplay = Label(self, textvariable = self.bankvariable)
                self.bankvariable.set("Bank: %s" % (self.bank))
                bankdisplay.grid(column=0,row=0)

                #display players hand
                displayhand()

                #variables for check boxes
                var0 = IntVar()
                var1 = IntVar()
                var2 = IntVar()
                var3 = IntVar()
                var4 = IntVar()

                #build the checkboxes for replacing
                c0 = Checkbutton(self,variable=var0)
                c0.grid(column=0,row=2)

                c1 = Checkbutton(self,variable=var1)
                c1.grid(column=1, row=2)

                c2 = Checkbutton(self,variable=var2)
                c2.grid(column=2, row=2)

                c3 = Checkbutton(self,variable=var3)
                c3.grid(column=3, row=2)

                c4 = Checkbutton(self,variable=var4)
                c4.grid(column=4, row=2)

                #build current hand label
                self.labelvariable = StringVar()
                handlabel = Label(self, textvariable=self.labelvariable, bg="#228B22", width = 35)
                handlabel.grid(column=1, row=0)
                self.labelvariable.set("Current Hand: %s" % (Deck.handtype(self.hand)))

                #function that begins replacing cards
                def beginreplacing():
                    #if structure so replacing can only be done once per hand
                    if self.alreadyrep == 0:
                        self.alreadyrep = 1
                        #start checking if check boxes are checked, if they are replace those cards
                        if var0.get() == 1:
                            Deck.replacecard(0,self.hand,self.d)
                        if var1.get() == 1:
                            Deck.replacecard(1,self.hand,self.d)
                        if var2.get() == 1:
                            Deck.replacecard(2,self.hand,self.d)
                        if var3.get() == 1:
                            Deck.replacecard(3,self.hand,self.d)
                        if var4.get() == 1:
                            Deck.replacecard(4,self.hand,self.d)

                        #display new hand
                        displayhand()

                        #display new hand type
                        self.labelvariable.set("Current Hand: %s" % (Deck.handtype(self.hand)))

                        #get the players payout and update bank
                        payout = Deck.payout(self.bet, Deck.handtype(self.hand))
                        self.bank += payout
                        self.labelvariable2 = StringVar()

                        #tell the player if they won last round or not
                        if payout > 0:
                            self.labelvariable2.set("Last Result: You Won: %d" % (payout))
                            handlabel = Label(self, textvariable=self.labelvariable2, bg="#228B22",width = 25)
                        elif payout <= 0:
                            self.labelvariable2.set("Last Result: You lost: %d" % (0-payout))
                            handlabel = Label(self, textvariable=self.labelvariable2, bg="red",width = 25)

                        #update bank variable
                        self.bankvariable.set("Bank: %s" % (self.bank))
                        handlabel.grid(column=4, row=3)

                        #reset alreadybet so the player can play again
                        self.alreadybet = 0


                #trigger the replace function as a button
                replacebutton = Button(self, text=u"Replace Checked Cards", command=beginreplacing)
                replacebutton.grid(column=2, row=3)

        #Button for placing bet with trigger to launch game
        betbutton = Button(self,text=u"Place Bet",command=begingame)
        betbutton.grid(column=3,row=0)

        #Button for having the ai play a hand
        aibutton = Button(self, text=u"Ai Plays", command=aiplay)
        aibutton.grid(column=4, row=0)

        #Button for starting Texas Holdem
        texasbutton = Button(self, text=u"Play Texas Holdem")
        texasbutton.grid(column=5,row=0)


#sets the main loop for the tkinter function
if __name__ == "__main__":
    app = parlorapp(None)
    app.title('Parlor Games')
    app.mainloop()