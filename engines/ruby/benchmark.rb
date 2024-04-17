require "benchmark"

if(ARGV.size <= 1)
  puts "Usage: ruby benchmark.rb <filename> regex1 regex2 ... regexN"
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

for i in 1...ARGV.size
  measure(data, ARGV[i])
end

# # Email
# measure(data, '[\w\.+-]+@[\w\.-]+\.[\w\.-]+')

# # URI
# measure(data, '[\w]+:\/\/[^\/\s?#]+[^\s?#]+(?:\?[^\s#]*)?(?:#[^\s]*)?')

# # IP
# measure(data, '(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9])')
