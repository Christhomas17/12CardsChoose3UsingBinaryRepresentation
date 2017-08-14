#calculates probability to end the game with 3 cards of a type


N=12

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

MAX=(1<<N)#max possible set is 1<<N-1
probs=[0.0]*MAX

#we always start with the empty set:
probs[0]=1.0    
#building bottom-up
for current_set in xrange(MAX):
    if end_group(current_set) is None:  #game not ended yet!
       decoded_set=decode_set(current_set)
       trans_probs=get_probs(decoded_set)
       for i, is_set in enumerate(decoded_set):
           if not is_set:
              new_set=current_set | (1<<i) 
              probs[new_set]+=probs[current_set]*trans_probs[i]

#filtering wins:
group_probs=[0.0]*4
for current_set in xrange(MAX):
   group_won=end_group(current_set)
   if group_won is not None:
      group_probs[group_won]+=probs[current_set]


print zip(["Grand", "Major", "Minor", "Bonus"], group_probs)