import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public final class Benchmark {
    public static int EXIT_FAILURE = 1;

    public static void main(String... args) throws IOException {
        if (args.length != 3) {
            System.out.println("Usage: java Benchmark <filename> regex numIterations");
            System.exit(EXIT_FAILURE);
        }

        final String data = Files.readString(Paths.get(args[0]));
        final String pattern = args[1];
        final int numIterations = Integer.parseInt(args[2]);

        for (int i = 0; i < numIterations; ++i) {
            measure(data, pattern);
        }
    }

    
    private static void measure(String data, String pattern) {

        try {
            final Pattern compiledPattern = Pattern.compile(pattern);
            long startTime = System.nanoTime();
            final Matcher matcher = compiledPattern.matcher(data);
            int count = 0;
            while (matcher.find()) {
                ++count;
            }

            long elapsed = System.nanoTime() - startTime;

            System.out.println(elapsed / 1e6 + " - " + count);
        } catch (Exception e) {
            System.err.println("compilation error: " + e);
            System.exit(EXIT_FAILURE);
        }
    }
}
