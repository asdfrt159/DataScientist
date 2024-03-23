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
			print(curr.key, curr.value, end = ' ')
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
		hashindex, linkindex = self.search(key,value)
		if hashindex != None :
			hashSlot = self.table[hashindex]  
			res = hashSlot.linkPop(linkindex-1) # search 에서 return +1 함
			return hashindex, res
		else : 
			return None, 'fail'

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
						return None, 'fail'
					else : 
						return i, index	+1	# index에 +1 해줘야한다.
		return None, 'fail'
	
	def printAll(self):
		for i in range(len(self.table)):
			print("Slot ", i, " : ", end=" ")
			if self.table[i].linklen() == -1:
				print("Empty")
			else:
				self.table[i].printList()
				




def main() :
	h = OpenAddressHashTable()
	output = []

	with open('input.txt', 'r') as f :
		input_str = f.read()
		# print(f'input : {input_str}')
		# print()

	input_str = input_str.strip()
	input_list = [i for i in input_str.split(' ')]
	
	# 입력 리스트를 순회하면서 분류
	i = 0
	while i < len(input_list):
		if input_list[i].isdigit():  # 현재 요소가 숫자인 경우
			next_i = i + 1  # 다음 요소
			if next_i < len(input_list) and input_list[next_i].isdigit():  # # 다음 요소도 숫자인 경우
				h.insert(int(input_list[i]), int(input_list[next_i]))
				i = next_i  # 다음 숫자도 처리됨
		else:
			# 현재 요소가 문자인 경우 (S 또는 D로 시작)
			command = input_list[i]
			num1 = int(input_list[i+1])
			num2 = int(input_list[i+2])
			if command == 'D':
				delete_hash, delete_res = h.delete(num1, num2)
				if delete_res == 'fail' :
					output.extend(['D',str(delete_res)])
				else :
					if delete_res == None :
						delete_res = 'none'
					output.extend(['D',str(delete_hash),str(delete_res)])
			elif command == 'S':
				search_hash, search_res = h.search(num1, num2)
				if search_res == 'fail' :
					output.extend(['S',str(search_res)])
				else :
					output.extend(['S',str(search_hash), str(search_res)])
			i += 2  # 두 숫자를 건너뜀
		i += 1
	
	output_res = ' '.join(output)

	# print()
	# print(f"output : {output_res}")
	with open('output.txt','w') as f :
		f.write(output_res)


if __name__ == '__main__' :
	main()


