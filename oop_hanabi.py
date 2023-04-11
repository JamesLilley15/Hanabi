import random
from re import L

class hanabi:
    def __init__(self):
        # Define basic variables
        self.num_players = int(input('How many players? '))
        self.info_num = 8
        self.lives_num = 4
        self.turn_count = 0
        self.end_game_count = 500
        self.player_turn = 0

        ## Deal Decks ##
        print('Dealing...')

        # Empty Discard and Played decks
        self.discard_decks = {'red':[],'green':[],'blue':[],'white':[],'yellow':[],'multi':[]}
        self.played_decks = {'red': 0, 'green': 0, 'blue': 0, 'white': 0, 'yellow': 0, 'multi': 0}
        
        # Main deck
        self.deck = []
        for colour in ['red', 'green', 'blue', 'white', 'yellow', 'multi']:
            for number in [1, 2, 3, 4, 5]:
                if number == 1:
                    add_number = 3
                if number in [2, 3, 4]:
                    add_number = 2
                elif number == 5:
                    add_number = 1
                for i in range(add_number):
                    self.deck.append([colour, number])

        # Players hands
        self.players_hands = []
        for self.player_turn in range(self.num_players):
            self.players_hands.append([])
            for j in range(5):
                self.deal_card()
        self.player_turn = 0

        # Start the game
        self.take_turn()

    ## Main Turn based Progression: ##
    def take_turn(self):
        if self.turn_count >= self.end_game_count:
                print('Gameover, final score:', self.played_decks)
                return
        else:
            print('Pass to Player ', self.player_turn+1, 'then press enter.')
            input()
            for i in range(80):
                print('')
            #print('Your hand:', self.players_hands[self.player_turn])
            print('Turn #',self.turn_count, '     Player ', self.player_turn+1, 's turn.')
            print('Info left: ', self.info_num, '      Lives left: ', self.lives_num)
            print('Played cards: ', self.played_decks)
            print('Discarded cards: ', self.discard_decks)
            print('')
            shown_hands = []
            i = 0
            for hand in self.players_hands:
                if i != self.player_turn:
                    shown_hands.append([i,hand])
                i += 1
            for i in shown_hands:
                print('Player ', i[0]+1,'s hand is: ', i[1])
            print('')


            if self.info_num == 0:
                choice = input('Play (0), or Discard (1)? You have no Info left. ')
            else:
                choice = int(input('Play (0), Discard (1), or Give Info (2)? '))
                if choice == 0:
                    print('')
                    print('Chosen to Play...')
                    self.play()
                if choice == 1:
                    print('')
                    print('Chosen to Discard...')
                    self.discard()
                if choice == 2:
                    print('')
                    print('Chosen to Give Info...')
                    self.info()
        self.turn_count =+ 1
        self.player_turn = (self.player_turn + 1)%self.num_players 
        print('')
        print('')
        print('End of turn. Please press enter.')
        input()
        for i in range(80):
            print('')
        self.take_turn()
        return


    def play(self):
        chosen_card = self.choose_card()
        if self.played_decks[chosen_card[0]]==(chosen_card[1]-1):
            print('Card: ', chosen_card, 'played successfully!')
            if self.win():
                print('Congratulations you have won! Turn number: ', self.turn_count)
                self.end_game_count = self.turn_count
            else:
                self.played_decks[chosen_card[0]] = chosen_card[1]
                self.players_hands[self.player_turn].remove(chosen_card)
                self.deal_card()
                print('New played piles: ', self.played_decks)
                #print('Your new hand: ', self.players_hands[self.player_turn])
        else:
            self.lives_num -=  1
            print('Card: ', chosen_card, 'failed to play!')
            if self.lives_num == 0:
                self.end_game_count = self.turn_count
            else:
                print('Lives remaining:', self.lives_num)
        return

    def discard(self):
        chosen_card = self.choose_card()
        self.discard_decks[chosen_card[0]].append(chosen_card[1])
        self.players_hands[self.player_turn].remove(chosen_card)
        self.deal_card()
        self.info_num += 1
        print('New Info left: ', self.info_num)
        print('New discard piles: ', self.discard_decks)
        #print('Your new hand: ', self.players_hands[self.player_turn])
        return

    def info(self):
        chosen_player = int(input('Choose a player: '))-1
        print('Reminder of Player ', chosen_player +1,'s hand:', self.players_hands[chosen_player])
        colour_number = int(input('Give Colour (0) or Number (1) info: '))
        if colour_number == 0:
            chosen_colour = input('Type the colour you want to reveal and press enter: ')
            reveal = []
            for i in range(len(self.players_hands[chosen_player])):
                if self.players_hands[chosen_player][i][0] in [chosen_colour, 'multi'] :
                    reveal.append(i+1)
            print('Cards: ',reveal, 'are ', chosen_colour)
        if colour_number == 1:
            chosen_number = int(input('Type the number you want to reveal and press enter: '))
            reveal = []
            for i in range(len(self.players_hands[chosen_player])):
                if self.players_hands[chosen_player][i][1] == chosen_number:
                    reveal.append(i+1)
            print('Tell Player ', chosen_player +1, 'that Cards: ',reveal, 'are ', chosen_number)
        self.info_num -= 1
        return

    def win(self):
        for i in self.played_decks.items():
            if i != 5:
                return False
        return True

    def choose_card(self):
        return self.players_hands[self.player_turn][int(input('Choose card from your hand: '))-1]

    def deal_card(self):
        dealt_card = random.randint(0, len(self.deck)-1)
        self.players_hands[self.player_turn].append(self.deck[dealt_card])
        del self.deck[dealt_card]
        return

