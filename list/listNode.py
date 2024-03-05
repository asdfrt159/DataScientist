class ListNode:
	def __init__(self, newItem, nextNode:'ListNode'):  # ListNode(값, 연결) 꼴로 넣어서 객체를 생성한다.
		self.item = newItem
		self.next = nextNode

# 코드 5-1