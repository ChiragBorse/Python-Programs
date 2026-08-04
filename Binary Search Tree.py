class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

class BinarySearchTree:
    def insert(self, root, key):
        if root is None:
            return Node(key)
        if key < root.val:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)
        return root

    def inorder(self, root):
        if root:
            self.inorder(root.left)
            print(root.val, end=" ")
            self.inorder(root.right)

bst = BinarySearchTree()
root = None

numbers = [50, 30, 20, 40, 70, 60, 80]

for num in numbers:
    root = bst.insert(root, num)

print("Inorder Traversal:")
bst.inorder(root)
