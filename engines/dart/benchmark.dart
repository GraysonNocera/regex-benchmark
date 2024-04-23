import 'dart:io';

main(List<String> arguments) {
  if (arguments.length != 3) {
    print('Usage: dart bencharmark.dart <filename> regex numIterations');
    exit(1);
  }

  new File(arguments[0])
    .readAsString()
    .then((String data) {
      for (var i = 1; i < arguments.length; i++) {
        measure(data, arguments[i]);
      }
    });
}

measure(data, pattern){
  RegExp exp = new RegExp(pattern);

  var stopwatch = new Stopwatch()..start();
  Iterable<Match> matches = exp.allMatches(data);
  var count = matches.length;

  stopwatch.stop();

  print('${stopwatch.elapsedMicroseconds / 1e3} - ${count}');
}
