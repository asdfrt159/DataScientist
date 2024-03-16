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





def main() : 
	list = [2,1,33,2,10,23,4,2,3,4,6,7,3]
	print(f'정렬 전 : {list}')
	start_time = time.time()
	insertion(list)
	end_time = time.time()
	print(f'정렬 후 : {list}')
	print(f'시간 : {end_time - start_time:.10f}')


if __name__ == '__main__' :
	main()