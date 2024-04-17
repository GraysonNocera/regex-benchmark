require "benchmark"

if(ARGV.size != 3)
  puts "Usage: ruby benchmark.rb <filename> regex numIterations"
  exit 1
end

def measure(data, pattern)
  count = 0
  regex = Regexp.compile(pattern)

  elapsed = Benchmark.measure {
    count = data.scan(regex).size
  }

  puts "#{elapsed.real * 1e3} - #{count}"
end

data = File.read(ARGV[0])
pattern = ARGV[1]
numIterations = Integer(ARGV[2])

for i in 0...numIterations
  measure(data, pattern)
end
