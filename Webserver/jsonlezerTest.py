import json

with open("testflowClientA.json", 'r')as jsonfile:
    data = json.load(jsonfile)
    print(data)
fsport = 3
data["flows"][2]["treatment"]["instructions"][0]["port"] = fsport

print(data["flows"][2])

print(data["flows"][3]["selector"]["criteria"][0]["port"])