import os
from enum import Enum

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../"))
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

BUILDS = [
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
    "Rust",
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