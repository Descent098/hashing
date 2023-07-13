import re
from typing import List
from hashing import hash_function
from hashtables import HashTableImproved

regex = r"<script (.*)>(.*)</script>" # Pattern used to find info

test_str = """<script>Hello world</script>\n
	<script integrity=\"hash_function-10863092770407275780296754544299212800001234567891111111111222222222233333333334444444444555555555566666666667777777777888888888\" src=\"file.js\"></script>\n
	<script integrity=\"hash_function-10863092770407275780296754544299212800001234567891111111111222222222233333333334444444444555555555566666666667777777777888888888\">console.log('Hello World')</script>\n
	<h1>Hello world</h1>"""

def get_script_tag_information(text:str) -> List[HashTableImproved]:
    """Parses HTML input and returns details about the script tags inside

    Parameters
    ----------
    text : str
        The input HTML to parse

    Returns
    -------
    List[HashTableImproved]
        Returns a list of HashTableImproved's representing each tags information
    """
    matches = re.finditer(regex, text, re.MULTILINE)
    results = []
    for match in matches:
        attributes = match.group(1).split(" ")
        src = ""
        integrity_hash = ""
        integrity_scheme = ""
        inner_content = match.group(2)

        # Find Attributes we care about
        if "src" in match.group(0):
            for attribute in attributes:
                if "src" in attribute:
                    src = attribute.split("=")[1].replace("\"","").replace("'","")

        if "integrity" in match.group(0): # Integrity exists in the tag
            for attribute in attributes: # Search for the integrity attribute
                if "integrity" in attribute:
                    integrity_string = attribute.split("=")[1].replace("\"","").replace("'","")
                    integrity_scheme, integrity_hash = integrity_string.split("-")
                    break
        
        # Store information about tag to a hash table
        current_tag_info = HashTableImproved()
        current_tag_info["src"] = src
        current_tag_info["integrity_scheme"] = integrity_scheme
        current_tag_info["integrity_hash"] = integrity_hash
        current_tag_info["inner_content"] = inner_content
        
        # Store hash table in results list
        results.append(current_tag_info)
    return results
            

def check_tag_integrity(tag_integrity_hash:str, tag_integrity_hash_function:callable=hash_function, file_location: str="", inline_js:str =""):
    """A function to check the integrity of an individual script tag

    Parameters
    ----------
    tag_integrity_hash : str
        The hash provided by the tag to check against

    tag_integrity_hash_function : callable, optional
        The hash function to check with, by default hash_function

    file_location : str, optional
        The location of the src file for the tag if one is available, by default ""

    inline_js : str, optional
        The inline javascript to check integrity against if it has any (overriden if file_location provided), by default ""
    
    Raises
    ------
    ValueError:
        If the integrity does not match
    """
    if file_location:
        with open(file_location, "r") as src_file:
            file_integrity = tag_integrity_hash_function(src_file.read())
        if not str(file_integrity) == str(tag_integrity_hash):
            raise ValueError(f"File {file_location} content does not match the integrity hash provided")
    else:
        js_integrity = tag_integrity_hash_function(inline_js)
        if not str(js_integrity) == str(tag_integrity_hash):
            raise ValueError(f"Provided inline JS does not match integrity hash:\n{inline_js}")


def check_input_integrities(input_text: str):
    """Finds and verifies the integrities of all script tags in input HTML

    Parameters
    ----------
    input_text : str
        The HTML you want to verify
    
    Raises
    ------
    ValueError:
        If the integrity of any tag does not match
    """
    tags = get_script_tag_information(input_text) # Get list of script tags and their information

    for tag in tags: # Check each tag's integrity
        if tag["integrity_scheme"] and tag["integrity_hash"]: # Has a hash and listed integrity scheme (hash function)
            if tag["src"]: # If tag pulls from a js file
                check_tag_integrity(tag["integrity_hash"], file_location=tag["src"])
            else: # If tag is inline JS
                check_tag_integrity(tag["integrity_hash"],inline_js=tag["inner_content"])


def generate_script_with_integrity(file_location: str="", inline_js:str ="") -> str:
    """Takes in either a JS file or inline JS and gives you a script tag with an integrity hash as a string

    Parameters
    ----------
    file_location : str, optional
        If you want to use a JS file, specify it's path, by default ""

    inline_js : str, optional
        If you want to use inline js then specify the JS, by default ""

    Returns
    -------
    str
        A script tag with an integrity hash, and either a src or innertext of the js

    Raises
    ------
    ValueError
        If neither a file location or inline JS is provided
    """
    if file_location:
        with open(file_location, "r") as src_file:
            integrity = hash_function(src_file.read())
        return f"<script src=\"{file_location}\" integrity=\"hash_function-{integrity}\"></script>"
    elif inline_js:
        integrity = hash_function(inline_js)
        return f"<script integrity=\"hash_function-{integrity}\">{inline_js}</script>"
    else:
        raise ValueError("Please provide a file location, or the inline javascript")

if __name__ == "__main__":
    # Testing generating a script with an integrity tag
    ## File based
    print(generate_script_with_integrity("file.js"))
    ## Inline JS
    print(generate_script_with_integrity(inline_js = r"console.log('Hello World')"))
    
    # Test the input integrities with the text string of 3 script tags
    check_input_integrities(test_str)
