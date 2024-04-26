require "benchmark"

EXIT_FAILURE = 1

if(ARGV.size != 3)
  puts "Usage: ruby benchmark.rb <filename> regex numIterations"
  exit EXIT_FAILURE
end

def measure(data, pattern)
  begin
    count = 0
    regex = Regexp.compile(pattern)
  
    elapsed = Benchmark.measure {
      count = data.scan(regex).size
    }
  
    puts "#{elapsed.real * 1e3} - #{count}"
  rescue => error
    STDERR.puts "compilation error: #{error}\n"
    exit EXIT_FAILURE
  end
end

data = File.read(ARGV[0])
pattern = ARGV[1]
numIterations = Integer(ARGV[2])

for i in 0...numIterations
  measure(data, pattern)
end
