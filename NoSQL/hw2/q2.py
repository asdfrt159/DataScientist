from sys import argv
from pymongo import MongoClient

client = MongoClient()
db = client.disaster

def q2(r):

    distance = r*1000
    db.site.create_index([ ("properties.type", "text"), ("properties.name","text"), ("properties.description","text") ])
    #School Field 검색을 위한 인덱스 생성
    school_fields = db.site.find({'$text':{'$search':' \"School Field\" '}},{'centroid':1,'site_id':1,'_id':0}).sort([('site_id',1)])
    school_fields = list(school_fields)
    #대피소 리스트 만들기
    shelter_site = db.shelter.distinct('site_id')
    #nearsphere 사용을 위한 인덱스 생성
    db.site.create_index([('centroid','2dsphere')])

    #대피소가 없는 학교 운동장을 저장할 리스트
    non_shelter_school_fields = []


    for i in school_fields:
        site_inf = i['site_id']
        center = i['centroid']['coordinates']

        geo_obj = {'type':'Point','coordinates':center}
        near_list = list(db.site.find(
            {'centroid':
            {'$nearSphere':{'$geometry':geo_obj, '$maxDistance':distance}}
            }).sort([('site_id',1)])
        )
        #학교 운동장으로부터 r km 내에 있는 site_id가 대피소 리스트에 있는지 확인하기
        shelter_exists = False
        for item in near_list:
            if item['site_id'] in shelter_site:
                shelter_exists = True
                break

        #대피소가 없는 학교 운동장을 추가하기
        if not shelter_exists:
            non_shelter_school_fields.append(site_inf)

    for i in non_shelter_school_fields:
        print(i)

if __name__ == '__main__':
    q2(float(argv[1]))

