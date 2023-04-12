import random
from re import L
from sys import float_repr_style, exit

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
        
        # Main deck
        self.colours = ['Red', 'Green', 'Blue', 'White', 'Yellow', 'Multi']
        self.numbers = [1, 1, 1, 2, 2, 3, 3, 4, 4, 5]
        self.deck = [[c, n] for c in self.colours for n in self.numbers]

        # Empty Discard and Played decks
        self.discard_decks = {c: [] for c in self.colours}
        self.played_decks = {c: 0 for c in self.colours}

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
            print(f'Pass to Player {self.player_turn + 1} then press enter.')
            input()
            for i in range(80):
                print('')
            #print('Your hand:', self.players_hands[self.player_turn])
            print(f'Turn #{self.turn_count}     Player {self.player_turn+1}\'s turn.')
            print(f'Info left: {self.info_num}      Lives left: {self.lives_num}')
            print(f'Played cards: {self.played_decks}')
            print(f'Discarded cards: {self.discard_decks}\n')
            
            shown_hands = list(enumerate(self.players_hands))
            del shown_hands[self.player_turn]
            for i in shown_hands:
                print('Player ', i[0]+1,'s hand is: ', i[1])
            print('')


            if self.info_num == 0:
                choice = input('Play (0), or Discard (1)? You have no Info left. ')
            else:
                choice = int(input('Play (0), Discard (1), or Give Info (2)? '))
                display_text = ['\nChosen to Play...', '\nChosen to Discard...', '\nChosen to Give Info...']
                action = [self.play, self.discard. self.info]
                print(display_text[choice])
                action[choice]()
  
        self.turn_count =+ 1
        self.player_turn = (self.player_turn + 1)%self.num_players 
        print('\n\nEnd of turn. Please press enter.')
        input()
        print('\n'*80)
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
            #Or new code
            #reveal = [i+1 if self.players_hands[chosen_player][i][0] in [chosen_colour, 'multi'] for i in range(len(self.players_hands[chosen_player]))]
            print(f'Cards: {reveal} are {chosen_colour}')
        if colour_number == 1:
            chosen_number = int(input('Type the number you want to reveal and press enter: '))
            reveal = []
            for i in range(len(self.players_hands[chosen_player])):
                if self.players_hands[chosen_player][i][1] == chosen_number:
                    reveal.append(i+1)
            #Or new code
            #reveal = [i+1 if self.players_hands[chosen_player][i][0] == chosen_number for i in range(len(self.players_hands[chosen_player]))]
            print(f'Tell Player {chosen_player + 1} that Cards: {reveal} are {chosen_number}')
        self.info_num -= 1
        return

    def win(self):
        # Checks if there's a 5 on top of all of the played decks
        return all([i != 5 for i in self.played_decks.items()])

    def choose_card(self):
        return self.players_hands[self.player_turn][int(input('Choose card from your hand: '))-1]

    def deal_card(self):
        # pop(index) method removes a random card from the deck and stores it in dealt_card
        dealt_card = self.deck.pop(random.randrange(len(self.deck)))
        self.players_hands[self.player_turn].append(dealt_card)
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
        self.menu.protocol("WM_DELETE_WINDOW", self.menu.destroy)

        # Set up temporary window to get the number of players
        self.menu.geometry('300x150')
        self.menu.label = tk.Label(self.menu, text='Select how many players and press "Continue"?')
        self.menu.label.pack()

        # Scale to set player number
        self.scalevar = tk.StringVar()
        self.menu.scale= tk.Scale(self.menu, from_=2, to=5, orient=tk.HORIZONTAL, variable=self.scalevar)
        self.menu.scale.pack()

        self.colours = ['Red', 'Green', 'Blue', 'White', 'Yellow', 'Multi']

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

    def colour_label(self, frame, colour_name):
                if colour_name == 'Multi':
                    return tk.Label(frame, text=f' {colour_name}:    empty ', borderwidth=2, relief="groove", width=15, height=5)
                elif colour_name in ['Red', 'Green', 'Blue']:
                    fg_colour = 'white'
                else:
                    fg_colour = 'black'
                return tk.Label(frame, text=f' {colour_name}:    empty ', bg=colour_name.lower(), fg=fg_colour, borderwidth=2, relief="groove", width=15, height=5)

    def colour_piles(self, frame):
        labels_dict = {}
        for c in self.colours:
            labels_dict[c] = self.colour_label(frame, c)
            if c == ['Red']:
                labels_dict[c].pack(side = LEFT, pady=(0, 5) ,padx=(5, 0))
            else:
                labels_dict[c].pack(side = LEFT, pady=(0, 5))
        return labels_dict

    def open_player_window(self, player_num):
        # Create window for this player
        window = tk.Toplevel(self.menu)
        window.protocol("WM_DELETE_WINDOW", exit)
        window.title('Player ' + str(player_num+1) + "'s Window")
        window.player_num = player_num
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
        window.discardpileslabel = tk.Label(window.discard_frame, text='Discard Piles')
        window.discardpileslabel.pack(side=TOP)
        window.discardpileslabels = self.colour_piles(window.discard_frame)

        window.play_frame = tk.Frame(window, borderwidth=2, relief="groove")
        window.play_frame.pack(side=TOP, pady=(10, 0))
        window.playpileslabel = tk.Label(window.play_frame, text='Play Piles')
        window.playpileslabel.pack(side=TOP)
        window.playpileslabels = self.colour_piles(window.play_frame)
        
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

    def refresh_display(self, windows_reset, last_player):
        for window in windows_reset:
            
            # Re-size window
            #window.geometry('1500x500')

            ## Display other players hands ##
            #last_player = 'window.actionslabel' in locals() or 'window.actionslabel' in globals()
            if window.player_num == last_player:
                window.actionsframe.pack_forget()
            #player_number

            # Set up frame for each other hand
            for [player_hand_num, players_hand_frame] in window.playershandsframe:
                # Clear widgets from each hands frames
                for widget in players_hand_frame.winfo_children():
                    widget.destroy
                
                # Name this frame
                name = 'Player ' + str(player_hand_num) + "'s Hand"
                window.label = tk.Label(players_hand_frame, text = name)
                window.label.pack(side=TOP)
                
                # Re-deal the hands
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

            
            ## Display discard and play piles ##
            # Display discard piles
            window.discard_frame = tk.Frame(window, borderwidth=2, relief="groove")
            window.discard_frame.pack(side=TOP, pady=(10, 0))

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


            # Display play piles
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

            ## Display appropriate buttons / play area
            
            # If no longer my turn
            if window.player_num == last_player:
                window.playaction.destroy()
                window.discardaction.destroy()
                window.infoaction.destroy()        
                window.waitmessage = tk.Label(self.PlayerWindows[window.player_num], text='\n\n Not your turn - talk to the others! :) \n\n', width =100, relief = 'groove')
                window.waitmessage.pack(side = TOP, pady=(0,10))
                # Start of go - display three buttons
                # Resolving action
                    # 
                # Someone elses go
            
            if window.player_num == last_player + 1:
                continue
            return

        
    def opens_player_window(self):
        
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
