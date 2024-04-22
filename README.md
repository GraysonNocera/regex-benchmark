# regex-benchmark


## Run
```
docker build -t regex_benchmark .
docker run -it -v $(pwd):/var/regex --name "regex_benchmark_server"  -p 8000:8000 regex_benchmark
```

## Open the UI

After running the docker go to [http://localhost:8000](http://localhost:8000)

![UI](ui.png)

## Format of output of runner programs

"[milliseconds_of_run] - [count of matches]"