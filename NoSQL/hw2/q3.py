from sys import argv
from pymongo import MongoClient

client = MongoClient()
db = client.disaster

def q3(m, r):
    # TODO:
    # 진도가 m 이상인 친구들 찾기
    r1 = db.earthquake.find({'magnitude' : {'$gte' : m}})
    result = {}

    # 진도 m 이상인 친구들을 하나하나에 해당하는 building들을 찾기

    for i in r1:
        t = db.site.aggregate([ {'$match' : {'properties.type' : 'building', 
                                            'centroid' : {'$geoWithin' : {'$centerSphere' : [i['coordinates'], r/6378.1]}}}}, 
                            {'$group' : {'_id' : '$properties.description', 's' : {'$sum': 1}}}])
        tmp_result = list(t)

        # 결과 넣기
        # 기존에 있는 key들은 더하고, 없는 것들은 만들어 주기
        for i in tmp_result:
            if i['_id'] in result:
                result[i['_id']] += i['s']
            else:
                result[i['_id']] = i['s']
    
    # 정렬 후 출력
    sorted_result = {k: result[k] for k in sorted(result)}

    for key, value in sorted_result.items():
        print(key, value)

    # result 확인을 위한 코드
    # with open(f'{m}_{r}.txt', 'w', encoding='utf-8') as f:
    #     for key, value in sorted_result.items():
    #         f.write(f'{key} {value}\n')



if __name__ == '__main__':
    q3(float(argv[1]), float(argv[2]))
