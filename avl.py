from bst import Node, BST

class AugmentedHeightNode(Node):
    def __init__(self, val, parent):
        super(AugmentedHeightNode, self).__init__(val, parent)
        self.count = 1 # To ensure each val in the tree is unique, use count to store duplicates
        
        # Augmentations
        self.height = 0
        self.size = self.count

    def __str__(self):
        return "AugmentedHeightNode(val=%s, height=%s)" % (self.val, self.height)

    def setHeight(self):
        leftChildHeight = self.leftChild.height if self.leftChild is not None else -1
        rightChildHeight = self.rightChild.height if self.rightChild is not None else -1
        self.height = 1 + max(leftChildHeight, rightChildHeight)

    def getHeight(self):
        return self.height

    def isBalanced(self):
        if self.leftChild is None and self.rightChild is None:
            return True
        elif self.leftChild is None and self.rightChild is not None:
            return (self.rightChild.getHeight() == 0)
        elif self.leftChild is not None and self.rightChild is None:
            return (self.leftChild.getHeight() == 0)
        else:
            return (abs(self.leftChild.getHeight() - self.rightChild.getHeight()) <= 1)

    # NOTE: False can also mean left == right, hence false does != right heavy
    def isLeftHeavy(self):
        if self.leftChild is None and self.rightChild is None:
            return False
        elif self.leftChild is None and self.rightChild is not None:
            return False
        elif self.leftChild is not None and self.rightChild is None:
            return True
        else:
            return (self.leftChild.getHeight() > self.rightChild.getHeight())

    def isRightHeavy(self):
        if self.leftChild is None and self.rightChild is None:
            return False
        elif self.leftChild is None and self.rightChild is not None:
            return True
        elif self.leftChild is not None and self.rightChild is None:
            return False
        else:
            return (self.leftChild.getHeight() < self.rightChild.getHeight())

    def incrementCount(self):
        self.count += 1

    def decrementCount(self):
        if self.count < 1: raise Exception("Cannot decrement count below 1")
        self.count -= 1

    def getCount(self):
        return self.count

    def updateSize(self):
        # update size
        leftSize = 0 if self.leftChild is None else self.leftChild.size
        rightSize = 0 if self.rightChild is None else self.rightChild.size
        self.size = leftSize + rightSize + self.count

