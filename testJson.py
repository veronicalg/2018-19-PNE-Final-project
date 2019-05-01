# CLIENT PROGRAM IN ORDER TO PROVE THE ADVANCED LEVEL:
import http.client
import json

PORT = 8000
SERVER = 'localhost'

print("\nConnecting to server: {}:{}\n".format(SERVER, PORT))

# Connect with the server
conn = http.client.HTTPConnection(SERVER, PORT)



# ENDPOINT 1
conn.request("GET", "/geneList?chromo=1&start=0&end=30000&json=1")
r1 = conn.getresponse()
print("Response received!: {} {}\n".format(r1.status, r1.reason))
data1 = r1.read().decode("utf-8")
response = json.loads(data1)
print("JSON FOR ENDPOINT 1 :", response)

# ENDPOINT 2
conn.request("GET", "/listSpecies?json=1")
r1 = conn.getresponse()
print("Response received!: {} {}\n".format(r1.status, r1.reason))
data1 = r1.read().decode("utf-8")
response = json.loads(data1)
print("JSON FOR ENDPOINT 2 :", response)

# ENDPOINT 3
conn.request("GET", "/listSpecies?limit=10&json=1")
r1 = conn.getresponse()
print("Response received!: {} {}\n".format(r1.status, r1.reason))
data1 = r1.read().decode("utf-8")
response = json.loads(data1)
print("JSON FOR ENDPOINT 3 :", response)

# ENDPOINT 4 :
conn.request("GET", "/karyotype?specie=MOUSE&json=1")
r1 = conn.getresponse()
print("Response received!: {} {}\n".format(r1.status, r1.reason))
data1 = r1.read().decode("utf-8")
response = json.loads(data1)
print("JSON FOR ENDPOINT 4 :", response)

# ENDPOINT 5 :
conn.request("GET", "/listSpecies?limit=&json=1")
r1 = conn.getresponse()
print("Response received!: {} {}\n".format(r1.status, r1.reason))
data1 = r1.read().decode("utf-8")
response = json.loads(data1)
print("JSON FOR ENDPOINT 5 :", response)

# ENDPOINT 6 :
conn.request("GET", "/geneSeq?gene=FRAT1&json=1")
r1 = conn.getresponse()
print("Response received!: {} {}\n".format(r1.status, r1.reason))
data1 = r1.read().decode("utf-8")
response = json.loads(data1)
print("JSON FOR ENDPOINT 6 :", response)

# ENDPOINT 7 :
conn.request("GET", "/geneInfo?gene=FRAT1&json=1")
r1 = conn.getresponse()
print("Response received!: {} {}\n".format(r1.status, r1.reason))
data1 = r1.read().decode("utf-8")
response = json.loads(data1)
print("JSON FOR ENDPOINT 7 :", response)

# ENDPOINT 8 :
conn.request("GET", "/geneCal?gene=FRAT1&json=1")
r1 = conn.getresponse()
print("Response received!: {} {}\n".format(r1.status, r1.reason))
data1 = r1.read().decode("utf-8")
response = json.loads(data1)
print("JSON FOR ENDPOINT 8 :", response)

