from sys import argv
from pymongo import MongoClient

client = MongoClient()
db = client.disaster

def q2(r):
    pass

if __name__ == '__main__':
    q2(float(argv[1]))

