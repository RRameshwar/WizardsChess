import httplib, urllib

h1 = httplib.HTTPConnection("http://localhost:8000")
h1.request("POST", "http://localhost:8000", "Hello")

response = conn.getresponse()
data = response.read()
conn.close()