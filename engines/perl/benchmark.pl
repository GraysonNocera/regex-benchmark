use Time::HiRes qw(gettimeofday);

sub measure {
    my ($data, $pattern) = @_;
    my $regex = qr/$pattern/;

    my $start = Time::HiRes::gettimeofday();

    my $count = () = $data =~ /$regex/g;

    my $elapsed = (Time::HiRes::gettimeofday() - $start) * 1e3;

    printf("%f - %d\n", $elapsed, $count);
}

if (@ARGV != 3) {
  die "Usage: ./benchmark.pl <filename> regex numIterations\n";
}

my ($filename) = @ARGV;

open my $fh, '<', $filename or die 'Could not open file.';
my $text;
read $fh, $data, -s $filename;
close $fh;

my $pattern = $ARGV[1];
my $numIterations = int($ARGV[2]);

for (my $i = 0; $i < $numIterations; $i++) {
  measure($data, $pattern);
}

