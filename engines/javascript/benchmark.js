const fs = require('fs')

if (process.argv.length < 3) {
  console.log('Usage: node benchmark.js <filename> regex1 regex2 ...')
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

// TODO: test this 
for (const regex of process.argv.slice(3)) {
  measure(data, regex)
}