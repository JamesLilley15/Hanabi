import random
from re import L
from sys import float_repr_style

class hanabi():
    def __init__(self, num_players):
        # Define basic variables
        #self.num_players = int(input('How many players? '))
        self.info_num = 8
        self.lives_num = 4
        self.turn_count = 0
        self.end_game_count = 500
        self.player_turn = 0
        self.num_players = num_players

        ## Deal Decks ##
        print('Dealing...')

        # Empty Discard and Played decks
        self.discard_decks = {'red':[],'green':[],'blue':[],'white':[],'yellow':[],'multi':[]}
        self.played_decks = {'red': 0, 'green': 0, 'blue': 0, 'white': 0, 'yellow': 0, 'multi': 0}
        
        # Main deck
        self.deck = []
        for colour in ['Red', 'Green', 'Blue', 'White', 'Yellow', 'Multi']:
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

        return 
        # Start the game
        #self.take_turn()

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
        win = FALSE
        if self.played_decks[chosen_card[0]]==(chosen_card[1]-1):
            print('Card: ', chosen_card, 'played successfully!')
            played = TRUE
            if self.win():
                win = TRUE
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
            played = FALSE
            if self.lives_num == 0:
                self.end_game_count = self.turn_count
            else:
                print('Lives remaining:', self.lives_num)
        return  (win, played)

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
import tkinter.ttk as ttk
from tkinter import *
from tkinter.ttk import *

