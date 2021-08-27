song = input('enter a song:')
song1 =song.replace('a', 'B')
song2 = song1.replace('A', 'a')
song3 = song2.replace('B', 'A')

l = len(song)
numberOf_a = song.count('a')
numberOf_A = song.count('A')

numberWithNo_Aa = l - numberOf_a - numberOf_A

percent = (numberOf_a + numberOf_A)/l*100

print('\n\n',song, '\n\n', song3, "\n\nNumber of characters without characters 'a' and 'A':",numberWithNo_Aa,"\n\nPercentage of characters 'a' and 'A' in song:",percent,'%')


##======================================================= RESTART: C:/Users/97250/Desktop/פייתון/ex2.py ======================================================
##enter a song:"Some things in life are bad They can really make you mad Other things just make you swear and curse When you're chewing on life's gristle Don't grumble, give a whistle And this'll help things turn out for the best And Always look on the bright side Of life Always look on the light side Of life"
##
##
## "Some things in life are bad They can really make you mad Other things just make you swear and curse
##When you're chewing on life's gristle Don't grumble, give a whistle And this'll help things turn out for the best
##And Always look on the bright side Of life Always look on the light side Of life" 
##
## "Some things in life Are bAd They cAn reAlly mAke you mAd Other things just mAke you sweAr And curse
##When you're chewing on life's gristle Don't grumble, give A whistle and this'll help things turn out for the best
##and alwAys look on the bright side Of life alwAys look on the light side Of life" 
##
##Number of characters without characters 'a' and 'A': 280 
##
##Percentage of characters 'a' and 'A' in song: 5.405405405405405 %
