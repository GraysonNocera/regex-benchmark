require "benchmark"

if (ARGV.size != 3)
  puts "Usage: benchmark <filename> regex num_iterations"
  exit 1
end

def measure(data, pattern)
  count = 0

  pattern = Regex.new(pattern)
  elapsed = Benchmark.measure {
    count = data.scan(pattern).size
  }

  puts "#{elapsed.real * 1e3} - #{count}"
end

data = File.read(ARGV[0])
pattern = ARGV[1]
num_iterations = ARGV[2].to_i(10)

(0...num_iterations).each do |i|
  measure(data, pattern)
end
