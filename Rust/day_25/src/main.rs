trait Snafu {
    fn to_snafu(&self) -> String;
}

impl Snafu for i64 {
    fn to_snafu(&self) -> String {
        let mut val = *self;
        let mut result = vec![];
        while val != 0 {
            let remainder = val % 5;
            val /= 5;
            if remainder <= 2 {
                result.push(remainder.to_string());
            } else if remainder == 3 {
                result.push('='.to_string());
                val += 1;
            } else if remainder == 4 {
                result.push('-'.to_string());
                val += 1;
            }
        }
        result.into_iter().rev().collect()
    }
}


fn to_decimal(val: &str, len: usize) -> i64 {
    val.chars()
        .enumerate()
        .map(|(i, c)| match c {
            '=' => (i, -2),
            '-' => (i, -1),
            _ => (i, c.to_digit(10).unwrap() as i64),
        })
        .map(|(i, val)| 5_i64.pow((len - i - 1) as u32) * val)
        .sum()
}

fn part1(input: &str) -> String {
    input
        .lines()
        .map(|line| to_decimal(line, line.len()))
        .sum::<i64>()
        .to_snafu()
}

fn main() {
    let input = include_str!("../../../inputs/input_25.txt");
    println!("Part 1: {}", part1(input));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_to_decimal() {
        let s = "1=-0-2";
        assert_eq!(to_decimal(s, s.len()), 1747 );
    }

    #[test]
    fn test_to_snafu() {
        let s = 1747;
        assert_eq!(s.to_snafu(), "1=-0-2" );
    }

}