from hashing import hash_function
from dataclasses import dataclass

# The salt and pepper to add to passwords (would need to be a secret)
SALT = "%^&(!%#@@#$&$@&#!^%)"
PEPPER = "!@^%@#&#@#(@*&@%&)"

@dataclass
class User:
    name: str
    username:str
    email:str
    age: int
    password: str

# The "database" of users

users = [
    User("Kieran", "descent098", "kieran@kieranwood.ca", 24, hash_function(PEPPER + "you'll_never_guess_my_password" + SALT))
]

def signup(name:str, username:str, email:str, age:int, password:str):
    """Lets you create a new user

    Parameters
    ----------
    name : str
        The users name

    username : str
        The username the user requested (used to login, must be unique)

    email : str
        The user's email

    age : int
        The age of the user

    password : str
        The user's password (unhashed)
        
    Notes
    -----
    - In the real world you should only ever pass the hashed version of a
    password to your app, so the hashing should happen ideally BEFORE this funciton

    Raises
    ------
    ValueError
        If you try to create a user with a username that already exists
    """
    password = PEPPER + password + SALT
    password = hash_function(password)
    for user in users:
        if user.username == username:
            raise ValueError(f"User with username: {username} already exists")
    # Update the global "database" (just a variable in our case)
    users.append(User(name, username, email, age, password))

def login(username:str, password:str) -> User:
    """Allows a user to login

    Parameters
    ----------
    username : str
        The username to login with

    password : str
        The plaintext password to login with (in real world you should hash before passing to a function)

    Returns
    -------
    User
        The User object for the corresponding user (if login successful)

    Raises
    ------
    ValueError
        Raised when password is incorrect
    """
    password = PEPPER + password + SALT
    password = hash_function(password)
    for user in users:
        if user.username == username:
            if user.password == password:
                return user
            else: # Bad password
                raise ValueError(f"Incorrect password for user {username}")


if __name__ == "__main__":
    signup("Jamie", "j-amy23", "jamie@canada.gov", 23, "ilovekittens23")
    print(users)
    print(login("j-amy23", "ilovekittens23"))
    print(login("descent098", "you'll_never_guess_my_password"))