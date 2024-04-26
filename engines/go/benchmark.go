package main

import (
    "bytes"
    "fmt"
    "log"
    "os"
    "regexp"
    "time"
    "strconv"
)

var EXIT_FAILURE int = 1

func measure(data string, pattern string) {

    r, err := regexp.Compile(pattern)
    if err != nil {
        log.Fatal(err)
        os.Exit(EXIT_FAILURE)
    }

    start := time.Now()

    matches := r.FindAllString(data, -1)
    count := len(matches)

    elapsed := time.Since(start)

    fmt.Printf("%f - %v\n", float64(elapsed) / float64(time.Millisecond), count)
}

func main() {
    if len(os.Args) != 4 {
        fmt.Println("Usage: benchmark <filename> regex numIterations")
        os.Exit(1)
    }

    filerc, err := os.Open(os.Args[1])
    if err != nil {
        log.Fatal(err)
    }
    defer filerc.Close()

    buf := new(bytes.Buffer)
    buf.ReadFrom(filerc)
    data := buf.String()

    pattern := os.Args[2]
    numIterations, err := strconv.Atoi(os.Args[3])

    for i := 0; i < numIterations; i++ {
        measure(data, pattern)
    }
}
