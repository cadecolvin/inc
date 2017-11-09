#include <stdarg.h>
#include <stdio.h>

#define result_file "test_results.txt"

#define print_pass()                                                        \
do {                                                                        \
    FILE *f = fopen(result_file, "a");                                      \
    fprintf(f, "PASS:%s:%s\n", __FILE__, __func__);                         \
    fclose(f);                                                              \
} while(0)

#define print_fail(format, ...)                                             \
do {                                                                        \
    FILE *f = fopen(result_file, "a");                                      \
    fprintf(f, "FAIL:%s:%s:", __FILE__, __func__);                          \
    fprintf(f, format, __VA_ARGS__);                                        \
    fprintf(f, "\n");                                                       \
    fclose(f);                                                              \
} while(0)

#define assert_eq_int(expected, actual)                                     \
do {                                                                        \
    if((expected) == (actual))                                              \
        print_pass();                                                       \
    else                                                                    \
        print_fail("Expected %d; Actual %d", expected, actual);             \
} while(0)
