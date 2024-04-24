import 'dart:io';

const EXIT_FAILURE = 1;

main(List<String> arguments) {
  if (arguments.length != 3) {
    print('Usage: dart bencharmark.dart <filename> regex numIterations');
    exit(1);
  }

  var numIterations = int.parse(arguments[2]);
  var pattern = arguments[1];
  new File(arguments[0])
    .readAsString()
    .then((String data) {
      for (var i = 0; i < numIterations; i++) {
        measure(data, pattern);
      }
    });
}

measure(data, pattern){
  try {
    RegExp exp = new RegExp(pattern);

    var stopwatch = new Stopwatch()..start();
    Iterable<Match> matches = exp.allMatches(data);
    var count = matches.length;

    stopwatch.stop();

    print('${stopwatch.elapsedMicroseconds / 1e3} - ${count}');
  } on Exception catch (e) {
    stderr.write('compilation failed: $e\n');
    exit(EXIT_FAILURE);
  }
}
