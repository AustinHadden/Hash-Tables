# '''
# Linked List hash table key/value pair
# '''
class LinkedPair:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class HashTable:
    '''
    A hash table that with `capacity` buckets
    that accepts string keys
    '''
    def __init__(self, capacity, max_load=0.7, min_load=0.2):
        self.capacity = capacity  # Number of buckets in the hash table
        self.storage = [None] * capacity
        self.size = 0 # Number of keys total; need this to calculate the load factor
        self.was_resized = False # Change to true after resizing once
        self.max_load = max_load # Maximum load factor allowed
        self.min_load = min_load # Minimum load factor allowed


    def _hash(self, key):
        '''
        Hash an arbitrary key and return an integer.
        You may replace the Python hash with DJB2 as a stretch goal.
        '''
        return hash(key)


    def _hash_djb2(self, key):
        '''
        Hash an arbitrary key using DJB2 hash
        OPTIONAL STRETCH: Research and implement DJB2
        '''
        if type(key) is str:
            bytes_key = key.encode()
            hash_value = 5381
            for char in bytes_key:
                hash_value = hash_value * 33 + char
            return hash_value
        elif type(key) is int:
            return key
        elif type(key) is float:
            return int(key)
        else:
            raise ValueError('Key must be a string, int, or float')


    def _hash_mod(self, key):
        '''
        Take an arbitrary key and return a valid integer index
        within the storage capacity of the hash table.
        '''
        return self._hash_djb2(key) % self.capacity


    def insert(self, key, value, auto_resize=True):
        '''
        Store the value with the given key.
        # Part 1: Hash collisions should be handled with an error warning. (Think about and
        # investigate the impact this will have on the tests)
        # Part 2: Change this so that hash collisions are handled with Linked List Chaining.
        Fill this in.
        '''
        index = self._hash_mod(key)
        if not self.storage[index]:
            new_node = LinkedPair(key, value)
            self.storage[index] = new_node
        else:
            node = self.storage[index]
            value_set = False
            while node:
                prev_node = node
                if key == node.key:
                    node.value = value
                    value_set = True
                    break
                else:
                    node = node.next
            if not value_set:
                new_node = LinkedPair(key, value)
                prev_node.next = new_node

        self.size += 1
        if auto_resize:
            self.auto_resize()


    def remove(self, key):
        '''
        Remove the value stored with the given key.
        Print a warning if the key is not found.
        Fill this in.
        '''
        index = self._hash_mod(key)
        node = self.storage[index]
        prev_node = None
        key_found = False
        while node:
            if node.key == key:
                if not prev_node:
                    self.storage[index] = node.next
                else:
                    prev_node.next = node.next
                key_found = True
                break
            else:
                prev_node = node
                node = node.next
        if not key_found:
            raise KeyError('key not found')
        else:
            self.size -= 1
            self.auto_resize()


    def retrieve(self, key):
        '''
        Retrieve the value stored with the given key.
        Returns None if the key is not found.
        Fill this in.
        '''
        index = self._hash_mod(key)
        node = self.storage[index]
        key_found = False
        while node:
            if node.key == key:
                key_found = True
                return node.value
            else:
                node = node.next
        if not key_found:
            return None


    def resize(self):
        '''
        Doubles the capacity of the hash table and
        rehash all key/value pairs.
        Fill this in.
        '''
        self.capacity *= 2
        self.size = 0
        old_storage = self.storage
        self.storage = [None] * self.capacity
        for i in range(len(old_storage)):
            node = old_storage[i]
            while node:
                self.insert(node.key, node.value, auto_resize=False)
                node = node.next
        self.was_resized = True
        self.auto_resize()


    def halve_capacity(self):
        '''
        Halves the capacity of the hash table and
        rehash all key/value pairs.
        '''
        self.capacity = self.capacity // 2
        self.size = 0
        old_storage = self.storage
        self.storage = [None] * self.capacity
        for i in range(len(old_storage)):
            node = old_storage[i]
            while node:
                self.insert(node.key, node.value, auto_resize=False)
                node = node.next
        self.auto_resize()


    def auto_resize(self):
        '''
        Double capacity when the load factor is above max_load;
        halve capacity when the load factor is below min_load.
        '''
        if self.was_resized:
            load_factor = self.size / self.capacity
            if load_factor > self.max_load:
                self.resize()
            elif load_factor < self.min_load:
                if self.capacity > 1:
                    self.halve_capacity()
                else:
                    pass

if __name__ == "__main__":
    ht = HashTable(2)

    ht.insert("line_1", "Tiny hash table")
    ht.insert("line_2", "Filled beyond capacity")
    ht.insert("line_3", "Linked list saves the day!")

    print("")

    # Test storing beyond capacity
    print(ht.retrieve("line_1"))
    print(ht.retrieve("line_2"))
    print(ht.retrieve("line_3"))

    # Test resizing
    old_capacity = len(ht.storage)
    ht.resize()
    new_capacity = len(ht.storage)

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    print(ht.retrieve("line_1"))
    print(ht.retrieve("line_2"))
    print(ht.retrieve("line_3"))

    print("")