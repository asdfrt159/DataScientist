def bubbleSort(A):
	for numElements in range(len(A), 0, -1):   # 시작 : 원소갯수(n) / 끝 : 1 / 간격 : -1
		for i in range(numElements-1):  # 시작 : 0 / 끝 : n-2 / 간격 : 1
			if A[i] > A[i+1]:
				A[i], A[i+1] = A[i+1], A[i]

