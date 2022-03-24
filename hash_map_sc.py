# Name: Fatima Cacho
# OSU Email: cachof@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 11 March 2022
# Description: Implementation of a HashMap using a dynamic array to store hash map
#              with chaining for collision resolution using linked list.
#              Functionality includes putting an entry in, getting a specific entry, removing
#              a specific entry, retrieving all the keys in the hash map, clearing the hash map
#              retrieving how many empty buckets, resizing the table, getting the table load,
#              and checking if a key is present.


from a6_include import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Init new HashMap based on DA with SLL for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Overrides object's string method
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table
        """
        # Loop through DA looking for empty_buckets, ie bucket.length() == 0
        empty_buckets = 0
        for i in range(self.capacity):
            bucket = self.buckets[i]
            if bucket.length() == 0:
                empty_buckets += 1
        return empty_buckets

    def table_load(self) -> float:
        """
        Returns the current hash table load factor
        """
        # table_load = num_of_elements / num_buckets
        return self.size / self.capacity

    def put(self, key: str, value: object) -> None:
        """
        Updates the key / value pair in the hash map. If the given key already
        exists in the hash map, its associated value must be replaced with the
        new value. If the given key is not in the hash map, a key / value pair
        must be added
        """
        # Determine the key / index in the DA
        hash_key = self.hash_function(key)
        bucket_index = hash_key % self.capacity

        # Grab the LL needed (bucket)
        bucket = self.buckets[bucket_index]

        # Check if key exists in bucket
        node = bucket.contains(key)
        if node is not None:
            node.value = value
        else:
            # Put key / value in LL
            bucket.insert(key, value)
            self.size += 1

    def clear(self) -> None:
        """
        Clears the contents of the hash map
        """
        self.buckets = DynamicArray()
        for _ in range(self.capacity):
            self.buckets.append(LinkedList())
        self.size = 0

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key
        """
        # Determine the key / index in the DA
        hash_key = self.hash_function(key)
        bucket_index = hash_key % self.capacity

        # Grab the LL needed (bucket)
        bucket = self.buckets[bucket_index]

        element = bucket.contains(key)
        if element:
            return element.value


    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map
        """
        # Determine the key / index in the DA
        hash_key = self.hash_function(key)
        bucket_index = hash_key % self.capacity

        # Grab the LL needed (bucket)
        bucket = self.buckets[bucket_index]

        if bucket.remove(key):
            self.size -= 1
        return


    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map, otherwise it returns False. An
        empty hash map does not contain any keys.
        """
        # Determine the key / index in the DA
        hash_key = self.hash_function(key)
        bucket_index = hash_key % self.capacity

        # Grab the LL needed (bucket)
        bucket = self.buckets[bucket_index]

        # Loop through elements in bucket
        for element in bucket:
            if element.key == key:
                return True
        return False

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table. All existing key / value pairs
        must remain in the new hash map, and all hash table links must be rehashed. If
        new_capacity is less than 1, the method does nothing
        """
        if new_capacity < 1:
            return

        # Create a new DA
        old_buckets = self.buckets
        self.capacity = new_capacity
        self.clear()

        # Loop through old buckets
        for i in range(old_buckets.length()):
            bucket = old_buckets[i]
            for element in bucket:
                self.put(element.key, element.value)

    def get_keys(self) -> DynamicArray:
        """
        Returns a DynamicArray that contains all the keys stored in the hash map
        """
        keys_da = DynamicArray()
        for i in range(self.buckets.length()):
            bucket = self.buckets[i]
            for element in bucket:
                keys_da.append(element.key)
        return keys_da


# BASIC TESTING
if __name__ == "__main__":

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
