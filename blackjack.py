
# face cards (jack, queen, king) count as 10
# aces count as 1 or 11 (whichever is more favorable for the player)


import random

suits = ['Spades', 'Clubs', 'Diamonds', 'Hearts']
ranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '8', '9', '10', 'Jack', 'Queen', 'King']
values = {'Ace': 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 
          'Jack': 10, 'Queen': 10, 'King': 10}


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


# initalize hand
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
    while True:
        try:
            chips.bet = int(input('How many chips would you like to bet? '))
        except ValueError:
            print('That is not a valid input. Enter an integer value.')
        else:
            if chips.bet > chips.total:
                print(f"Sorry, your bet can't exceed {chips.total}")

def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_aces()  # Adjust for aces after each deal





# Testing
test_deck = Deck()
test_deck.shuffle()
test_player = Hand()
test_player.add_card(test_deck.deal())
test_player.add_card(test_deck.deal())

for card in test_player.cards:
    print(card)

print(test_player.value)
