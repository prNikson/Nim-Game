## Tim Liu
## TCSS 142
## Charles Bryan

import random

MIN_COUNT_OF_STONES = 1
MAX_COUNT_OF_STONES = 9
MIN_COUNT_OF_PILE = 2
MAX_COUNT_OF_PILE = 5

def main():
    # Define an empty rocklist to append rocks to, define random integers, call functions
    rockList = []
    randPile = random.randint(MIN_COUNT_OF_PILE, MAX_COUNT_OF_PILE)
    randRock = random.randint(MIN_COUNT_OF_STONES, MAX_COUNT_OF_STONES)
    players_tuple = get_players()
    player = players_tuple[random.randint(0, 1)] # Set current player to 1 (for switching later)
    name1, name2 = players_tuple
    
    get_board(rockList, randPile, randRock) # Set initial board
    play_again(rockList, randPile, randRock, name1, name2, player) 

# Post: takes no arguments and returns the player names as strings entered by the user            
def get_players():
    while True:
        name1 = input("Enter player 1 name: ")
        if len(name1) < 3:
            print("Very short nickname. Limitation for input - from 3 for 16 characters. Try again")
        elif len(name1) > 10:
            print("Very long nickname. Limitation for input - from 3 for 16 characters. Try again")
        else:
            break
    while True:
        name2 = input("Enter player 2 name: ")
        if len(name2) < 3:
            print("Very short nickname. Limitation for input - from 3 for 16 characters. Try again")
        elif len(name2) > 10:
            print("Very long nickname. Limitation for input - from 3 for 16 characters. Try again")
        else:
            break
    return name1, name2

# Pre : accepts empty rockList, random pile and rock as integers, current player as string
# Post: modifies rockList with random piles and stones, prints initial starting board
def get_board(rockList, randPile, randRock):

    # Get initial board
    print("Let's look at the board now.")
    print("-" * 25)
    for i in range(0, randPile):
        randRock = random.randint(1, 8)
        print('Pile {}: {}'.format(i + 1, 'O' * randRock))
        rockList.append(randRock)
    print("-" * 25)

    # Call nim function to display computer hints
    nim_sum(rockList, randPile)

# Pre : accepts modified rockList, random integer for piles, current player as string
# Post: returns a string when input is invalid, updates game board for following turns
def get_valid_input(rockList, randPile, player):

    # Begin loop that tests for valid input - if valid, break loop - if not, keep asking
    while True:
        stones = input('{}, how many stones to remove? '.format(player))
        if valid_stones_count(stones, rockList):
            break
        print(f"You can enter from {min(rockList)} to {max(rockList)} stones, and you have entered {stones}. Try again")

    while True:   
        piles = input('Pick a pile to remove from: ')
        if valid_piles_count(piles, stones, rockList):
            break

    rockList[int(piles) - 1] -= int(stones)
        

    # Keep playing game
    continue_game(rockList, randPile, player)

def valid_stones_count(stones: int, rockList: list[int]) -> bool:
    if stones and stones.isdigit() and int(stones) >= 1 and int(stones) <= max(rockList):
        return True
    return False

def valid_piles_count(piles: int, stones: int, rockList: list[int]) -> bool:
    if piles and piles.isdigit() and int(piles) >= 1 and int(piles) <= len(rockList):
        if rockList[int(piles) - 1] - int(stones) < 0:
            print(f"You can`t remove {stones} stones from {piles} pile. Try again")
            return False
        return True
    print(f"You can enter from 1 to {len(rockList)} piles, and you entered {piles}. Try again")
    return False

# Pre : accepts modified rockList, random integer for piles, current player as string
# Post: prints out updated game board after moves have been made, displays computer hint
def continue_game(rockList, randPile, player): 
    print("Let's look at the board now.")
    print("-" * 25)
    for i in range(0, randPile):
        print("Pile {}: {}".format(i + 1, 'O' * rockList[i]))

    print("-" * 25)

    # In the case when game is over, do not display computer hint for empty board
    if rockList != [0] * len(rockList):
        nim_sum(rockList, randPile)

    #print(rockList)

# Pre : accepts modified rockList, random integer for piles, names of players, current palyer as string
# Post: prints winner of game, asks if players want to play game again, determine current player
def play_again(rockList, randPile, randRock, name1, name2, player):

    # Begin loop to initiate player switching
    while True:
        get_valid_input(rockList, randPile, player)
        
        # To determine winner, check if rockList contains all 0's on that player's turn
        if rockList == [0] * len(rockList):
            print("{} is the winner of this round!".format(player))
            user = input("Do you want to play again? Enter y for yes, any characters for no: ")

            if user.lower() == 'y':
                # reset all conditions, start the game again
                rockList = []
                randPile = random.randint(2, 5)
                name1, name2 = get_players()
                player = name1
                get_board(rockList, randPile, randRock)
                get_valid_input(rockList, randPile, player)
                
            else:
                break
            
        # switch players 2->1, 1->2 
        if player == name1:
            player = name2

        else:
            player = name1

# Pre : accepts modified rockList, random integer for piles
# Post: calculates nim sum and prints the computer hint for optimal moves
def nim_sum(rockList, randPile):
    nim = 0

    # Calculate nim sum for all elements in the rockList
    for i in rockList:
        nim = nim ^ i
        
    print("Hint: nim sum is {}.".format(nim))

    # Determine how many rocks to remove from which pile
    stones_to_remove = max(rockList) - nim
    stones_to_remove = abs(stones_to_remove)    

    # Logic for certain configurations on determining how many stones to remove from which pile
    # "rockList.index(max(rockList))+ 1 )" determines the index in rockList at which the biggest
    # pile of stones exists.
    if (nim > 0) and (len(rockList) > 2) and (nim != max(rockList)) and (nim !=1):
        print("Pick {} stones from pile {}".format(stones_to_remove, rockList.index(max(rockList))+ 1 ))

    if (nim > 0) and (len(rockList) > 2) and (nim == max(rockList)) and (nim !=1):
        print("Pick {} stones from pile {}.".format(nim, rockList.index(max(rockList))+ 1 ))

    if nim > 0 and len(rockList) <= 2 and (stones_to_remove != 0):
        print("Pick {} stones from pile {}".format(stones_to_remove, rockList.index(max(rockList))+ 1 ))

    if nim > 0 and len(rockList) <= 2 and (stones_to_remove == 0):
        print("Pick {} stones from pile {}".format(nim, rockList.index(max(rockList))+ 1 ))

    elif (nim == 1) and (len(rockList) <= 2):
        print("Pick {} stones from pile {}".format(nim, rockList.index(max(rockList))+ 1 ))

    if (nim == 1) and (nim == max(rockList)) and (nim != 0) and (len(rockList) > 2):
        print("Pick {} stones from pile {}".format(nim, rockList.index(max(rockList))+ 1))
        
    if nim == 0:
        print("Pick all stones from pile {}.".format(rockList.index(max(rockList))+ 1 ))

main()
