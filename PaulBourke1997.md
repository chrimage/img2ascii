# Character representation of grey scale images

Written by [Paul Bourke](../)\
February 1997

"Standard" character ramp for grey scale pictures, black -> white.

```
"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,"^`'. "
```

A more convincing but shorter sequence for representing 10 levels of grey is

```
" .:-=+*#%@"
```

An obvious problem is the variation in apparent density between some typefaces.\
Another issue is the stretching in height due to the rectangular aspect ratio of characters. When creating such images by software by sampling "real" images it is common to sample half as often in the vertical direction. Of course if the aspect ratio of the font being used is known then exact vertical and horizontal sampling can occur.

As an example consider the following grey scale ramp on the left and the corresponding ASCII character representation on the right.


```
=======--------:::::::::........                  
=========--------:::::::::........                
++=========--------:::::::::........              
++++========---------:::::::::........            
++++++========---------:::::::::........          
++++++++=========--------:::::::::........        
*+++++++++=========--------:::::::::........      
***+++++++++=========--------:::::::::........    
******++++++++=========--------:::::::::........  
********++++++++=========--------:::::::::........
#*********++++++++=========--------:::::::::......
###*********++++++++=========--------:::::::::....
#####********+++++++++=========--------:::::::::..
#######********+++++++++=========--------:::::::::
#########*********++++++++=========--------:::::::
%%#########********+++++++++========---------:::::
%%%%#########********+++++++++=========--------:::
%%%%%%#########********+++++++++=========--------:
%%%%%%%%#########*********++++++++========--------
@@%%%%%%%%#########********+++++++++========------
@@@@%%%%%%%%#########*********++++++++========----
@@@@@@%%%%%%%%#########********+++++++++=========-
@@@@@@@@%%%%%%%%########1********+++++++++========
@@@@@@@@@@%%%%%%%%######*********++++++++======
@@@@@@@@@@@@%%%%%%%%#####********+++++++++====
```
