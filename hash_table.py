class Contact:
    '''
    Contact class to represent a contact with a name and number.
    Attributes:
        name (str): The name of the contact.
        number (str): The phone number of the contact.
    '''
    def __init__(self, name, number):
        self.name = name
        self.number = number

    def __str__(self):
        return f"{self.name}: {self.number}"


class Node:
    '''
    Node class to represent a single entry in the hash table.
    Attributes:
        key (str): The key (name) of the contact.
        value (Contact): The value (Contact object) associated with the key.
        next (Node): Pointer to the next node in case of a collision.
    '''
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashTable:
    '''
    HashTable class to represent a hash table for storing contacts.
    Attributes:
        size (int): The size of the hash table.
        data (list): The underlying array to store linked lists for collision handling.
    '''
    def __init__(self, size):
        self.size = size
        self.data = [None] * size

    def hash_function(self, key):
        total = sum(ord(char) for char in key)
        return total % self.size

    def insert(self, key, number):
        index = self.hash_function(key)
        new_contact = Contact(key, number)
        node = self.data[index]

        if node is None:
            self.data[index] = Node(key, new_contact)
            return

        prev = None
        current = node
        while current:
            if current.key == key:
                current.value.number = number  # Update existing contact
                return
            prev = current
            current = current.next
        prev.next = Node(key, new_contact)  # Add new node at the end

    def search(self, key):
        index = self.hash_function(key)
        current = self.data[index]
        while current:
            if current.key == key:
                return current.value
            current = current.next
        return None

    def print_table(self):
        for i, node in enumerate(self.data):
            output = f"Index {i}:"
            if node is None:
                output += " Empty"
            else:
                current = node
                while current:
                    output += f" - {current.value}"
                    current = current.next
            print(output)


# Test your hash table implementation here. 

# Initialize hash table
table = HashTable(10)

# Test 1: Empty table
for i in range(10):
    assert table.data[i] is None, f"Index {i} should be empty initially."

# Test 2: Add John and Rebecca
table.insert("John", "909-876-1234")
table.insert("Rebecca", "111-555-0002")
assert str(table.search("John")) == "John: 909-876-1234", "John should be found with correct number."
assert str(table.search("Rebecca")) == "Rebecca: 111-555-0002", "Rebecca should be found with correct number."

# Test 3: Collision handling (Amy and May)
table.insert("Amy", "111-222-3333")
table.insert("May", "222-333-1111")
# Both should exist in the same linked list
index_amy = table.hash_function("Amy")
current = table.data[index_amy]
found_keys = set()
while current:
    found_keys.add(current.key)
    current = current.next
assert "Amy" in found_keys, "Amy should be in the table."
assert "May" in found_keys, "May should be in the table."

# Test 4: Duplicate key update (Rebecca)
table.insert("Rebecca", "999-444-9999")
assert str(table.search("Rebecca")) == "Rebecca: 999-444-9999", "Rebecca's number should be updated."

# Test 5: Search for non-existent contact
assert table.search("Chris") is None, "Chris should not be found in the table."

# Test 6: Hash table structure (optional, visual verification)
print("Hash table after all insertions and updates:")
table.print_table()

print("\nAll assertions passed! Hash table implementation works correctly.")

"""
Design Memo:

Hash tables are ideal for fast lookups because they use a hash function to compute the index where each 
value should reside, providing average O(1) search time. This efficiency is critical for contact management 
systems with hundreds of entries, where linear search through a list would be slow.

Collisions are handled using separate chaining. Each index of the hash table stores a linked list of Node 
objects. If multiple keys hash to the same index, the new contact is appended to the linked list. If a 
contact with the same key already exists, its number is updated to maintain unique keys.

An engineer might choose a hash table over a list when fast, key-based retrieval is more important than 
order. Compared to a tree, hash tables offer faster average lookup and insertion times, though they do 
not maintain a sorted structure. They are especially useful when the dataset requires frequent searches, 
updates, or uniqueness enforcement on keys.

"""
 