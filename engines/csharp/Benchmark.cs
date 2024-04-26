using System;
using System.IO;
using System.Text.RegularExpressions;
using System.Diagnostics;



class Benchmark
{
    public const Int32 EXIT_FAILURE = 1;

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
        try {
            Regex compiledPattern = new Regex(pattern);

            Stopwatch stopwatch = Stopwatch.StartNew();
            MatchCollection matches = compiledPattern.Matches(data);
            stopwatch.Stop();

            int count = matches.Count;
            Console.WriteLine(stopwatch.Elapsed.TotalMilliseconds.ToString("G", System.Globalization.CultureInfo.InvariantCulture) + " - " + count);
        } catch (Exception e) {
            Console.Error.WriteLine("compilation failed: " + e.Message);
            System.Environment.Exit(EXIT_FAILURE);
        }
    }
}
