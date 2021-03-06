
# face cards (jack, queen, king) count as 10
# aces count as 1 or 11 (whichever is more favorable for the player)


import random

suits = ['Spades', 'Clubs', 'Diamonds', 'Hearts']
ranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '8', '9', '10', 'Jack', 'Queen', 'King']
values = {'Ace': 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 
          'Jack': 10, 'Queen': 10, 'King': 10}
playing = True # Indicates if player still wants to play the game
hitting = True # Indicates if player is hitting (adding cards)

# **** Functions and classes ****

# Create individual card 
class Card:     
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]
    
    def __str__(self):
        return f'{self.rank} of {self.suit}'

# Create 52 card deck    
class Deck:
    def __init__(self):
        self.deck = []
        for rank in ranks:
            for suit in suits:
                self.deck.append(Card(suit, rank))

    # Prints out current deck
    def __str__(self) -> str:
        deck_comb = ''
        for card in self.deck:
            deck_comb += '\n ' + card.__str__()
        return f'Current deck: {deck_comb}'

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        card = self.deck.pop()
        return card


# initalize hand for player/dealer
class Hand:
    def __init__(self):
        self.cards =[]
        self.value = 0
        self.aces = 0
    
    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1
    
    # adjust aces in players favor
    def adjust_aces(self):
        while (self.value > 21) and (self.aces > 0):
            self.value -= 10
            self.aces -= 1

# class for chip betting, player starts with 100 chips
class Chips:
    def __init__(self):
        self.total = 100
        self.bet = 0
    
    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


# take user bet, loops until user enters valid bet (int)
def take_bet(chips):
    print(f'Current balance: {chips.total} chips')
    bet = int(input('How many chips would you like to bet? ==> '))
    while bet > chips.total:
          print(f"Sorry, your bet can't be more than {chips.total} chips")
          bet = int(input('How many chips would you like to bet? ==> '))
    chips.bet = bet
    

def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_aces()  # Adjust for aces after each deal

def hit_or_stand(deck, hand):
    global hitting
    while hitting and player_hand.value <= 21:  
        move = input('Would you like to hit or stand (h/s)? ==> ').lower().strip(".!? ")
        if move == 'h':
            print('\nPlayer hits...')
            hit(deck, hand)
            show_some(player_hand, dealer_hand)
        elif move == 's':
            print('\nPlayer stands. Dealer is playing...')
            hitting = False
        else:
            print('\nInvalid input. Please try again')

# show only 1 dealer card and hide other
def show_some(player, dealer):
    print("\nDealer's hand:")
    print('[Card Hidden]')
    print(dealer.cards[1])
    print(f"\nPlayer's hand - Value {player_hand.value}:")
    print(*player.cards, sep='\n')

# Shows all cards. Used only at end of game
def show_all(player, dealer):
    print(f"\nDealer's hand - Value {dealer_hand.value}: ")
    print(*dealer.cards, sep='\n')
    print(f"\nPlayer's hand  - Value {player_hand.value}: ")
    print(*player.cards, sep='\n')

# Functions to display corresponding win/lose messages and update player's chip balance 
def player_win(chips):
    chips.win_bet()
    print('\nPlayer wins!')
    print(f'You receive {chips.bet} chips.\n')

def dealer_win(chips):
    chips.lose_bet()
    print('\nDealer wins!')
    print(f'You lose {chips.bet} chips.\n')

def player_bust(chips):
    chips.lose_bet()
    print('\nPlayer busts! Dealer wins!')
    print(f'You lose {chips.bet} chips.\n')

def dealer_bust(chips):
    chips.win_bet()
    print('\nDealer busts! Player wins!')
    print(f'You receive {chips.bet} chips.\n')

# Player receives their initial bet back in case of push. (i.e. they do not lose/gain chips)
def push():
    print("\nIt's a push! Neither player nor dealer win.")
    print('You do not lose or receive any chips.\n')


# **** Implementing the game ****

while playing:

    print('\nWelcome to Black Jack! Get as close to 21 as possible without going over!')
    print('Dealer hits until they reach 17. Aces count as 1 or 11.\n')

    # Create and shuffle deck
    deck = Deck()
    deck.shuffle()

    # Give dealer and player 2 cards each
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    player_hand =  Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    player_chips = Chips()
    take_bet(player_chips)

    # Display all player cards, and only 1 dealer card
    show_some(player_hand, dealer_hand)

    while hitting:
        hit_or_stand(deck, player_hand)
        print()
        show_some(player_hand, dealer_hand)

        if player_hand.value > 21:
            player_bust(player_chips)
            hitting = False

    if player_hand.value <= 21:

        while dealer_hand.value < 17:
            hit(deck, dealer_hand)
        
        show_all(player_hand, dealer_hand)

        if dealer_hand.value > 21:
            dealer_bust(player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_win(player_chips)
        elif player_hand.value > dealer_hand.value:
            player_win(player_chips)
        elif player_hand.value == dealer_hand.value:
            push()
    

    print(f'Player current balance: {player_chips.total} chips\n')

    print("That's the end of the game!\n")

    new_game = input("Would you like to play another game? (y/n) ==> ").lower().strip(' .?!')
    if new_game == 'n':
        playing = False
        print('\nOk, Bye!')
