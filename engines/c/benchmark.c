#include <stdio.h>
#include <string.h>
#include <sys/time.h>

// This errors for something like [\w-\.] because of ranges of character classes
// the "-" must be escaped

#if __has_include(<time.h>)
#include <time.h>
#endif

#define PCRE2_CODE_UNIT_WIDTH 8
#include <pcre2.h>

#define OK_COMPILE_CODE 100

void print_error(int errorcode, int erroroffset) {
  int error_length = 5000; // just a guess
  char * error_buffer = malloc(sizeof(char) * error_length);
  int retval =  pcre2_get_error_message(errorcode, (PCRE2_UCHAR *) error_buffer, (PCRE2_SIZE) error_length);
  fprintf(stderr, "Error at position %d: %s\n", erroroffset, error_buffer);
  free(error_buffer);
  return;
}

char *read_file(char *filename)
{
  char *data;
  long length = 0;

  FILE *fh = fopen(filename, "rb");

  fseek(fh, 0, SEEK_END);
  length = ftell(fh);
  fseek(fh, 0, SEEK_SET);

  data = malloc(length);

  size_t result = fread(data, length, 1, fh);
  if (result != 1)
  {
    fputs("err", stderr);
    exit(1);
  }
  fclose(fh);

  return data;
}

int measure(char *data, char *pattern)
{
  int count = 0;
  double elapsed;
  struct timespec start, end;
  pcre2_code *re;

  int errorcode;
  PCRE2_SIZE erroroffset;

  pcre2_match_data *match_data;
  PCRE2_SIZE offset = 0;
  PCRE2_SIZE *ovector;

  int string_length;
  int pattern_length;

  pattern_length = strlen(pattern);
  re = pcre2_compile((PCRE2_SPTR)pattern, pattern_length, 0, &errorcode, &erroroffset, NULL);
  
  if (errorcode != OK_COMPILE_CODE) {
    print_error(errorcode, erroroffset);
    return 0;
  }

  // This is just for allocating memory, so it should not be considered part of the timing
  match_data = pcre2_match_data_create_from_pattern(re, NULL);
  string_length = strlen(data);

  clock_gettime(CLOCK_MONOTONIC, &start);

  // Reference this page (https://www.pcre.org/current/doc/html/pcre2demo.html) toward the 
  // bottom, there is an example of matching multiple times in the same string
  // This version is prone to errors if something like an empty match occurs. Ideally,
  // we would fix this, but for now it should work
  while (pcre2_match(re, (PCRE2_SPTR8)data, string_length, offset, 0, match_data, NULL) > 0)
  {
    count++;

    ovector = pcre2_get_ovector_pointer(match_data);
    offset = ovector[1];
  }
  clock_gettime(CLOCK_MONOTONIC, &end);
  elapsed = ((end.tv_sec - start.tv_sec) * 1e9 + end.tv_nsec - start.tv_nsec) / 1e6;

  printf("%f - %d\n", elapsed, count);

  pcre2_match_data_free(match_data);
  pcre2_code_free(re);

  return 1;
}

int main(int argc, char **argv)
{
  if (argc != 4)
  {
    printf("Usage: benchmark <filename> regex num_iterations\n");
    exit(1);
  }

  char *data = read_file(argv[1]);
  char *pattern = argv[2];
  int num_iterations = strtol(argv[3], NULL, 10);

  for (int i = 0; i < num_iterations; i++)
  {
    if (!measure(data, pattern)) {
      return EXIT_FAILURE;
    }
  }

  free(data);

  return EXIT_SUCCESS;
}
