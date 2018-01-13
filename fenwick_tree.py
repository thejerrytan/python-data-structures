# A 1-indexed Bit Indexed Tree or Fenwick Tree
class FenwickTree:
	def __init__(self, a):
		for (idx,v) in enumerate(a):
			nextIdx = (idx+1) + lowestSetBit(idx+1) - 1
			if nextIdx < len(a):
				a[nextIdx] += v
		self.tree = a

	def __str__(self):
		return str(self.tree)

	# Find the sum of elements from start of array to end
	def prefixSum(self, end):
		ans = 0
		while end > 0:
			ans += self.tree[end-1]
			end -= lowestSetBit(end)
		return ans

	# Find the sum of elements from start to end inclusive
	def range(self, start, end):
		if start < 1:
			raise Exception("Starting index must be at least 1.")
		if end < start:
			raise Exception("End index must be greater than or equal to start")
		return self.prefixSum(end) - self.prefixSum(start-1)

	# idx is based on a 1-based array
	def update(self, idx, value):
		if idx < 1:
			raise Exception("Invalid index, must be at least 1")
		delta = value - self.tree[idx-1]
		while idx <= len(self.tree):
			self.tree[idx-1] += delta
			idx += lowestSetBit(idx)

def lowestSetBit(intType):
	return (intType & -intType)

def test():
	import copy
	a = [1,2,3,4,5,6,7,8,9,10]
	tree = FenwickTree(copy.deepcopy(a))
	assert(tree.tree == [1,3,3,10,5,11,7,36,9,19])
	# print(tree)

	assert(tree.prefixSum(1) == 1)
	assert(tree.prefixSum(10) == 55)
	assert(tree.prefixSum(0) == 0)
	assert(tree.prefixSum(-1) == 0)

	assert(tree.range(1,4) == 10)
	assert(tree.range(2,5) == 14)
	assert(tree.range(5, 10) == 45)

	tree.update(1, 10)
	assert(tree.tree == [10,12,3,19,5,11,7,45,9,19])
	assert(tree.range(1,4) == 19)
	assert(tree.range(2,5) == 14)
	assert(tree.range(5, 10) == 45)

if __name__ == "__main__":
	test()