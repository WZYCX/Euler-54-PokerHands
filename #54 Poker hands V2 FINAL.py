#54  Poker hands
#V1: Problem solved
#V2: CORRECT
'''
----------Rankings (Low to High)-----------
High Card (0): Highest value card. X
One Pair (1): Two cards of the same value. X
Two Pairs (2): Two different pairs. X
Three of a Kind (3): Three cards of the same value. X
Straight (4): All cards are consecutive values.
Flush (5): All cards of the same suit. X
Full House (6): Three of a kind and a pair. X
Four of a Kind (7): Four cards of the same value. X
Straight Flush (8): All cards are consecutive values of same suit.
Royal Flush (9): Ten, Jack, Queen, King, Ace, in same suit.
-------------------------------------------

Order of value : 2 , 3 , 4 , 5 , 6 , 7, 8, 9 , T , J , Q , K , A

-------------------------------------------

'''
import urllib.request

file= open("#54 Poker Hands results FINAL.txt","w+")

#requesting hands file from URL
def pokerHands():
    hands = []
    file=urllib.request.urlopen("https://projecteuler.net/project/resources/p054_poker.txt")  
    for line in file: 
        line = line.decode("utf-8")
        hands.append([line[:15].split(),line[15:].split()]) 
    #pprint.pprint(hands) #debug
    return hands
    


#works out hand score
def checkScore(hand):
    #cards are ["2","3","4","5","6","7","8","9","T","J","Q","K","A"]
    numbers = []
    suits = []
    rank = 0
    #sort in card value order
    SORT_ORDER = {"2": 0, "3": 1, "4": 2,"5": 3, "6": 4, "7": 5,"8": 6, "9": 7, "T": 8,"J": 9, "Q": 10, "K": 11,"A": 12}
    hand.sort(key=lambda val: SORT_ORDER[val[0]])
    #split into numbers and suits
    for i in hand:
        numbers.append(i[0])
        suits.append(i[1])
    #print(numbers,"and",suits) #debug
    #Turn letters into numbers
    for i in range(0,len(numbers)):
        a = numbers[i]
        #print(a) # debug
        if a == "T":
            numbers[i] = "10"
        elif a == "J":
            numbers[i] = "11"
        elif a == "Q":
            numbers[i] = "12"
        elif a == "K":
            numbers[i] = "13"
        elif a == "A":
            numbers[i] = "14"
    print(numbers,"and",suits) #debug 
    #this is all to be removed: it is to write in all p1 wins for debugging
    file.write(str(numbers)+" and "+str(suits)+"\n") # input in text file (used once)

    # pairs, threes or fours
    unit = 0
    repeats =False
    for i in numbers:
        repeat = 0
        
        for y in numbers:
            #print(i)
            #print(y)
            if i == y:
                repeat+=1
                if repeat>1:
                    unit = int(y) # saves largest repeated value for 'draw checking'
        # all ranks divided by their repeat to account for 'double' counting
        if repeat ==2: # pair / two pair
            repeats =True
            rank+=1/2
            #print("+0.5") # debug
        elif repeat == 3: # three same
            repeats =True
            if rank==1:
                rank = 6 # Full House
            else:
                rank = 3 # Three of a Kind
        elif repeat == 4: # Four of a Kind
            repeats =True
            rank = 7
        #print(unit) # debug
    
    # flushes
    sameSuit = True
    for i in suits:
        if i != suits[0]:
            sameSuit=False
    if sameSuit == True:
        if rank < 5:
            rank= 5 #Flush

    # straights
    if int(numbers[-1])-int(numbers[0]) ==4 and repeats == False: # PROBLEM: does not check for repeated numbers. If numbers are repeated, a straight is not possible 
        if sameSuit == True:
            rank = 8 # straight flush
            if numbers[-1] == "14":
                rank = 9 # royal flush
        else:
            if rank < 4:
                rank = 4 
    return int(rank), numbers, unit

# finds the highest pair or card for a draw in rank
def draw(p1score,numbers1,unit1,numbers2,unit2):
    if unit1 > unit2 and (p1score == 1 or p1score == 2 or p1score == 3 or p1score == 6 or p1score == 7):
        return 1
    elif unit1 < unit2 and (p1score == 1 or p1score == 2 or p1score == 3 or p1score == 6 or p1score == 7):
        return 2
    else:
        # highest card
        for i in range(1,len(numbers1)+1):
            a = int(numbers1[-i])
            b = int(numbers2[-i])
            if a > b:
                return 1
            elif a < b:
                return 2

#ive missed if first pair of two pair draws *NOT THE PROBLEM*
            

#main game running
def pokerGame(playerhands):
    player1 = playerhands[0]
    player2 = playerhands[1]
    #print("Player 1 hand: ",player1)  # debug
    #print("Player 2 hand: ",player2)  # debug

    player1score,numbers1,unit1 = checkScore(player1)
    player2score,numbers2,unit2 = checkScore(player2)
    #print("Player 1 score: ",player1score) # debug
    #print("Player 2 score: ",player2score) # debug
    
    #calculates winner
    #player 1 wins
    if player1score > player2score:
        print("Player 1 Wins!")
        file.write("Player 1 Wins!\n") # input in text file (used once)
        return 1
    #player 2 wins
    elif player1score < player2score:
        print("Player 2 Wins!")
        file.write("Player 2 Wins!\n") # input in text file (used once)
        return 2
    else:
        #draw (highest card)
        if draw(player1score,numbers1,unit1,numbers2,unit2) == 1:
            print("Player 1 Wins!")
            file.write("Player 1 Wins!\n") # input in text file (used once)
            return 1
        else:
            print("Player 2 Wins!")
            file.write("Player 2 Wins!\n") # input in text file (used once)
            return 2
    

#pokerGame([['3S', '5D', '5H', '6D', '7C'],['2H', '3D', '5C', '5S', 'JC']]) # debug


#working out the outcomes of all games in .txt file
allhands = pokerHands()
player1wins = 0
player2wins = 0
for i in allhands:
    file.write("----------------------------------\n")# input in text file (used once)
    win = pokerGame(i)
    if win == 1:
        player1wins += 1
    elif win==2:
        player2wins +=1

print(player1wins)
file.write(str(player1wins)) # input in text file (used once)
# answer is 376
