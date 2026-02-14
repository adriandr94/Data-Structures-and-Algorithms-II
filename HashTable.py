# Below is a hashtable class with a cap of 45 instead of 40 just incase I wanted insert more
# keys for testing purposes:

class HashTable:
    def __init__(self):
        self.MAX = 45
        self.arr = [None] * self.MAX


# Because the keys are the package ID, which are already formated from 1 to 40,
# I kept the method simple by just having the exact key of value represent it's index, assining it's respective value.


    def add(self, key, value):
        self.arr[key] = value

# I was getting an error from having value as an argument for this method.
# which makes sense because all we need is the key in order to assign it a new value of 'None'

    def remove(self, key):

        self.arr[key] = None

# same as above, we only need the key to extract a value just like a normal dictionary object:
# equivalant to d = {}; getKV would be the same as d[1] = "value"

    def getKV(self, key):

        return self.arr[key]


WGUPS = HashTable()

WGUPS.add(1, ['10415 Jardine Ave', 'Sunland', '91040', 'EOD', 5])
WGUPS.add(2, ['5935 Whitnall Hwy', 'North Hollywod', '91601', '10:30AM', 15])

# Testing if I could make this HashTable iterable. As of now I can't figure out how without
# having to insert a fixed number in the range value. Will be updating this soon.

for i in range(3):
    print(WGUPS.getKV(i))
