from sys import argv
from pymongo import MongoClient

client = MongoClient()
db = client.disaster

def q3(m, r):
    # TODO:
    pass

if __name__ == '__main__':
    q3(float(argv[1]), float(argv[2]))
