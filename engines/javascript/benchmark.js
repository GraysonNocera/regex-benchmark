const fs = require('fs')

if (process.argv.length != 5) {
  console.log('Usage: node benchmark.js <filename> regex numIterations')
  process.exit(1)
}

function measure(data, pattern) {

  const regex = new RegExp(pattern, 'g')
  const start = process.hrtime()

  const matches = data.match(regex)
  const count = matches.length

  const end = process.hrtime(start)

  console.log((end[0] * 1e9 + end[1]) / 1e6 + ' - ' + count)
}

const data = fs.readFileSync(process.argv[2], 'utf8')
const pattern = process.argv[3]
const numIterations = parseInt(process.argv[4])

for (var i = 0; i < numIterations; i++) {
  measure(data, pattern)
}