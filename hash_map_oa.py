# Name: Fatima Cacho
# OSU Email: cachof@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 11 March 2022
# Description: Implementation of a HashMap using a dynamic array to store hash map
#              through open addressing with quadratic probing for collision resolution.
#              Functionality includes putting an entry in, getting a specific entry, removing
#              a specific entry, retrieving all the keys in the hash map, clearing the hash map
#              retrieving how many empty buckets, resizing the table, getting the table load,
#              and checking if a key is present.


from a6_include import *


class HashEntry:

    def __init__(self, key: str, value: object):
        """
        Initializes an entry for use in a hash map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.key = key
        self.value = value
        self.is_tombstone = False

    def __str__(self):
        """
        Overrides object's string method
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return f"K: {self.key} V: {self.value} TS: {self.is_tombstone}"


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with HashMap implementation
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
        Initialize new HashMap that uses Quadratic Probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()

        for _ in range(capacity):
            self.buckets.append(None)

        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Overrides object's string method
        Return content of hash map in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            out += str(i) + ': ' + str(self.buckets[i]) + '\n'
        return out

    def put(self, key: str, value: object) -> None:
        """
        Updates the key / value pair in the hash map. If the given key already exists in
        the hash map, its associated value must be replaced with the new value. If the
        given key is not in the hash map, a key / value pair must be added. Table is
        resized to double its current capacity when this method is called and the
        current load factor of the table is greater than or equal to 0.5
        """
        if self.table_load() >= 0.5:
            self.resize_table(self.capacity * 2)

        j = 0
        hash_key = self.hash_function(key)

        while j <= self.capacity:
            quad_index = self.__quad(hash_key, j)
            bucket_index = quad_index % self.capacity
            hash_entry = self.buckets[bucket_index]

            if hash_entry is not None:  # if hash_entry has a value
                if hash_entry.key == key:  # and the hash_entry's key == key
                    hash_entry.value = value
                    return
            else:
                element = HashEntry(key, value)
                self.buckets.set_at_index(bucket_index, element)
                self.size += 1
                return
            j += 1

    def __quad(self, key, j):
        """Quadratic probing equation"""
        return key + j ** 2

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key
        """
        j = 0
        hash_key = self.hash_function(key)

        while j <= self.capacity:
            quad_index = self.__quad(hash_key, j)
            bucket_index = quad_index % self.capacity
            hash_entry = self.buckets.get_at_index(bucket_index)
            if hash_entry is not None and hash_entry.key == key and hash_entry.is_tombstone is False:
                return hash_entry.value
            j += 1

    def clear(self) -> None:
        """
        Clears the contents of the hash map
        """
        self.buckets = DynamicArray()
        for _ in range(self.capacity):
            self.buckets.append(None)
        self.size = 0

    def table_load(self) -> float:
        """
        Returns the current hash table load factor
        """
        # table_load = num_of_elements / num_buckets
        return self.size / self.capacity

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table. All existing key / value pairs
        must remain in the new hash map, and all hash table links must be rehashed. If
        new_capacity is less than 1 or less than the current number of elements in the map, the
        method does nothing
        """
        if new_capacity <= 1 or new_capacity < self.size:
            return

        old_buckets = self.buckets
        self.capacity = new_capacity
        self.clear()

        for i in range(old_buckets.length()):
            # bucket returns HashEntry
            hash_entry = old_buckets.get_at_index(i)

            if hash_entry is not None and hash_entry.is_tombstone is False:
                self.put(hash_entry.key, hash_entry.value)

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map
        """
        j = 0
        hash_key = self.hash_function(key)

        while j <= self.capacity:
            quad_index = self.__quad(hash_key, j)
            bucket_index = quad_index % self.capacity
            hash_entry = self.buckets.get_at_index(bucket_index)
            if hash_entry is not None and hash_entry.key == key and hash_entry.is_tombstone is False:
                # hash_entry.key = None
                # hash_entry.value = None
                hash_entry.is_tombstone = True
                self.size -= 1
                return
            j += 1
        return

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map, otherwise it returns False.
        """
        j = 0
        hash_key = self.hash_function(key)

        while j <= self.capacity:
            quad_index = self.__quad(hash_key, j)
            bucket_index = quad_index % self.capacity
            hash_entry = self.buckets.get_at_index(bucket_index)
            if hash_entry is not None and hash_entry.is_tombstone is False and hash_entry.key == key:
                return True
            j += 1
        return False

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table
        """
        return self.capacity - self.size

    def get_keys(self) -> DynamicArray:
        """
        Returns a DynamicArray that contains all the keys stored in the hash map
        """
        keys_da = DynamicArray()
        for i in range(self.buckets.length()):
            hash_entry = self.buckets.get_at_index(i)
            if hash_entry is not None and hash_entry.is_tombstone is False:
                keys_da.append(hash_entry.key)
        return keys_da



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
    # this test assumes that put() has already been correctly implemented
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
