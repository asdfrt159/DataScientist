class Node :
    def __init__(self, no, x, y) : 
        self.no = no
        self.x = x
        self.y = y
        
# 두 좌표 거리 계산
def uclid(a,b) :
    return ((a.x - b.x)**2 + (a.y - b.y)**2)**(0.5) 

# 방문하지 않은 것중에 최소값 찾아야함
def find_min(visit , real_dis) :
    min_index = None
    min_val = float('inf')
    for ind, val in enumerate(visit) :
        if val != 1 : # 방문하지 않은것
            if min_val >= real_dis[ind] :
                 min_val = real_dis[ind]
                 min_index = ind
    return min_index

def find_dis(x, list, dis_arr, real_dis, visit) :  # list는 그래프 연결, dis_arr 는 그래프 거리 , visit은 방문 , real_dis 는 실제 거리
	visit[x] = 1 
	for index, i in enumerate(list) :
		if i != None :
			if min(real_dis[x] + dis_arr[x][index] , real_dis[index]) == real_dis[x] + dis_arr[x][index] :
				real_dis[index] = round(real_dis[x] + dis_arr[x][index],2)

				


def main() :
    # input.txt 에서 정보 받아오기
    with open('input.txt','r') as f :
        inputs = f.readlines()
    contents = [x.rstrip('\n') for x in inputs]
    content = []
    for i in range(len(contents)) :
        content.append([int(x) for x in contents[i].split()])

    length = content[0]
    input = content[1]  
    graph = content[2:]

    # classNode 생성 : 리스트 안에 class 에 정보 저장
    classNode = []
    for i in range(len(input)) :
        if i%2 == 0 :
            classNode.append(Node(i//2, input[i] , input[i+1])) 

    # ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
    # dis_arr 생성 : 행렬로 i,j 성분에 대한 거리 입력
    dis_arr = [[None for _ in range(len(classNode))] for _ in range(len(classNode))] 
    for i in range(len(classNode)) :
        for j in range(len(classNode)) :
            dis_arr[i][j] = round(uclid(classNode[i], classNode[j]),2)

    # visit 생성 : 방문했으면 None -> 1
    visit = [None for i in range(len(classNode))]
    real_dis = [float('inf') for i in range(len(classNode))]

    # graph_arr 생성 : 각 노드가 어느 노드에 연결되어 있는지에 대한 정보 (1로 되어 있으면 연결)
    graph_arr = [[None for _ in range(len(classNode))] for _ in range(len(classNode))]
    for i in range(len(classNode)) :  # 그래프 연결 노드를 돌면서 확인
        for j in graph[i] :
            graph_arr[i][j] = 1
    # ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

    # 시작점 초기화
    real_dis[0] = 0

    # 시작점에서 시작 그 이후에는 방문하지 않은 노드 중에서 최소 거리인 것부터 시작한다.
    # 모든 노드가 방문처리 됬을때 끝난다.
    for i in range(len(classNode)) :
            if None in visit : 
                 min_index = find_min(visit, real_dis)
                 find_dis(min_index, graph_arr[min_index],dis_arr, real_dis, visit)


    print(real_dis)
    print(f'좌표 0에서 좌표 {classNode[-1].no}까지, 거리 : {real_dis[-1]}')
    
    
if __name__ == "__main__":
    main()