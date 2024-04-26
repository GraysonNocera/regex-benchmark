#include <chrono>
#include <fstream>
#include <iostream>

#ifdef USE_BOOST
  // This errors for something like [\w-\.] because of ranges of character classes
  // the "-" must be escaped
  #include <boost/regex.hpp>
  #define REGEX_NAMESPACE boost
#elif USE_SRELL
  #include <srell.hpp>
  // This errors for something like [\w-\.] because of ranges of character classes
  // the "-" must be escaped
  // srell throws a bunch of nondescript errors that are hard to debug
  #define REGEX_NAMESPACE srell
#else
  #include <regex>
  #define REGEX_NAMESPACE std
#endif

int measure(const std::string& data, const std::string& pattern) {
  using clock = std::chrono::high_resolution_clock;
  REGEX_NAMESPACE::regex re;

  try
  {
    re = REGEX_NAMESPACE::regex{pattern};
  }
  catch (const REGEX_NAMESPACE::regex_error& e)
  {
    std::cerr << "compilation error " << e.code() << ": " << e.what() << '\n';
    return EXIT_FAILURE;
  }

  unsigned count = 0;

  const auto start = clock::now();
  for (REGEX_NAMESPACE::sregex_token_iterator it{data.cbegin(), data.cend(), re}, end{}; it != end; ++it)
    count++;

  const auto end = clock::now();
  const double elapsed = std::chrono::duration_cast<std::chrono::nanoseconds>(end - start).count() * 1e-6;
  std::cout << elapsed << " - " << count << "\n";

  return EXIT_SUCCESS;
}

int main(int argc, char** argv) {
  if (argc != 4) {
    std::cerr << "Usage: benchmark <filename> regex num_iterations\n";
    return EXIT_FAILURE;
  }

  std::ifstream file{argv[1]};
  if (!file) {
    std::cerr << "unable to open " << argv[1] << "\n";
    return EXIT_FAILURE;
  }

  const std::string data{std::istreambuf_iterator<char>{file}, std::istreambuf_iterator<char>{}};
  char * pattern = argv[2];
  int num_iterations = std::stoi(argv[3]);

  for (int i = 0; i < num_iterations; i++) {
    if (measure(data, pattern) == EXIT_FAILURE) {
      return EXIT_FAILURE;
    }
  }

  return EXIT_SUCCESS;
}
