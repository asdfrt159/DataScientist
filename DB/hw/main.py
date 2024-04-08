#!/usr/bin/env python
# coding: utf-8

###################################################################
#                                                                 #
#   2024 DS2 Database Project : Recommendation using SQL-Python   #
#                                                                 #
###################################################################

import mysql.connector
from tabulate import tabulate
import pandas as pd
import math
import sys

## Connect to Remote Database
## Insert database information

HOST = "147.46.15.238"
PORT = ""
USER = "DS2024_0024"
PASSWD = "DS2024_0024"
DB = "DS_proj_12"

connection = mysql.connector.connect(
    host=HOST,
    port=7000,
    user=USER,
    passwd=PASSWD,
    db=DB,
    autocommit=True  # to create table permanently
)

cur = connection.cursor(dictionary=True)

## 수정할 필요 없는 함수입니다.
# DO NOT CHANGE INITIAL TABLES IN prj.sql
def get_dump(mysql_con, filename):
    '''
    connect to mysql server using mysql_connector
    load .sql file (filename) to get queries that create tables in an existing database (fma)
    '''
    query = ""
    try:
        with mysql_con.cursor() as cursor:
            for line in open(filename, 'r'):
                if line.strip():
                    line = line.strip()
                    if line[-1] == ";":
                        query += line
                        cursor.execute(query)
                        query = ""
                    else:
                        query += line

    except Warning as warn:
        print(warn)
        sys.exit()


## 수정할 필요 없는 함수입니다.
# SQL query 를 받아 해당 query를 보내고 그 결과 값을 dataframe으로 저장해 return 해주는 함수
def get_output(query):
    cur.execute(query)
    out = cur.fetchall()
    df = pd.DataFrame(out)
    return df


# [Algorithm 1] Popularity-based Recommendation - 1 : Popularity by rating count
def popularity_based_count(user_input=True, item_cnt=None):
    if user_input:
        rec_num = int(input('Number of recommendations?: '))
    else:
        assert item_cnt is not None
        rec_num = int(item_cnt)
    print(f"Popularity Count based recommendation")
    print("=" * 99)


    #-----------------------------------------------------------------------------------------------
    query = 'SELECT A.item, A.count\
            FROM (SELECT item, count(user) AS count\
                    FROM ratings\
                    WHERE rating is not null\
                    GROUP BY item\
                    ORDER BY count DESC) AS A\
            WHERE A.item >= 150 AND A.item < 350'
    df = get_output(query)

    # 쿼리의 결과를 sample 변수에 저장하세요.
    # rec_num 만큼 뽑음
    sample = df.head(rec_num)
    #-----------------------------------------------------------------------------------------------


    # do not change column names
    df = pd.DataFrame(sample, columns=['item', 'count'])

    # TODO end

    # Do not change this part
    with open('pbc.txt', 'w') as f:
        f.write(tabulate(df, headers=df.columns, tablefmt='psql', showindex=False))
    print("Output printed in pbc.txt")


# [Algorithm 1] Popularity-based Recommendation - 2 : Popularity by average rating
def popularity_based_rating(user_input=True, item_cnt=None):
    if user_input:
        rec_num = int(input('Number of recommendations?: '))
    else:
        assert item_cnt is not None
        rec_num = int(item_cnt)
    print(f"Popularity Rating based recommendation")
    print("=" * 99)


    # TODO: remove sample, return actual recommendation result as df
    #-----------------------------------------------------------------------------------------------
    query ='SELECT F.item, F.prediction\
            FROM (SELECT A.item, ROUND(avg(A.scaled_rating),4) AS prediction\
                    FROM (SELECT user, item, (rating-min)/(max-min) AS scaled_rating\
                            FROM ratings AS R NATURAL JOIN (SELECT user,\
                                                            CASE count(rating)\
                                                                    WHEN 1 then 0\
                                                            ELSE min(rating)\
                                                            END AS min,\
                                                            max(rating) AS max\
                                                            FROM ratings\
                                                            GROUP BY user) AS S\
                            ) AS A\
                    GROUP BY A.item\
                    ORDER BY prediction DESC) AS F\
            WHERE F.item >= 150 AND F.item < 350'
    df = get_output(query)

    # 쿼리의 결과를 sample 변수에 저장하세요.
    # rec_num 만큼 뽑음
    sample = df.head(rec_num)
    #-----------------------------------------------------------------------------------------------


    # do not change column names
    df = pd.DataFrame(sample, columns=['item', 'prediction'])
    # TODO end

    # Do not change this part
    with open('pbr.txt', 'w') as f:
        f.write(tabulate(df, headers=df.columns, tablefmt='psql', showindex=False))
    print("Output printed in pbr.txt")


