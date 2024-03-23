import time
import copy

def bubbleSort(A):
	for numElements in range(len(A), 0, -1):   # 시작 : 원소갯수(n) / 끝 : 1 / 간격 : -1
		for i in range(numElements-1):  # 시작 : 0 / 끝 : n-2 / 간격 : 1
			if A[i] > A[i+1]:
				A[i], A[i+1] = A[i+1], A[i]
	return A

def insertionSort(A):
	for i in range(1, len(A)):  # 1부터 < 최대 갯수 까지
		loc = i-1
		newItem = A[i]
		while loc >= 0 and newItem < A[loc]:
			A[loc+1] = A[loc]
			loc -= 1
		A[loc+1] = newItem
	return A

def shellSort(A):  # A[0...n-1]: 정렬할 리스트
	H = gapSequence(len(A))
	for h in H:  # H = [h0, h1, ..., 1]: 갭 수열
		for k in range(h):
			stepInsertionSort(A, k, h)
	return A

def stepInsertionSort(A, k:int, h:int):  # A[k, k+h, k+2h, ...]을 정렬한다
	for i in range(k + h, len(A), h):
		j = i - h
		newItem = A[i]
		# 이 지점에서 A[..., j-2h, j-h, j]는 이미 정렬되어 있는 상태임
		# A[..., j-2h, j-h, j, j+h]의 맞는 곳에 A[j+h]를 삽입한다
		while 0 <= j and newItem < A[j]:
			A[j + h] = A[j]
			j -= h
		A[j + h] = newItem
		
def gapSequence(n:int) -> list: # 갭 수열 만들기. 다양한 선택이 있음
	H = [1]; gap = 1
	while gap < n/5:
		gap = 3 * gap + 1
		H.append(gap)
	H.reverse()
	return H




def measure_sort_time(sort_func, copy_list):
    
    times = []
    for _ in range(10):
        arr_copy = copy.deepcopy(copy_list)
        start_time = time.time()
        sorting_list = sort_func(arr_copy)
        end_time = time.time()
        times.append(end_time - start_time)
    result =  sum(times) / len(times)

    return result, sorting_list




def checkSum(arr) : 
    sum = 0
    for i in range(10) :
        sum += arr[i*len(arr) // 10 ]
    print('checkSum: ', sum)

def main() : 
    
    with open('./prac_4/input4-1.txt','r') as f : 
        val = [int(x) for x in f.read().split()]
        val.pop(0)
        # val list 생성

    

    bubble_sort_time, bubble_list = measure_sort_time(bubbleSort, val)
    insertion_sort_time, insertion_list = measure_sort_time(insertionSort, val)
    shell_sort_time, shell_list = measure_sort_time(shellSort, val)

	
    checkSum(bubble_list)
    print(f"Bubble Sort 평균 실행 시간: {bubble_sort_time:0.3f}초")
    checkSum(insertion_list)
    print(f"Insertion Sort 평균 실행 시간: {insertion_sort_time:0.3f}초")
    checkSum(shell_list)
    print(f"Shell Sort 평균 실행 시간: {shell_sort_time:0.3f}초")

    # print(bubble_list) # 확인
        



if __name__ == '__main__' :
    main()