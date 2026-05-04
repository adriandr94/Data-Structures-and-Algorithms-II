# Below is a hashtable class with a cap of 45. It can be adjusted to a larger number if needed
# changed self.arr = [] within the list comprehension from None because we have key value pair for insertion
# in order for the chaining collision method to work.
# the list of lists within the self.arr comprehension are buckets for key's that may have the same value hash value.
# the hash table will be able to access them like linked lists since a key may share the same value/index home.

class HashTable:
    def __init__(self):
        self.capacity = 45
        self.arr = [[] for i in range(self.capacity)]

    def hash(self, key):
        h = 0
        for char in str(key):
            h += ord(char)
        return h % self.capacity


# using magic method __setitem__ operators for easier readablilty when executing methods
# for future use in the project:
# In order to get prevent collision, the set, del and get methods
# needed modifications now that (key, value) inserted as a pair

    def __setitem__(self, key, value):
        h = self.hash(key)
        for index, (k, v) in enumerate(self.arr[h]):
            if k == key:
                self.arr[h][index] = (key, value)
                return
        self.arr[h].append((key, value))

# magic method for deleting key value pair from array and dictionary.
    def __delitem__(self, key):
        h = self.hash(key)
        for index, (k, v) in enumerate(self.arr[h]):
            if k == key:
                del self.arr[h][index]
                return

# Look-up function using magic methods: __getitem__
# It's the same concept as above, we only need the key to extract a value just like a normal dictionary object:
# so instead of having to do the following:
# WGUPS.get['1'] = Value --changed to--> WGUPS['1'] = Value
    def __getitem__(self, key):
        h = self.hash(key)
        for k, v in self.arr[h]:
            if k == key:
                return v

    def items(self):
        for bucket in self.arr:
            for key, value in bucket:
                yield key, value


# Testing Hash function and collision below. 4 and 10 have the same hash value, but are successfully chained:
# WGUPS = HashTable()

# val1 = WGUPS.hash('4')
# print(val1)

# val2 = WGUPS.hash('10')
# print(val2)
# val3 = WGUPS.hash('11')
# print(val3)
# WGUPS['4'] = ["Address1"]
# WGUPS['10'] = ["Address2"]
# WGUPS['11'] = ["Address3"]
# for i, value in WGUPS.items():
#     print(value)
