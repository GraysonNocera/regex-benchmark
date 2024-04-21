import os

PROJECT_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../")
AVAILABLE_TEXT_FILES = os.listdir(os.path.join(PROJECT_ROOT, "haystacks"))

ENGINES = [
    "C PCRE2",
    "Crystal",
    "C++ STL",
    "C++ Boost",
    "C++ SRELL",
    "C# Mono",
    "C# .Net Core",
    "D dmd",
    "D ldc",
    "Dart Native",
    "Go",
    "Java",
    "Kotlin",
    "Nim",
    "Nim Regex",
    "Perl",
    "PHP",
    "Python 2",
    "Python 3",
    "Python PyPy2",
    "Python PyPy3",
    "Ruby",
    "Rust"
]