import tkinter as tk
from tkinter import *

class gui(tk.Tk, hanabi):
    def __init__(self):
        super().__init__()

        self.title('Hanabi')

        # Set up temporary window to get the number of players
        self.geometry('300x150')
        self.label = tk.Label(self, text='Select how many players and press "Continue"?')
        self.label.pack()

        # Scale to set player number
        scalevar = StringVar()
        self.scale= tk.Scale(self, from_=2, to=5,orient=HORIZONTAL, variable=scalevar)
        self.scale.pack()

        # Button to set player number to the scale and continue
        cont = tk.IntVar()
        self.button = tk.Button(self, text='Continue', command=lambda: cont.set(1))
        self.button.pack()
        self.button.wait_variable(cont)
        hanabi.num_players = int(scalevar.get())

        # Clear window and enlarge for normal game
        for widget in self.winfo_children():
            widget.destroy()
        self.geometry('1500x500')

        
        # Display other players hands:
        # Set up frame for the hands
        self.playershandsframe =tk.Frame(self, borderwidth=2, relief="groove")
        self.playershandsframe.pack(side=TOP)
        # Set up frame for each hand
        self.playershandsframes = []
        for i in range(hanabi.num_players):
            self.frame = tk.Frame(self.playershandsframe, borderwidth=2, relief="groove")
            self.frame.pack(side=LEFT)
            self.playershandsframes.append(self.frame)
        # Populate each hand
        k = 1
        for i in self.playershandsframes:
            name = 'Player ' + str(k) + 's Hand'
            self.label = tk.Label(i, text = name)
            self.label.pack(side=TOP)
            k += 1
            for j in range(5):
                self.label = tk.Label(i, text=' Green:  1 ', bg = 'green', fg = 'white', borderwidth=2, relief="groove")
                self.label.pack(side = LEFT)
        
        # Display discard and play piles:
        self.discard_frame = tk.Frame(self, borderwidth=2, relief="groove")
        self.discard_frame.pack(side=TOP)

        self.discardpileslabels = {}
        self.discardpileslabel = tk.Label(self.discard_frame, text='Discard Piles')
        self.discardpileslabel.pack(side=TOP)
        self.discardredlabel = tk.Label(self.discard_frame, text=' Red:    empty ', bg = 'red', fg = 'white', borderwidth=2, relief="groove")
        self.discardredlabel.pack(side = LEFT)
        self.discardpileslabels['Red'] = self.discardpileslabel
        self.discardgreenlabel = tk.Label(self.discard_frame, text=' Green:  empty ', bg = 'green', fg = 'white', borderwidth=2, relief="groove")
        self.discardgreenlabel.pack(side = LEFT)
        self.discardpileslabels['Green'] = self.discardpileslabel
        self.discardbluelabel = tk.Label(self.discard_frame, text=' Blue:   empty ', bg = 'blue', fg = 'white', borderwidth=2, relief="groove")
        self.discardbluelabel.pack(side = LEFT)
        self.discardpileslabels['Blue'] = self.discardpileslabel
        self.discardwhitelabel = tk.Label(self.discard_frame, text=' White:  empty ', bg = 'white', borderwidth=2, relief="groove")
        self.discardwhitelabel.pack(side = LEFT)
        self.discardpileslabels['White'] = self.discardpileslabel
        self.discardyellowlabel = tk.Label(self.discard_frame, text=' Yellow: empty ', bg = 'yellow', borderwidth=2, relief="groove")
        self.discardyellowlabel.pack(side = LEFT)
        self.discardpileslabels['Yellow'] = self.discardpileslabel
        self.discardmultilabel = tk.Label(self.discard_frame, text=' Multi:  empty ', borderwidth=2, relief="groove")
        self.discardmultilabel.pack(side = LEFT)
        self.discardpileslabels['Multi'] = self.discardpileslabel

        self.play_frame = tk.Frame(self, borderwidth=2, relief="groove")
        self.play_frame.pack(side=TOP)

        self.playpileslabels = {}
        self.playpileslabel = tk.Label(self.play_frame, text='Play Piles')
        self.playpileslabel.pack(side=TOP)
        self.playredlabel = tk.Label(self.play_frame, text=' Red:    empty ', bg = 'red', fg = 'white', borderwidth=2, relief="groove")
        self.playredlabel.pack(side = LEFT)
        self.playpileslabels['Red'] = self.playpileslabel
        self.playgreenlabel = tk.Label(self.play_frame, text=' Green:  empty ', bg = 'green', fg = 'white', borderwidth=2, relief="groove")
        self.playgreenlabel.pack(side = LEFT)
        self.playpileslabels['Green'] = self.playpileslabel
        self.playbluelabel = tk.Label(self.play_frame, text=' Blue:   empty ', bg = 'blue', fg = 'white', borderwidth=2, relief="groove")
        self.playbluelabel.pack(side = LEFT)
        self.playpileslabels['Blue'] = self.playpileslabel
        self.playwhitelabel = tk.Label(self.play_frame, text=' White:  empty ', bg = 'white', borderwidth=2, relief="groove")
        self.playwhitelabel.pack(side = LEFT)
        self.playpileslabels['White'] = self.playpileslabel
        self.playyellowlabel = tk.Label(self.play_frame, text=' Yellow: empty ', bg = 'yellow', borderwidth=2, relief="groove")
        self.playyellowlabel.pack(side = LEFT)
        self.playpileslabels['Yellow'] = self.playpileslabel
        self.playmultilabel = tk.Label(self.play_frame, text=' Multi:  empty ', borderwidth=2, relief="groove")
        self.playmultilabel.pack(side = LEFT)
        self.playpileslabels['Multi'] = self.playpileslabel
                
        self.button = tk.Button(self, text='Click to Start', borderwidth=2, relief="groove")
        self.button['command'] = hanabi()
        self.button.pack(side=TOP)
    
    def start(self):
        hanabi
        return
        #showinfo(title='Information', message='Hello, Tkinter!') 

    def set_player_num(self, i):
        hanabi.num_players = i
        #self.destroy()
        return          


#hanabi()
if __name__ == "__main__":
    app = gui()
    app.mainloop()
