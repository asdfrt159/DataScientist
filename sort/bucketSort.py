import math
from insertionSort import insertionSort

def bucketSort(A):  # [0, 1) 범위의 실수 정렬
	n = len(A)
	B = [[] for _ in range(n)]
	for i in range(n):
		B[math.floor(n*A[i])].append(A[i])
	A.clear()
	for i in range(n):
		insertionSort(B[i])
		A.extend(B[i])


A= [2,3,12,4,5]
bucketSort(A)
print(A)
# 코드 9-11

