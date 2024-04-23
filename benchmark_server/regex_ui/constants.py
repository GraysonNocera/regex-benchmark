import os
from enum import Enum

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../"))
AVAILABLE_TEXT_FILES = os.listdir(os.path.join(PROJECT_ROOT, "haystacks"))

ENGINES = [
    "C PCRE2",
    "C# .Net Core",
    "C++ Boost",
    "C++ SRELL",
    "C++ STL",
    "Crystal",
    "D dmd",
    "D ldc",
    "Dart Native",
    "Go",
    "Grep",
    # "Hyperscan",
    "Java",
    "Kotlin",
    "Nim",
    "Nim Regex",
    "PHP",
    "Perl",
    "Python 2",
    "Python 3",
    "Python PyPy2",
    "Python PyPy3",
    "Re2",
    "Ruby",
    "Rust"
]

BUILDS = [
    "C PCRE2",
    "Crystal",
    "C++ STL",
    "C++ Boost",
    "C++ SRELL",
    "C# .Net Core",
    "D dmd",
    "D ldc",
    "Dart Native",
    "Go",
    "Java",
    "Kotlin",
    "Nim",
    "Nim Regex",
    "Rust"
]

class RUN_STATUS(Enum):
    NOT_STARTED = 0
    COMPILING = 1
    RUNNING = 2
    COMPLETED = 3
    FAILED = 4
    CANCELLED = 5

class ENGINE_STATUS(Enum):
    NOT_STARTED = 0
    RUNNING = 1
    COMPLETED = 2