from random import randint
from functools import reduce

MARKER_INTERVAL = 5
MAX_NUM_PILES = 100
MAX_STONES_IN_PILE = 80

def draw_piles( lst ):
    num_markers = max(lst) // MARKER_INTERVAL
    if num_markers > 0:
        print('   *',end='')
    for i in range(num_markers):
        if i == num_markers - 1:
            print('    *')
        else:
            print('    *', end='')
    pile_num = 0
    for el in lst:
        if pile_num < 10:
            print('0',end='')
        print(str(pile_num)+': ',end='')
        pile_num += 1
        for i in range(el):
            if i == el-1:
                print('#')
            else:
                print('#', end='')
    print()
    return

# Choose Player 2
while True:
    try:
        ai = input('Play with Human or AI?\n')
        if ai.upper() == 'A' or ai.upper() == 'AI':
            ai = input('Random or Intelligent?\n')
            if ai.upper() == 'R' or ai.upper() == 'RANDOM':
                ai = 'R'
            elif ai.upper() == 'I' or ai.upper() == 'INTELLIGENT':
                ai = 'I'
            else:
                raise ValueError
        elif ai.upper() == 'H' or ai.upper() == 'HUMAN':
            ai = 'H'
        else:
            raise ValueError
        break
    except ValueError:
        print('Invalid AI code')

# Get number of piles
while True:
    try:
        num_piles = int(input('Number of Piles:\n'))
        if num_piles < 1 or num_piles > MAX_NUM_PILES:
            raise ValueError
        break
    except ValueError:
        print('Number of piles must be a positive integer between 1 and %i' % MAX_NUM_PILES)

piles = []
# Populate piles with stones
for i in range(num_piles):
    while True:
        try:
            num_stones = int(input('Stones in Pile %i:\n'%i))
            if num_stones < 1 or num_stones > MAX_STONES_IN_PILE:
                raise ValueError
            else:
                piles.append(num_stones)
            break
        except ValueError:
            print('Number of stones must be a positive integer between 1 and %i' % MAX_STONES_IN_PILE)

turn = 0
# While there are still stones on the board
while piles:
    # Display current game state
    draw_piles(piles)
    if turn == 0 or (turn == 1 and ai == 'H'):
        print('Player %i Turn' % (turn+1))
        # Choose pile to take from
        while True:
            try:
                take_pile = int(input('Take from Pile '))
                if take_pile < 0 or take_pile > len(piles)-1:
                    raise ValueError
                break
            except ValueError:
                print('Pile number should be an integer between 0 and %i' % (len(piles)-1))
        # Choose how many stones to take from pile
        while True:
            try:
                stones_taken = int(input('Number of stones to take: '))
                if stones_taken < 1 or stones_taken > piles[take_pile]:
                    raise ValueError
                break
            except ValueError:
                print('Number of stones taken should be an integer between 1 and %i' % (piles[take_pile]))
    elif turn == 1:
        if ai == 'R':
            print('Computer Turn')
            take_pile = randint(0,len(piles)-1)
            stones_taken = randint(1,piles[take_pile])
            print('Computer took %i stones from Pile %i' % (stones_taken, take_pile))
        if ai == 'I':
            print('Computer Turn')
            nim_sum = reduce(lambda x, y: x ^ y, piles)
            if nim_sum != 0:
                for i in range(len(piles)):
                    if nim_sum ^ piles[i] < piles[i]:
                        take_pile = i
                        stones_taken = piles[i] - (nim_sum ^ piles[i])
            else:
                take_pile = randint(0,len(piles)-1)
                stones_taken = randint(1,piles[take_pile])
            print('Computer took %i stones from Pile %i' % (stones_taken, take_pile))
    # Take away stones from pile
    piles[take_pile] -= stones_taken
    # Remove piles with zero stones
    piles = list(filter(lambda num: num != 0, piles))
    if piles:
        turn = 1 - turn
    else:
        if turn == 0 or (turn == 1 and ai == 'H'):
            print('Player %i Wins' % (turn+1))
        else:
            print('Computer Wins')
