import time


def bubble(A) :
	for i in range(len(A)-1,0,-1) :  # 전체 비교 횟수 (전체 n-1 비교횟수 부터 1 비교 횟수까지)
		for j in range(i) :
			if A[j] > A[j+1] :  # 오름차순
				A[j], A[j+1] = A[j+1], A[j]


def selection(A) :
	for i in range(len(A)-1, 0, -1) :  # 검색 범위 (전체 index 부터 1인 index 까지)
		large_index = 0
		for j in range(i+1) :  # 최솟값을 찾기 위한 for 문
			if A[j] > A[large_index] : 
				large_index = j
		A[large_index], A[i] = A[i], A[large_index]


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
	for i in H : 
		for j in range(i) :
			stepinsert(A, j, i) 

def stepinsert(A, start, step) :
	# insert 정렬
	for i in range(start + step, len(A), step) :
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



def main() : 
	list = [2,4,5,6,7,8,54,3,8,9,4,2,3,54,1,0,2,4,6,9,7,5,1,3,2,0,4,6,8,2]
	print(f'정렬 전 : {list}')
	start_time = time.time()
	shell(list)
	end_time = time.time()
	print(f'정렬 후 : {list}')
	print(f'시간 : {(end_time - start_time):.10f}')


if __name__ == '__main__' :
	main()