class AVLTree(BST):
    LEFT_LEFT_HEAVY   = 1
    LEFT_RIGHT_HEAVY  = 2
    RIGHT_LEFT_HEAVY  = 3
    RIGHT_RIGHT_HEAVY = 4
    BALANCED          = 5

    def __init__(self):
        super(AVLTree, self).__init__()

    def size(self):
        return 0 if self.root is None else self.root.size

    def setRoot(self, val):
        self.root = AugmentedHeightNode(val, None)

    def getHeight(self):
        return self.root.getHeight() if self.root is not None else 0

    # Returns (Node, path to node), (None, path to leaf) if not found
    def findPathToNode(self, val, startNode=None):
        path = []
        currentNode = self.root if startNode is None else startNode
        while True:
            if currentNode is not None:
                path.append(currentNode)
                if val < currentNode.val:
                    currentNode = currentNode.leftChild
                elif val > currentNode.val:
                    currentNode = currentNode.rightChild
                else:
                    # val == currentNode.val
                    return (currentNode, path)
            else:
                # Not found
                return (None, path)

    # insertNode now keeps track of nodes along its search path whose height needs to be updated
    def insertNode(self, currentNode, val):
        dirtyNodes = []
        while True:
            if (val < currentNode.val):
                dirtyNodes.append(currentNode)
                if currentNode.leftChild:
                    currentNode = currentNode.leftChild
                else:
                    currentNode.leftChild = AugmentedHeightNode(val, currentNode)
                    break
            elif val > currentNode.val:
                dirtyNodes.append(currentNode)
                if currentNode.rightChild:
                    currentNode = currentNode.rightChild
                else:
                    currentNode.rightChild = AugmentedHeightNode(val, currentNode)
                    break
            else:
                # val == currentNode.val, remember to increment size of subtree rooted at currentNode
                currentNode.incrementCount()
                currentNode.size += 1
                break
        while dirtyNodes:
            n = dirtyNodes.pop()
            # update height
            n.setHeight()
            if not n.isBalanced(): self.balanceTree(n)
            n.updateSize()


    def remove(self, val, startNode=None):
        (target, path) = self.findPathToNode(val)

        if target is not None:
            if target.getCount() > 1: 
                target.decrementCount()
                # remember to update size of subtree rooted at target
                target.size -= 1
                return True
            
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
                    return True
                else:
                    return False
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
                    return True
                else:
                    # Funny edge case
                    return False

            # Update heights and rebalance trees
            while path:
                n = path.pop()
                n.setHeight()
                if not n.isBalanced(): self.balanceTree(n)
                n.updateSize()

            return True
        else:
            # Nothing to remove
            return False

    def balanceTree(self, startNode):
        imbalanceType = self.determineImbalanceType(startNode)
        if imbalanceType == AVLTree.LEFT_LEFT_HEAVY:
            newSubRoot = startNode.leftChild
            newLeftChild = startNode.leftChild.leftChild
            self.rightRotate(-1, startNode)
            # Update height of new child nodes followed by parent nodes
            startNode.setHeight()
            startNode.updateSize()
            if newLeftChild is not None:
                newLeftChild.setHeight()
                newLeftChild.updateSize()
            if newSubRoot is not None:
                newSubRoot.setHeight()
                newSubRoot.updateSize()
            assert(newSubRoot.isBalanced() == True)
        elif imbalanceType == AVLTree.LEFT_RIGHT_HEAVY:
            newLeftChild = startNode.leftChild
            newSubRoot = startNode.leftChild.rightChild
            self.leftRotate(-1, startNode.leftChild)
            self.rightRotate(-1, startNode)
            # Update height of new child nodes followed by parent nodes
            if newLeftChild is not None: 
                newLeftChild.setHeight()
                newLeftChild.updateSize()
            startNode.setHeight()
            startNode.updateSize()
            if newSubRoot is not None: 
                newSubRoot.setHeight()
                newSubRoot.updateSize()
            assert(newSubRoot.isBalanced() == True)
        elif imbalanceType == AVLTree.RIGHT_LEFT_HEAVY:
            newRightChild = startNode.rightChild
            newSubRoot = startNode.rightChild.leftChild
            self.rightRotate(-1, startNode.rightChild)
            self.leftRotate(-1, startNode)
            # Update height of new child nodes followed by parent nodes
            if newRightChild is not None: 
                newRightChild.setHeight()
                newRightChild.updateSize()
            startNode.setHeight()
            startNode.updateSize()
            if newSubRoot is not None:
                newSubRoot.setHeight()
                newSubRoot.updateSize()
            assert(newSubRoot.isBalanced() == True)
        elif imbalanceType == AVLTree.RIGHT_RIGHT_HEAVY:
            newSubRoot = startNode.rightChild
            newRightChild = startNode.rightChild.rightChild
            self.leftRotate(-1, startNode)
            # Update height of new child nodes followed by parent nodes
            startNode.setHeight()
            startNode.updateSize()
            if newRightChild is not None: 
                newRightChild.setHeight()
                newRightChild.updateSize()
            if newSubRoot is not None: 
                newSubRoot.setHeight()
                newSubRoot.updateSize()
            assert(newSubRoot.isBalanced() == True)
        elif imbalanceType == AVLTree.BALANCED:
            pass
        else:
            raise Exception("Invalid imbalance situation found")

    # startNode is node which is imbalanced
    def determineImbalanceType(self, startNode):
        if startNode.isBalanced():
            return AVLTree.BALANCED
        else:
            if startNode.isLeftHeavy():
                childNode = startNode.leftChild
                if childNode.isLeftHeavy(): return AVLTree.LEFT_LEFT_HEAVY
                if childNode.isRightHeavy(): return AVLTree.LEFT_RIGHT_HEAVY
            if startNode.isRightHeavy():
                childNode = startNode.rightChild
                if childNode.isLeftHeavy(): return AVLTree.RIGHT_LEFT_HEAVY
                if childNode.isRightHeavy(): return AVLTree.RIGHT_RIGHT_HEAVY
            return AVLTree.BALANCED

    # Given a key x, how many elements are smaller than or equal to x?
    def rank(self, x):
        curr = self.root
        size = 0
        while curr is not None:
            if x < curr.val:
                curr = curr.leftChild
            elif x == curr.val:
                leftSize = curr.leftChild.size if curr.leftChild is not None else 0
                size += curr.count + leftSize
                break
            else: # x > curr.val
                leftSize = curr.leftChild.size if curr.leftChild is not None else 0
                size += curr.count + leftSize
                curr = curr.rightChild
        return size if curr is not None else -1


    # Find the kth-smallest element
    def select(self, k):
        found = False
        curr = self.root
        while not found and curr is not None:
            leftSize = curr.leftChild.size if curr.leftChild is not None else 0
            rightSize = curr.rightChild.size if curr.rightChild is not None else 0
            if k <= leftSize:
                curr = curr.leftChild
            elif leftSize < k <= leftSize + curr.count:
                found = True
                break
            else: # k > leftSize + curr.count
                k -= (leftSize + curr.count)
                curr = curr.rightChild
        return curr.val


def testPerformanceWorstCase():
    RANGE = 1E5
    print("Testing performance for worse case: insert %s nodes in ascending order" % int(2*RANGE))
    t = AVLTree()
    for i in xrange(int(-RANGE), int(RANGE)+1):
        t.insert(i)
    
def testPerformanceAverageCase():
    import math, random
    RANGE = 1E5
    print("Testing performance for average case: insert %s nodes generated randomly in the interval [-1000, 1000]" % int(2*RANGE))
    t = AVLTree()
    for i in xrange(int(-RANGE), int(RANGE)+1):
        val = int(math.floor(random.uniform(-1000, 1000)))
        t.insert(val)
    
