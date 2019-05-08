from Node import Node, LeafNode, Pair
MAX_INT = 20000000000

class B_tree:
    def __init__(self, B_size):
        self.B_size = B_size
        self.root = LeafNode(elements=[Pair(MAX_INT, None)])

    def traverse_to_leaf(self, key):
        cur_node = self.root
        while not cur_node.is_leaf:
            index = cur_node.traverse(key=key)
            cur_node = cur_node.elements[index].value
        return cur_node

    def insert(self, key, value):
        # DEBUG = True if key == 1000 else False
        leaf_node = self.traverse_to_leaf(key)
        node = leaf_node
        node.add_element(key, value)
        while node.is_overload(B_size=self.B_size):
            # if DEBUG: print('node :', node)
            par_node = node.parent
            left_node, right_node = node.split()
            if par_node:
                par_node.remove_element(key=node.max_key, value=node.max_value)
            else:
                par_node = Node()
                node.parent = par_node
                self.root = par_node
            par_node.add_child(key=left_node.max_key, child=left_node)
            par_node.add_child(key=right_node.max_key, child=right_node)
            if isinstance(left_node, LeafNode) and isinstance(right_node, LeafNode):
                left_node.set_prev(node.prev)
                left_node.set_next(right_node)
                right_node.set_next(node.next)
            del node
            node = par_node

    def mergeable(self, node1, node2):
        if not node1 or not node2: return False
        return len(node1.elements) + len(node2.elements) <= self.B_size

    @staticmethod
    def merge_nodes(node1, node2):
        par_node = node1.parent
        Type = type(node1)
        new_node = Type(elements=sorted(
                            node1.elements + node2.elements,
                            key=lambda x: x.key))
        if par_node:
            par_node.remove_element(key=node1.max_key, value=node1)
            par_node.remove_element(key=node2.max_key, value=node2)
            par_node.add_child(key=new_node.max_key, child=new_node)
        del node1
        del node2
        return new_node

    def delete(self, key, value=None):
        node = self.traverse_to_leaf(key)
        index = node.traverse(key=key)
        if node.elements[index].key != key: return
        old_max_key = node.max_key
        node.remove_element(key=key, value=value)
        if node.parent:
            index = node.parent.traverse(key=old_max_key)
            node.parent.elements[index].key = node.max_key
        while not node.is_root:
            siblings = node.find_siblings()
            print(siblings[1])
            par_node = node.parent
            for s in siblings:
                if self.mergeable(s, node):
                    print('merging: ', node, s)
                    new_node = self.merge_nodes(s, node)
                    if len(par_node.elements) == 1:
                        self.root = new_node
                        new_node.parent = None
                        return
                    break
            node = par_node

    def get(self, key):
        node = self.traverse_to_leaf(key=key)
        index = node.traverse(key=key)
        if node.elements[index].key != key: return None
        return node.elements[index].value

    @staticmethod
    def traverse(node):
        print(node)
        if isinstance(node, LeafNode):
            print(f'   prev={id(node.prev)} next={id(node.next)}')
        for _ in node.elements:
            if isinstance(_.value, Node):
                B_tree.traverse(_.value)

    def display(self):
        print('----------------------')
        B_tree.traverse(self.root)
        print('----------------------')
