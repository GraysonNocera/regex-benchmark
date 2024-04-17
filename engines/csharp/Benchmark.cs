using System;
using System.IO;
using System.Text.RegularExpressions;
using System.Diagnostics;

class Benchmark
{
    static void Main(string[] args)
    {
        if (args.Length != 3)
        {
            Console.WriteLine("Usage: benchmark <filename> regex num_iterations");
            Environment.Exit(1);
        }

        StreamReader reader = new System.IO.StreamReader(args[0]);
        string data = reader.ReadToEnd();
        string pattern = args[1];
        int numIterations = Int32.Parse(args[2]);
        Regex.CacheSize = 0;

        for (int i = 0; i < numIterations; i++)
        {
            Benchmark.Measure(data, pattern);
        }
    }

    static void Measure(string data, string pattern)
    {
        Stopwatch stopwatch = Stopwatch.StartNew();

        Regex compiledPattern = new Regex(pattern);
        MatchCollection matches = compiledPattern.Matches(data);
        int count = matches.Count;

        stopwatch.Stop();

        Console.WriteLine(stopwatch.Elapsed.TotalMilliseconds.ToString("G", System.Globalization.CultureInfo.InvariantCulture) + " - " + count);
    }
}
