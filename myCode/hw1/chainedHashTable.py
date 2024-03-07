from circularLinkedList import *
from listNode import *

class ChainedHashTable:

# --------------- 초기화 ----------------
	def __init__(self, n):
		self.__table = [CircularLinkedList() for i in range(n)]
		self.__numItems = 0
		for i in self.__table : 
			print(i.printList())

# --------------- 해쉬 함수 ---------------

	def __hash(self, x:int): # 편의상 int 타입으로 제한
		return x % len(self.__table)
	
# --------------- 필수 함수 (삽입, 삭제, 검색) --------------------

	# [알고리즘 12-1] 구현: 검색, 삽입, 삭제
	def insert(self, x:int):
		slot = self.__hash(x)
		self.__table[slot].insert(0, x)
		self.__numItems += 1

	def search(self, x:int) -> ListNode:
		slot = self.__hash(x)
		if self.__table[slot].isEmpty():
			return None # null list
		else:
			head = prev = self.__table[slot].getNode(-1)  # 더미 헤드
			curr = prev.next  # 0번 노드
			while curr != head:
				if curr.item == x:
					return curr
				else:
					prev = curr; curr = curr.next
			return None
		
	def delete(self, x:int):
		slot = self.__hash(x)
		success = self.__table[slot].remove(x)
		if success != None:
			self.__numItems -= 1

#--------------- 보조 함수 (isempty, clear, print)---------------

 	# 기타
	def isEmpty(self):
		return self.__numItems == 0

	def clear(self):
		for i in range(len(self.__table)):
			self.__table[i] = CircularLinkedList()
		self.__numItems = 0

# 코드 12-1
		

print("List Hash Table Demo!")
h = ChainedHashTable(11)
h.insert(10)
# print(h._ChainedHashTable__table)
h.insert(21)
#h.delete(20)   # 아무 영향 없어야 함
h.insert(20)
h.insert(5)
h.insert(80)
h.insert(32)
# h.printAll()
# print(h._ChainedHashTable__table)
h.delete(20)
h.delete(80)
# print(h._ChainedHashTable__table)
# Just for checking purpose
item = 32
print(h.search(item).item)
# (i, j) = h.search(item)