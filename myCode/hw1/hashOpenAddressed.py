class HashOpenAddressed:

# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ 초기화 ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
	def __init__(self, n:int):
		self.__table = [None for i in range(n)]  # None 값으로 리스트 초기화
		self.__numItems = 0  # 숫자 카운트
		self.__DELETED = -54321  # __DELETED 이면 -54321 값을 넣는다.

# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ 해쉬함수 ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
	def __hash(self, i:int, x):
		return (x + i) % len(self.__table)
 
# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ 필수함수 (삽입, 삭제, 검색) ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
	def insert(self, x):
		if self.__numItems == len(self.__table):  # 꽉 차는경우 err 처리
			""" 에러 처리 """

		else:  # 꽉찬게 아니라면 실행됨
			for i in range(len(self.__table)):  # 전체를 한번씩 돈다.
				slot = self.__hash(i, x)  # 기본 h(x)는 i에 0을 넣고 돌린다. 
				# 그 자리가 None 이거나, __DELETED 이면 그 자리에 값을 넣고 멈추고, 아니면 for 문 돈다.
				if self.__table[slot] == None or self.__table[slot] == self.__DELETED:
					self.__table[slot] = x  # index 에 x 넣고
					self.__numItems += 1  # 값을 하나 올린다.
					break

	NOT_FOUND = -12345  # constant
	def search(self, x) -> int:
		for i in range(len(self.__table)):  # 전체를 한번씩 도는데
			slot = self.__hash(i, x)  # i를 0부터 넣어서 값을 찾는다.
			if self.__table[slot] == None:  # 값이 비어있으면 못찾았다고 리턴한다. (삭제해도 결국 넘어가서 못찾았다고 인식)
			# 순차적으로 해쉬함수가 적용되기 때문에 처음 만나는게 None이면 이후에도 없다 생각하고 못찾았다고함
				return HashOpenAddressed.NOT_FOUND
			if self.__table[slot] == x:  # 찾으면 index를 리턴
				return slot  # Found at self.__table[slot]
		return self.__NOT_FOUND  # 전부다 다른 값이 들어있거나 __DELETED 들어있으면

	def delete(self, x):
		for i in range(len(self.__table)):  # 전체를 한번씩 훑는데
			slot = self.__hash(i, x)  # i를 0부터 넣어서 값을 찾는다.
			if self.__table[slot] == None:  # i를 처음부터 끝까지 전체를 다 돌면 아예 없는거라서 멈춘다.
				break
			if self.__table[slot] == x:  # i를 돌다가 특정 index에 x 값이 있으면 찾고 멈춘다.
				self.__table[slot] = self.__DELETED  # 찾으면 삭제 하고 DELETED 됬다고 표시한다.
				self.__numItems -= 1  # 삭제하고 전체 길이를 하나 빼준다.
				break

# 코드 12-3