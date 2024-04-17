function measure(data, pattern)

    compiled_pattern = Regex(pattern)
    start = time()
    count = length(collect(eachmatch(compiled_pattern, data)))
    elapsed = time() - start
    elapsed_ms = 1000 * elapsed

    println(string(elapsed_ms) * " - " * string(count))
end

if length(ARGS) != 3
    println("Usage: julia benchmark.jl <filename> regex num_iterations")
    exit(1)
end

data = open(f->read(f, String), ARGS[1])
pattern = ARGS[2]
num_iterations = parse(Int64, ARGS[3])
for i in 1:num_iterations
    measure(data, pattern)
end
