import re
from typing import List
from hashing import hash_function
from hashtables import HashTableImproved

regex = r"<script (.*)>(.*)</script>" # Pattern used to find info

test_str = ("<script>Hello world</script>\n"
	"<script integrity=\"hash_function-10863092770407275780296754544299212800001234567891111111111222222222233333333334444444444555555555566666666667777777777888888888\" src=\"file.js\"></script>\n"
	"<script integrity=\"hash_function-10863092770407275780296754544299212800001234567891111111111222222222233333333334444444444555555555566666666667777777777888888888\">console.log('Hello World')</script>\n"
	"<h1>Hello world</h1>")

def get_script_tag_information(text:str) -> List[HashTableImproved]:
    matches = re.finditer(regex, text, re.MULTILINE)
    results = []
    for match in matches:
        attributes = match.group(1).split(" ")
        src = ""
        integrity_hash = ""
        integrity_scheme = ""
        inner_content = match.group(2)
        

        if "src" in match.group(0):
            print('has src')
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
    """
    print(f"Check called with {file_location=}, {inline_js=}")
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
    tags = get_script_tag_information(input_text)
    print(f"{tags=}")
    for tag in tags:
        print(f"{tag=}")
        if tag["integrity_scheme"] and tag["integrity_hash"]:
            if tag["src"]:
                check_tag_integrity(tag["integrity_hash"], file_location=tag["src"])
            else:
                check_tag_integrity(tag["integrity_hash"],inline_js=tag["inner_content"])


def generate_script_with_integrity(file_location: str="", inline_js:str ="") -> str:
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
    print(generate_script_with_integrity("file.js"))
    # print(generate_script_with_integrity(inline_js = r"console.log('Hello World')"))
    check_input_integrities(test_str)