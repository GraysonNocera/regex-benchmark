import java.io.File
import java.io.InputStream
import kotlin.text.Regex
import kotlin.system.exitProcess
import kotlin.system.measureNanoTime

fun main(args: Array<String>) {
    if (args.count() <= 1) {
        println("Usage: kotlin benchmark.jar <filename> regex1 regex2 ... regexN");
        exitProcess(1);
    }

    val inputStream: InputStream = File(args[0]).inputStream()
    val data = inputStream.bufferedReader().use { it.readText() }


    for (i in 1 until args.count()) {
        match(data, args[i])
    }
    // Email
    // match(data, "[\\w\\.+-]+@[\\w\\.-]+\\.[\\w\\.-]+")

    // URI
    // match(data, "[\\w]+://[^/\\s?#]+[^\\s?#]+(?:\\?[^\\s#]*)?(?:#[^\\s]*)?")

    // IP
    // match(data, "(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9])\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9])")
}

fun match(data: String, pattern: String) {

    val regex = Regex(pattern)
    
    val start = System.nanoTime()
    var results = regex.findAll(data)
    val count = results.count()

    val elapsed = System.nanoTime() - start
    
    println((elapsed / 1e6).toString() + " - " + count)
}
