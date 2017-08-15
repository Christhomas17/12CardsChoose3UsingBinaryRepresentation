# 12CardsChoose3UsingBinaryRepresentation
You have 12 cards, comprising 4 groups of 3 cards. We have to find the probability of choosing an entire group. For example, we could have [Biggest,Biggest,Biggest,Big, Big,Big, Small,Small,Small, Smallest, Smallest, Smallest]. We need to find the probability of choosing 3 biggest, 3 big, 3 small or 3 smallest before choosing 3 of the other kinds. 

First and foremost, I am taking no credit for creating this. User ead[https://stackoverflow.com/users/5769463/ead] created this in response to a question that I asked on Stackoverflow. I am only posting this here in order to create, what I consider, better documention about his method in case anyone else, like myself, was very very confused by his method and also amazed at the quickness. This method takes well under a second where as an R script using no functions takes a few minutes and a poorly designed Python script takes > 20 minutes. 

I have changed some of his function names for better readability and I have added comments but this is again, completely his code. 

```Python
#calculates probability to end the game with 3 cards of a type


N=12
```
This represents the total number of cards that we have

```Python
MAX=(1<<N)#max possible set is 1<<N-1
probs=[0.0]*MAX

#we always start with the empty set:
probs[0]=1.0    
```
EAD is using binary representation of a number to represent a set. For example, if we have a set [A,B,C,D] and we choose A and B, then we have [1,1,0,0] where the 1's are the letters we picked and the zeros are those that we didn't. Nothing fancy yet but here comes the amazingness. Rather than using a list to represent True and Falses, EAD uses a binary representation, using only 1's and 0's. I believe that this is because it much faster to access these numbers than any other data type.  1<<N means 1*2^N, or 2^12, the total possible permutations of either selecting a card or not.


```Python
#building bottom-up
for current_set in xrange(MAX):
    if end_group(current_set) is None:  #game not ended yet!
       decoded_set=decode_set(current_set)
       trans_probs=get_probs(decoded_set)
       for i, is_set in enumerate(decoded_set):
           if not is_set:
              new_set=current_set | (1<<i) 
              probs[new_set]+=probs[current_set]*trans_probs[i]

```
This code is cycling through every possible permutation. 
```Python
if end_group(current_set) is None:  #game not ended yet!
```
1) Each set, end_group(current_set) checks if this is a winning selection, i.e. we have chosen 3 cards from the same group. If we have, then we do nothing. If we don't have 3 from the same group, we continue.
```Python
decoded_set=decode_set(current_set)
```
2) decode_set(current_set) returns a list of True/False values where True represents if the card is chosen and False represents when the card isn't chosen. 
```Python
trans_probs=get_probs(decoded_set)
```
3) get_probs(decoded_set) uses the list just returned and returns a list of conditional probabilities of choosing the cards that were not selected

```Python
for i, is_set in enumerate(decoded_set):
           if not is_set:
              new_set=current_set | (1<<i) 
              probs[new_set]+=probs[current_set]*trans_probs[i]
```              
              
4) new_set is our current_set combined with a new card being chosen. For example, current set could be 010000100000, which means cards 0,1,and 6 have been chosen. If i is 6, we have 1<<6 which is the same as 1*2^6 which is 1000000 in binary. So, by using the
```Python
current_set | (1<<i)
```
we are comparing each bit(byte? I'm not really sure) using an or statement so the final result would be 110000100000, where the first digit has been replaced with a 1. 

```Python
And what's the probability of getting to this new step? The probability of being at the prior step(current_step) times the probability of picking that first card. If we already had that card, then it's 0 which makes perfect sense. 
```

#And here is where actually calculate the finally probabilities and print them. 
```Python
#filtering wins:
group_probs=[0.0]*4
for current_set in xrange(MAX):
   group_won=end_group(current_set)
   if group_won is not None:
      group_probs[group_won]+=probs[current_set]


print zip(["Grand", "Major", "Minor", "Bonus"], group_probs)
```
We cycle through each state, using group_won to determine if we have chosen 3 cards from the same group on this current state.
```Python
if group_won is not None:
      group_probs[group_won]+=probs[current_set]
```
This is used to calculate the total probability of each state. group_won returns 0 if 3 cards are chosen from the first group, 1 if 3 are chosen from the second group etc. This is adding the probability from that given state to the probability of choosing 3 from the given group.



#Below are the functions that have already been used in greater detail

```Python
#set representation int->list
def decode_set(encoded):
    decoded=[False]*N
    for i in xrange(N):
        if encoded&(1<<i):
            decoded[i]=True
    return decoded
    
```
This function cycles through all 12 positions and returns a list of True/False values where True are those cards that are chosen and False are those that are not.



```Python
weights = [170000, 170000, 105, 170000, 170000, 215, 150000, 150000, 12000, 105000, 105000, 105000]    
```
These are the initial weights of the 12 cards

```Python
def get_probs(decoded_set):
    denom=float(sum((w for w,is_taken in zip(weights, decoded_set) if not is_taken)))
    return [w/denom if not is_taken else 0.0 for w,is_taken in zip(weights, decoded_set)]
```
The denom line is summing all of the values where we have a False, i.e. the card was not chosen. the return line is returning a list of conditional probabilities of choosing each of the cards that have yet to be selected. 


```Python
def end_group(encoded_set):
    for i in xrange(4):
       whole_group =  7<<(3*i) 
       if (encoded_set & whole_group)==whole_group:
           return i
    return None
```

This function is used to find those groupings where 3 cards are chosen from the same group, i.e. the first 3 cards, the next 3 cards and so on. Encoded set will be an integer between 0 and 2^(max number of cards. In this case 12)-1.We are subtracting 1 because Python starts counting at 0. 

```Python
whole_group =  7<<(3*i) 
```

This line took me a while to figure out until I simply did the calculations. 

| i        | Integer Value           | Binary Representation  |
|:------------- |:-------------:| -----:|
| 0     | 7 | 111 |
| 1      | 56      |   111000 |
| 2 | 448     |    111000000 |
| 3 | 3584    |    111000000000 |

So as you can see, the whole_group variable 







