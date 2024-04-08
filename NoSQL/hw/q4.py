from sys import argv
from pymongo import MongoClient

client = MongoClient()
db = client.movielens

def q4(input_userid: int):

    # TODO:
    ratings = db['ml_ratings']

    # movieId 로 index 생성
    ratings.create_index([('userId',1),('movieId',1)])

    # userId가 평가한 영화의 수
    N = ratings.count_documents({'userId': input_userid})

    result = []

    for i in ratings.distinct('movieId') :
        # user가 평가한 movie 에 대한 rating 정보
        val1 = list(ratings.find({'userId': input_userid,'movieId':i},{'rating':1,'_id':0}))

        # u가 평가한 movie 가 없으면 다음 user로 continue
        if len(val1) == 0 : 
            continue
        
        # user가 평가한 movie의 rating
        res1 = val1[0]['rating']

        # movie의 전체 사용자 rating의 평균
        val2 = list(ratings.find({'movieId' : i},{'rating':1, '_id':0}))
        res2 = [item['rating'] for item in val2]
        avg_val = sum(res2)/len(res2)

        result.append(res1-avg_val)

    # bias 계산
    bias = sum(result)/N
    print('{:.3f}'.format(bias))

if __name__ == '__main__':
    q4(int(argv[1]))
    

