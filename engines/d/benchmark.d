import std.stdio;
import std.file;
import std.regex;
import std.datetime;
import std.datetime.stopwatch : StopWatch, AutoStart;
import core.stdc.stdlib;
import std.typecons : Flag, Yes, No;
import std.conv;

int EXIT_FAILURE = 1;

void measure(string data, string pattern) {
    int count = 0;

    try {
        auto r = regex(pattern);

        auto sw = StopWatch(AutoStart.yes);
        foreach (m; data.matchAll(r)) {
            count++;
        }
        sw.stop();

        double end = sw.peek().total!"nsecs" / 1e6;

        printf("%f - %d\n", end, count);
    }
    catch (Exception e) {
        stderr.writeln("compilation failed: %s", e.msg);
        exit(EXIT_FAILURE);
    }
}

void main(string [] args) {
    if(args.length != 4) {
        writeln("Usage: benchmark <filename> regex numIterations");
        exit(1);
    }

    string data = readText(args[1]);
    string pattern = args[2];
    int numIterations = std.conv.to!int(args[3]);

    for(int i = 0; i < numIterations; i++) {
        measure(data, pattern);
    }
}
