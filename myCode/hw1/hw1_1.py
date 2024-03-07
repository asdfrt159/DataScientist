# input 값 list 형식으로 분류
def classify_input(input_str):
	# 입력 문자열을 공백으로 분리하여 리스트로 변환
	input_list = [i for i in input_str.split(' ')]
	
	# 결과를 저장할 리스트 초기화
	insert_list = []
	delete_list = []
	search_list = []
	
	# 입력 리스트를 순회하면서 분류
	i = 0
	while i < len(input_list):
		# 현재 요소가 숫자인 경우
		if input_list[i].isdigit():
			next_i = i + 1
			# 다음 요소도 숫자인 경우
			if next_i < len(input_list) and input_list[next_i].isdigit():
				insert_list.append([int(input_list[i]), int(input_list[next_i])])
				i = next_i  # 다음 숫자도 처리됨
		else:
			# 현재 요소가 문자인 경우 (S 또는 D로 시작)
			command = input_list[i]
			num1 = int(input_list[i+1])
			num2 = int(input_list[i+2])
			if command == 'D':
				delete_list.append([num1, num2])
			elif command == 'S':
				search_list.append([num1, num2])
			i += 2  # 두 숫자를 건너뜀
		i += 1
	
	return insert_list, delete_list, search_list





class Node:
	def __init__(self, key, value):
		self.key = key
		self.value = value
		self.next = None


class LinkedList : 
	def __init__(self) :  # 더미 key, val 생성
		self.head = Node('dummy_key', 'dummy_val')
		self.num = -1 # index 값

	def getNode(self, i) : # index 번째의 Node 주소값 리턴
		curr = self.head
		for index in range(i+1) :  # 노드갯수 = self.num(index) + 1
			curr = curr.next
		return curr
	
			
	def findindex(self, x) :
		curr = self.head.next # 0번째 index 가르킴
		for index in range(self.num+1) : #전체 갯수 검색
			if curr.value == x :
				return index
			else :
				curr = curr.next
		return None

	def linkAppend(self, key, value) :
		prev = self.getNode(self.num) 
		newNode = Node(key, value)
		prev.next = newNode
		self.num += 1

	# 삭제 했을때는 삭제한 slot 과 그 다음 Node의 value값 리턴
	def linkPop(self, i) : # index 번째의 Node 삭제후 그다음 Node value 리턴
		if (i>=0 and i <= self.num) :
			prev = self.getNode(i-1)
			curr = prev.next
			prev.next = curr.next
			self.num -= 1
			if curr.next == None :
				return None
			else : 
				popValue = curr.next.value  # 다음 노드의 값
				return popValue
		else :
			return None
		
	def linklen(self) :
		return self.num
	
	
	def printList(self):
		curr = self.head.next # index 노드
		while curr != None:
			print(curr.value, end = ' ')
			curr = curr.next
		print()
	

class OpenAddressHashTable:
	def __init__(self, size=101):
		self.size = size
		self.table = [LinkedList() for i in range(self.size)]

	def hash_function(self, key, iter):  # 처음에는 key % self.size
		return (key + iter) % self.size

	def insert(self, key, value):
		for i in range(self.size) :
			index = self.hash_function(key,i)
			hashSlot = self.table[index]
			# Slot이 비어있으면 바로 Node를 추가
			if hashSlot.linklen() == -1 :
				hashSlot.linkAppend(key,value)
				break

			# Slot이 비어있지 않으면, key 값이 같은지 보고, 같으면 링크, 다르면 다음 해쉬
			else:
				if hashSlot.getNode(0).key == key : 
					hashSlot.linkAppend(key, value)
					break
				else : 
					continue

	def delete(self, key, value) :
		for i in range(self.size) :
			if self.table[i].linklen() != -1 :
				if self.table[i].getNode(0).key == key :
					print(self.table[i].getNode(0).key)
			else : 
				continue

	def search(self, key, value):
		for i in range(self.size) :
			hashSlot = self.table[i]
			if hashSlot.linklen() == -1 :  # 비어있음
				continue
			else :  # 비어있지 않으면 key를 비교
				if hashSlot.getNode(0).key != key :
					continue
				else : 
					index = hashSlot.findindex(value)
					if index == None :
						return 'fail'
					else : 
						return index

		return 'fail'
	
		# index = self.hash_function(key)
		# current = self.table[index]
		# while current:
		# 	if current.key == key:
		# 		return current.value
		# 	current = current.next
		# return None
	
	def printAll(self):
		for i in range(len(self.table)):
			print("Slot ", i, " : ", end=" ")
			if self.table[i].linklen() == -1:
				print("Empty")
			else:
				# for j in range(len(self.table[i])):
				# 	print(self.table[i][j], end=" ")
				# print()
				self.table[i].printList()
				







def main() :

	# 예제 입력
	input_str = '123 50 224 30 123 25 24 25 123 40 224 77 S 123 25 D 123 25 D 123 40 D 224 100'
	input_str = input_str.strip()
	insert_list, delete_list, search_list = classify_input(input_str)

	# 결과 출력
	print("Insert List:", insert_list)
	print("Delete List:", delete_list)
	print("Search List:", search_list)

	h = OpenAddressHashTable()
	h.insert(123,30)
	h.insert(22,20)
	h.insert(22,25)
	h.insert(23,2)
	h.insert(224,3)
	h.insert(123,40)
	h.insert(123,50)
	
	h.printAll()

	print(h.search(22,25))
if __name__ == '__main__' :
	main()


