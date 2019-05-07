class Pair:
    def __init__(self, key, value=None):
        self.key = key
        self.value = value

    def __str__(self): return f'({self.key}, {self.value})'


class Node:
    def __init__(self, parent=None, elements=[]):
        self.parent = parent
        self.elements = elements

    def add_element(self, key, value):
        insert_position = len(self.elements)  # insert new element at the end by default
        for i in range(len(self.elements)):
            if self.elements[i].key > key:
                insert_position = i
                break
        self.elements = self.elements[:insert_position] \
            + [Pair(key, value)] \
            + self.elements[insert_position:]
        return insert_position

    def traverse(self, key):
        for i in self.elements:
            if self.elements[i].key >= key: return i
        return -1

    def split_largest_element(self):
        if len(self.elements) == 0:
            raise ValueError(f'Node has no element!')
        splitted_element = self.elements[-1]
        del self.elements[-1]
        return splitted_element

    @property
    def is_leaf(self):
        return False

    @property
    def is_root(self):
        return self.parent == None

    def __str__(self):
        str_elements = ''
        for _ in self.elements:
            str_elements += f' {str(_)}\n'
        return '[\n' + str_elements + ']'


class LeafNode(Node):
    def __init__(self, parent=None, prev=None, next=None, refs=[]):
        super().__init__(parent=parent, elements=refs)
        self.prev = prev
        self.next = next

    def set_next(self, next):
        self.next = next

    def set_prev(self, prev):
        self.prev = prev

    @property
    def is_leaf(self):
        return True
