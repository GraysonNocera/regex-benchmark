import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public final class Benchmark {
    public static void main(String... args) throws IOException {
        if (args.length != 3) {
            System.out.println("Usage: java Benchmark <filename> regex numIterations");
            System.exit(1);
        }

        final String data = Files.readString(Paths.get(args[0]));
        final String pattern = args[1];
        final int numIterations = Integer.parseInt(args[2]);

        for (int i = 0; i < numIterations; ++i) {
            measure(data, pattern);
        }
    }

    
    private static void measure(String data, String pattern) {
        final Pattern compiledPattern = Pattern.compile(pattern);

        long startTime = System.nanoTime();
        final Matcher matcher = compiledPattern.matcher(data);
        int count = 0;
        while (matcher.find()) {
            ++count;
        }

        long elapsed = System.nanoTime() - startTime;

        System.out.println(elapsed / 1e6 + " - " + count);
    }
}
