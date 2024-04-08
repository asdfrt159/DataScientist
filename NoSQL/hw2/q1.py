from sys import argv
from pymongo import MongoClient
from datetime import datetime  # 문자 <-> 시간 간 변경 모듈


client = MongoClient()
db = client.disaster
gps = db.gps  # gps collection 할당

def q1(input_date):

    # 입력 받은 문자열을 시간 변수로 변경
    specific_time = datetime.strptime(input_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    val = gps.aggregate([
        {'$match' : {'time' : specific_time}},  # 시점 검색
        {'$group' : {'_id' : {'trunc_coor' : {'$map' : {  # coordinates의 array 요소를 소수점 2째에서 버리고 난 후 grouping
                        'input' : '$coordinates',
                        'as' : 'coord',
                        'in' : {'$trunc' : ['$$coord',1]}}}},
                    'count' : {'$sum' : 1}}},  # 각 grouping 된 coordinates 당 count 계산
        {'$project' : {'_id' : 1, 'count' : 1}}, 
        {'$sort' : {'_id.trunc_coor.0' : 1, '_id.trunc_coor.1' : 1}}  # lon 과 lat 으로 차례로 오름차순 정리
    ])
    res = list(val)

    # 주어진 형태로 출력
    for i in res : 
        print(f"{i['_id']['trunc_coor']}: {i['count']}")

if __name__ == '__main__':
    q1(argv[1])