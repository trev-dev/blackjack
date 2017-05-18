## 21 

import random

import textwrap

import os

import time

def clear(): # function that clears the terminal screen

	os.system('cls' if os.name == 'nt' else 'clear')


class Cards: # individual card constructor

	def __init__(self, value, suit):

		self.card = (value, suit)



class Deck: # Deck Generating Class. Generates an instance of a deck and can return cards by popping them off it's current stack of cards list

	suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs'] #hearts, diamonds, spades, clubs

	values = ['Ace', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King'] # All possible card values

	def __init__(self):

		self.current = [] # reset deck if in a new game scenario

		for suit in self.suits:

			for value in self.values:

				this = Cards(value, suit)
				self.current.append(this.card)

		random.shuffle(self.current)


	def drawCard(self):

		return self.current.pop()

	def countCards(self):

		return len(self.current)


	def __str__(self):

		return 'Current deck: {deck} - {len} Cards'.format(deck = self.current, len = len(self.current))



class Player: # individual player class. Stores bet, current hand and draws cards from the active game global's deck instance

	def __init__(self, name = 'Jeff', cash = 100, human = True):

		self.name = name
		self.cash = cash
		self.human = human
		self.bet = 0
		self.hand = []
		self.score = 0

	def __str__(self):

		if self.human:

			return 'Player: {p}, Cash: ${m}'.format(p = self.name, m = self.cash)

		else:

			return 'Player "{p}" is the computer'.format(p = self.name)

	def displayHand(self, game): # Displays hand dynamically based on if the hand belongs to the player or the dealer, or whether or not it's the player's or the dealer's turn.

		string = '{n}\'s Hand:\n  Score: {s}\n'.format(n = self.name, s = self.score)

		
		if self.human or not game.playerTurn:

			for card in self.hand:

				(value, suit) = card

				string += '\n  {v} of {s}'.format(v = value, s = suit)

			if self.human:
				string += '\n\n This Bet: ${b}'.format(b = self.bet)
				string += self.displayCash()

			print(string)
			print('')

		else:

			string += '\n  (Facedown Card)'

			i = 1

			while i < len(self.hand):

				(value, suit) = self.hand[i]

				string += '\n  {v} of {s}'.format(v = value, s = suit)

				i += 1

			print(string)
			print('')

	def displayCash(self):

		return '\n Cash: ${c}'.format(c = self.cash)


	def calculateHand(self, game):

		aceCount = []

		if game.playerTurn:

			self.score = 0

		else:

			self.score = 0

		if game.playerTurn and not self.human:

			i = 1

		else:

			i = 0

		while i < len(self.hand):

			(value, suit) = self.hand[i]

			if value == 'Ace':

				aceCount.append(value)
				i += 1

			else:

				try:

					self.score += int(value)

				except:

					self.score += 10

				finally:

					i += 1

		if len(aceCount) > 0:

			for ace in aceCount:

				if self.score < 11:

					self.score += 11

				else:

					self.score += 1



	def dealCards(self, game): # Draw first 2 initial cards.
		
		for i in range(2):

			card = game.deck.drawCard()
			self.hand.append(card) 




class Game: # For Tracking Game States & Playing Deck

	def __init__(self, goal, player, dealer):

		self.deck = Deck()
		self.goal = goal
		self.playerTurn = True
		self.player = player
		self.dealer = dealer


	def __str__(self):

		return 'Playing Round: {p}, Winning Goal: ${g}, Cards In Deck: {c}'.format(p = self.playing, g = self.goal, c = self.deck.countCards())


	def chooseAction(self):

		while True:

			choice = input('Enter "h" to hit, "s" to stay or "q" to quit (h/s/q): ').lower()


			if choice == 'h':
				self.hit()
				break

			elif choice == 's':
				self.stay()
				break

			elif choice == 'q':
				exit('\nThanks for playing!')


			else:

				print('\nInvalid Selection. Please try again.\n')
				continue

	def hit(self):
		card = self.deck.drawCard()

		if self.playerTurn:

			self.player.hand.append(card)
			self.player.calculateHand(self)
			self.player.displayHand(self)

			if self.player.score > 21:

				input('\nYou busted!! Better luck next round. Press enter to continue')
				self.playRound()

			elif len(self.player.hand) >= 5:

				input('\nYour hand exceeded 5 cards without busting. You win! Press enter to continue')
				self.player.cash += self.player.bet*2
				self.playRound()

			self.chooseAction()

		else:

			self.dealer.hand.append(card)
			self.dealer.calculateHand(self)
			self.dealer.displayHand(self)


	def stay(self):
		
		self.playerTurn = False
		self.dealer.calculateHand(self)

		while self.dealer.score < 17:
			print('Dealer Hits...\n')
			time.sleep(2)
			self.hit()

		print('Dealer Stays...\n')

		if self.dealer.score > 21:
			self.player.cash += (self.player.bet*2)
			self.player.displayCash()
			input('\nDealer busted!! You win. Press enter to continue')
			self.playRound()

		self.dealer.calculateHand(self)
		self.dealer.displayHand(self)

		if self.dealer.score > self.player.score:

			input('\nThe Dealer beat you. Better luck next round. Press enter to continue')
			self.playRound()

		elif self.dealer.score == 21 and self.player.score == 21:

			input('\nYou both got 21...unfortunately, the house always wins. Press enter to continue')
			self.playRound()

		else:
			self.player.cash += (self.player.bet*2)
			input('\nYou beat the Dealer! Press enter to continue')
			self.playRound()

	def winLoseCheck(self):

		if self.player.cash == 0:

			while True:

				choice = input('You\'ve run out of money and luck. Play again? (Y/N)').lower()

				if choice == 'y':

					init()
					break

				elif choice =='n':

					exit('Thanks for playing!')
					break

				else: 

					print('\nInvalid input, please try again\n')

		elif len(self.deck.current) < 9:

			while True:
				print('The deck doesn\'t have enough cards to continue.')
				print('You lose the game with ${c}. The goal was ${g}'.format(c = self.player.cash, g = self.goal))
				choice = input('Play again? (Y/N)').lower()

				if choice == 'y':

					init()
					break

				elif choice =='n':

					exit('Thanks for playing!')
					break

				else: 

					print('\nInvalid input, please try again\n')

		elif self.player.cash >= self.goal:

			while True:

				choice = input('You\'ve won the game with ${x}!!. Play again? (Y/N)'.format(x = self.player.cash)).lower()

				if choice == 'y':

					init()
					break

				elif choice =='n':

					exit('Thanks for playing!')
					break

				else: 

					print('\nInvalid input, please try again\n')


	def playRound(self):
		self.player.bet = 0
		self.dealer.score = 0
		self.player.score = 0

		self.winLoseCheck()

		while True:

			try:

				print(self.player.displayCash())
				bet = int(input('Enter an amount to bet: '))

			except: 

				print('\nBet must be a whole number\n')
				continue

			else: 

				if bet > self.player.cash:

					print('\nYou cannot bet more than you have in cash!\n')
					continue

				else:

					self.player.cash -= bet
					self.player.bet += bet
					break

		clear()
		self.playerTurn = True

		self.player.hand = []

		self.dealer.hand = []

		self.dealer.dealCards(self)

		self.dealer.calculateHand(self)
		
		self.player.dealCards(self)
		self.player.calculateHand(self)

		self.dealer.displayHand(self)
		self.player.displayHand(self)

		self.chooseAction()



#globals 

class Messages:

	def welcome(self):

		print(textwrap.fill('Welcome to blackjack! You will be dealt 2 cards in the beginning of a round and are expected to place a minimum bet of $5. The point of the game is to get a hand value as close to 21 as possible without "busting" (going over 21). You may "hit" (have a card dealt) as many times as you\'d like. If you don\'t want to hit any longer, you may "stay" and let the dealer go his round. If you get a total of 5 cards without busting, you win the round regardless of how close the dealer\'s hand value is to 21. If your total hand value is higher than the dealer\'s hand after the dealer\'s turn, you win as well. When you win, you get back double your bet. When you lose, you lose your bet. If you cannot bet any further, or the deck runs out of cards, you lose the game. If your cash exceeds the winning total, you win the game.', 75))
		print('')

echo = Messages()

def init(): # sets up initial game settings.
	clear()

	echo.welcome()

	name = input('Please enter your name: ')
	
	while True:
		
		try:

			money = int(input('Please enter your starting cash (minimum $5): '))

		except:

			print('\nPlease make sure your starting cash is a whole number.\n')

			continue

		else:

			if money < 5:

				print('\nPlease make sure your starting cash is at least $5\n')
				continue

			else:

				break

	while True:

		try:

			goal = int(input('Please enter the amount cash required to win: '))

		except:

			print('\nPlease make sure the winning amount is a whole number\n')
			continue

		else:

			if not goal >= (money * 2):

				print('\nYour target amount must be at least 2 times greater than your starting cash.\n')
				continue

			else:

				break

	
	player = Player(name, money, True)
	dealer = Player('Dealer', 0, False)
	game = Game(goal, player, dealer)
	clear()
	game.playRound()

	# goal = prompt('Please enter the goal amount to win the game (default is $500): ')

init()
	

