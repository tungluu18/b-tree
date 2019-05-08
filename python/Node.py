class Pair:
    def __init__(self, key, value=None):
        self.key = key
        self.value = value

    def __str__(self): return f'({self.key}, {self.value})'


class Node:
    def __init__(self, parent=None, elements=[]):
        self.parent = parent
        self.elements = elements
        for _ in self.elements:
            if isinstance(_.value, Node): _.value.parent = self

    def find_siblings(self):
        par_node = self.parent
        if not par_node: return None
        m = len(par_node.elements)
        for index in range(m):
            if par_node.elements[index].value == self:
                return (
                    par_node.elements[index-1].value if index else None,
                    par_node.elements[index+1].value if index+1 < m else None)


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

    def add_child(self, key, child):
        self.add_element(key=key, value=child)
        child.parent = self

    def remove_element(self, key=None, value=None):
        for i in range(len(self.elements)):
            if self.elements[i].key == key and (not value or self.elements[i].value == value):
                del self.elements[i]
                return

    def traverse(self, key):
        for i in range(len(self.elements)):
            if self.elements[i].key >= key: return i
        return -1

    def split(self):
        if len(self.elements) == 0:
            raise ValueError(f'Node has no element!')
        n = len(self.elements) // 2
        Type = type(self)
        return Type(elements=self.elements[:n]), \
               Type(elements=self.elements[n:])

    @property
    def max_key(self):
        return self.elements[-1].key

    @property
    def is_leaf(self):
        return False

    @property
    def is_root(self):
        return self.parent == None

    def is_overload(self, B_size):
        return len(self.elements) > B_size

    def __str__(self):
        str_elements = ''
        for _ in self.elements:
            if self.is_leaf:
                str_elements += f'({_.key}, {_.value}) '
            else:
                str_elements += f'({_.key}, {id(_.value)}) '
        return f'{"Leaf " if self.is_leaf else ""}Node {id(self)}' + f'\n   elements=[{str_elements}]' + f'\n   parent={id(self.parent)}'


class LeafNode(Node):
    def __init__(self, parent=None, prev=None, next=None, elements=[]):
        super().__init__(parent=parent, elements=elements)
        self.prev = prev
        self.next = next

    def set_next(self, _next):
        self.next = _next
        if isinstance(_next, LeafNode):
            _next.prev = self

    def set_prev(self, _prev):
        self.prev = _prev
        if isinstance(_prev, LeafNode):
            _prev.next = self

    @property
    def is_leaf(self):
        return True
