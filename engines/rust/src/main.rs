use std::time::Instant;

use regex::bytes::RegexBuilder;

const EXIT_FAILURE: i32 = 1;

fn measure(data: &str, pattern: &str) -> Result<(), Box<dyn std::error::Error + Send + Sync>> {
    let regex = RegexBuilder::new(pattern).build().unwrap();

    let start = Instant::now();
    let count = regex.find_iter(data.as_bytes()).count();
    let elapsed = Instant::now().duration_since(start);

    println!("{} - {}", elapsed.as_secs_f64() * 1e3, count);
    Ok(())
}

fn main() -> Result<(), Box<dyn std::error::Error + Send + Sync>> {
    let path = match std::env::args_os().nth(1) {
        None => return Err(From::from("Usage: benchmark <filename> regex num_iterations")),
        Some(path) => path,
    };

    let args: Vec<String> = std::env::args().collect();
    if args.len() != 4 {
        return Err(From::from("Usage: benchmark <filename> regex num_iterations"));
    }

    let data = std::fs::read_to_string(path)?;
    let pattern = &args[2];
    let num_iterations = args[3].parse::<i32>().unwrap();

    for _i in 0..num_iterations {
        let _result = match measure(&data, &pattern) {
            Ok(()) => {}
            Err(error) => {
                eprintln!("compilation error: {}", error);
                std::process::exit(EXIT_FAILURE);
            }
        };
    }

    Ok(())
}
