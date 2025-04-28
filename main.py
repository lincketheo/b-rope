
class LeafNode:
    ID = 1

    def __init__(self, values, prev = None, next = None):
        self.values = values
        self.capacity = 5
        self.prev = prev
        self.next = next
        self.id = LeafNode.ID
        LeafNode.ID += 1

    def insert(self, start, array):
        _array = array

        # Append
        if start == -1:
            start = len(self.values)
        elif start > len(self.values):
            raise IndexError(f"Invalid index: {start} for leaf node "+
                             "of size: {len(self.values)}")

        """
        Append (start = -1):
            Split:
                Before:
                    self.values   = [1, 2, 3, 4, _, _, _]
                    array         = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]

                Return:
                    self          = LeafNode([1, 2, 3, 4, 5, 6, 7])
                    right         = LeafNode([8, 9, 10, 11, 12, 13, 14])
                    key           = 7
                    array         = [15, 16, 17]

            Split Not Full:
                Before:
                    self.values   = [1, 2, 3, 4, _, _, _]
                    array         = [5, 6, 7, 8, 9, 10]

                Return:
                    self          = LeafNode([1, 2, 3, 4, 5, 6, 7])
                    right         = LeafNode([8, 9, 10, _, _, _, _])
                    key           = 7
                    array         = []

            No Split
                Before:
                    self.values   = [1, 2, 3, 4, _, _, _]
                    array         = [5, 6]

                Return:
                    self          = LeafNode([1, 2, 3, 4, 5, 6, _])
                    right         = None
                    key           = 6
                    array         = []

        Insert (start = 2):
            Split:
                Before:
                    self.values   = [1, 2, 3, 4, _, _, _]
                    array         = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]

                Return:
                    self          = LeafNode([1, 2, 5, 6, 7, 8, 9])
                    right         = LeafNode([10, 11, 12, 13, 14, 3, 4])
                    key           = 7
                    array         = [15, 16, 17]

            Split Not Full:
                Before:
                    self.values   = [1, 2, 3, 4, _, _, _]
                    array         = [5, 6, 7, 8, 9, 10]

                Return:
                    self          = LeafNode([1, 2, 5, 6, 7, 8, 9])
                    right         = LeafNode([10, 3, 4, _, _, _, _])
                    key           = 7
                    array         = []

            No Split
                Before:
                    self.values   = [1, 2, 3, 4, _, _, _]
                    array         = [5, 6]

                Return:
                    self          = LeafNode([1, 2, 5, 6, 3, 4, _])
                    right         = None
                    key           = 6
                    array         = []
        """

        # Split into two arrays
        left = self.values[:start]
        right = self.values[start:]

        # Get the space that each array can hold
        lavail = self.capacity - len(left)
        ravail = self.capacity - len(right)

        assert lavail >= 0
        assert ravail >= 0

        # *append* to the left array
        left.extend(_array[:lavail])
        _array = _array[lavail:]

        # *prepend* to the right array
        right = _array[:ravail] + right
        _array = _array[ravail:]

        # Construct left node (links may change later)
        self.values = left

        # Construct right node
        rightNode = None
        if len(right) > 0:
            rightNode = LeafNode(right)

            # Link new nodes together
            next = self.next
            self.next = rightNode
            rightNode.prev = self
            rightNode.next = next
            if next is not None:
                next.prev = rightNode

        return {
                "right" : rightNode,
                "key" : len(left),
                "array" : _array
                }

    def locate(self, idx):
        if idx > self.capacity:
            return self, len(self.values)
        return self, idx

    def __str__(self):
        return "\n".join(self._str(0))

    def _str(self, level):
        indent = "    " * level
        return [f"{indent}Leaf {self.id}: {self.values} prev: {self.prev.id if self.prev else None} next: {self.next.id if self.next else None}"]

