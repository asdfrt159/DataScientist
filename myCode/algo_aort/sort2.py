import time
import math

def bubble(A) :
    for i in range(len(A)-1, 0, -1) :
        for j in range(i) :
            if A[j] > A[j+1] :
                A[j] , A[j+1] = A[j+1] , A[j]

def select(A) :
    for i in range(len(A)-1, 0, -1) :
        large_index = 0 
        for j in range(i+1) :
            if A[j] > A[large_index] :
                large_index = j
        A[i], A[large_index] = A[large_index], A[i]

def insert(A) :
    for i in range(1, len(A)) :
        prev = i-1
        new = A[i]
        while prev >= 0 and new < A[prev] :
            A[prev+1] = A[prev]
            prev -= 1
        A[prev+1] = new


def shell(A) :
    H = gapMake(len(A))
    for h in H :
        for index in range(h) :
            stepInsert(A, index, h)

def gapMake(n) :
    gap = 1; H = [1]
    while gap < n//9 :
        gap = gap *3 +1
        H.append(gap)
    H.reverse()
    return H

def stepInsert(A, start:int, step:int) :
    for i in range(start+step , len(A), step):
        prev = i - step
        new = A[i]
        while prev >= 0 and new < A[prev] :
            A[prev+step] = A[prev]
            prev -= step
        A[prev+step] = new
    

def quick(A) :
    quickSort(A, 0, len(A)-1) 

def quickSort(A, start, end) :
    if start < end :
        middle = partition(A, start, end)
        quickSort(A, start, middle-1)
        quickSort(A, middle+1, end)

def partition(A, start, end) :
    x = A[end]
    left = start - 1
    for right in range(start, end) :
        if x > A[right] :
            left += 1
            A[left], A[right] = A[right], A[left]
    A[left+1], A[end] = A[end] , A[left+1]
    return left+1    


def merge(A) :
    mergeSort(A, 0, len(A)-1) 

def mergeSort(A, start, end) :
    if start < end :
        middle = (start + end) // 2
        mergeSort(A, start, middle) 
        mergeSort(A, middle +1, end)
        merge2list(A, start, middle, end)

def merge2list(A, start, middle, end) :
    group1 = start; group2 = middle + 1; b_index = 0
    buffer = [0 for _ in range(len(A))]

    while group1 <= middle and group2 <= end :
        if A[group1] >= A[group2] :
            buffer[b_index] = A[group2]
            b_index += 1; group2 +=1
        else :
            buffer[b_index] = A[group1]
            b_index += 1; group1 +=1
    
    while group1 <= middle :
        buffer[b_index] = A[group1]
        b_index +=1; group1 +=1
    
    while group2 <= end :
        buffer[b_index] = A[group2]
        b_index += 1; group2 +=1
    
    group1 = start; b_index =0
    while group1 <= end :
        A[group1] = buffer[b_index]
        group1 +=1; b_index +=1


def heap(A) :
    buildHeap(A)
    for last in range(len(A)-1, 0, -1) :
        A[last], A[0] = A[0], A[last]
        percolateDown(A, 0, last-1)

def buildHeap(A) :
    for i in range( (len(A)-2)//2, -1, -1) :
        percolateDown(A, i, len(A)-1)

def percolateDown(A, start, end) :
    child = start *2 +1
    right = start *2 +2
    if child <= end :
        if right <= end and A[right] > A[child]:
            child = right
        if A[start] < A[child] :
            A[start],A[child] = A[child],A[start]
            percolateDown(A, child, end)
    

def count(A) :
    k = max(A)
    C = [0 for _ in range(k+1)]
    for i in range(len(A)) :
        C[A[i]] += 1
    for i in range(1,k+1) :
        C[i] = C[i] + C[i-1]

    B = [0 for _ in range(len(A))]
    for i in range(len(A)-1, -1, -1) :
        B[C[A[i]]-1] = A[i]
        C[A[i]] -= 1

    for i in range(len(A)) :
        A[i] = B[i]


import math
def radix(A) :
    digit = math.ceil(math.log10(max(A)))
    buffer = [[] for _ in range(10)]
    for i in range(digit) :
        for x in A :
            y = (x // 10**i)%10
            buffer[y].append(x)
        A.clear()
        for j in range(10) :
            A.extend(buffer[j])
            buffer[j].clear()


import math
def bucket(A) :
    n = len(A)
    buffer = [[] for _ in range(n)]
    for i in range(n) :
        buffer[math.floor(n*A[i])] = A[i]
    A.clear()
    for i in range(n) :
        insert(buffer[i])
        A.extend(buffer[i])

def main() : 
	list = [2,4,5,6,7,8,54,3,8,9,4,2,3,54,1,0,2,4,6,9,7,5,1,3,2,0,4,6,8,2]
	# list2 = [0.12,0.234,0.45,0.23,0.98,0.76,0.34]
	print(f'정렬 전 : {list}, 길이 : {len(list)}')
	start_time = time.time()
     

	radix(list)
     

	end_time = time.time()
	print(f'정렬 후 : {list}')
	print(f'시간 : {(end_time - start_time):.10f}')


if __name__ == '__main__' :
	main()