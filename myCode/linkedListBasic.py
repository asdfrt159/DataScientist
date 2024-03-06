from listNode import ListNode

class LinkedListBasic:

# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ 초기화 ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
	# 각각의 노드 값에는 객체 주소 값이 저장된다. (주소.item = value / 주소.next = 다음노드 주소)
	def __init__(self):
		self.__head = ListNode('dummy', None)	# ListNode 객체에서 값을 dummy, 연결값은 None으로 설정한다. (끝이기 때문)
		self.__numItems = 0  # 총 카운트 


# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ 필수함수 (insert, append, pop, )
	# [알고리즘 5 - 2] 구현: 연결 리스트에 원소 삽입하기(더미 헤드를 두는 대표 버전)
	def insert(self, i:int, newItem):
		if i >= 0 and i <= self.__numItems:  # 0이면 dummy만 있는상태
			prev = self.__getNode(i - 1)
			newNode = ListNode(newItem, prev.next)  # 이전 연결을 끊고 이전연결의 주소를 Node주소로 받고 
			prev.next = newNode  # 
			self.__numItems += 1  # 전체 갯수 1증가
		else:
			print("index", i, ": out of bound in insert()") # 필요 시 에러 처리

	def append(self, newItem):
		prev = self.__getNode(self.__numItems - 1)  # 처음이면 prev가 dummy node 의 주소값을 가르킨다.
		newNode = ListNode(newItem, prev.next)  # prev.next 가 None 이었으므로 newNode.next = prev.next = None 이다.
		prev.next = newNode  # prev.next 가 None 이었는데, 이걸 newNode를 가르키도
		self.__numItems += 1  # 전체 갯수 1증가

	# [알고리즘 5-3] 구현: 연결 리스트의 원소 삭제하기
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
	
	# [알고리즘 5 -4] 구현: 연결 리스트의 원소 x 삭제하기 (더미 헤드를 두는 대표 버전)
	def remove(self, x):  # remove는 값을 기준으로 삭제 pop은 index 기준으로 삭제
		(prev, curr) = self.__findNode(x)  # 쭉찾아도 없으면 None None
		if curr != None:  # 특정 값을 찾았으면
			prev.next = curr.next  # 중간을 점핑 시킨다. (삭제)
			self.__numItems -= 1
			return x
		else:
			return None

	# [알고리즘 5 - 5] 구현: 연결 리스트의 i번 원소 알려주기
	def get(self, i:int):
		if self.isEmpty():
			return None
		if (i >= 0 and i <= self.__numItems - 1):
			return self.__getNode(i).item  # i 번째 index Node 의 값을 알려준다.
		else:
			return None
 
	# [알고리즘 5 -7] 구현: x가 연결 리스트의 몇 번 원소인지 알려주기
	def index(self, x) -> int:
		curr = self.__head.next	 # 0번 노드:  더미 헤드 다음 노드
		for index in range(self.__numItems):  # 처음부터 쭉 돌면서 x 값을 찾는다.
			if curr.item == x:
				return index
			else:
				curr = curr.next
		return -2 # 안 쓰는 인덱스

	# [알고리즘 5 -8] 구현: 기타 작업들
	def isEmpty(self) -> bool:
		return self.__numItems == 0

	def size(self) -> int:
		return self.__numItems

	def clear(self):
		self.__head = ListNode("dummy", None)
		self.__numItems = 0

	def count(self, x) -> int:
		cnt = 0
		curr = self.__head.next  # 0번 노드
		while curr != None:
			if curr.item == x:
					cnt += 1
			curr = curr.next
		return cnt

	def extend(self, a): # 여기서 a는 self와 같은 타입의 리스트
		for index in range(a.size()):
			self.append(a.get(index))
 
	def copy(self):
		a = LinkedListBasic()
		for index in range(self.__numItems):
			a.append(self.get(index))
		return a

	def reverse(self):
		a = LinkedListBasic()
		for index in range(self.__numItems):
			a.insert(0, self.get(index))
		self.clear()
		for index in range(a.size()):
			self.append(a.get(index))

	def sort(self) -> None:
		a = []
		for index in range(self.__numItems):
			a.append(self.get(index))
		a.sort()
		self.clear()
		for index in range(len(a)):
			self.append(a[index])

	def __findNode(self, x) -> (ListNode, ListNode):
		prev = self.__head  # 더미 헤드부터 순차적으로 넘어감
		curr = prev.next    # 0번 index의 노드
		while curr != None:  # 값이 있으면 계속 진행
			if curr.item == x:  # 현재 node의 값이 x와 같으면 prev, curr return
				return (prev, curr)
			else:  # curr 값에 x가 없으면 다음 노드 검색 (현재 node를 이전 node 로 설정하고 curr를 현재 노드의 다음 값으로 설정)
				prev = curr; curr = curr.next
		return (None, None)  # 쭉 찾아도 없으면 None, None 리턴

	# [알고리즘 5-6] 구현: 연결 리스트의 i번 노드 알려주기 (특정 index를 넣었을때 해당 주소값을 리턴)
	#! 매개변수:int : 매개변수에 대한 주석이다. (없거나 다르더라도 에러가 발생하지 않는다.)
	#! 함수 -> : 함수의 return 값에 대한 주석이다. (없거나 다르더라도 에러가 발생하지 않는다.)
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
	
# 코드 5-15