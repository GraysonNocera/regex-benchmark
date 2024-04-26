const fs = require('fs')

const EXIT_FAILURE = 1;

if (process.argv.length != 5) {
  console.log('Usage: node benchmark.js <filename> regex numIterations')
  process.exit(EXIT_FAILURE)
}

function measure(data, pattern) {

  try {
    const regex = new RegExp(pattern, 'g')
    const start = process.hrtime()
  
    const matches = data.match(regex)
    const count = matches?.length ?? 0
  
    const end = process.hrtime(start)
  
    console.log((end[0] * 1e9 + end[1]) / 1e6 + ' - ' + count)
  } catch (e) {
    console.error(`compilation failed: ${e}\n`)
    process.exit(EXIT_FAILURE)
  }
}

const data = fs.readFileSync(process.argv[2], 'utf8')
const pattern = process.argv[3]
const numIterations = parseInt(process.argv[4])

for (var i = 0; i < numIterations; i++) {
  measure(data, pattern)
}