require "benchmark"

# this simply takes way too long to build

EXIT_FAILURE = 1
EXIT_SUCCESS = 0

if (ARGV.size != 3)
  puts "Usage: benchmark <filename> regex num_iterations"
  exit 1
end

def measure(data, pattern)
  begin
    count = 0

    pattern = Regex.new(pattern)
    elapsed = Benchmark.measure {
      count = data.scan(pattern).size
    }
    puts "#{elapsed.real * 1e3} - #{count}"
  rescue ex
    STDERR.puts ex.message
    exit(EXIT_FAILURE)
  end
end

data = File.read(ARGV[0])
pattern = ARGV[1]
num_iterations = ARGV[2].to_i(10)

(0...num_iterations).each do |i|
  measure(data, pattern)
end
