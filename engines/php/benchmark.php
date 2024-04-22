<?php

if (count($argv) == 2) {
    echo 'Usage: php benchmark.php <filename> regex1 regex2 regex3 ...';
    die(1);
}

$data  = file_get_contents($argv[1]);

for ($i = 2; $i < count($argv); $i++) {
    measure($data, $argv[$i]);
}

// // Email
// measure($data, '/[\w\.+-]+@[\w\.-]+\.[\w\.-]+/');

// // URI
// measure($data, '/[\w]+:\/\/[^\/\s?#]+[^\s?#]+(?:\?[^\s#]*)?(?:#[^\s]*)?/');

// // IP
// measure($data, '/(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9])/');

function measure($data, $pattern) {
    // Add engine delimiter if not present
    if ($pattern[0] !== '/') {
        $pattern = '/' . $pattern . '/';
    }

    $startTime = microtime(true);

    $count = preg_match_all($pattern, $data, $matches);

    $elapsed = (microtime(true) - $startTime) * 1e3;

    echo $elapsed . ' - ' . $count . PHP_EOL;
}