# [Algorithm 2] Item-based Recommendation
def ibcf(user_input=True, user_id=None, item_cnt=None):
    if user_input:
        user = int(input('User Id: '))
        rec_num = int(input('Number of recommendations?: '))
    else:
        assert user_id is not None
        assert item_cnt is not None
        user = int(user_id)
        rec_num = int(item_cnt)

    print("=" * 99)
    print(f'Item-based Collaborative Filtering')
    print(f'Recommendations for user {user}')


    # TODO: remove sample, return actual recommendation result as df
    #-----------------------------------------------------------------------------------------------
    # 아이템-아이템 테이블
    query = 'SELECT item_1, sum(sim) AS sim_sum \
            FROM (SELECT item_1, item_2, sim, ROW_NUMBER() OVER(PARTITION BY item_1 ORDER BY sim DESC, item_2 ASC) AS ranking\
                FROM item_similarity) AS A\
            WHERE A.ranking <= 5\
            GROUP BY item_1'

    query2 = 'SELECT I.item_1, I.item_2, ROUND(I.sim/S.sim_sum , 4) AS nor_sim\
            FROM (SELECT item_1, item_2, sim, ROW_NUMBER() OVER(PARTITION BY item_1 ORDER BY sim DESC, item_2 ASC) AS ranking\
                FROM item_similarity) AS I NATURAL JOIN ('+ query +') AS S\
            WHERE I.ranking <= 5'

    query3 = 'SELECT L.item_1, L.item_2,  CASE \
                        WHEN R.nor_sim is null THEN 0\
                        ELSE R.nor_sim\
                        END AS chg_sim\
            FROM item_similarity AS L LEFT OUTER JOIN (' + query2 + ') AS R USING (item_1, item_2)\
                '
    item_sim = get_output(query3)

    # 아이템-유저 테이블 아이템 평균으로 sim 나눔
    query = 'SELECT R.item, R.user,\
                CASE \
                    WHEN R.rating is null THEN T.rate_avg\
                ELSE R.rating\
                END AS rate\
            FROM ratings AS R NATURAL JOIN (SELECT item, avg(rating) AS rate_avg\
                                            FROM ratings\
                                            GROUP BY item) AS T'

    item_user = get_output(query)


    # 아이템-아이템 피벗, 아이템-유저 피벗, 합성곱 
    ii_pivot = pd.pivot_table(item_sim, index= 'item_1', columns= 'item_2', values= 'chg_sim')
    iu_pivot = pd.pivot_table(item_user, index='item', columns='user', values='rate')
    dot_df = ii_pivot.dot(iu_pivot)

    # stack 형식으로 변환, 반올림
    df_mid = dot_df.stack().reset_index()
    df_mid[0] = df_mid[0].astype(float).round(4)
    df_nd = df_mid.rename(columns={'item_1':'item',0:'prediction'}).sort_values(['user','prediction','item'], ascending=[True,False,True])
    
    # 기존에 평가했던 item 제외
    query = 'SELECT * FROM ratings'
    origin = get_output(query)
    or_list = origin[(origin.user == user) & (origin.rating.isnull())].item.to_list()
    df_nd = df_nd[df_nd.item.isin(or_list)]

    # rec_num 만큼 갯수 뽑음
    df_fin = df_nd.groupby('user').head(rec_num)[['user','item','prediction']].reset_index(drop=True)

    # 쿼리의 결과를 sample 변수에 저장하세요.
    # user 에 해당하는 결과 뽑음
    sample = df_fin[df_fin.user == user]
    #-----------------------------------------------------------------------------------------------


    # do not change column names
    df = pd.DataFrame(sample, columns=['user', 'item', 'prediction'])
    # TODO end

    # Do not change this part
    with open('ibcf.txt', 'w') as f:
        f.write(tabulate(df, headers=df.columns, tablefmt='psql', showindex=False))
    print("Output printed in ibcf.txt")



