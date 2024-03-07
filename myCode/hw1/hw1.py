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




# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

# 기본적인 listnode 형식의 class 생성
class ListNode :
	def __init__(self, key, value, next) : 
		self.key = key
		self.item = value
		self.next = next

# Linkedlist class 생성 (append(맨마지막추가), pop(맨마지막삭제))
class LinkedListBasic:
# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ 초기화 ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
	def __init__(self):
		self.__head = ListNode(None, 'dummy', None)	# ListNode 객체에서 값을 dummy, 연결값은 None으로 설정한다. (끝이기 때문)
		self.__numItems = 0  # 총 카운트 

	def append(self, key_x, newItem):
		prev = self.__getNode(self.__numItems - 1)  # 처음이면 prev가 dummy node 의 주소값을 가르킨다.
		newNode = ListNode(key_x, newItem, prev.next)  # prev.next 가 None 이었으므로 newNode.next = prev.next = None 이다.
		prev.next = newNode  # prev.next 가 None 이었는데, 이걸 newNode를 가르키도
		self.__numItems += 1  # 전체 갯수 1증가
		
	def pop(self, i:int):   # i번 노드 삭제. 고정 파라미터
		if (i >= 0 and i <= self.__numItems-1):
			prev = self.__getNode(i - 1)  # getnode (i=1 : curr = 첫번째 node)
			curr = prev.next  # 삭제하고자 하는 node 가르킴
			prev.next = curr.next  # 점핑 삭제하고자 하는 다음 주소를 이전 주소에 넣어버린다 (현재 node 정보 날라간다.)
			retItem = curr.item  # pop 이므로 현재 value 를 return 하기 위한 변수
			self.__numItems -= 1  # 전체 node 갯수 감소
			return retItem
		else:
			return None

	def __getNode(self, i:int) -> ListNode:  # 객체를 리턴한다는게 그 객체의 주소를 리턴한다는 것
		# -1 이면 range 함수가 안돌기 때문에 curr 값이 self.__head 가 된다.
		curr = self.__head # 더미 헤드, index: -1  
		for index in range(i+1):  # range는 0부터 ()값 미만으로 돈다 (0이면 실행안됨)
			curr = curr.next  # i=0 이면 1번 도니까 dummy.next 라서 처음 index가 나옴 
		return curr  # 해당 index의 객체값(주소값)을 리턴, 값을 알려면 객체값.item 해야함
	# getNode는 무조건 head 부터 시작해서 num의 갯수만큼 next로 진전한다. (ex, num = 1 curr.next / num =2 curr.next.next)


	def printList(self):
		curr = self.__head.next # 0번 노드: 더미 헤드 다음 노드
		while curr != None:
			print(curr.item, end = ' ')
			curr = curr.next
		print()



class HashOpenAddressed:

# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ 초기화 ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
	def __init__(self):
		self.__table = [LinkedListBasic() for i in range(101)]  # linkedlist로 리스트 초기화(dummy 값이 다 들어가 있음)
		self.__numItems = 0  # 숫자 카운트
		self.__DELETED = -54321  # __DELETED 이면 -54321 값을 넣는다.
		
		cnt =0
		for i in self.__table : 
			print(cnt,i.next)
			cnt += 1

# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ 해쉬함수 ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
	def __hash(self, key_x):  # x = key 값
		return key_x % 101 
			
				

# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ 필수함수 (삽입, 삭제, 검색) ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
	def insert(self, key_x, key_y):
		slot = self.__hash(key_x)
		print(slot)
		if self.__table[slot] == None :
			print(2)
			self.__table[slot].append(key_x, key_y)
			print(self.__table[slot])
		# if self.__numItems == 101:  # 꽉 차는경우 err 처리
		# 	""" 에러 처리 """

		# else:  # 꽉찬게 아니라면 실행됨
		# 	for i in range(101):  # 전체를 한번씩 돈다.
		# 		slot = self.__hash(i, x)  # 기본 h(x)는 i에 0을 넣고 돌린다. 
		# 		# 그 자리가 None 이거나, __DELETED 이면 그 자리에 값을 넣고 멈추고, 아니면 for 문 돈다.
		# 		if self.__table[slot] == None or self.__table[slot] == self.__DELETED:
		# 			self.__table[slot] = x  # index 에 x 넣고
		# 			self.__numItems += 1  # 값을 하나 올린다.
		# 			break

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








def main() :

	# 예제 입력
	input_str = '123 50 224 30 123 25 24 25 123 40 224 77 S 123 25 D 123 25 D 123 40 D 224 100'
	input_str = input_str.strip()
	insert_list, delete_list, search_list = classify_input(input_str)

	# 결과 출력
	print("Insert List:", insert_list)
	print("Delete List:", delete_list)
	print("Search List:", search_list)
	
	hash = HashOpenAddressed()
	hash.insert(123,50)

if __name__ == '__main__' :
	main()


