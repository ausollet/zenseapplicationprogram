# zenseapplicationprogram
web server containing a 7x7 minesweeper game with 16 mines to apply for joining zense.
first run the program by passing the command: 
:~$ python zense.py runserver xxx.x.x.x:xxx (here xxx.x.x.x:xxx is the public ip of the host or the system that hosts the server. if not public ip is passed, then the default is 127.0.0.1:5000, in which case the server is accessible only by the host)
once an user has logged in, you (the host) can see his minsweeper grid in matrix format.

if the webpage is to be accessed via the same wifi, then access http://<public-ip of host>
first you are redirected to the start page, where some content about this server will be displayed.You can choose whether you want to read the next page or Login/Register. You will be redirected to Login page or Register page by clicking their respective buttons on the navbar.
After registration, you will be sent a confirmation mail. after clicking on the confirmation link, you can login to your account, prior to which you will be denied access to your account.
After logging in, you can either choose to view your personal details, return to home page(if you are not already in that page) where you can play the 7x7 minesweeper game.you can play the game by clicking on the buttons, if you land on a mine, it is game over for you. The home and personal details button can be accessed from the navigation bar.
       
