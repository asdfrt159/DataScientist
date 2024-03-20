import time

# bubble
def bubble(A) :
	for i in range(len(A)-1,0,-1) :  # 전체 비교 횟수 (전체 n-1 비교횟수 부터 1 비교 횟수까지)
		for j in range(i) :
			if A[j] > A[j+1] :  # 오름차순
				A[j], A[j+1] = A[j+1], A[j]


# selection
def selection(A) :
	for i in range(len(A)-1, 0, -1) :  # 검색 범위 (전체 index 부터 1인 index 까지)
		large_index = 0
		for j in range(i+1) :  # 최솟값을 찾기 위한 for 문
			if A[j] > A[large_index] : 
				large_index = j
		A[large_index], A[i] = A[i], A[large_index]


# insertion
def insertion(A) :
	for i in range(1,len(A)) :
		prev = i-1
		new = A[i]
		while prev >= 0 and new < A[prev] :  # shift 과정 (index 0 되기까지 new 값이 작은데가 나올때까지 찾는다.)
			A[prev+1] = A[prev]  # 이전값을 현재 index에 shift
			prev -= 1
		A[prev+1] = new


# shell
def shell(A) :
	H = gapspace(len(A)) 
	for i in H :  # gap ex> 7,3,1 이런식으로 받는다.
		for j in range(i) :  # 3을 받으면 0,1,2 이런식으로 3으로 쪼개진 것들을 각각 정렬한다.
			stepinsert(A, j, i)   # (리스트, 시작index, 간격)

def stepinsert(A, start, step) :
	# insert 정렬
	for i in range(start + step, len(A), step) :  # 삽입정렬은 시작은 1부터 즉 시작 + step 으로 시작한다.
		prev = i - step
		curr_val = A[i]
		while prev >= 0 and curr_val < A[prev] :
			A[prev+step] = A[prev]
			prev -= step
		A[prev+step] = curr_val

def gapspace(n:int)->list :
	gap = 1; H = [1]
	while gap < n//9 :
		gap = gap * 3 + 1
		H.append(gap)
	return H


# quick
def quick(A) :
	quicksort(A, 0, len(A)-1) # 처음과 끝 정보를 받는다.

def quicksort(A, start, end) :
	if start < end :  # 재귀의 종료 조건
		middle = partition(A, start, end) 
		quicksort(A, start, middle-1)
		quicksort(A, middle+1, end)

def partition(A, start, end) :
	x = A[end]  # 기준값
	base = start - 1  # base 기준 왼쪽 작은것
	for j in range(start, end) :  # j 기준 오른쪽 큰것
		if x > A[j] :
			base += 1
			A[base], A[j] = A[j], A[base]
	A[base+1], A[end] = A[end], A[base+1]
	return base + 1  # 기준을 바꾼 위치를 return
	

# merge
def merge(A) :
	mergeSort(A, 0, len(A)-1)  # 처음과 끝 정보
	
def mergeSort(A, start, end) :
	if start < end :  # 종료조건 설정
		middle = (start+end) // 2
		mergeSort(A, start, middle)
		mergeSort(A, middle+1, end)
		merge2list(A, start, middle, end)

def merge2list(A, start, middle, end) :
	# group1, group2 의 시작 index를 지정하고, buffer 로 사용할 list를 만든다.
	group1 = start; group2 = middle + 1; b_index = 0
	buffer = [0 for _ in range(len(A))]

	# group1과 group2를 비교하여 buffer에 넣는다. 
	while group1 <= middle and group2 <= end :
		if A[group1] <= A[group2] :
			buffer[b_index] = A[group1]
			group1 += 1; b_index += 1 
		else :
			buffer[b_index] = A[group2]
			group2 += 1; b_index += 1
	
	# group1과 group2를 비교하고 남은 index가 있으면 buffer에 넣는다.
	while group1 <= middle :
		buffer[b_index] = A[group1]
		group1 += 1; b_index += 1
	
	while group2 <= end :
		buffer[b_index] = A[group2]
		group2 += 1; b_index += 1
	
	# buffer의 정렬이 끝나서, A로 다시 옮긴다.
	group1 = start; b_index = 0
	while group1 <= end : 
		A[group1] = buffer[b_index]
		group1 += 1; b_index += 1
	

# heap
def heap(A:list) : 
	buildHeap(A)
	for last in range(len(A)-1, 0, -1) :  # 우선순위 큐 처럼 최고 높은게 젤 밑으로 보내고 관심제외
		A[last], A[0] = A[0], A[last]
		percolateDown(A, 0, last-1)  # 맨 마지막 원소는 제외하고 percolateDwon

def buildHeap(A:list) : 
	lastParent = (len(A)-2) // 2  # 마지막 원소 len(A)-1 에 i-1//2
	for i in range(lastParent, -1, -1) :
		percolateDown(A, i, len(A)-1)  # 젤 밑부터 차례대로 percolateDown

def percolateDown(A, parent, end) :
	child = parent *2 +1
	right = parent *2 +2
	if child <= end :  #자식이 있고
		if right <= end and A[child] < A[right] : #오른자식이 존재하고 왼자식보다 크면
			child = right
		if A[parent] < A[child] : #자식노드가 부모보다 크면
			A[parent] , A[child] = A[child] , A[parent]
			percolateDown(A, child, end)  # 자식 관점에서 다시 시작 


# 계수 정렬
def countSort(A) :
	k = max(A)
	C = [0 for _ in range(k+1)]  # 0 ~ 최고차항 자연수 셀수 있는 도수분포표
	for i in range(len(A)) :
		C[A[i]] += 1
	for i in range(1, k+1) :  # 누적도수분포표
		C[i] = C[i] + C[i-1]

	B = [0 for _ in range(len(A))]
	for i in range(len(A)-1,-1,-1) :
		B[C[A[i]]-1] = A[i]  # C자리에서 값있으면 index 이하 값이 그 정도 있다는 소리
		C[A[i]] -= 1  # 동일 분포에 있는것 값 처리
	
	for i in range(len(A)) : 
		A[i] = B[i]

# 기수 정렬
import math
def radixSort(A) :
	maxdigit = math.ceil(math.log10(max(A)))
	buffer = [[] for _ in range(10)]
	for i in range(maxdigit) :  # 자릿수 별로 정렬
		for x in A : 
			y = (x//10**i)%10
			buffer[y].append(x)  # buffer 자릿수 index 에 값 넣음
		A.clear()
		for j in range(10) :
			A.extend(buffer[j])  # index 순으로 전부 합침
			buffer[j].clear()

# 버킷 정렬
import math
def bucketSort(A) :
	n = len(A)
	buffer = [[] for _ in range(n)] 
	for i in range(n) :
		buffer[math.floor(A[i]*n)].append(A[i])  # 스케일링 값을 index 에 넣는다.
	A.clear()
	for i in range(n) :
		insertion(buffer[i])  # index 별로 sorting
		A.extend(buffer[i])  # 합침





def main() : 
	list = [2,4,5,6,7,8,54,3,8,9,4,2,3,54,1,0,2,4,6,9,7,5,1,3,2,0,4,6,8,2]
	# list2 = [0.12,0.234,0.45,0.23,0.98,0.76,0.34]
	print(f'정렬 전 : {list}, 길이 : {len(list)}')
	start_time = time.time()
	radixSort(list)
	end_time = time.time()
	print(f'정렬 후 : {list}')
	print(f'시간 : {(end_time - start_time):.10f}')


if __name__ == '__main__' :
	main()