#!/usr/bin/env python3
from datetime import date
from enum import Enum
from pathlib import Path

from requests import get


class Language(str, Enum):
    Python = "Python"
    Haskell = "Haskell"
    Rust = "Rust"
    Cargo = "Cargo"


extension = {Language.Python: "py", Language.Haskell: "hs", Language.Rust: "rs", Language.Cargo: "toml"}

cookie = open(".cookie", 'r').readline().strip()
cookies = {'session': cookie}
year = 2022


def python_stub(day: int) -> str:
    return f"""from aoc import get_lines
from pathlib import Path


def parse_input(lines):
    return lines


def part_1(lines):
    pass


def part_2(lines):
    pass


def main():
    lines = get_lines("input_{day:02d}.txt")
    lines = parse_input(lines)
    print("Part 1:", part_1(lines))
    print("Part 2:", part_2(lines))


if __name__ == '__main__':
    main()
"""


def rust_stub(day: int) -> str:
    return f"""fn part1(input: &str) -> &str {{
    input
}}

fn part2(input: &str) -> &str {{
    input
}}

fn main() {{
    let input = include_str!("../../../inputs/input_{day:02d}.txt");
    println!("Part 1: {{}}", part1(&input));
    println!("Part 2: {{}}", part2(&input));
}}

"""


def cargo_stub(day):
    return f"""[package]
name = "day_{day:02d}"
version = "0.1.0"
edition = "2021"
authors = ["weichslgartner <weichslgartner@gmail.com>"]

# See more keys and their definitions at https://doc.rust-lang.org/cargo/reference/manifest.html

[dependencies]

"""


def haskell_stub(day: int) -> str:
    return f"""
main = do  
    contents <- readFile "../../inputs/input_{day:02d}.txt"
    print . map readInt . words $ contents
readInt :: String -> Int
readInt = read
    """


stubs = {
    Language.Python: python_stub,
    Language.Rust: rust_stub,
    Language.Cargo: cargo_stub,
    Language.Haskell: haskell_stub
}


def get_input(day: int):
    input_file = Path("inputs") / f"input_{day:02d}.txt"
    input_file.parent.mkdir(parents=True, exist_ok=True)
    if input_file.exists():
        return
    print(f"Fetching day {day}")
    raw_input = get(f"https://adventofcode.com/{year}/day/{day}/input", cookies=cookies)
    with input_file.open('w') as f:
        f.writelines(raw_input.content.decode('utf-8'))


def generate_stub(day: int, lang: Language) -> None:
    source_file = generate_source_path(day, lang)
    source_file.parent.mkdir(parents=True, exist_ok=True)
    if source_file.exists():
        return
    print(f"Creating stub day {day} for {lang.name}")
    with source_file.open('w') as f:
        f.write(stubs[lang](day))


def generate_source_path(day: int, lang: Language) -> Path:
    if lang == Language.Rust:
        return Path(f"{lang.name}") / f"day_{day:02d}" / "src" / f"main.{extension[lang]}"
    if lang == Language.Cargo:
        return Path(f"{Language.Rust.name}") / f"day_{day:02d}" / f"Cargo.{extension[lang]}"
    return Path(f"{lang.name}") / f"day_{day:02d}.{extension[lang]}"


def main():
    today = date.today()
    print("Today is:", today)
    for day in range(1, 26):
        if today.year == year and (today.day < day or today.month != 12):
            break
        get_input(day)
        generate_stub(day, lang=Language.Python)
        generate_stub(day, lang=Language.Rust)
        generate_stub(day, lang=Language.Cargo)
    print("Done")


if __name__ == '__main__':
    main()