# [Algorithm 3] (Optional) User-based Recommendation
def ubcf(user_input=True, user_id=None, item_cnt=None):
    if user_input:
        user = int(input('User Id: '))
        rec_num = int(input('Number of recommendations?: '))
    else:
        assert user_id is not None
        assert item_cnt is not None
        user = int(user_id)
        rec_num = int(item_cnt)

    print("=" * 99)
    print(f'User-based Collaborative Filtering')
    print(f'Recommendations for user {user}')

    # TODO: remove sample, return actual recommendation result as df

    #-----------------------------------------------------------------------------------------------------
    # 유저-유저 테이블
    query = 'SELECT user_1, sum(sim) AS sim_sum \
            FROM (SELECT user_1, user_2, sim, ROW_NUMBER() OVER(PARTITION BY user_1 ORDER BY sim DESC, user_2 ASC) AS ranking\
                FROM user_similarity) AS A\
            WHERE A.ranking <= 5\
            GROUP BY user_1'
    
    query2 = 'SELECT I.user_1, I.user_2, ROUND(I.sim/S.sim_sum , 4) AS nor_sim\
            FROM (SELECT user_1, user_2, sim, ROW_NUMBER() OVER(PARTITION BY user_1 ORDER BY sim DESC, user_2 ASC) AS ranking\
                FROM user_similarity) AS I NATURAL JOIN ('+ query +') AS S\
            WHERE I.ranking <= 5'

    query3 = 'SELECT L.user_1, L.user_2,  CASE \
                        WHEN R.nor_sim is null THEN 0\
                        ELSE R.nor_sim\
                        END AS chg_sim\
            FROM user_similarity AS L LEFT OUTER JOIN (' + query2 + ') AS R USING (user_1, user_2)\
            '
    user_sim = get_output(query3)

    # 유저-아이템 테이블 유저 평균으로 sim 나눔
    query = 'SELECT R.user, R.item,\
                CASE \
                    WHEN R.rating is null THEN T.rate_avg\
                ELSE R.rating\
                END AS rate\
            FROM ratings AS R NATURAL JOIN (SELECT user, avg(rating) AS rate_avg\
                                            FROM ratings\
                                            GROUP BY user) AS T'
    
    user_item = get_output(query)

    # 유저-유저 피벗, 유저-아이템 피벗, 합성곱 
    uu_pivot = pd.pivot_table(user_sim, index= 'user_1', columns= 'user_2', values= 'chg_sim')
    ui_pivot = pd.pivot_table(user_item, index='user', columns='item', values='rate')
    dot_df = uu_pivot.dot(ui_pivot)

    # stack 형식으로 변환, 반올림
    df_mid = dot_df.stack().reset_index()
    df_mid[0] = df_mid[0].astype(float).round(4)
    df_nd = df_mid.rename(columns={'user_1':'user',0:'prediction'}).sort_values(['user','prediction','item'], ascending=[True,False,True])
    
    # 기존에 평가했던 item 제외
    query = 'SELECT * FROM ratings'
    origin = get_output(query)
    or_list = origin[(origin.user == user) & (origin.rating.isnull())].item.to_list()
    df_nd = df_nd[df_nd.item.isin(or_list)]

    # rec_num 만큼 갯수 뽑음
    df_fin = df_nd.groupby('user').head(rec_num)[['user','item','prediction']].reset_index(drop=True)

    # 쿼리의 결과를 sample 변수에 저장하세요.
    # user 에 해당하는 결과 뽑음
    sample = df_fin[df_fin.user == user]
    #-----------------------------------------------------------------------------------------------------



    # do not change column names
    df = pd.DataFrame(sample, columns=['user', 'item', 'prediction'])
    # TODO end

    # Do not change this part
    with open('ubcf.txt', 'w') as f:
        f.write(tabulate(df, headers=df.columns, tablefmt='psql', showindex=False))
    print("Output printed in ubcf.txt")


## 수정할 필요 없는 함수입니다.
# Print and execute menu 
def menu():
    print("=" * 99)
    print("0. Initialize")
    print("1. Popularity Count-based Recommendation")
    print("2. Popularity Rating-based Recommendation")
    print("3. Item-based Collaborative Filtering")
    print("4. User-based Collaborative Filtering")
    print("5. Exit database")
    print("=" * 99)

    while True:
        m = int(input("Select your action : "))
        if m < 0 or m > 5:
            print("Wrong input. Enter again.")
        else:
            return m

def execute(argv):
    terminated = False
    while not terminated:
        if len(argv)<2:
            m = menu()
            if m == 0:
                # 수정할 필요 없는 함수입니다.
                # Upload prj.sql before this
                # If autocommit=False, always execute after making cursor
                get_dump(connection, 'prj.sql')
            elif m == 1:
                popularity_based_count()
            elif m == 2:
                popularity_based_rating()
            elif m == 3:
                ibcf()
            elif m == 4:
                ubcf()
            elif m == 5:
                terminated = True
            

        # 평가를 위한 코드입니다. 수정하지 마세요.
        else:
            with open(argv[1], 'r') as f:
                lines = f.readlines()
                for line in lines:
                    rec_args = list(map(float, line.split(',')))
                    if len(rec_args) > 1:
                        rec_args[1] = int(rec_args[1])
                    m = rec_args[0]
                    if m==0:
                        get_dump(connection, 'prj.sql')
                    elif m == 1:
                        popularity_based_count(False, *rec_args[1:])
                    elif m == 2:
                        popularity_based_rating(False, *rec_args[1:])
                    elif m == 3:
                        ibcf(False, *rec_args[1:])
                    elif m == 4:
                        ubcf(False, *rec_args[1:])
                    elif m == 5:
                        terminated = True
                    else:
                        print('Invalid menu option')

# DO NOT CHANGE
if __name__ == "__main__":
    execute(sys.argv)
