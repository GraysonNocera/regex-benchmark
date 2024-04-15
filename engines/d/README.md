# D Regex Benchmark

## How to build

```sh
# DMD
dmd -O -release -inline benchmark.d

# LDC
ldc2 -O3 -release benchmark.d
```

## How to run

```sh
./benchmark <filename>
```
