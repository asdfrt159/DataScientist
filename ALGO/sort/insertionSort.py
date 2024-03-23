def insertionSort(A):
	for i in range(1, len(A)):  # 1부터 < 최대 갯수 까지
		loc = i-1
		newItem = A[i]
		while loc >= 0 and newItem < A[loc]:
			A[loc+1] = A[loc]
			loc -= 1
		A[loc+1] = newItem

# 코드 9-3