def test():
    # Test balancing
    import math, random
    t = AVLTree()
    print("Testing correctness for tree size augmentation...")
    t.insert(10)
    t.insert(9)
    t.insert(20)
    t.insert(5)
    t.insert(15)
    t.insert(25)
    t.insert(3)
    t.insert(7)
    t.insert(13)
    t.insert(17)
    t.insert(30)
    assert(t.size() == 11)
    assert(t.root.leftChild.size == 4)
    assert(t.root.rightChild.size == 6)
    assert(t.root.leftChild.leftChild.size == 1)
    assert(t.root.leftChild.rightChild.size == 2)
    assert(t.root.leftChild.rightChild.leftChild.size == 1)
    assert(t.root.rightChild.leftChild.size == 3)
    assert(t.root.rightChild.leftChild.leftChild.size == 1)
    assert(t.root.rightChild.leftChild.rightChild.size == 1)
    assert(t.root.rightChild.rightChild.size == 2)
    assert(t.root.rightChild.rightChild.rightChild.size == 1)

    # Test size updates after removal of nodes
    t.remove(9)
    assert(t.root.leftChild.rightChild.size == 1)
    assert(t.root.leftChild.size == 3)
    t.remove(13)
    assert(t.root.size == 9)
    assert(t.root.rightChild.size == 5)
    assert(t.root.rightChild.rightChild.size == 2)
    assert(t.root.rightChild.leftChild.size == 2)
    assert(t.root.rightChild.leftChild.rightChild.size == 1)

    # Test size for duplicate keys
    t.insert(3)
    t.insert(3)
    assert(t.root.size == 11)
    assert(t.root.leftChild.size == 5)
    assert(t.root.leftChild.leftChild.size == 3)
    t.insert(20)
    t.insert(20)
    assert(t.root.size == 13)
    assert(t.root.rightChild.size == 7)
    print("Passed!")

    print("Testing correctness for rank and select...")
    # Test rank 
    assert(t.rank(1) == -1)
    assert(t.rank(3) == 3)
    assert(t.rank(5) == 4)
    assert(t.rank(7) == 5)
    assert(t.rank(10) == 6)
    assert(t.rank(15) == 7)
    assert(t.rank(17) == 8)
    assert(t.rank(20) == 11)
    assert(t.rank(25) == 12)
    assert(t.rank(30) == 13)

    # Test select
    assert(t.select(1) == 3)
    assert(t.select(2) == 3)
    assert(t.select(3) == 3)
    assert(t.select(4) == 5)
    assert(t.select(5) == 7)
    assert(t.select(6) == 10)
    assert(t.select(7) == 15)
    assert(t.select(8) == 17)
    assert(t.select(9) == 20)
    assert(t.select(10) == 20)
    assert(t.select(11) == 20)
    assert(t.select(12) == 25)
    assert(t.select(13) == 30)
    print("Passed!")


    # t = AVLTree()
    # RANGE = 1E4
    # print("Testing correctness for worse case: inserting %s nodes in ascending order" % int(2*RANGE))
    # for i in xrange(int(-RANGE), int(RANGE)+1):
    #     t.insert(i)
    #     if i % 1000 == 0: print("Num of nodes processed: %d k" % ( (i+RANGE) / 1000))
    #     assert(t.getHeight() == math.ceil(math.log(i+RANGE+1+1, 2))-1)

    # print("Testing correctness for remove: removing nodes")
    # TOTAL_NUM_NODES = int(2*RANGE)
    # for i in xrange(int(-RANGE), int(RANGE)+1):
    #     t.remove(i)
    #     assert(t.getHeight() <= 1.44 * math.log(TOTAL_NUM_NODES - i+RANGE+1, 2))

    # print("Testing correctness for average case: inserting %s nodes generated randomly in the interval [-1000, 1000]" % int(2*RANGE))
    # t = AVLTree()
    # for i in xrange(int(-RANGE), int(RANGE)+1):
    #     val = int(math.floor(random.uniform(-1000, 1000)))
    #     t.insert(val)
    #     # print(i+RANGE+1, val, newT.getHeight(), 1.44 * math.log(i+RANGE+1, 2))
    #     if i % 1000 == 0: print("Num of nodes processed: %d k" % ( (i+RANGE) / 1000))
    #     # See https://www.youtube.com/watch?v=FNeL18KsWPc&t=2484s (25:16) for fomula h < 1.440 lg n
    #     assert(t.getHeight() <= 1.44 * math.log(i+RANGE+1, 2))


    # # Test performance
    # import timeit
    # print(timeit.timeit("testPerformanceWorstCase()", setup="from __main__ import testPerformanceWorstCase", number=1))
    # print(timeit.timeit("testPerformanceAverageCase()", setup="from __main__ import testPerformanceAverageCase", number=1))

if __name__ == "__main__":
    test()