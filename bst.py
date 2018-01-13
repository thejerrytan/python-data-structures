class Node:
    def __init__(self, val, parent):
        self.val = val
        self.leftChild = None
        self.rightChild = None
        self.parent = parent
        self.hasTraversedLeft = False
        self.hasTraversedRight = False
    
    def __str__(self):
        return "Node(%s)" % self.val

    def get(self):
        return self.val
    
    def set(self, val):
        self.val = val
        
    def getChildren(self):
        children = []
        if (self.leftChild != None):
            children.append(self.leftChild)
        if (self.rightChild != None):
            children.append(self.rightChild)
        return children

    def isLeftChild(self):
        if self.parent is None: return False
        return (self.val <= self.parent.val)

    def isRightChild(self):
        if self.parent is None: return False
        return (self.val > self.parent.val)

# Duplicates are kept as left child of currentNode        
class BST:
    def __init__(self):
        self.root = None

    # def __str__(self):
    #     ans = []
    #     currentNode = self.root
    #     while currentNode

    def setRoot(self, val):
        self.root = Node(val, None)

    def insert(self, val):
        if(self.root is None):
            self.setRoot(val)
        else:
            self.insertNode(self.root, val)

    def insertNode(self, currentNode, val):
        if (val <= currentNode.val):
            if (currentNode.leftChild):
                self.insertNode(currentNode.leftChild, val)
            else:
                currentNode.leftChild = Node(val, currentNode)
        elif (val > currentNode.val):
            if (currentNode.rightChild):
                self.insertNode(currentNode.rightChild, val)
            else:
                currentNode.rightChild = Node(val, currentNode)

    def remove(self, val, startNode=None):
        target = self.find(val, startNode)
        if target is not None:
            if target is self.root:
                if target.leftChild is None and target.rightChild is None:
                    self.root = None
                elif target.leftChild is None and target.rightChild is not None:
                    self.root = target.rightChild
                elif target.leftChild is not None and target.rightChild is None:
                    self.root = target.leftChild
                elif target.leftChild is not None and target.rightChild is not None:
                    rightMin = self.min(target.rightChild)
                    target.val = rightMin
                    self.remove(rightMin, target.rightChild)
                else:
                    return False
                return True
            else:
                if target.leftChild is None and target.rightChild is None:
                    if target.parent.val > target.val: target.parent.leftChild = None
                    elif target.parent.val == target.val: target.parent.rightChild = None
                    elif target.parent.val < target.val: target.parent.rightChild = None
                elif target.leftChild is None and target.rightChild is not None:
                    if target.parent.val > target.val: target.parent.leftChild = target.rightChild
                    elif target.parent.val == target.val: target.parent.rightChild = target.rightChild
                    elif target.parent.val < target.val: target.parent.rightChild = target.rightChild
                    target.rightChild.parent = target.parent
                elif target.leftChild is not None and target.rightChild is None:
                    if target.parent.val > target.val: target.parent.leftChild = target.leftChild
                    elif target.parent.val == target.val: target.parent.rightChild = target.leftChild
                    elif target.parent.val < target.val: target.parent.rightChild = target.leftChild
                    target.leftChild.parent = target.parent
                elif target.rightChild is not None and target.rightChild is not None:
                    rightMin = self.min(target.rightChild)
                    target.val = rightMin
                    self.remove(rightMin, target.rightChild)
                else:
                    # Funny edge case
                    return False
                return True
        else:
            return False


    def find(self, val, startNode=None):
        # Returns node if found, else None
        return self.findNode(self.root if startNode is None else startNode, val)

    def getPredecessor(self, val):
        n = self.find(val)
        if n is not None:
            # Case 1: Node has a left subtree
            if n.leftChild is not None:
                return self.max(n.leftChild, returnVal=False)
            else:
                # Case 2: Node has no left subtree, it is the left child of its parent
                predecessor = n
                while predecessor.isLeftChild():
                    predecessor = predecessor.parent
                # Case 3: Node has no left subtree, it is the right child of its parent
                return predecessor.parent
        else:
            return None

    # Return smallest Node greater than val
    def getSuccessor(self, val):
        n = self.find(val)
        if n is not None:
            # Case 1: Node has a right subtree
            if n.rightChild is not None:
                return self.min(n.rightChild, returnVal=False)
            else:
                # Case 2: Node has no right subtree, it is the right child of its parent
                successor = n
                while successor.isRightChild():
                    successor = successor.parent
                # Case 3: Node has no right subtree, it is left child of its parent
                return successor.parent
        else:
            return None

    def findNode(self, currentNode, val):
        if(currentNode is None):
            return None
        elif(val == currentNode.val):
            return currentNode
        elif(val < currentNode.val):
            return self.findNode(currentNode.leftChild, val)
        else:
            return self.findNode(currentNode.rightChild, val)

    def min(self, node=None, returnVal=True):
        if self.root is None: return None
        currentNode = self.root if node is None else node
        while currentNode.leftChild is not None:
            currentNode = currentNode.leftChild
        return currentNode.val if returnVal else currentNode

    def max(self, node=None, returnVal=True):
        if self.root is None: return None
        currentNode = self.root if node is None else node
        while currentNode.rightChild is not None:
            currentNode = currentNode.rightChild
        return currentNode.val if returnVal else currentNode

    # Iterative in-order traversal of nodes
    def sort(self, reverse=False):
        # Returns tree in ascending order
        import copy
        currentNode = copy.deepcopy(self.root)
        while True:
            if currentNode.hasTraversedLeft and currentNode.hasTraversedRight and currentNode.parent is None:
                break
            else:
                if not currentNode.hasTraversedLeft:
                    currentNode.hasTraversedLeft = True
                    if currentNode.leftChild is not None: currentNode = currentNode.leftChild
                else:
                    if not currentNode.hasTraversedRight:
                        yield currentNode.val
                        currentNode.hasTraversedRight = True
                        if currentNode.rightChild is not None: currentNode = currentNode.rightChild
                    else:
                        currentNode = currentNode.parent


