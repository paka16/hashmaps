

from underlying_strucutres import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def table_load(self) -> float:
        """
        This method will return the load factor of the table.
        """
        elements = self._size
        load_factor = elements / self.get_capacity()
        return load_factor

    def empty_buckets(self) -> int:
        """
        This method returns the number of empty buckets in the hash table.
        """
        count = 0
        for index in range(0, self._buckets.length()):
            if self._buckets[index] == None:
                count += 1
            elif self._buckets[index] is not None:
                if self._buckets[index].is_tombstone == True:
                    count += 1
        return count

    def resize_table(self, new_capacity: int) -> None:
        """
        This method will change the capacity of the hash table to keep the load factor under 0.5.
        All existing key/value pairs will remain in the new hash map, and all hash table links must be rehashed.
        """
        # WHEN REHASHING, GET RID OF THE TOMBSTONES.

        #  NEW_CAPACITY CHECK:
        if new_capacity <= self._size:
            return
        # PRIME CAPACITY:
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        temp = self._buckets  # old bucket / map
        self._buckets = DynamicArray()
        self._capacity = new_capacity
        self._size = 0

        #  INITIALIZE THE NEW BUCKET:
        for i in range(0, new_capacity):
            self._buckets.append(None)

        # COPY OVER:
        for i in range(0, temp.length()):
            current_item = temp[i]
            if current_item is not None:
                #  IF TOMBSTONE, SET TO NONE
                if current_item.is_tombstone:
                    self._buckets[i] = None
                #  COPY OVER VALUE
                else:
                    self.put(current_item.key, current_item.value)


    def put(self, key: str, value: object) -> None:
        """
        This method will put in the key/value pair into the hash map.
        If the given key exists, it'll update the value.
        The table will be rehashed when the load factor is greater than or equal to 0.5.
        """
        # CHECK LOAD FACTOR:
        if self.table_load() >= 0.5:
            new_capacity = self.get_capacity() * 2
            self.resize_table(new_capacity)

        # GET THE INITIAL INDEX - IMPLEMENT PROBING.
        index = self._hash_function(key) % self.get_capacity()

        #  IF THE INDEX IS EMPTY - INSERT THE VALUE:
        if self._buckets[index] == None:
            new_entry = HashEntry(key, value)
            self._buckets[index] = new_entry
            self._size += 1

        #  INDEX IS NOT EMPTY:
        elif self._buckets[index] is not None:
            #  TOMBSTONE PRESENT
            if self._buckets[index].is_tombstone == True:
                new_entry = HashEntry(key, value)
                self._buckets.set_at_index(index, new_entry)
                self._size += 1
            # IF KEY MATCHES/EXISTS, UPDATE:
            elif self._buckets[index].key == key:
                new_entry = HashEntry(key, value)
                self._buckets.set_at_index(index, new_entry)

            # NEED TO PROBE:
            else:
                updated = False
                j = 1
                initial_index = index
                while self._buckets[index] is not None:
                    index = initial_index + (j ** 2)
                    #  WRAP AROUND:
                    if index >= self.get_capacity():
                        index = index % self.get_capacity()

                    # IF KEY MATCHES/EXISTS, UPDATE:
                    if self._buckets[index] is not None:
                        #  IF TOMBSTONE:
                        if self._buckets[index].is_tombstone == True:
                            if self._buckets[index].key == key:
                                updated = True
                                new_entry = HashEntry(key, value)
                                self._buckets.set_at_index(index, new_entry)
                                self._size += 1

                        elif self._buckets[index].key == key and self._buckets[index].is_tombstone is False:
                            updated = True
                            new_entry = HashEntry(key, value)
                            self._buckets.set_at_index(index, new_entry)

                    j += 1

                # KEY DOES NOT EXIST - ADD:
                if updated is False:
                    if self._buckets[index] is None or self._buckets[index].is_tombstone == True:
                        new_entry = HashEntry(key, value)
                        self._buckets[index] = new_entry
                        self._size += 1
                        self._buckets[index].is_tombstone = False

    def get(self, key: str) -> object:
        """
        This method returns the value associated with the given key.
        If the key is not in the hashmap, the method returns None.
        """
        # IF MAP IS EMPTY, RETURN.
        if self._buckets.length() == 0:
            return None

        # FIND THE INDEX:
        index = self._hash_function(key) % self.get_capacity()

        # IN THE GIVEN INDEX:
        if self._buckets[index] is not None:
            #  NOT A TOMBSTONE:
            if self._buckets[index].is_tombstone == False:
                if self._buckets[index].key == key:
                    return self._buckets[index].value
                else:
                    j = 1
                    initial_index = index
                    while self._buckets[index] is not None:
                        index = initial_index + (j ** 2)
                        #  WRAP AROUND:
                        if index >= self.get_capacity():
                            index = index % self.get_capacity()

                        # IF KEY MATCHES/EXISTS, UPDATE:
                        if self._buckets[index] is not None:
                            if self._buckets[index].is_tombstone == False:
                                if self._buckets[index].key == key:
                                    return self._buckets[index].value
                        j += 1

            # PROBE
            else:
                j = 1
                initial_index = index
                while self._buckets[index] is not None:
                    index = initial_index + (j ** 2)
                    #  WRAP AROUND:
                    if index >= self.get_capacity():
                        index = index % self.get_capacity()

                    # IF KEY MATCHES/EXISTS, UPDATE:
                    if self._buckets[index] is not None:
                        if self._buckets[index].is_tombstone is False:
                            if self._buckets[index].key == key:
                                return self._buckets[index].value
                            else:
                                return None
                    j += 1
            return None
        return None

    def contains_key(self, key: str) -> bool:
        """
        This method returns True if the given key is in the hash map, otherwise it returns False.
        An empty hash map does not contain any keys.
        """
        # EMPTY MAP:
        if self._buckets.length() == 0:
            return False
        # FIND THE INDEX:
        index = self._hash_function(key) % self.get_capacity()

        # FIND THE KEY:
        key_found = False
        if self._buckets[index] is not None:
            if self._buckets[index].is_tombstone is False:
                if self._buckets[index].key == key:
                    key_found = True
                    return key_found
                    # PROBE
                else:
                    j = 1
                    initial_index = index

                    while self._buckets[index] is not None:
                        index = initial_index + (j ** 2)
                        #  WRAP AROUND:
                        if index >= self.get_capacity():
                            index = index % self.get_capacity()

                        # IF KEY MATCHES/EXISTS:
                        if self._buckets[index] is not None:
                            if self._buckets[index].is_tombstone is False:
                                if self._buckets[index].key == key:
                                    key_found = True
                                    return key_found

                        j += 1
        if key_found is True:
            return True
        else:
            return False

    def remove(self, key: str) -> None:
        """
        This method removes the given key and its associated value from the hash map.
        If the key is not in the hash map, the method does nothing (no exception needs to be raised).
        """
        # CHECK IF EMPTY:
        if self._buckets.length() == 0:
            return None

        # FIND THE INDEX:
        index = self._hash_function(key) % self.get_capacity()

        # FIND THE KEY - NOT EMPTY :
        if self._buckets[index] is not None:
            #  NOT TOMBSTONE:
            if self._buckets[index].is_tombstone is False:
                if self._buckets[index].key == key:
                    self._buckets[index].is_tombstone = True
                    self._size -= 1

                # PROBING
                else:
                    j = 1
                    initial_index = index
                    while self._buckets[index] is not None:
                        index = initial_index + (j ** 2)
                        #  WRAP AROUND:
                        if index >= self.get_capacity():
                            index = index % self.get_capacity()

                        # IF KEY MATCHES/EXISTS:
                        if self._buckets[index] is not None:
                            if self._buckets[index].is_tombstone is False:
                                if self._buckets[index].key == key:
                                    self._size -= 1
                                    self._buckets[index].is_tombstone = True
                                    return
                        j += 1
            # PROBING IGNORING THE TOMBSTONES:
            else:
                j = 1
                initial_index = index
                while self._buckets[index] is not None:
                    index = initial_index + (j ** 2)
                    #  WRAP AROUND:
                    if index >= self.get_capacity():
                        index = index % self.get_capacity()

                    # IF KEY MATCHES/EXISTS:
                    if self._buckets[index] is not None:
                        if self._buckets[index].is_tombstone == False:
                            if self._buckets[index].key == key:
                                self._size -= 1
                                self._buckets[index].is_tombstone = True
                                return
                    j += 1

        else:
            j = 1
            initial_index = index
            while self._buckets[index] is not None:
                index = initial_index + (j ** 2)
                #  WRAP AROUND:
                if index >= self.get_capacity():
                    index = index % self.get_capacity()

                # IF KEY MATCHES/EXISTS:
                if self._buckets[index] is not None:
                    if self._buckets[index].is_tombstone == False:
                        if self._buckets[index].key == key:
                            self._size -= 1
                            self._buckets[index].is_tombstone = True
                            return
                j += 1

    def clear(self) -> None:
        """
        This method clears the entire hash map.
        It will not change the underlying hash table capacity.
        """
        # CAPACITY:
        new_capacity = self.get_capacity()

        # NEW HASHMAP
        new_hash = HashMap(new_capacity, self._hash_function)

        # RESET SIZE:
        self._size = 0

        # SET SELF TO NEW HASH.
        self._buckets = new_hash._buckets

    def get_keys_and_values(self) -> DynamicArray:
        """
        This method returns a dynamic array where each index contains a tuple of a key/value pair stored in the hash map.
        The order of the keys in the dynamic array does not matter.
        """
        # CREATE A NEW DYNAMIC ARRAY:
        new_arr = DynamicArray()

        # TRAVERSE EACH BUCKET AND FILL THE NEW_ARR:
        for i in range(0, self.get_capacity()):
            current_item = self._buckets[i]
            if self._buckets[i] is not None:
                if self._buckets[i].is_tombstone == False:
                    object = (current_item.key, current_item.value)
                    new_arr.append(object)
        return new_arr

    def __iter__(self):
        """
        This method enables the hash map to iterate across itself.
        This will return the iterator after setting it up.
        A variable will initialized to track the iterator's progress.
        """
        self._index = 0
        return self

    def __next__(self):
        """
        This method will return the next item in the hash map, based on the current location of the iterator.
        It will need to only iterate over active items.
        """
        try:
            value = self._buckets[self._index]
            count = 0
            #  THE VALUE IS NONE - PROBE TO NEXT:
            if value is None:
                while value is None or count < self.get_capacity():
                    self._index += 1
                    if self._buckets[self._index] is not None:
                        if self._buckets[self._index].is_tombstone == False:
                            value = self._buckets[self._index]
                            self._index += 1
                            return value
                    value = self._buckets[self._index]
                    count += 1
            # TO CATCH TOMBSTONES:
            elif value is not None:
                if value.is_tombstone == True:
                    while value is None or count < self.get_capacity():
                        self._index += 1
                        value = self._buckets[self._index]
                        count += 1
                        if self._buckets[self._index] is not None:
                            return value

        # CATCH OUT OF BOUNDS:
        except DynamicArrayException:
            raise StopIteration

        if self._buckets[self._index] is not None:
            if self._buckets[self._index].is_tombstone == False:
                self._index += 1
                return value