class gui(tk.Tk, hanabi):
    def __init__(self):
        #super().__init__()

        self.menu = tk.Tk()
        self.menu.title('Hanabi')

        # Set up temporary window to get the number of players
        self.menu.geometry('300x150')
        self.menu.label = tk.Label(self.menu, text='Select how many players and press "Continue"?')
        self.menu.label.pack()

        # Scale to set player number
        self.scalevar = tk.StringVar()
        self.menu.scale= tk.Scale(self.menu, from_=2, to=5, orient=tk.HORIZONTAL, variable=self.scalevar)
        self.menu.scale.pack()

        # Button to set player number to the scale and continue
        cont = tk.IntVar()
        self.menu.button = tk.Button(self.menu, text='Continue', command=lambda: cont.set(1))
        self.menu.button.pack()
        self.menu.button.wait_variable(cont)
        self.deal()
        self.menu.mainloop()

    def deal(self):
        self.Hanabi = hanabi(int(self.scalevar.get()))
        self.menu.withdraw()

        # Open a window (inc. dealing a hand) for each player.
        self.PlayerWindows = []
        if self.Hanabi.num_players == 2:
            self.PlayerOne = self.open_player_window(0)
            self.PlayerWindows.append(self.PlayerOne)
            self.PlayerTwo = self.open_player_window(1)
            self.PlayerWindows.append(self.PlayerTwo)
        if self.Hanabi.num_players == 3:
            self.PlayerOne = self.open_player_window(0)
            self.PlayerWindows.append(self.PlayerOne)
            self.PlayerTwo = self.open_player_window(1)
            self.PlayerWindows.append(self.PlayerTwo)
            self.PlayerThree = self.open_player_window(2)
            self.PlayerWindows.append(self.PlayerThree)
        if self.Hanabi.num_players == 4:
            self.PlayerOne = self.open_player_window(0)
            self.PlayerWindows.append(self.PlayerOne)
            self.PlayerTwo = self.open_player_window(1) 
            self.PlayerWindows.append(self.PlayerTwo)           
            self.PlayerThree = self.open_player_window(2)
            self.PlayerWindows.append(self.PlayerThree)
            self.PlayerFour = self.open_player_window(3)
            self.PlayerWindows.append(self.PlayerFour)
        if self.Hanabi.num_players == 5:
            self.PlayerOne = self.open_player_window(0)
            self.PlayerWindows.append(self.PlayerOne)
            self.PlayerTwo = self.open_player_window(1)
            self.PlayerWindows.append(self.PlayerTwo)
            self.PlayerThree = self.open_player_window(2)
            self.PlayerWindows.append(self.PlayerThree)
            self.PlayerFour = self.open_player_window(3)
            self.PlayerWindows.append(self.PlayerFour)
            self.PlayerFive = self.open_player_window(4)
            self.PlayerWindows.append(self.PlayerFive)

    def open_player_window(self, player_num):
        # Create window for this player
        window = tk.Toplevel(self.menu)
        window.title('Player ' + str(player_num+1) + "'s Window")
        # Set up frame for the hands
        window.playershandsframe =ttk.Frame(window)#, borderwidth=2, relief="groove")
        window.playershandsframe.pack(side=TOP)

        # Set up frame for each hand
        window.playershandsframes = []
        k = 1
        for i in range(self.Hanabi.num_players-1):
            if k == player_num+1:
                k += 1
            window.frame = tk.Frame(window.playershandsframe, borderwidth=2, relief="groove")
            window.frame.pack(side=LEFT)
            name = 'Player ' + str(k) + "'s Hand"
            window.label = tk.Label(window.frame, text = name)
            window.label.pack(side=TOP)
            window.playershandsframes.append([k, window.frame])
            k += 1

        # Populate each hand
        other_players_hands = self.Hanabi.players_hands[:]
        del other_players_hands[player_num]
        for handnum in range(len(other_players_hands)):
            for cardnum in range(5):
                colour = str(other_players_hands[handnum][cardnum][0])
                number = str(other_players_hands[handnum][cardnum][1])
                if colour == 'Blue' or colour == 'Red' or colour == 'Green':
                    window.cardlabel = tk.Label(window.playershandsframes[handnum][1], fg = 'White', bg = colour, relief = "groove", borderwidth = 2, text = colour + ' ' + number, width=10, height=5)
                    window.cardlabel.pack(side = LEFT)
                if colour == 'Yellow' or colour == 'White':
                    window.cardlabel = tk.Label(window.playershandsframes[handnum][1], bg = colour, relief = "groove", borderwidth = 2, text = colour + ' ' + number, width=10, height=5)
                    window.cardlabel.pack(side = LEFT)
                if colour == 'Multi':                    
                    window.cardlabel = tk.Label(window.playershandsframes[handnum][1], relief = "groove", borderwidth = 2, text = colour + ' ' + number, width=10, height=5)
                    window.cardlabel.pack(side = LEFT)
        
        # Display discard and play piles:
        window.discard_frame = tk.Frame(window, borderwidth=2, relief="groove")
        window.discard_frame.pack(side=TOP, pady=(10, 0))
        window.geometry('1500x500')

        window.discardpileslabels = {}
        window.discardpileslabel = tk.Label(window.discard_frame, text='Discard Piles')
        window.discardpileslabel.pack(side=TOP)
        window.discardredlabel = tk.Label(window.discard_frame, text=' Red:    empty ', bg = 'red', fg = 'white', borderwidth=2, relief="groove", width=15, height=5)
        window.discardredlabel.pack(side = LEFT, padx=(5, 0), pady=(0, 5))
        window.discardpileslabels['Red'] = window.discardpileslabel
        window.discardgreenlabel = tk.Label(window.discard_frame, text=' Green:  empty ', bg = 'green', fg = 'white', borderwidth=2, relief="groove", width=15, height=5)
        window.discardgreenlabel.pack(side = LEFT, pady=(0, 5))
        window.discardpileslabels['Green'] = window.discardpileslabel
        window.discardbluelabel = tk.Label(window.discard_frame, text=' Blue:   empty ', bg = 'blue', fg = 'white', borderwidth=2, relief="groove", width=15, height=5)
        window.discardbluelabel.pack(side = LEFT, pady=(0, 5))
        window.discardpileslabels['Blue'] = window.discardpileslabel
        window.discardwhitelabel = tk.Label(window.discard_frame, text=' White:  empty ', bg = 'white', borderwidth=2, relief="groove", width=15, height=5)
        window.discardwhitelabel.pack(side = LEFT, pady=(0, 5))
        window.discardpileslabels['White'] = window.discardpileslabel
        window.discardyellowlabel = tk.Label(window.discard_frame, text=' Yellow: empty ', bg = 'yellow', borderwidth=2, relief="groove", width=15, height=5)
        window.discardyellowlabel.pack(side = LEFT, pady=(0, 5))
        window.discardpileslabels['Yellow'] = window.discardpileslabel
        window.discardmultilabel = tk.Label(window.discard_frame, text=' Multi:  empty ', borderwidth=2, relief="groove", width=15, height=5)
        window.discardmultilabel.pack(side = LEFT, padx=(0, 5), pady=(0, 5))
        window.discardpileslabels['Multi'] = window.discardpileslabel

        window.play_frame = tk.Frame(window, borderwidth=2, relief="groove")
        window.play_frame.pack(side=TOP, pady=(10, 0))

        window.playpileslabels = {}
        window.playpileslabel = tk.Label(window.play_frame, text='Play Piles')
        window.playpileslabel.pack(side=TOP)

        window.playredlabel = tk.Label(window.play_frame, text=' Red:    empty ', bg = 'red', fg = 'white', borderwidth=2, relief="groove", width=15, height=5)
        window.playredlabel.pack(side = LEFT, padx=(5, 0), pady=(0, 5))
        window.playpileslabels['Red'] = window.playpileslabel
        window.playgreenlabel = tk.Label(window.play_frame, text=' Green:  empty ', bg = 'green', fg = 'white', borderwidth=2, relief="groove", width=15, height=5)
        window.playgreenlabel.pack(side = LEFT, pady=(0, 5))
        window.playpileslabels['Green'] = window.playpileslabel
        window.playbluelabel = tk.Label(window.play_frame, text=' Blue:   empty ', bg = 'blue', fg = 'white', borderwidth=2, relief="groove", width=15, height=5)
        window.playbluelabel.pack(side = LEFT, pady=(0, 5))
        window.playpileslabels['Blue'] = window.playpileslabel
        window.playwhitelabel = tk.Label(window.play_frame, text=' White:  empty ', bg = 'white', borderwidth=2, relief="groove", width=15, height=5)
        window.playwhitelabel.pack(side = LEFT, pady=(0, 5))
        window.playpileslabels['White'] = window.playpileslabel
        window.playyellowlabel = tk.Label(window.play_frame, text=' Yellow: empty ', bg = 'yellow', borderwidth=2, relief="groove", width=15, height=5)
        window.playyellowlabel.pack(side = LEFT, pady=(0, 5))
        window.playpileslabels['Yellow'] = window.playpileslabel
        window.playmultilabel = tk.Label(window.play_frame, text=' Multi:  empty ', borderwidth=2, relief="groove", width=15, height=5)
        window.playmultilabel.pack(side = LEFT, padx=(0, 5), pady=(0, 5))
        window.playpileslabels['Multi'] = window.playpileslabel
        
        window.actionsframe = ttk.Frame(window)#, borderwidth=2, relief='groove')
        window.actionsframe.pack(side=TOP, pady=(10, 0))

        window.actionslabel = ttk.Label(window.actionsframe, text='Choose your Action:')
        window.actionslabel.pack(side=TOP)

        window.playaction = tk.Button(window.actionsframe, text='\n Play a Card \n', width=20, command = lambda: self.guiplay(player_num))#, tk.borderwidth=2, relief="groove", width=15, height=3)
        #window.playaction['command'] = self.guiplay(player_num)
        window.playaction.pack(side=LEFT, padx=(5, 0), pady=(0, 5))
        window.discardaction = tk.Button(window.actionsframe, text='\nDiscard a Card\n', width=20)
        window.discardaction['command'] = self.guidiscard(player_num)
        window.discardaction.pack(side=LEFT, pady=(0, 5))
        if self.Hanabi.info_num != 0:
            window.infoaction = tk.Button(window.actionsframe, text='\nGive Information\n', width=20)
            #window.infoaction['command'] = self.guigiveinfo(player_num)
            window.infoaction.pack(side=LEFT, pady=(0, 5))
        else:
            window.infoaction = tk.Label(window.actionsframe, text = "\nCan't Give Information\n", width=20)
            window.infoaction.pack(side=LEFT, pady=(0, 5))
            
        return window

    def guidiscard(self, player_num):
        return

    def guiplay(self, player_num):
        #win, played = self.Hanabi.play()
        if FALSE:#win:
            self.guiwin()
        elif True:
            self.PlayerWindows[player_num].playaction.destroy()
            self.PlayerWindows[player_num].discardaction.destroy()
            self.PlayerWindows[player_num].infoaction.destroy()        
            self.PlayerWindows[player_num].successmessage = tk.Label(self.PlayerWindows[player_num], text='\n\n Card Successfully Played! :) \n\n', width =100, relief = 'groove')
            self.PlayerWindows[player_num].successmessage.pack(side = TOP, pady=(0,10))
        else:
            self.PlayerWindows[player_num].playaction.destroy()
            self.PlayerWindows[player_num].discardaction.destroy()
            self.PlayerWindows[player_num].infoaction.destroy()            
            self.PlayerWindows[player_num].successmessage = ttk.Label(self.PLayerWindows[player_num], text='\n\n Failed to Play Card... :(\n\n', width =100)
            self.PlayerWindows[player_num].successmessage.pack(side = TOP, pady=(0,10))
        return
        #self.refresh_display()

    def refresh_display(self, windows_reset, window_turn):
        for window in windows_reset:
            last_player = 'window.actionslabel' in locals() or 'window.actionslabel' in globals()
            if last_player:
                window.actionsframe.pack_forget()
            player_number
            # Set up frame for each hand
            for [player_hand_num, players_hand_frame] in window.playershandsframe:
                for widget in players_hand_frame.winfo_children():
                    widget.destroy
                name = 'Player ' + str(player_hand_num) + "'s Hand"
                window.label = tk.Label(players_hand_frame, text = name)
                window.label.pack(side=TOP)
                for cardnum in range(5):
                    colour = str(self.Hanabi.players_hands[player_hand_num][cardnum][0])
                    number = str(self.Hanabi.players_hands[player_hand_num][cardnum][1])
                    if colour == 'Blue' or colour == 'Red' or colour == 'Green':
                        window.cardlabel = tk.Label(players_hand_frame[handnum][1], fg = 'White', bg = colour, relief = "groove", borderwidth = 2, text = colour + ' ' + number, width=10, height=5)
                        window.cardlabel.pack(side = LEFT)
                    if colour == 'Yellow' or colour == 'White':
                        window.cardlabel = tk.Label(players_hand_frame[handnum][1], bg = colour, relief = "groove", borderwidth = 2, text = colour + ' ' + number, width=10, height=5)
                        window.cardlabel.pack(side = LEFT)
                    if colour == 'Multi':                    
                        window.cardlabel = tk.Label(players_hand_frame[handnum][1], relief = "groove", borderwidth = 2, text = colour + ' ' + number, width=10, height=5)
                        window.cardlabel.pack(side = LEFT)

            # Display discard and play piles:
            window.discard_frame = tk.Frame(window, borderwidth=2, relief="groove")
            window.discard_frame.pack(side=TOP, pady=(10, 0))
            window.geometry('1500x500')

            for pile, pile_depth  in self.Hanabi.discard_decks:
                name = str(pile) + ': ' + str(pile_depth)
                window.discardlabel = tk.Label(window.discard_frame, text=name)
            window.discardpileslabels = {}
            window.discardpileslabel = tk.Label(window.discard_frame, text='Discard Piles')
            window.discardpileslabel.pack(side=TOP)
            window.discardredlabel = tk.Label(window.discard_frame, text=' Red:    empty ', bg = 'red', fg = 'white', borderwidth=2, relief="groove", width=15, height=5)
            window.discardredlabel.pack(side = LEFT, padx=(5, 0), pady=(0, 5))
            window.discardpileslabels['Red'] = window.discardpileslabel
            window.discardgreenlabel = tk.Label(window.discard_frame, text=' Green:  empty ', bg = 'green', fg = 'white', borderwidth=2, relief="groove", width=15, height=5)
            window.discardgreenlabel.pack(side = LEFT, pady=(0, 5))
            window.discardpileslabels['Green'] = window.discardpileslabel
            window.discardbluelabel = tk.Label(window.discard_frame, text=' Blue:   empty ', bg = 'blue', fg = 'white', borderwidth=2, relief="groove", width=15, height=5)
            window.discardbluelabel.pack(side = LEFT, pady=(0, 5))
            window.discardpileslabels['Blue'] = window.discardpileslabel
            window.discardwhitelabel = tk.Label(window.discard_frame, text=' White:  empty ', bg = 'white', borderwidth=2, relief="groove", width=15, height=5)
            window.discardwhitelabel.pack(side = LEFT, pady=(0, 5))
            window.discardpileslabels['White'] = window.discardpileslabel
            window.discardyellowlabel = tk.Label(window.discard_frame, text=' Yellow: empty ', bg = 'yellow', borderwidth=2, relief="groove", width=15, height=5)
            window.discardyellowlabel.pack(side = LEFT, pady=(0, 5))
            window.discardpileslabels['Yellow'] = window.discardpileslabel
            window.discardmultilabel = tk.Label(window.discard_frame, text=' Multi:  empty ', borderwidth=2, relief="groove", width=15, height=5)
            window.discardmultilabel.pack(side = LEFT, padx=(0, 5), pady=(0, 5))
            window.discardpileslabels['Multi'] = window.discardpileslabel

            window.play_frame = tk.Frame(window, borderwidth=2, relief="groove")
            window.play_frame.pack(side=TOP, pady=(10, 0))

            window.playpileslabels = {}
            window.playpileslabel = tk.Label(window.play_frame, text='Play Piles')
            window.playpileslabel.pack(side=TOP)

            window.playredlabel = tk.Label(window.play_frame, text=' Red:    empty ', bg = 'red', fg = 'white', borderwidth=2, relief="groove", width=15, height=5)
            window.playredlabel.pack(side = LEFT, padx=(5, 0), pady=(0, 5))
            window.playpileslabels['Red'] = window.playpileslabel
            window.playgreenlabel = tk.Label(window.play_frame, text=' Green:  empty ', bg = 'green', fg = 'white', borderwidth=2, relief="groove", width=15, height=5)
            window.playgreenlabel.pack(side = LEFT, pady=(0, 5))
            window.playpileslabels['Green'] = window.playpileslabel
            window.playbluelabel = tk.Label(window.play_frame, text=' Blue:   empty ', bg = 'blue', fg = 'white', borderwidth=2, relief="groove", width=15, height=5)
            window.playbluelabel.pack(side = LEFT, pady=(0, 5))
            window.playpileslabels['Blue'] = window.playpileslabel
            window.playwhitelabel = tk.Label(window.play_frame, text=' White:  empty ', bg = 'white', borderwidth=2, relief="groove", width=15, height=5)
            window.playwhitelabel.pack(side = LEFT, pady=(0, 5))
            window.playpileslabels['White'] = window.playpileslabel
            window.playyellowlabel = tk.Label(window.play_frame, text=' Yellow: empty ', bg = 'yellow', borderwidth=2, relief="groove", width=15, height=5)
            window.playyellowlabel.pack(side = LEFT, pady=(0, 5))
            window.playpileslabels['Yellow'] = window.playpileslabel
            window.playmultilabel = tk.Label(window.play_frame, text=' Multi:  empty ', borderwidth=2, relief="groove", width=15, height=5)
            window.playmultilabel.pack(side = LEFT, padx=(0, 5), pady=(0, 5))
            window.playpileslabels['Multi'] = window.playpileslabel

        
        return

        
    def opens_player_window():
        
        # Label each frame
        #k = 1
        #window.playershandslabels = []
        #for i in window.playershandsframes:
        #    playershand = []
        #    name = 'Player ' + str(k) + "'s Hand"
        #    self.label = tk.Label(i, text = name)
        #    self.label.pack(side=TOP)
        #    k += 1
        #    self.playershandslabels.append(playershand)
        
        
                
        self.button = tk.Button(self, text='Click to Start', borderwidth=2, relief="groove")
        self.button['command'] = self.start()
        self.button.pack(side=TOP)
    
    
    def start_turn(self, hanabi):
        print(hanabi.num_players)
        # Display players hands
        

    def set_player_num(self, i):
        hanabi.num_players = i
        #self.destroy()
        return          


#hanabi()
if __name__ == "__main__":
    game = gui()
    #game.mainloop()
