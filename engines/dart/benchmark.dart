import 'dart:io';

main(List<String> arguments) {
  if (arguments.length <= 1) {
    print('Usage: dart bencharmark.dart <filename> regex1 regex2 ... regexN');
    exit(1);
  }

  new File(arguments[0])
    .readAsString()
    .then((String data) {
      
      for (var i = 1; i < arguments.length; i++) {
        measure(data, arguments[i]);
      }
      // // Email
      // measure(data, r"[\w.+-]+@[\w.-]+\.[\w.-]+");

      // // URI
      // measure(data, r"[\w]+:\/\/[^\/\s?#]+[^\s?#]+(?:\?[^\s#]*)?(?:#[^\s]*)?");

      // // IP
      // measure(data, r"(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9])");
    });
}

measure(data, pattern){
  RegExp exp = new RegExp(pattern);

  var stopwatch = new Stopwatch()..start();
  Iterable<Match> matches = exp.allMatches(data);
  var count = matches.length;

  stopwatch.stop();

  print('${stopwatch.elapsedMicroseconds / 1e3} ${count}');
}
