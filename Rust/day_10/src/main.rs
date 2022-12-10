use std::collections::HashSet;

fn solve(lines: &str) -> (i32, String) {
    let mut cycl_cnt = 1;
    let mut signal_strength = 0;
    let mut register: i32 = 1;
    let mut pos = 0;
    let measure_points: HashSet<i32> = (20..=220).step_by(40).collect();
    let mut display = String::from("\n");
    for line in lines.lines() {
        let mut tokenz = line.splitn(2, ' ');
        add_pixel(&mut display, &mut pos, register);
        let instruction = tokenz.next().unwrap();
        if instruction == "noop" {
            cycl_cnt += 1;
        }
        if instruction == "addx" {
            add_pixel(&mut display, &mut pos, register);
            signal_strength =
                cond_inc_signal_strength(&measure_points, cycl_cnt + 1, register, signal_strength);
            cycl_cnt += 2;
            register += tokenz.next().unwrap().parse::<i32>().unwrap();
        }
        signal_strength =
            cond_inc_signal_strength(&measure_points, cycl_cnt, register, signal_strength);
    }
    (signal_strength, display)
}

fn cond_inc_signal_strength(
    measure_points: &HashSet<i32>,
    cycl_cnt: i32,
    register: i32,
    signal_strength: i32,
) -> i32 {
    if measure_points.contains(&cycl_cnt) {
        return signal_strength + cycl_cnt * register;
    }
    signal_strength
}

fn add_pixel(display: &mut String, pos: &mut i32, register: i32) {
    if (register - 1..=register + 1).contains(pos) {
        *display += "#";
    } else {
        *display += ".";
    }
    if *pos == 39 {
        *display += "\n";
        *pos = 0;
        return;
    }
    *pos += 1;
}

fn main() {
    let input = include_str!("../../../inputs/input_10.txt");
    let (part_1, part_2) = solve(input);
    println!("Part 1: {}", part_1);
    println!("Part 2: {}", part_2);
}
