import subprocess
import json

PATTERNS_COUNT = 3
RUN_TIMES = 10

BUILDS = {
    'C PCRE2': 'gcc -O3 -DNDEBUG c/benchmark.c -I/usr/local/include/ -lpcre2-8 -o c/bin/benchmark',
    'Crystal': 'crystal build crystal/benchmark.cr --release -o crystal/bin/benchmark',
    'C++ STL': 'g++ -std=c++11 -O3 cpp/benchmark.cpp -o cpp/bin/benchmark-stl',
    'C++ Boost': 'g++ -std=c++11 -O3 cpp/benchmark.cpp -DUSE_BOOST -lboost_regex -o cpp/bin/benchmark-boost',
    'C++ SRELL': 'g++ -std=c++11 -O3 cpp/benchmark.cpp -DUSE_SRELL -o cpp/bin/benchmark-srell',
    'C# Mono': 'mcs csharp/Benchmark.cs -out:csharp/bin-mono/benchmark.exe -debug- -optimize',
    'C# .Net Core': 'dotnet build csharp/benchmark.csproj -c Release',
    'D dmd': 'dmd -O -release -inline -of=d/bin/benchmark d/benchmark.d',
    'D ldc': 'ldc2 -O3 -release -of=d/bin/benchmark-ldc d/benchmark.d',
    'Dart Native': 'mkdir -p /var/regex/dart/bin && dart2native dart/benchmark.dart -o dart/bin/benchmark',
    'Go': 'go env -w GO111MODULE=auto && go build -ldflags "-s -w" -o go/bin/benchmark ./go',
    'Java': 'javac java/Benchmark.java',
    'Kotlin': 'kotlinc kotlin/benchmark.kt -include-runtime -d kotlin/benchmark.jar',
    'Nim': 'nim c -d:release --opt:speed --verbosity:0 -o:nim/bin/benchmark nim/benchmark.nim',
    'Nim Regex': 'nim c -d:release --opt:speed --verbosity:0 -o:nim/bin/benchmark_regex nim/benchmark_regex.nim',
    'Rust': 'cargo build --quiet --release --manifest-path=rust/Cargo.toml',
}

COMMANDS = {
    'C PCRE2': 'c/bin/benchmark',
    'Crystal': 'crystal/bin/benchmark',
    'C++ STL': 'cpp/bin/benchmark-stl',
    'C++ Boost': 'cpp/bin/benchmark-boost',
    'C++ SRELL': 'cpp/bin/benchmark-srell',
    'C# Mono': 'mono -O=all csharp/bin-mono/benchmark.exe',
    'C# .Net Core': 'dotnet csharp/bin/Release/net5.0/benchmark.dll',
    'D dmd': 'd/bin/benchmark',
    'D ldc': 'd/bin/benchmark-ldc',
    'Dart Native': 'dart/bin/benchmark',
    'Go': 'go/bin/benchmark',
    'Java': 'java -XX:+UnlockExperimentalVMOptions -XX:+UseEpsilonGC -classpath java Benchmark',
    'Kotlin': 'kotlin kotlin/benchmark.jar',
    'Nim': 'nim/bin/benchmark',
    'Nim Regex': 'nim/bin/benchmark_regex',
    'Perl': 'perl perl/benchmark.pl',
    'PHP': 'php php/benchmark.php',
    'Python 2': 'python2.7 python/benchmark.py',
    'Python 3': 'python3.6 python/benchmark.py',
    'Python PyPy2': 'pypy2 python/benchmark.py',
    'Python PyPy3': 'pypy3 python/benchmark.py',
    'Ruby': 'ruby ruby/benchmark.rb',
    'Rust': 'rust/target/release/benchmark',
}

TEST_DATA = json.load(open('test.json', 'r'))


print("-------------------------------------------")
print("Building compilable files for testing .....")
for language, build_cmd in BUILDS.items():
    subprocess.run(build_cmd, shell=True)
    print(f'{language} built.')


print("------------------------")
print("Running benchmarks .....")
results = {}

for data in TEST_DATA:
    print("------------------------------------------")
    print(f'Running benchmarks for {data["name"]} ...')
    for language in data['engines']:
        command = COMMANDS[language]
        print(f'{language} running.', end=' ')

        current_results = [[] for _ in range(PATTERNS_COUNT)]

        for input_text in data['texts']:
            for i in range(RUN_TIMES):
                out = subprocess.run(f'{command} {input_text}', shell=True, capture_output=True, text=True).stdout
                matches = [float(match) for match in out.splitlines() if match.strip()]

                if not matches:
                    break

                for j in range(PATTERNS_COUNT):
                    current_results[j].append(matches[j])

                print('.', end='', flush=True)

            if current_results:
                avg_times = [sum(times) / len(times) for times in current_results]
                results[language] = avg_times + [sum(avg_times)]

            print(f' {language} ran.')

    print("------------------------")
    print("Benchmark results .....")

    results = dict(sorted(results.items(), key=lambda item: item[1][-1]))

    for language, result in results.items():
        result_formatted = [f'{time:.2f}' for time in result]
        print(f'**{language}** | {" | ".join(result_formatted)}')