class tree:
    def __init__(self,key):
        self.left = None
        self.right = None
        self.value = key

def insert(node, value):
    if node is None:
        return (tree(value))

    else:
        # 2. Otherwise, recur down the tree
        if value <= node.value:
            node.left = insert(node.left, value)
        else:
            node.right = insert(node.right, value)

        # Return the (unchanged) node pointer
        return node
'''


def insert(self, data):

    if self.data:

        if data < self.data:

            if self.left is None:
                self.left = Node(data)
            else:
                self.left.insert(data)

        elif data > self.data:

            if self.right is None:

                self.right = Node(data)

            else:

                self.right.insert(data)

        else:

            self.data = data

'''
def size(root):
    if root is None:
        return 0
    else:
        return (size(root.left)+ 1 + size(root.right))

def inorder(node):
    if node:
        inorder(node.left)
        print(node.value)
        inorder(node.right)

def find_node(root,key):
    if root is None or root.value == key:
        return root

    if root.value < key:
        if find_node(root.right,key):
            return True
        elif find_node(root.left,key):
            return True
        else:
            return False


def minvalue(self):
        if self.left:
            return self.left.minvalue()
        else:
            return self.value

def maxvalue(root):
    while(root.right is not None):
        root = root.right
    return root.value



r = tree(6)
insert(r,15)
insert(r,13)
insert(r,8)
insert(r,9)
insert(r,40)
insert(r,70)
insert(r,9)
insert(r,10)


def convertBST(self, root):
    p, acc = root, 0
    while p:
        if p.right:
            pre = p.right
            while pre.left and pre.left is not p: pre = pre.left
            if pre.left:
                p.value += acc
                acc = p.value
                pre.left = None
                p = p.left
            else:
                pre.left = p
                p = p.right
        else:
            p.value += acc
            acc = p.value
            p = p.left
    return root



print(inorder(r))
#print(inorder(convertBST(0,r)))
#print(size(r))
print(find_node(r,10))

#print(minvalue(r))
#print(maxvalue(r))


