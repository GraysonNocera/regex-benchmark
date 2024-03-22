import re

def test(regex, string):
  pattern = re.compile(regex)
  # print(f"regex: {regex}. string: {string}.", end="")
  print(f"{pattern.search(string)}")

# Special characters
pattern = re.compile(r'^1*2+?(a|b)+(A|B){2,3}$')
string = "2222abaaaABB"
print(pattern.search(string))

# Non-printable characters
pattern = re.compile(r'\t+\n*')
string = "				\n"
print(pattern.search(string))

# Character classes
pattern = re.compile(r'gr[ae]y')
string = "gray"
print(pattern.search(string))

pattern = re.compile(r'[0-9a-fxA-FX]+')
string = "0x19X"
print(pattern.search(string))

pattern = re.compile(r'q[^0-9\r\n]')
string = "qr"
print(pattern.search(string))

pattern = re.compile(r'[+*1]+')
string = "1++11****1"
print(pattern.search(string))

""" I don't think python has nested character classes """

# Shorthand character classes

pattern = re.compile(r'\d\s\w')
string = "9 w"
print(pattern.search(string))

pattern = re.compile(r'\D\S\W')
string = "a9 "
print(pattern.search(string))

# Anchors

pattern = re.compile(r'^word$')
string = "This will not match the word in the middle"
print(pattern.search(string))

# Word Boundaries

pattern = re.compile(r'\bis\b')
string = "Won't match island but will match is in the string"
print(pattern.search(string))

pattern = re.compile(r'\Ba\B')
string = "Won't with a but matches that a but not these a"
print(pattern.search(string))

# Alternations

pattern = re.compile(r'\b(cat|dog)\b')
string = "Will match the first dog and skip the cat"
print(pattern.search(string))

# Optional items

pattern = re.compile(r'Feb(ruary)? 23(rd)?')
string = "Will match Feb 23 and February 23rd and Feb 23"
print(pattern.search(string))

# Repetition with Star and Plus

pattern = re.compile(r'<[A-Za-z0-9]+>')
string = "Will not match <> but will match <a>"
print(pattern.search(string))

# Grouping and Capturing groups

pattern = re.compile(r'Set(Value)?')
string = "SetValue"
print(pattern.search(string).group(1))

pattern = re.compile(r'Set(?:Value)?')
string = "SetValue"
# print(pattern.search(string).group(1)) # Gives error, no groups
print(pattern.search(string))

# Backreferences (the regex stores the last backreference used, so it can change over time)

pattern = re.compile(r'([a-c])x\1x\1')
string = "axaxa"
print(pattern.search(string)) # matches

pattern = re.compile(r'([a-c])x\1x\1')
string = "axbxa"
print(pattern.search(string)) # doesn't match

# the backreference is the last letter before the =
pattern = re.compile(r'([abc]+)=\1')
string = "abbaca=a"
print(pattern.search(string))

# Backreferences to failed groups

pattern = re.compile(r'(q?)b\1')
string = "b"
print(pattern.search(string))

test(r'(q)?b\1', "b") # matches b

# Forward references (python does not support)

# Named capturing groups

test(r'<(?P<tag>[A-Z][A-Z0-9]*)\b[^>]*>.*?</(?P=tag)>', "<I>hi</I>")

# Relative backreferences (not in Python I don't think)

# Branch reset groups (these are nasty and Python doesn't have them)

# Free-spacing mode (?x)

test(r'(?x)    \d+     \w+ ', "1290ave")
test(r'(?x)   \d+ # matches a number    \
              \w+ # matches a character \
', "12lane")
test(r"""(?x)
                 \d+  # matches a number
      \w+               # matches a character

""", "56avelane")

# Unicode is weird

# Mode modifiers

test(r'(?i)test', "TEst")
test(r'(?s).*', "multi-line \n stuff")
test(r'(?m).*', "multi-line \n stuff")

# Atomic grouping (discards all backtracking)

test(r'\b(?>in|integer|insert)\b', "insert")
test(r'\b(in|integer|insert)\b', "insert")

# Possessive Quantifiers (add a + at the end) (performance boost)

test(r'"[^"]*+"', "\"abc\"")
test(r'".*+"', "\"abc\"")
test(r'".*"', "\"abc\"")

# These are equivalent (atomic grouping and possessive quantifiers are the same)
test(r'(?:a|b)*+', "bac")
test(r'(?>(?:a|b)*)', "bac")

# Lookahead and Lookbehind (Python only allows fixed length look behind) (atomic)

# Lookhead
test(r'q(?!u)', "qit")
test(r'q(?!u)', "quit")
test(r'q(?=u)', "quit")
test(r'q(?=u)', "qit")

# Lookbehind
test(r'(?<!a)b', "bed")
test(r'(?<!a)b', "cab")
test(r'(?<=a)b', "cab")
test(r'(?<=a)b', "bed")

test(r'\b(?=\w{6}\b)\w{0,3}cat\w*', "Matches six letter word with cat in it: shcats")

# If-then-else conditionals

test(r'(a)?b(?(1)c|d)', "bd")
test(r'(a)?b(?(1)c|d)', "abc")
test(r'(a)?b(?(1)c|d)', "bc")
test(r'(a)?b(?(1)c|d)', "abd")

# Balancing groups (too complicated)
# test(r'''(?'open'o)+(?'between-open'c)+''', "ooccc") # will not compile

"""There is a lot of stuff on recursion here (https://www.regular-expressions.info/recurse.html)
but since it's only allowed in a few regex flavors, I didn't dive into it"""
# Recursion (too complicated)

# Subroutines (also too complicated)

# Zero-length regex match (some handle these differently)

test(r'\d*|x', "x1")

# Continuing at the end of a previous match (python no like this)



