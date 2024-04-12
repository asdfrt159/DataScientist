from sys import argv
from pymongo import MongoClient
from datetime import datetime, timedelta #time 처리 함수 호출

client = MongoClient()
db = client.disaster

def q4(longitude, latitude, ts):
    # TODO:
    
    #Index 생성 (이전 문제에서 생성하였으면 주석 처리 가능)
    #site: centroid (2dsphere)
    #shelter: site_id(1)
    #gps: coordinates(2d), time(1)

    db.site.create_index([('centroid', '2dsphere')])
    db.shelter.create_index([('site_id', 1)])
    db.gps.create_index([('coordinates', '2d')])
    db.gps.create_index([('time', 1)])

    #발생지점으로부터 10Km 이내이며 1시간 이내에 기록된 GPS 지점 찾기
    
    # 1시간 이내 시간 정의
    ts = ts.strip("'")
    low_time = datetime.fromisoformat(ts) - timedelta(hours=1)
    high_time = datetime.fromisoformat(ts) + timedelta(hours=1)
    
    #좌표 정의
    loc = [longitude, latitude]

    #첫번째 stage: geowithin을 이용하여 10km 이내를 정의
    #두번째 stage: 1시간 이내로 정의한 변수를 time 기준으로 정의
    #세번째 stage: gps_id와 좌표 정보, time 정보만 출력
    #네번째 stage: gps_id 기준 오름차순으로 정렬 
    result = db.gps.aggregate([{'$match': {'coordinates': {'$geoWithin': {'$centerSphere':[loc, 10/6378.1]}}}},
                            {'$match': {'time': {'$gte': low_time, '$lte': high_time }}},
                            {'$project': {'_id': 0, 'gps_id': 1, 'coordinates': 1, 'time': 1}},
                            {'$sort': {'gps_id': 1}}])
    #gps 정보를 list 형태로 저장
    gps_infos = list(result)

    #gps_id 마다 가장 가까운 대피소의 site id를 찾음 
    for gps_info in gps_infos:

        # 좌표 정보는 GeoJSON 형태로 변환
        gps_obj = {'type': 'Point', 'coordinates': gps_info['coordinates']}

        #가장 가까운 대피소를 찾기 위해 Near 함수를 이용하여 반복 수행할 것이기에 min/max distance와 step을 지정함
        #만약 최초 min/max_distance에서 shelter를 찾는다면 그때 종료되고, 그렇지 않으면 거리를 1km씩 늘려가면서 찾을때까지 반복 실행함
        #site의 해당 범위내 객체 정보를 다 받아서 대피소 여부를 각각 확인하여 대피소가 맞으면 종료되고 그렇지 않으면 find 함수를 반복 실행함
        #geoNear 함수가 가장 가까운 객체부터 반환하기 때문에 별도의 정렬은 하지 않음

        #min/max, step distance 변수 할당 

        min_dist = 0
        max_dist = 1000
        step = 1000

        #shelter를 찾을때까지 while문 실행
        while(True):    

            #geoNear를 통해 site내 후보지를 찾고 그걸 List로 변환하여 후보지 변수(candidates)에 저장
            res = db.site.aggregate([{'$geoNear': {'near': gps_obj, 'distanceField': 'distance', 'minDistance': min_dist, 'maxDistance': max_dist, 'spherical': True}}])
            candidates = list(res)
            
            #site에서 찾은 후보지(candidates) 중 가까운 곳부터 site_id가 shelter에 있는지 여부 확인
            #만약 shelter가 있다면 for문은 종료되고 그렇지 않으면 끝까지 실행됨
            for candidate in candidates:
                s_info = candidate['site_id']
                shelter = db.shelter.find_one({'site_id': s_info}, {'_id': 0, 'site_id': 1})
                if shelter != None:
                    break
            #만약 shelter를 찾았다면 while문은 종료됨
            #그렇지 않다면 min/max_distance가 증가되고 후보지 및 shelter를 찾는 것을 반복 실행함 
            if shelter != None:
                break
            else:
                min_dist += step
                max_dist += step
    
        # 정의에 따라 gps_id, gps_time, shelter_id 출력
        print(f"{gps_info['gps_id']} {gps_info['time']} {shelter['site_id']}")
    
if __name__ == '__main__':
    q4(float(argv[1]), float(argv[2]), argv[3])
