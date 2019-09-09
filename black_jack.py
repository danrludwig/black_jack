from deck import Deck
import time
deck = Deck()

def sum_card_value(myList):
    values = []
    for i in range(len(myList)):
        a = myList[i].getCardValue()
        if a == 11 or a == 12 or a == 13:
            a = 10
        if sum(values) > 10 and a == 14:
            a = 1
        elif sum(values) < 10 and a == 14:
            a = 11
        values.append(a)
    return sum(values)

def main():
    deck.shuffle()
    players = True
    while players:
        num_of_players = eval(input('How many players? (1-5): '))
        if num_of_players <= 5 and num_of_players >= 1:
            players = False
        num_of_players += 1

    balance = [100] * num_of_players

    playing = True

    while playing:
        player_hands = []
        player_bets = []
        busts = []
        holds = []

        for i in range(num_of_players):
            player_hands.append([])

        for i in range(num_of_players - 1):
            betSize = True
            while betSize:
                print('Current balance for player' + str(i + 1) + ': ' + str(balance[i]))
                bet = eval(input('Enter bet amount for player' + str(i + 1) + ': '))
                if bet >= 5:
                    player_bets.append(bet)
                    betSize = False
                else:
                    print('Bet needs to be at least $5.')
                if bet > balance[i]:
                    print('You don\'t have enough money to bet that much.')
                    betSize = True

        for i in range(2):
            for j in range(len(player_hands)):
                player_hands[j].append(deck.draw())

        print('\nDealer\'s second card is the', player_hands[num_of_players - 1][1], '\n')

        for i in range(num_of_players - 1):
            print('Player' + str(i + 1) + '\'s hand is: ')

            for j in range(len(player_hands[i])):
                print(player_hands[i][j])
            print('\n')

            another = True
            while another:
                another = eval(input('1) Hit\n2) Hold\nChoose action: '))
                if another == 1:
                    player_hands[i].append(deck.draw())
                    for j in range(len(player_hands[i])):
                        print(player_hands[i][j])
                    print('\n')
                    if sum_card_value(player_hands[i]) > 21:
                        print('Player' + str(i + 1) + ' busts\n')
                        busts.append(i)
                        another = False
                elif another == 2:
                    holds.append(i)
                    another = False
                else:
                    print('Invalid choice.')

        print('\nDealer\'s hand:')
        for j in range(len(player_hands[num_of_players - 1])):
            print(player_hands[num_of_players - 1][j])
        bigEnough = False
        while not bigEnough:
            total = sum_card_value(player_hands[num_of_players - 1])
            if total >= 17:
                bigEnough = True
                if total > 21:
                    print('The dealer busts.')
                    dealer_busts = True
                elif total <= 21:
                    print('The dealer holds.')
                    dealer_busts = False
            elif total < 17:
                time.sleep(1)
                player_hands[num_of_players - 1].append(deck.draw())
                print('\nThe dealer takes a card.')
                print('Dealer\'s new card is the', player_hands[num_of_players - 1][len(player_hands[num_of_players - 1]) - 1])

        if dealer_busts == True:
            for i in holds:
                balance[i] += player_bets[i]
                print('Player' + str(i + 1) + ' wins, and has a balance of', balance[i])
            for i in busts:
                balance[i] -= player_bets[i]
                print('Player' + str(i + 1) + ' loses, and has a balance of', balance[i])
        if dealer_busts == False:
            for i in holds:
                if sum_card_value(player_hands[i]) > sum_card_value(player_hands[num_of_players - 1]):
                    balance[i] += player_bets[i]
                    print('Player' + str(i + 1) + ' wins, and has a balance of', balance[i])
                elif sum_card_value(player_hands[i]) == sum_card_value(player_hands[num_of_players - 1]):
                    print('Player' + str(i + 1) + ' ties, and has a balance of', balance[i])
                elif sum_card_value(player_hands[i]) < sum_card_value(player_hands[num_of_players - 1]):
                    balance[i] -= player_bets[i]
                    print('Player' + str(i + 1) + ' loses, and has a balance of', balance[i])
            for i in busts:
                balance[i] -= player_bets[i]
                print('Player' + str(i + 1) + ' loses, and has a balance of', balance[i])

        again = input('Enter "Y" if you would like to play again: \n')
        again.lower()
        if again == 'y':
            for i in range(num_of_players):
                if balance[i] <= 0:
                    balance[i] += 20
                    print('Player' + str(i + 1) + ' was given an extra $20 in their account to continue playing.')
        elif again != 'n':
            print('Thank you for playing!')
            for i in range(num_of_players - 1):
                print('Player' + str(i + 1) + ' has a balance of', balance[i])
            playing = False


main()
