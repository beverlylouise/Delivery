# Author: Beverly L Murray
# Student ID: #001328583
# C950 WGUPS

# Task E and F

# hash table with chaining

# chaining uses a list for buckets to manage collisions.
# O(n) time complexity because in the worst case, it finds the bucket and has to go through the list of items to
#       look up, update, or remove, which could be every item if they are all in the same bucket
# O(n) space complexity because the space required changes with the number of items, more items need more storage space

class ChainingHashTable:
    # constructor with initial capacity
    def __init__(self, initial_capacity=20):
        # assign all buckets with an empty list
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

# insert item into the hash table
    def insert(self, key, item):
        # get bucket that will hold the item
        # using modular hashing
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # update key if it is already in the bucket
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True
        # if key is not in the bucket, insert the item at the end of the list
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    # Task F: develop a look-up function
    # search for an item with matching key in the hash table
    # returns None if not found
    def lookup(self, key):
        # get bucket that would hold the key
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        # search for key in the bucket
        for kv in bucket_list:
            if kv[0] == key:
                return kv[1]
        return None

    # remove an item from the hash table
    def remove(self, key):
        # get the bucket that has the item to be removed
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        # if item is in the bucket, remove item
        for kv in bucket_list:
            if kv[0] in bucket_list:
                bucket_list.remove([kv[0], kv[1]])
