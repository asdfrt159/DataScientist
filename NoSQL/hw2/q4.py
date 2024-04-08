from sys import argv
from pymongo import MongoClient

client = MongoClient()
db = client.disaster

def q4(longitude, latitude, ts):
    # TODO:
    pass
   
if __name__ == '__main__':
    q4(float(argv[1]), float(argv[2]), argv[3])
