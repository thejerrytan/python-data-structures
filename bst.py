class Node(object):
    def __init__(self, val, parent):
        self.val = val
        self.leftChild = None
        self.rightChild = None
        self.parent = parent
        self.hasTraversedLeft = False
        self.hasTraversedRight = False
    
    def __str__(self):
        return "Node(%s)" % self.val

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__ and 
            self.val == other.val
            )

    def __ne__(self, other):
        return not self.__eq__(other)

    def get(self):
        return self.val
    
    # Note: when a node is used in a BST, a node's val is immutable 
    # DO NOT change a node's value using n.set(newVal) or directly by n.val = newVal
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
class BST(object):
    def __init__(self):
        self.root = None

    def __eq__(self, other):
        currentSelfNode = self.root
        currentOtherNode = other.root
        if currentSelfNode is not None and currentOtherNode is not None:
            selfStack = [currentSelfNode]
            otherStack = [currentOtherNode]
            while selfStack and otherStack:
                currentSelfNode = selfStack.pop()
                currentOtherNode = otherStack.pop()
                if currentSelfNode != currentOtherNode:
                    return False
                else:
                    # Depth-first in-order traversal
                    if currentSelfNode.rightChild is not None: selfStack.append(currentSelfNode.rightChild)
                    if currentOtherNode.rightChild is not None: otherStack.append(currentOtherNode.rightChild)
                    if currentSelfNode.leftChild is not None: selfStack.append(currentSelfNode.leftChild)
                    if currentOtherNode.leftChild is not None: otherStack.append(currentOtherNode.leftChild)
            return True
        elif currentSelfNode != currentOtherNode:
            return False
        else:
            # Both roots are None
            return True

    def __ne__(self, other):
        return not self.__eq__(other)

    # TODO: a string represetation of a BST
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
                    self.remove(rightMin, target.rightChild)
                    target.val = rightMin
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
                    self.remove(rightMin, target.rightChild)
                    target.val = rightMin
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

    def leftRotate(self, val, startNode=None):
        # Let x be node you are rotating, y be x.rightChild
        # left-rotate x would place 
        #   y.leftChild under x.rightChild
        #   parent of y = parent of x
        #   y.leftChild = x
        #     x                 y
        #    / \               / \
        #   A   y      =>     x   C
        #      / \           / \
        #     B   C         A   B
        x = startNode if startNode is not None else self.find(val)
        if x is not None:
            y = x.rightChild
            if y is None: return # invalid operation
            parentOfX = x.parent
            # Change parent of x
            if parentOfX is not None:
                y.parent = parentOfX
                if x.isLeftChild():
                    parentOfX.leftChild = y
                else:
                    parentOfX.rightChild = y
            else:
                # x is root
                self.root = y
                y.parent = None
            
            # Change right child of x
            x.rightChild = y.leftChild
            if y.leftChild is not None: y.leftChild.parent = x

            # Change left child of y
            y.leftChild = x
            x.parent = y

    def rightRotate(self, val, startNode=None):
        # Opposite of leftRotate
        #     y               x      
        #    / \             / \
        #   x   C    =>     A   y
        #  / \                 / \
        # A   B               B   C  
        #
        y = startNode if startNode is not None else self.find(val)
        if y is not None:
            x = y.leftChild
            if x is None: return # invalid operation
            parentOfY = y.parent
            # Change parent of y
            if parentOfY is not None:
                x.parent = parentOfY
                if y.isLeftChild():
                    parentOfY.leftChild = x
                else:
                    parentOfY.rightChild = x
            else:
                # y is root
                self.root = x
                x.parent = None

            # Change left child of y
            y.leftChild = x.rightChild
            if x.rightChild is not None: x.rightChild.parent = y

            # Change rightChild of x
            x.rightChild = y
            y.parent = x

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

    # Test leftRotate
    t.leftRotate(4)
    assert(t.find(11).leftChild.val == 5)
    assert(t.find(5).parent.val == 11)
    assert(t.find(4).parent.val == 5)
    assert(t.find(5).leftChild.val == 4)
    assert(t.find(4).leftChild.val == 2)
    assert(t.find(2).parent.val == 4)
    assert(t.find(4).rightChild == None)
    assert(t.find(5).rightChild.val == 8)
    assert(t.find(8).parent.val == 5)

    # Test rightRotate
    t.rightRotate(5)
    assert(t.find(11).leftChild.val == 4)
    assert(t.find(4).parent.val == 11)
    assert(t.find(4).leftChild.val == 2)
    assert(t.find(2).parent.val == 4)
    assert(t.find(4).rightChild.val == 5)
    assert(t.find(5).parent.val == 4)
    assert(t.find(5).leftChild == None)
    assert(t.find(5).rightChild.val == 8)
    assert(t.find(8).parent.val == 5)

    # Test that leftRotate and rightRotate are inverse of each other
    import copy
    newT = copy.deepcopy(t)
    assert(newT == t)
    newT.leftRotate(4)
    newT.rightRotate(5)
    assert(t == newT)
    newT.leftRotate(5)
    newT.rightRotate(8)
    assert(t == newT)

    # Test that invalid operations do not go through
    newT.leftRotate(11)
    assert(t == newT)

if __name__ == "__main__":
    test()