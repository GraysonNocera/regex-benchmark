import argparse
import csv
import json
import os
import csv
import sys
import subprocess
import time
from haystack import Haystack
from pattern import Pattern
from typing import List

EXIT_FAILURE = 1
EXIT_SUCCESS = 0

parser = argparse.ArgumentParser()
parser.add_argument("testfile", default="test.json", help="Path to the test file", nargs='?')
args = parser.parse_args()

BUILDS = {
    "C PCRE2": "gcc -O3 -DNDEBUG engines/c/benchmark.c -I/usr/local/include/ -lpcre2-8 -o engines/c/bin/benchmark",
    "Crystal": "crystal build engines/crystal/benchmark.cr --release -o engines/crystal/bin/benchmark",
    "C++ STL": "g++ -std=c++11 -O3 engines/cpp/benchmark.cpp -o engines/cpp/bin/benchmark-stl",
    "C++ Boost": "g++ -std=c++11 -O3 engines/cpp/benchmark.cpp -DUSE_BOOST -lboost_regex -o engines/cpp/bin/benchmark-boost",
    "C++ SRELL": "g++ -std=c++11 -O3 engines/cpp/benchmark.cpp -DUSE_SRELL -o engines/cpp/bin/benchmark-srell",
    "C# Mono": "mcs engines/csharp/Benchmark.cs -out:engines/csharp/bin-mono/benchmark.exe -debug- -optimize",
    "C# .Net Core": "dotnet build engines/csharp/benchmark.csproj -c Release",
    "D dmd": "dmd -O -release -inline -of=engines/d/bin/benchmark engines/d/benchmark.d",
    "D ldc": "ldc2 -O3 -release -of=engines/d/bin/benchmark-ldc engines/d/benchmark.d",
    "Dart Native": "mkdir -p /var/regex/engines/dart/bin && dart compile aot-snapshot engines/dart/benchmark.dart -o engines/dart/bin/benchmark.aot",
    "Go": 'go env -w GO111MODULE=auto && go build -ldflags "-s -w" -o engines/go/bin/benchmark ./engines/go',
    "Java": "javac engines/java/Benchmark.java",
    "Kotlin": "kotlinc engines/kotlin/benchmark.kt -include-runtime -d engines/kotlin/benchmark.jar",
    "Nim": "nim c -d:release --opt:speed --verbosity:0 -o:engines/nim/bin/benchmark engines/nim/benchmark.nim",
    "Nim Regex": "nim c -d:release --opt:speed --verbosity:0 -o:engines/nim/bin/benchmark_regex engines/nim/benchmark_regex.nim",
    "Rust": "cargo build --quiet --release --manifest-path=engines/rust/Cargo.toml",
}

COMMANDS = {
    "C PCRE2": "engines/c/bin/benchmark",
    "Crystal": "engines/crystal/bin/benchmark",
    "C++ STL": "engines/cpp/bin/benchmark-stl",
    "C++ Boost": "engines/cpp/bin/benchmark-boost",
    "C++ SRELL": "engines/cpp/bin/benchmark-srell",
    "C# Mono": "mono -O=all engines/csharp/bin-mono/benchmark.exe",
    "C# .Net Core": "dotnet engines/csharp/bin/Release/net5.0/benchmark.dll",
    "D dmd": "engines/d/bin/benchmark",
    "D ldc": "engines/d/bin/benchmark-ldc",
    "Dart Native": "/usr/lib/dart/bin/dartaotruntime engines/dart/bin/benchmark.aot",
    "Go": "engines/go/bin/benchmark",
    "Java": "java -XX:+UnlockExperimentalVMOptions -XX:+UseEpsilonGC -XX:+AlwaysPreTouch -Xmx256M -Xms256M -classpath engines/java Benchmark",
    "JavaScript": "node engines/javascript/benchmark.js",
    "Kotlin": "kotlin engines/kotlin/benchmark.jar",
    "Julia": "julia engines/julia/benchmark.jl",
    "Nim": "engines/nim/bin/benchmark",
    "Nim Regex": "engines/nim/bin/benchmark_regex",
    "Perl": "perl engines/perl/benchmark.pl",
    "PHP": "php engines/php/benchmark.php",
    "Python 2": "python2.7 engines/python/benchmark.py",
    "Python 3": "python3.6 engines/python/benchmark.py",
    "Python PyPy2": "pypy2 engines/python/benchmark.py",
    "Python PyPy3": "pypy3 engines/python/benchmark.py",
    "Ruby": "ruby engines/ruby/benchmark.rb",
    "Rust": "engines/rust/target/release/benchmark",
    "Grep": "python3 engines/grep/benchmark.py",
    "Hyperscan": "python3 engines/hyperscan/benchmark.py",
    "Re2": "python3 engines/re2/benchmark.py"
}

