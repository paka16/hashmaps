
from underlying_strucutres import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map - stored elements
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map - number of buckets
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def table_load(self) -> float:
        """
        This method will determine the load factor - the average number of elements in each bucket.
        """
        elements = self.get_size()
        # self._buckets is the whole map. buckets or chains - linked lists.
        load_factor = elements / self.get_capacity()
        # load factor is the number of elements (the size) divided by the number of slots in the array, capacity.
        return load_factor

    def resize_table(self, new_capacity: int) -> None:
        """
        This method will be used to resize when the load_factor is greater than or equal to 1.
        This means that we increase the number of buckets.
        This method will take a new_capacity parameter, which is double the original capacity.
        """
        # CHECK THE NEW_CAPACITY:
        if new_capacity < 1:
            return
        # MAKE SURE NEW_CAPACITY IS PRIME - IF THE CAPACITY IS NOT PRIME, GET THE NEXT PRIME:
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        temp = self._buckets  # old map
        self._buckets = DynamicArray()
        self._capacity = new_capacity
        self._size = 0

        #  NEW DYNAMIC ARRAY SHOULD HAVE CAP OF NEW_CAPACITY SO INITIALIZE IT:
        for i in range(0, new_capacity):
            self._buckets.append(LinkedList())
        # INSERT EVERYTHING FROM THE OLD HASHMAP TO THE NEW ONE:
        for i in range(0, temp.length()):  # traversing through each old bucket
            # FIND THE KEY:
            current_bucket_head = temp[i]._head
            if current_bucket_head is not None:
                current_node = temp[i]._head
                while current_node is not None:
                    # INSERT ELEMENT INTO NEW BUCKET:
                    self.put(current_node.key, current_node.value)
                    current_node = current_node.next

    def empty_buckets(self) -> int:
        """
        This method will return the number of empty buckets currently present in the hash table.
        """
        # SET UP THE COUNTER:
        count = 0
        # USE FOR LOOP TO LOOP THROUGH THE LENGTH OF THE HASH MAP - COUNT THE NUMBER OF EMPTY BUCKETS.
        for index in range(0, self._buckets.length()): 
            #  COUNT THE NUMBER OF EMPTY BUCKETS:
            if self._buckets[index].length() == 0:
                count += 1
        return count

    def clear(self) -> None:
        """
        This method will clear the contents of the hash map.
        However, it will not change the current capacity.
        """
        # CAPACITY:
        new_capacity = self.get_capacity()

        # NEW HASHMAP:
        new_hash = HashMap(new_capacity)

        # RESET SIZE:
        self._size = 0

        # SET SELF TO NEW HASH.
        self._buckets = new_hash._buckets
        self = new_hash

    def put(self, key: str, value: object) -> None:
        """
        This method updates the key/value pair in the hash map.
        If the given key already exists in the hash map, its associated value must be replaced with the new value.
        If the given key is not in the hash map, a new key/value pair must be added.
        The table must be resized to double its current capacity when this method is called if the current load factor
        of the table is greater than or equal to 1.0.
        """
        # CHECK THE LOAD FACTOR:
        load_factor = self.table_load()
        # IF LOAD FACTOR >= 1: RESIZE - CAPACITY WILL DOUBLE.
        if load_factor >= 1:
            new_capacity = self.get_capacity() * 2
            self.resize_table(new_capacity)

        # GET THE INDEX - INDEX = HASH % ARR SIZE:
        hash = self._hash_function(key)
        index = hash % self.get_capacity()
        bucket = self._buckets[index]

        # DOES THE LIST CONTAIN THE KEY:
        node = LinkedList.contains(bucket, key)
        # WHAT IS THE NODE:
        if node is not None:
            # UPDATE THE VALUE:
            if node.key == key:
                node.value = value
            # INSERT IT
        else:
            bucket.insert(key, value)
            #  INCREASE THE SIZE:
            self._size += 1

    def get(self, key: str):
        """
        This method will return the value associated with the given key.
        If the key does not exist within the hash map, the method will return None.
        """
        # IF THE KEY EXISTS:
        # GET THE INDEX - INDEX = HASH % ARR SIZE:
        hash = self._hash_function(key)
        index = hash % self.get_capacity()
        # GET THE BUCKET:
        bucket = self._buckets[index]

        node = LinkedList.contains(bucket, key)
        if node == None:
            return None
        else:
            if node.key == key:
                return node.value

    def contains_key(self, key: str) -> bool:
        """
        This method will return True if the given key is currently in the hash map.
        Else, it will return False.
        If the hash map is empty, will return false as well? # TODO???
        """
        #  FIND THE BUCKET USING THE INDEX.
        hash = self._hash_function(key)
        index = hash % self.get_capacity()
        bucket = self._buckets[index]

        node = LinkedList.contains(bucket, key)
        if node == None:
            return False
        else:
            if node.key == key:
                return True

    def remove(self, key: str) -> None:
        """
        This method will remove the given key and its associated value from the hashmap.
        If the key is not in the map, it'll simply return.
        """
        # IF THE MAP CONTAINS THE KEY:
        if self.contains_key(key):
            #  FIND THE BUCKET USING THE INDEX.
            hash = self._hash_function(key)
            index = hash % self.get_capacity()
            bucket = self._buckets[index]

            node = LinkedList.contains(bucket, key)
            # REMOVE THE NODE USING REMOVE FROM LINKED LIST
            LinkedList.remove(bucket, key)
            self._size -= 1
        else:
            return

    def get_keys_and_values(self) -> DynamicArray:
        """
        This method returns a dynamic array where each index contains a tuple of the key/value pair stored in the hash
        map.
        The order of the keys in the dynamic array does not matter.
        """
        # CREATE A NEW DYNAMIC ARRAY:
        new_arr = DynamicArray()

        # TRAVERSE EACH BUCKET AND FILL THE NEW_ARR:
        for i in range(0, self.get_capacity()):
            current_node = self._buckets[i]._head
            while current_node != None:
                if self._buckets[i].length() != 0:
                    object = (current_node.key, current_node.value)
                    new_arr.append(object)
                    current_node = current_node.next
        return new_arr

def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    This method will receive a dynamic array (that may not be sorted).
    Its goal is to return a tuple that contains the: most occurring value/s and its frequency of appearance.
    Runtime Complexity: O(n)

    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap()

    # add everything into the hash map: key = element, value = freq of element.
    value = 0
    item_count = 1 # count of items in the new_arr
    for index in range(0, da.length()):
        key = da[index]
        if map.contains_key(key):
            value = map.get(key)
            value += 1
        else:
            value = 1
        map.put(key, value)
    # using for loop (O(n)), traverse until you find the highest frequency and append to dynamic array.
    new_arr = DynamicArray()
    new_map = HashMap()
    key = da[0]
    max_freq = map.get(key)
    new_arr.append(key)
    new_map.put(key, max_freq)

    for index in range(1, da.length()):
        key = da[index]
        freq = map.get(key)
        #  BIGGER FREQUENCY FOUND:
        if freq > max_freq:
            new_arr = DynamicArray()
            new_arr.append(key)
            max_freq = freq
            new_map.put(key, freq)
        # FREQ = MAX_FREQ:
        elif freq == max_freq:
            #  IF THE KEY IS ALREADY IN THE DA:
            if new_map.contains_key(key):
                max_freq = freq
            else:
                new_arr.append(key)
                new_map.put(key, freq)


    returning_arr = DynamicArray()
    for index in range(0, new_arr.length()):
        item = new_arr[index]
        returning_arr.append(item)
    returning_tuple = (returning_arr, max_freq)

    return returning_tuple



