import subprocess
import json
import os
import numpy as np
import csv


RUN_TIMES = 25

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
    "Dart Native": "mkdir -p /var/regex/engines/dart/bin && dart2native engines/dart/benchmark.dart -o engines/dart/bin/benchmark",
    "Go": 'go env -w GO111MODULE=auto && go build -ldflags "-s -w" -o engines/go/bin/benchmark ./go',
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
    "Dart Native": "engines/dart/bin/benchmark",
    "Go": "engines/go/bin/benchmark",
    "Java": "java -XX:+UnlockExperimentalVMOptions -XX:+UseEpsilonGC -XX:+AlwaysPreTouch -Xmx256M -Xms256M -classpath engines/java Benchmark",
    "Kotlin": "kotlin engines/kotlin/benchmark.jar",
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
    "grep": "python3 engines/grep/benchmark.py",
    "hyperscan": "python3 engines/hyperscan/benchmark.py",
    "re2": "python3 engines/re2/benchmark.py"
}

test_name = "test_new_engines.json"
path_to_test_file = os.path.join("benchmarks", test_name)
TEST_DATA = json.load(open(path_to_test_file, "r"))

class Benchmark:

    def __init__(self, path_to_haystack: str, patterns: list(str), run_times: int):
        self.path_to_haystack = path_to_haystack
        self.patterns = patterns
        self.run_times = run_times

    def run(self, command: str):
        runs = [[] * run_times]
        for i in range(run_times):
            # list that has length len(patterns)
            times = self.run_one(command)
            runs[i] = times

        # returns average list of times with length len(pattern)
        runs = np.array(runs)
        average_times = runs.mean(axis=0)
        return average_times

    def run_one(self, command: str) -> list:
        patterns = '" "'.join(self.patterns)
        subproc = subprocess.run(
            f'{command} {self.path_to_haystack} "{patterns}"',
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = subproc.stdout, subproc.stderr
        # print(stdout.decode(), stderr.decode())
        times = [
            float(line.split(b"-")[0].strip())
            for line in stderr.splitlines()
            if line.strip()
        ]
        print(".", end="", flush=True)
        return times

def build_engines():
    print("-------------------------------------------")
    print("Building compilable files for testing .....")
    list_of_test_languages = set.union(*[set(data["engines"]) for data in TEST_DATA])
    for language, build_cmd in BUILDS.items():
        if language in list_of_test_languages:
            subprocess.run(build_cmd, shell=True)
            print(f"{language} built.")

def write_one_row(path_to_csv, row):
    with open(path_to_csv, "a+") as f:
        csv_writer = csv.writer(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(row)

print("------------------------")
print("Running benchmarks .....")
results = {}

for test_number, data in enumerate(TEST_DATA):
    print("------------------------------------------")
    print(f'Running benchmarks for {data["name"]} ...')
    for engine in data["engines"]:
        csv_file_name = f"{engine}_{test_name.strip(".json")}[{test_number}].csv"
        path_to_csv = os.path.join("csv", csv_file_name)
        first_row = [f"{test_name.strip(".json")}"] + [data["test_regexes"]]
        write_one_row(path_to_csv, first_row)

        command = COMMANDS[engine]
        print(f"{engine} running.", end=" ")

        PATTERNS_COUNT = len(data["test_regexes"])
        current_results = [[] for _ in range(PATTERNS_COUNT)]

        for input_text in data["test_string_files"]:
            input_text = os.path.join(os.path.dirname(__file__), "haystacks", input_text)

            if "split_string_file" in data and data["split_string_file"]:
                lines = []
                with open(input_text, "r") as f:
                    lines = f.readlines()
                for line in lines:
                    temp_file = os.path.join(os.path.dirname(__file__), "haystacks", "temp")
                    with open(temp_file, "w") as f:
                        f.write(line)
                    benchmark = Benchmark(line, data[test_regexes], RUN_TIMES)
                    average_times = benchmark.run(command)
                    csv_row = [line] + average_times
                    write_one_row(path_to_csv, csv_row)
            else:
                benchmark = Benchmark(input_text, data[test_regexes], RUN_TIMES)
                average_times = benchmark.run(command)
                csv_row = [input_text] + average_times
                write_one_row(path_to_csv, csv_row)

            print(f" {engine} ran.")

    print("------------------------")
    print("Benchmark results .....")

    results = dict(sorted(results.items(), key=lambda item: item[1][-1]))

    for language, result in results.items():
        result_formatted = [f"{time:.2f}" for time in result]
        print(f'**{language}** | {" | ".join(result_formatted)}')