class InnerNode:
    def __init__(self, keys = [], children = []):
        self.keys = keys
        self.children = children
        self.capacity = 5

    def _assert(self):
        assert len(self.children) >= 2
        assert len(self.keys) >= 1
        assert len(self.children) == len(self.keys) + 1

    def insert(self, start, array):

        while len(self.keys) < self.capacity:
            self._assert()

            cid, idx = self.child_that_has_idx(start)
            result = self.children[cid].insert(idx, array)

            ##### There was no split beneath me
            if result["right"] is None:
                return {
                        "right" : None,
                        "key" : None,
                        "array" : result["array"],
                        }

            ##### There was a split

            # Add my left total to the key that just came up
            newkey = result["key"]
            if cid > 0:
                newkey += self.keys[cid - 1]

            # Add how much total data was inserted into keys after cid
            total_added = len(array) - len(result["array"])
            for i in range(cid, len(self.keys)):
                self.keys[i] += total_added

            # Split keys up
            leftk = self.keys[:cid]
            rightk = self.keys[cid:]

            # Skipping cid because that's in left / right
            leftc = self.children[:cid+1]
            rightc = self.children[cid+1:]

            self.keys = leftk + [newkey] + rightk
            self.children = leftc + [result["right"]] + rightc

            # Update array
            array = result["array"]

            if len(array) == 0:
                return {
                        "right" : None,
                        "key" : None,
                        "array" : array,
                        }


        # At capacity - we need to split
        result = self.split()

        return {
                "right" : result["right"],
                "key" : result["key"],
                "array" : array,
                }

    def split(self):
        mid = len(self.keys) // 2

        # Key
        key = self.keys[mid]

        # Left
        lkeys = self.keys[:mid]
        lchildren = self.children[:mid+1]

        # Right
        rkeys = [i - key for i in self.keys[mid+1:]]
        rchildren = self.children[mid+1:]
        rightNode = InnerNode(rkeys, rchildren)

        # Finally, update my keys and children
        self.keys = lkeys 
        self.children = lchildren

        return {
                "right" : rightNode,
                "key" : key,
                }

    def child_that_has_idx(self, idx):
        """
        Returns:
            i: Index of self.children that contains idx (from my perspective)
            idx: idx from the perspective of children[i]
        """
        if idx == -1:
            # Return the last index
            i = len(self.children) - 1
            return i, -1

        for i in range(len(self.keys)):
            if self.keys[i] > idx:
                # Think about it like there's
                # an invisible far left 0 key
                idx -= (self.keys[i - 1] if i > 0 else 0)
                return i, idx

        # Return the last index
        i = len(self.children) - 1
        idx -= self.keys[i - 1] # len(self.keys) is always > 0
        return i, idx

    def locate(self, idx):
        cid, idx = self.child_that_has_idx(idx)
        return self.children[cid].locate(idx)

    def __str__(self):
        return "\n".join(self._str(0))

    def _str(self, level):
        indent = "    " * level
        lines = [f"{indent}Inner: keys={self.keys}"]
        for child in self.children:
            lines.extend(child._str(level + 1))
        return lines

class BTRope:
    def __init__(self):
        self.root = LeafNode([])

    def insert(self, start, array):
        while len(array) > 0:
            print("===========================================")
            print(self)
            print("===========================================")
            result = self.root.insert(start, array)

            # No split
            if result["right"] is None:
                assert len(result["array"]) == 0
                return

            # There was a split underneath me
            self.root = InnerNode([result["key"]], [self.root, result["right"]])

            # New starting pos is where we left off 
            if start != -1:
                start += len(array) - len(result["array"])
            array = result["array"]

    def locate(self, idx):
        return self.root.locate(idx)

    def read(self, start, stop, step):
        leaf, idx = self.locate(start)
        ret = []
        while leaf:
            while idx < len(leaf.values) and idx < (stop - step):
                ret.append(leaf.values[idx])
                idx += step
            idx -= len(leaf.values)
            leaf = leaf.next
        return ret

    def __str__(self):
        return self.root.__str__()

a = BTRope()
a.insert(-1, [i for i in range(100)])
a.insert(48, [-1])
print(a)

print(len(a.read(0, 1000, 1)))

#print(a)
