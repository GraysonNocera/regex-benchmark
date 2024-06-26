import java.io.File
import java.io.InputStream
import kotlin.text.Regex
import kotlin.system.exitProcess
import kotlin.system.measureNanoTime

val EXIT_FAILURE = 1

fun main(args: Array<String>) {
    if (args.count() != 3) {
        println("Usage: kotlin benchmark.jar <filename> regex numIterations");
        exitProcess(EXIT_FAILURE);
    }

    val inputStream: InputStream = File(args[0]).inputStream()
    val data = inputStream.bufferedReader().use { it.readText() }
    val pattern = args[1];
    val numIterations = args[2].toInt();

    for (i in 0 until numIterations) {
        match(data, pattern)
    }
}

fun match(data: String, pattern: String) {

    try {
        val regex = Regex(pattern)
        
        val start = System.nanoTime()
        var results = regex.findAll(data)
        val count = results.count()

        val elapsed = System.nanoTime() - start
        
        println((elapsed / 1e6).toString() + " - " + count)
    } catch (e: Exception) {
        System.err.println("compilation failed: " + e)
        exitProcess(EXIT_FAILURE)
    }
}
