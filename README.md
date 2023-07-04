# Hashing

This is a helper repository to the blog post on `https://schulichignite.com/blog/<ENTER URI>` that explains a basic hashing algorithm, and it's uses. You can find useful resources here:

- [Associated blog post (TODO)]()
- [Ignite Definition of hashing](https://schulichignite.com/definitions/hashing)

Specifically this will walk through:

1. Creating a custom [hash function](https://en.wikipedia.org/wiki/Hash_function)
2. Creating a password storage and validation system
3. Creating a [HashTable](https://en.wikipedia.org/wiki/Hash_table#:~:text=It%20is%20an%20abstract%20data,the%20corresponding%20value%20is%20stored.)
4. Creating a [subresource integrity](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity) scheme from scratch

## Hashing algorithm

You can find the hashing algorithm in `hashing.py`, this function will be used in the other files and is called `hash_function()`. The basic steps are:

1. Convert the input value to string if it's another data type
2. Start with the number 1, for each character in the input multiply the current hash by the index of the character in the following lokoup table:

```python
ASCII_TABLE = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~', ' ', '\t', '\n', '\r', '\x0b', '\x0c']
```

3. Fix the length of the output to 128 characters.
    - If the resulting hash is less than 128 characters take the difference between the current length of hash and 128, for each of those characters append the character at the index of the current loop itteration in the lookup table (see below for example)
    - if longer truncate to the first 128 characers

Here is the code for step 3:

```python
if len(hash) < 128:
    for number in range(128-len(hash)):
        if number > 99: # Only single digit values allowed
            number //= 100
        elif number > 9:
            number //=10
        hash += str(number)
```

For example if you had a hash with 126 characters then the loop would start '0' would be appended to end of current hash, then on next itteration '1' would be appended. Leaving us with `<current_hash>10` to pad it to 128. Since we want exactly 128 characters we go to 9, then strip the digit for every digit added (i.e. 101 would become 1, and 20 would become 0)

The biggest problem with this approach is there are tons of collisions. Any text which contains the same first 128 characters (an anagram) will **always** collide (this was somewhat intentional to be able to show how bad collisions are for performance of HashTables).

## Password storage (TODO)


## HashTable (TODO)

## Integrity (TODO)

- Regex
    - You technically [don't want to use regex for this parsing](https://blog.codinghorror.com/parsing-html-the-cthulhu-way/)
