# 12CardsChoose3UsingBinaryRepresentation
You have 12 cards, comprising 4 groups of 3 cards. We have to find the probability of choosing an entire group.

First and foremost, I am taking no credit for creating this. User ead[https://stackoverflow.com/users/5769463/ead] created this in response to a question that I asked on Stackoverflow. I am only posting this here in order to create, what I consider, better documention about his method. 

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
1) Each set, end_group(current_set) checks if this is a winning selection, i.e. we have chosen 3 cards from the same group. 
2) decode_set(current_set) returns a list of True/False values where True represents if the card is chosen and False represents when the card isn't chose. 
3) get_probs(decoded_set) uses the list just returned and finds the prob 

#set representation int->list
def decode_set(encoded):
    decoded=[False]*N
    for i in xrange(N):
        if encoded&(1<<i):
            decoded[i]=True
    return decoded

weights = [170000, 170000, 105, 170000, 170000, 215, 150000, 150000, 12000, 105000, 105000, 105000]     
def get_probs(decoded_set):
    denom=float(sum((w for w,is_taken in zip(weights, decoded_set) if not is_taken)))
    return [w/denom if not is_taken else 0.0 for w,is_taken in zip(weights, decoded_set)]

def end_group(encoded_set):
    for i in xrange(4):
       whole_group =  7<<(3*i) #7=..000111, 56=00111000 and so on
       if (encoded_set & whole_group)==whole_group:
           return i
    return None


#MAIN: dynamic program:




#filtering wins:
group_probs=[0.0]*4
for current_set in xrange(MAX):
   group_won=end_group(current_set)
   if group_won is not None:
      group_probs[group_won]+=probs[current_set]


print zip(["Grand", "Major", "Minor", "Bonus"], group_probs)

