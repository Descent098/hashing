from hashing import hash_function
from dataclasses import dataclass, field
from typing import Any, List

@dataclass
class Node:
    """A node to be inserted into a HashTable
    
    Attributes
    ----------
    key: str
        The key for the node to use
    
    value: Any
        The value to associate to the key
    """
    key:str
    value: Any

@dataclass
class HashTable:
    """A standard HashTable to store key-value pairs

    Attributes
    ----------
    buckets:List[List[Node]]
        The list of buckets to use for hash lookups
    """
    buckets:List[List[Node]] = field(default_factory=lambda: [[] for _ in range(16)])
    
    def insert(self, key:str, value:Any):
        """Inserts a key-value pair into the buckets

        Parameters
        ----------
        key : str
            The key to associate to a value

        value : Any
            A value to store at the index hash for the key
        """

        # 2 & 3 Hash the key and then modulo the result by 16
        index = int(hash_function(key) % 16)
        
        # 4.  Create a node which contains the value and the key
        new_node = Node(key, value)
        
        # 5. Insert the node into the index you calculated from the key
        if self.buckets[index]: ## If the bucket already has values
            self.buckets[index].append(new_node)
        else: ## If bucket was empty
            self.buckets[index] = [new_node]
            
    def find(self, key:str) -> Any:
        """Find a value for a given key

        Parameters
        ----------
        key : str
            The key to search for

        Returns
        -------
        Any
            The value associated with the key

        Raises
        ------
        ValueError
            If the key does not exist
        """
        # 1 & 2 Hash the key and then modulo the result by 16
        index = int(hash_function(key) % 16)
        
        # 3. Look into the bucket at the given index
        if self.buckets[index]:
            ## 3.1 Check each node in the bucket to find the matching one
            for node in self.buckets[index]:
                ## 3.2 The current node matches the key you're looking for
                if node.key == key:
                    return node.value
            raise ValueError(f"No value found for key {key}")
        else: 
            raise ValueError(f"No value found for key {key}")

@dataclass
class HashTableImproved:
    buckets:List[List[Node]] = field(default_factory=lambda: [[] for _ in range(16)])
    
    def __getitem__(self, key:str) -> Any:
        """Find a value for a given key

        Parameters
        ----------
        key : str
            The key to search for

        Returns
        -------
        Any
            The value associated with the key

        Raises
        ------
        ValueError
            If the key does not exist

        Notes
        -----
        The naming allows for dictionary lookup (HashTable()[key])
        """

        # 1 & 2 Hash the key and then modulo the result by 16
        index = int(hash_function(key) % 16)

        # 3. Look into the bucket at the given index
        if self.buckets[index]:
            ## 3.1 Check each node in the bucket to find the matching one
            for node in self.buckets[index]:
                if node.key == key:
                    ## 3.2 The current node matches the key you're looking for
                    return node.value
        else: 
            raise ValueError(f"No value found for key {key}")
    
    def __setitem__(self, key:str, value:Any):
        """Inserts a key-value pair into the buckets

        Parameters
        ----------
        key : str
            The key to associate to a value

        value : Any
            A value to store at the index hash for the key
        
        Notes
        -----
        The naming allows for dictionary lookup (HashTable()[key] = "value")
        """
        
        # 2 & 3 Hash the key and then modulo the result by 16
        index = int(hash_function(key) % 16)
        
        # 4.  Create a node which contains the value and the key
        new_node = Node(key, value)
        if self.buckets[index]: # If current bucket isn't empty
            # 5. Insert the node into the index you calculated from the key
            for node in self.buckets[index]:
                ## 5.1 If key already existed, update value
                if node.key == key:
                    node.value = value
                    return
            ## 5.2 If key did not exist in bucket append node to bucket
            self.buckets[index].append(new_node)
            
        else: # If current bucket is empty
            self.buckets[index] = [new_node]
            
    def __repr__(self) ->str:
        result = "HashTableImproved: {"
        for bucket in self.buckets:
            if bucket:
                for node in bucket:
                    result += f"'{node.key}':{f'{node.value}' if type(node.value) == str else node.value},"
        return result[:-1] + "}" # Remove last , and finish string
    
    def __str__(self) ->str:
        return self.__repr__()
        

if __name__ == "__main__":
    # Test original Hash table
    ht = HashTable()

    ht.insert("novelty", 10)
    ht.insert("yeotlvn", 11)
    ht.insert("voetlny", 12)
    ht.insert("eoltvyn", 13)
    ht.insert("asdfgsdfg", 10)
    print(ht.find("novelty"))
    print(ht.find("yeotlvn"))
    print(ht.find("eoltvyn"))
    # print(ht.find("Ay Lmao"))
    print(ht.buckets)

    # Test improved hash Table
    ht2 = HashTableImproved()

    ht2["novelty"]=10
    ht2["yeotlvn"]=11
    ht2["voetlny"]=12
    ht2["eoltvyn"]=13
    ht2["asdfgsdfg"]=10
    
    print(ht2)
    print(ht2["novelty"])
    print(ht2["yeotlvn"])
    print(ht2["eoltvyn"])
    # print(ht2["Ay Lmao"])