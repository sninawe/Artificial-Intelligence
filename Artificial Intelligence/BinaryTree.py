class Item():
    def __init__(self,key):
        self.left = None
        self.right = None
        self.val = key

def insert(root,node):
#Check if root node is present if not insert the item as Root node
    if root is None:
        root = node
    else:
#Inserting item to the left is value is greater than root.
        if root.val > node.val:
#Check if left has no elements
            if root.left is None:
                root.left = node
            else:
#If left has already elements call the Insert function with left item to insert
                insert(root.left, node)
        else:
#Check if right has no elements
            if root.right is None:
                root.right = node
            else:
#If right has already elements call the Insert function with right item to insert
                insert(root.right, node)


def contains(root, x):
#Check if root is not empty
    if root is not None:
#Check if root is equal to value provided
        if root.val == x:
            return True
#If not then call function again checking for left and right elements with the number provided
        else:
            return contains(root.left, x) or contains(root.right, x)
#If not, return False
    return False


def inorder(root):
#If item is present then first print the smallest items and then the largest items in ascending order
    if root:
        inorder(root.left)
        print(root.val)
        inorder(root.right)

#Check the size of the tree
def size(root):
    if root is None:
        return 0
    else:
        return (size(root.left)+ 1 + size(root.right))

#Traverse to the left of the tree to find out the smallest item in the tree
def smallest(root):
    while(root.left is not None):
        root = root.left
    return root.val

#Traverse to the right of the tree to find out the largest item in the tree
def largest(root):
    while(root.right is not None):
        root = root.right
    return root.val

def greaterSumTree(root):
        total = 0
        item = root
        l = []
        while l or item is not None:
            while item is not None:
                l.append(item)
                item = item.right
            item = l.pop()
            total += item.val
            item.val = total
            item = item.left
        return root


r = Item(10)
insert(r,Item(20))
insert(r,Item(30))
insert(r,Item(40))

inorder(r)
print(size(r))
print(contains(r,2))
print(smallest(r))
print(largest(r))
inorder(greaterSumTree(r))