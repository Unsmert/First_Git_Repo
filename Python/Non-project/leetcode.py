class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def create_node(sorted_list):
    if sorted_list == []:
        return None
    value = sorted_list.pop(-1)
    return ListNode(val = value, next = create_node(sorted_list))

def print_list_node(list_node):
    print_list = []
    node = list_node
    while node != None:
        print_list.append(node.val)
        node = node.next
    
    print(print_list)

print_list_node(create_node([4, 4, 3, 2, 1, 1]))