def test():
    data = [10,4,5,2,3,8,9,9]
    t = BST()
    for i in data:
        t.insert(i)

    # Test sort
    sorted = []
    for i in t.sort():
        sorted.append(i)
    assert(sorted == [2,3,4,5,8,9,9,10])

    # Test min max
    assert(t.min() == 2)
    assert(t.max() == 10)
    t.insert(11)
    assert(t.max() == 11)
    t.insert(-10)
    assert(t.min() == -10)

    # Test find
    assert(t.find(10).val == 10)

    # Test remove
    assert(t.remove(9) == True)
    assert(t.remove(10) == True)
    assert(t.remove(6) == False)
    sorted = []
    for i in t.sort():
        sorted.append(i)
    assert(sorted == [-10, 2, 3, 4, 5, 8, 9, 11])

    # Current state of tree
    #       11
    #      / 
    #     4
    #    / \
    #   2   5
    #  / \    \
    #-10  3    8
    #           \
    #            9

    # Test getSuccessor
    assert(t.getSuccessor(4).val == 5)
    assert(t.getSuccessor(2).val == 3)
    assert(t.getSuccessor(3).val == 4)
    assert(t.getSuccessor(9).val == 11)
    assert(t.getSuccessor(-10).val == 2)
    assert(t.getSuccessor(15) == None)
    assert(t.getSuccessor(11) == None)

    # Test getPredecessor
    assert(t.getPredecessor(4).val == 3)
    assert(t.getPredecessor(2).val == -10)
    assert(t.getPredecessor(3).val == 2)
    assert(t.getPredecessor(5).val == 4)
    assert(t.getPredecessor(9).val == 8)
    assert(t.getPredecessor(-10) == None)
    assert(t.getPredecessor(11).val == 9)
    assert(t.getPredecessor(15) == None)

if __name__ == "__main__":
    test()