class Benchmark:

    def __init__(self, path_to_haystack: str, pattern: str, run_times: int):
        self.path_to_haystack = path_to_haystack
        self.pattern = pattern
        self.run_times = run_times

    def run(self, command: str):
        subproc = subprocess.run(
            f'{command} {self.path_to_haystack} "{self.pattern}" {self.run_times}',
            shell=True,
            stdout=subprocess.PIPE,
        )
        if subproc.returncode != 0: # some error in the runner program for this regex
            # we shouldn't print here because the runner programs print the actual error, which is more useful
            return -1

        stdout = subproc.stdout
        times = [
            float(line.split(b"-")[0].strip())
            for line in stdout.splitlines()
            if line.strip()
        ]

        average_time = sum(times) / len(times)
        print(".", end="", flush=True)
        return average_time


class CSVWriter:
    def __init__(self, csv_file_name: str, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL):
        path_to_csv = os.path.join("csv", csv_file_name)
        self.f = open(path_to_csv, "w")
        self.writer = csv.writer(self.f, delimiter=delimiter, quotechar=quotechar, quoting=quoting)

    def write_one_row(self, data: List[float], label: str = ""):
        row = [label] + data if label else data
        self.writer.writerow(row)

    def __del__(self):
        self.f.close()

def verify_engines(engines):
    for engine in engines:
        if engine not in COMMANDS:
            raise Exception(f"Unrecognized engine {engine}")

def build_engines(engines):
    print("-------------------------------------------", flush=True)
    print("Building compilable files for testing .....", flush=True)
    list_of_test_languages = set.union(*[set(data["engines"]) for data in TEST_DATA])
    for language, build_cmd in BUILDS.items():
        if language in list_of_test_languages:
            result = subprocess.run(build_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode != 0:
                print(f"Build {build_cmd} failed")
                sys.exit(EXIT_FAILURE)
            print(f"{language} built.", flush=True)

def all_engines(data):
    return set.union(*[set(x["engines"]) for x in data])

path_to_test_file = os.path.join("benchmarks", args.testfile)
TEST_DATA = json.load(open(path_to_test_file, "r"))

engines = all_engines(TEST_DATA)
verify_engines(engines)
build_engines(engines)

print("------------------------", flush=True)
print("Running benchmarks .....", flush=True)
csv_outputs = []

for test_number, data in enumerate(TEST_DATA):
    print("------------------------------------------", flush=True)
    print(f'Running benchmarks for {data["name"]} ...', flush=True)
    run_times = data.get("run_times", 10)

    for engine in data["engines"]:
        print(f"Running engine {engine}\n", file=sys.stderr, flush=True)

        p = Pattern(data["test_regexes"], data.get("regexes_in_file", False))
        h = Haystack(data["test_string_files"], data.get("split_string_file", False))

        test_name_no_json = args.testfile.strip(".json")
        csv_file_name = f"{engine}_{test_name_no_json}[{test_number}].csv"
        csv_outputs.append(csv_file_name)
        csv_writer = CSVWriter(csv_file_name)
        csv_writer.write_one_row(label=test_name_no_json, data=list(range(1, len(p.patterns) + 1)))

        bad_patterns = []

        command = COMMANDS[engine]
        print(f"{engine} running.", end=" ", flush=True)
        line = h.get_one_haystack()
        while line:
            row = []
            pattern = p.get_one_pattern()
            while pattern:
                start = time.time()
                if pattern in bad_patterns:
                    average_time = -1
                else:
                    benchmark = Benchmark(line, pattern, run_times)
                    average_time = benchmark.run(command)
                    if average_time == -1:
                        bad_patterns.append(pattern)
                row += [average_time]
                print(f"Ran {pattern} against {line} in {time.time() - start}", file=sys.stderr, flush=True)
                pattern = p.get_one_pattern()
            p.reset()
            csv_writer.write_one_row(data=row, label=str(h.line_index))
            line = h.get_one_haystack()
        h.reset()
        print(f"\n{engine} ran.", flush=True)
        print(f"Ran engine {engine}\n", file=sys.stderr, flush=True)

    print("------------------------", flush=True)
    print(f"Benchmark results written to files {csv_outputs}", flush=True)
