#!/usr/bin/perl

use English;
use Time::HiRes qw( gettimeofday tv_interval );

$haystack = "xxxxxxxx=xxxxxxx";
$pattern = m/x=x/;

$t0 = [gettimeofday];
if ($haystack =~ $pattern) {
  $elapsed = tv_interval ($t0);
  print "Matched\n";
  print "Time: " . ($elapsed) . "\n";
} else {
  print "Not Matched\n";
}