<?php

$EXIT_FAILURE = 1;

set_error_handler(function($errno, $errstr, $errfile, $errline) {
    // error was suppressed with the @-operator
    if (0 === error_reporting()) {
        return false;
    }
    
    throw new ErrorException($errstr, 0, $errno, $errfile, $errline);
});


if (count($argv) != 4) {
    echo 'Usage: php benchmark.php <filename> regex num_iterations' . PHP_EOL;
    die($EXIT_FAILURE);
}

$data  = file_get_contents($argv[1]);
$pattern = $argv[2];
// Add engine delimiter if not present
if ($pattern[0] !== '/') {
    $pattern = '/' . $pattern . '/';
}

$num_iterations = intval($argv[3]);

for ($i = 0; $i < $num_iterations; $i++) {
    measure($data, $pattern);
}

function measure($data, $pattern) {
    try {
        $compiled_pattern = $pattern;

        $startTime = microtime(true);
        $count = preg_match_all($compiled_pattern, $data, $matches);
        $elapsed = (microtime(true) - $startTime) * 1e3;

        echo $elapsed . ' - ' . $count . PHP_EOL;
    } catch (Exception $e) {
        echo 'compilation failure: ' .  $e->getMessage() . PHP_EOL;
        die($EXIT_FAILURE);
    }
}
