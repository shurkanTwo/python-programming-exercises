from typing import List

# def sum_numbers(values: List[int]) -> int:
#     return sum(values)

# print(sum_numbers([1, 2, 3]))

# def count_vowels(text: str) -> int:
#     vowels = "aeiouAEIOU"
#     return sum(1 for c in text if c in vowels)

# print(count_vowels("Hello World"))


def encrypt(text: str, shift: int) -> str:
    charsLower = "abcdefghijklmnopqrstuvwxyz"
    charsUpper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    newString: str = ""

    for char in text:
        if char in charsLower:
            newString += charsLower[(charsLower.index(char) + shift) % 26]
        elif char in charsUpper:
            newString += charsUpper[(charsUpper.index(char) + shift) % 26]
        else:
            newString += char
    return newString


def encrypt2(text: str, shift: int) -> str:
    result: List[str] = []

    for char in text:
        if "a" <= char <= "z":
            base = ord("a")
            result.append(chr((ord(char) - base + shift) % 26 + base))
        elif "A" <= char <= "Z":
            base = ord("A")
            result.append(chr((ord(char) - base + shift) % 26 + base))
        else:
            result.append(char)

    return "".join(result)


def encrypt3(text: str, shift: int) -> str:
    return "".join(shift_char(c, shift) for c in text)


def shift_char(char: str, shift: int) -> str:
    if "a" <= char <= "z":
        base = ord("a")
        return chr((ord(char) - base + shift) % 26 + base)
    elif "A" <= char <= "Z":
        base = ord("A")
        return chr((ord(char) - base + shift) % 26 + base)
    else:
        return char


def decrypt(text: str, shift: int) -> str:
    charsLower = "abcdefghijklmnopqrstuvwxyz"
    charsUpper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    newString: str = ""

    for char in text:
        if char in charsLower:
            newString += charsLower[(charsLower.index(char) - shift) % 26]
        elif char in charsUpper:
            newString += charsUpper[(charsUpper.index(char) - shift) % 26]
        else:
            newString += char
    return newString


print(encrypt3("abc", 2))  # "cde"
print(encrypt3("Zebra!", 1))  # "Afcsb!"
print(encrypt3("Hello, World!", 3))  # "Khoor, Zruog!"

print(decrypt("Khoor, Zruog!", 3))  # "Hello, World!"
print(decrypt(encrypt("Python", 5), 5))  # "Python"


def count_words(text: str) -> dict[str, int]:
    newString: str = "".join(c for c in text if c.isalpha() or c == " ")

    newString = newString.lower().strip()
    strings: List[str] = newString.split(" ")
    findings: dict[str, int] = {}

    for word in strings:
        count: int = newString.count(word)
        findings[word] = count

    return findings


import re
from collections import Counter


def count_words2(text: str) -> dict[str, int]:
    words = re.findall(r"[a-zA-Z]+", text.lower())
    return dict(Counter(words))


print(count_words("Das hier ist ist ist, ein Text, mal sehen !"))

# Use str.lower()
# Use str.isalpha() or regex (re.sub) to remove punctuation
# Use a dictionary to store counts
# Optional: type hint with dict[str, int]
