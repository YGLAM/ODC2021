The first thing I've done was an inspection of the site, registring a user and checking out the offered features:
- clicking on your name saves to the browser a file called "replay" displaying the following text
'''
  O:4:"User":5:{s:4:"name";s:11:"zerocalcare";s:2:"id";i:7500;s:7:"isAdmin";b:0;s:6:"solved";a:0:{}s:6:"points";i:0;}
'''
The points of interest in this case are the "isAdmin" and "solved"
This challenge, being based in php will either exploit
- register globals : automatically register HTT
