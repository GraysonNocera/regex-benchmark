import subprocess
import json
import os


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

TEST_DATA = json.load(open("benchmarks/test_new_engines.json", "r"))


print("-------------------------------------------")
print("Building compilable files for testing .....")
list_of_test_languages = set.union(*[set(data["engines"]) for data in TEST_DATA])
for language, build_cmd in BUILDS.items():
    if language in list_of_test_languages:
        subprocess.run(build_cmd, shell=True)
        print(f"{language} built.")


print("------------------------")
print("Running benchmarks .....")
results = {}

for data in TEST_DATA:
    print("------------------------------------------")
    print(f'Running benchmarks for {data["name"]} ...')
    for language in data["engines"]:
        command = COMMANDS[language]
        print(f"{language} running.", end=" ")

        PATTERNS_COUNT = len(data["test_regexes"])
        current_results = [[] for _ in range(PATTERNS_COUNT)]

        for input_text in data["test_string_files"]:
            input_text = os.path.join(os.path.dirname(__file__), "haystacks", input_text)
            for i in range(RUN_TIMES):
                # TODO: add support for splitting the text file, or just passing in the text not in a file
                test_regexes = '" "'.join(data["test_regexes"])
                # print(f'{command} {input_text} "{test_regexes}"')
                subproc = subprocess.run(
                    f'{command} {input_text} "{test_regexes}"',
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                out, err = subproc.stdout, subproc.stderr
                # print(out.decode(), err.decode())
                matches = [
                    float(match.split(b"-")[0].strip())
                    for match in out.splitlines()
                    if match.strip()
                ]

                if not matches:
                    break

                for j in range(PATTERNS_COUNT):
                    current_results[j].append(matches[j])

                print(".", end="", flush=True)

            if current_results:
                avg_times = [sum(times) / len(times) for times in current_results]
                results[language] = avg_times + [sum(avg_times)]

            print(f" {language} ran.")

    print("------------------------")
    print("Benchmark results .....")

    results = dict(sorted(results.items(), key=lambda item: item[1][-1]))

    for language, result in results.items():
        result_formatted = [f"{time:.2f}" for time in result]
        print(f'**{language}** | {" | ".join(result_formatted)}')
