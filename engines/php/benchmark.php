<?php

if (count($argv) != 4) {
    echo 'Usage: php benchmark.php <filename> regex num_iterations';
    die(1);
}

$data  = file_get_contents($argv[1]);
$pattern = $argv[2];
$num_iterations = intval($argv[3]);

for ($i = 0; $i < num_iterations; $i++) {
    measure($data, $pattern);
}

function measure($data, $pattern) {
    $compiled_pattern = /$pattern/;

    $startTime = microtime(true);
    $count = preg_match_all($compiled_pattern, $data, $matches);
    $elapsed = (microtime(true) - $startTime) * 1e3;

    echo $elapsed . ' - ' . $count . PHP_EOL;
}
