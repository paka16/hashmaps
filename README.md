# hashmaps
Use of python to create separatechaining and open addressing hashmaps to prevent/reduce collisions.

# description 
The separate chaining file uses a linked list along with a dynamic array as the underlying structure. 
The open addressing hashmap was made using quadratic probing and a dynamic array and hashmap to create the underlying structure. 
The underlying structures are located in underlying_structures.py file

# methods
* put()
* remove()
* table load()
* resize_table()
* empty_buckets()
* clear()
* get()
* contains_key()
* get_keys_and_values()

# functions
Each hashmap implementation has a function, besides from the methods:
* find_mode() - separate chaining
* __iter__(), __next__() - open addressing

# usage example
```python
# declare a hashmap first:
m = HashMap(11, hash_function_1)

# insert an entry:
m.put('key1', 10)
m.put('key2', 20)
m.put('key3', 30)

# remove an entry:
m.remove('key3')

# check if 'key3' got removed:
print(m.contains_key('key3'))     # False

```
