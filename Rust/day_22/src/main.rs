
use std::collections::HashMap;
use std::collections::HashSet;
#[derive(Debug, Copy, Clone, Eq, PartialEq, Hash)]
struct Point {
    x: i32,
    y: i32,
}

impl Point {
    fn new(x: i32, y: i32) -> Point {
        Point { x, y }
    }
}

#[derive(Debug, Copy, Clone, Eq, PartialEq)]
enum Dir {
    Right,
    Down,
    Left,
    Up,
}

struct Board {
    walls: HashSet<Point>,
    min_max_line: HashMap<i32, (i32, i32)>,
    min_max_row: HashMap<i32, (i32, i32)>,
    side_sz: i32,
}

fn do_turn(cur_dir: Dir, turn: &str) -> Dir {
    if turn.is_empty() || !turn.chars().all(|c| c == 'L' || c == 'R') {
        return cur_dir;
    }
    match cur_dir {
        Dir::Right => {
            if turn == "L" {
                Dir::Up
            } else {
                Dir::Down
            }
        }
        Dir::Down => {
            if turn == "L" {
                Dir::Right
            } else {
                Dir::Left
            }
        }
        Dir::Left => {
            if turn == "L" {
                Dir::Down
            } else {
                Dir::Up
            }
        }
        Dir::Up => {
            if turn == "L" {
                Dir::Left
            } else {
                Dir::Right
            }
        }
    }
}

fn add_to_min_max(min_max: &mut HashMap<i32, (i32, i32)>, entry: i32, index: i32) {
    if !min_max.contains_key(&index) {
        min_max.insert(index, (entry, entry));
    } else {
        let e = min_max[&index]; //[index][1] = entry
        min_max.insert(index, (e.0, entry));

    }
}

fn split_string(s: &str) -> Vec<String> {
    let mut result = vec![String::from(" ")];
    let mut current_token = String::new();
    for c in s.chars() {
        if c.is_numeric() {
            current_token.push(c);
        } else {
            result.push(current_token.clone());
            result.push(String::from(c));
            current_token.clear();
        }
    }
    result.push(current_token.clone());

    result
}

fn parse_input(lines: &str) -> (Board, Vec<String>) {
    let (grid, instructions) = lines.split_once("\n\n").unwrap();
    let mut walls = HashSet::new();
    let mut min_max_line = HashMap::new();
    let mut min_max_row = HashMap::new();
    for (y, line) in grid.split('\n').enumerate() {
        for (x, c) in line.chars().enumerate() {
            let p = Point {
                x: x as i32,
                y: y as i32,
            };
            if c == '#' {
                add_to_min_max(&mut min_max_line, x as i32, y as i32);
                add_to_min_max(&mut min_max_row, y as i32, x as i32);
                walls.insert(p);
            } else if c == '.' {
                add_to_min_max(&mut min_max_line, x as i32, y as i32);
                add_to_min_max(&mut min_max_row, y as i32, x as i32);
            }
        }
    }
    let instructions: Vec<String> = split_string(instructions.trim());
    let min_side = min_max_line
        .values()
        .min_by(|v, y| (v.1 - v.0).cmp(&(y.1 - y.0)))
        .unwrap();
    let side_sz = min_side.1 - min_side.0 + 1;
    (
        Board {
            walls,
            min_max_line,
            min_max_row,
            side_sz,
        },
        instructions,
    )
}

fn get_next_wrap(p: Point, direction: Dir, board: &Board) -> (Dir, Point) {
    if direction == Dir::Right {
        let mut x_new = p.x + 1;
        if x_new > board.min_max_line[&p.y].1 {
            x_new = board.min_max_line[&p.y].0;
        }
        return (direction, Point { x: x_new, y: p.y });
    }
    if direction == Dir::Down {
        let mut y_new = p.y + 1;
        if y_new > board.min_max_row[&p.x].1 {
            y_new = board.min_max_row[&p.x].0;
        }
        return (direction, Point { x: p.x, y: y_new });
    }
    if direction == Dir::Left {
        let mut x_new = p.x - 1;
        if x_new < board.min_max_line[&p.y].0 {
            x_new = board.min_max_line[&p.y].1;
        }
        return (direction, Point { x: x_new, y: p.y });
    }
    if direction == Dir::Up {
        let mut y_new = p.y - 1;
        if y_new < board.min_max_row[&p.x].0 {
            y_new = board.min_max_row[&p.x].1;
        }
        return (direction, Point { x: p.x, y: y_new });
    }
    unreachable!()
}

fn get_next_cube(p: Point, direction: Dir, board: &Board) -> (Dir, Point) {
    if direction == Dir::Right {
        let x_new = p.x + 1;
        if x_new > board.min_max_line[&p.y].1 {
            if p.y < board.side_sz {
                return (
                    Dir::Left,
                    Point {
                        x: 2 * board.side_sz - 1,
                        y: (3 * board.side_sz - 1) - p.y,
                    },
                );
            } else if p.y < 2 * board.side_sz {
                let direction = Dir::Up;
                return (
                    direction,
                    Point {
                        x: 2 * board.side_sz + (p.y - board.side_sz),
                        y: board.side_sz - 1,
                    },
                );
            } else if p.y < 3 * board.side_sz {
                let direction = Dir::Left;
                return (
                    direction,
                    Point {
                        x: 3 * board.side_sz - 1,
                        y: (3 * board.side_sz - 1) - p.y,
                    },
                );
            } else if p.y < 4 * board.side_sz {
                let direction = Dir::Up;
                return (
                    direction,
                    Point {
                        x: board.side_sz + p.y - (3 * board.side_sz),
                        y: (3 * board.side_sz - 1),
                    },
                );
            } else {
                println!("error");
            }
        }
        return (direction, Point { x: x_new, y: p.y });
    }
    if direction == Dir::Down {
        let y_new = p.y + 1;
        if y_new > board.min_max_row[&p.x].1 {
            if p.x < board.side_sz {
                return (
                    Dir::Down,
                    Point {
                        x: 2 * board.side_sz + p.x,
                        y: 0,
                    },
                );
            } else if p.x < 2 * board.side_sz {
                return (
                    Dir::Left,
                    Point {
                        x: board.side_sz - 1,
                        y: 3 * board.side_sz + p.x - board.side_sz,
                    },
                );
            } else if p.x < 3 * board.side_sz {
                return (
                    Dir::Left,
                    Point {
                        x: 2 * board.side_sz - 1,
                        y: board.side_sz + p.x - 2 * board.side_sz,
                    },
                );
            } else {
                println!("error");
            }
        }
        return (direction, Point { x: p.x, y: y_new });
    }
    if direction == Dir::Left {
        let x_new = p.x - 1;
        if x_new < board.min_max_line[&p.y].0 {
            if p.y < board.side_sz {
                return (
                    Dir::Right,
                    Point {
                        x: 0,
                        y: (3 * board.side_sz - 1) - p.y,
                    },
                );
            } else if p.y < 2 * board.side_sz {
                let direction = Dir::Down;
                return (
                    direction,
                    Point {
                        x: p.y - board.side_sz,
                        y: 2 * board.side_sz,
                    },
                );
            } else if p.y < 3 * board.side_sz {
                let direction = Dir::Right;
                return (
                    direction,
                    Point {
                        x: board.side_sz,
                        y: (3 * board.side_sz - 1) - p.y,
                    },
                );
            } else if p.y < 4 * board.side_sz {
                let direction = Dir::Down;
                return (
                    direction,
                    Point {
                        x: board.side_sz + p.y - (3 * board.side_sz),
                        y: 0,
                    },
                );
            } else {
                println!("error");
            }
        }
        return (direction, Point { x: x_new, y: p.y });
    }
    if direction == Dir::Up {
        let y_new = p.y - 1;
        if y_new < board.min_max_row[&p.x].0 {
            if p.x < board.side_sz {
                return (
                    Dir::Right,
                    Point {
                        x: board.side_sz,
                        y: board.side_sz + p.x,
                    },
                );
            } else if p.x < 2 * board.side_sz {
                return (
                    Dir::Right,
                    Point {
                        x: 0,
                        y: 3 * board.side_sz + p.x - board.side_sz,
                    },
                );
            } else if p.x < 3 * board.side_sz {
                return (
                    Dir::Up,
                    Point {
                        x: p.x - 2 * board.side_sz,
                        y: 4 * board.side_sz - 1,
                    },
                );
            } else {
                println!("error");
            }
        }
        return (direction, Point { x: p.x, y: y_new });
    }

    unreachable!()
}

fn solve(
    board: &Board,
    instructions: &Vec<String>,
    next_fun: &dyn Fn(Point, Dir, &Board) -> (Dir, Point),
) -> i32 {
    let mut cur = Point {
        y: 0,
        x: board.min_max_line[&0].0,
    };
    let mut direction = Dir::Right;
    for i in (0..instructions.len() - 1).step_by(2) {
        let (turn, length) = (
            instructions[i].as_str(),
            instructions[i + 1].parse::<i32>().unwrap(),
        );
        direction = do_turn(direction, turn);
        (cur, direction) = do_move(cur, direction, length, board, next_fun);
       // println!("{:?},{:?}", cur, direction);
    }
    1000 * (cur.y + 1) + 4 * (cur.x + 1) + direction as i32
}

fn do_move(
    mut cur: Point,
    mut direction: Dir,
    length: i32,
    board: &Board,
    next_fun: &dyn Fn(Point, Dir, &Board) -> (Dir, Point),
) -> (Point, Dir) {
    let mut next_pos = cur;
    let mut next_dir = direction;
    for _ in 0..length + 1 {
        cur = next_pos;
        direction = next_dir;
        let (new_dir, new_pos) = next_fun(cur, direction, board);
        next_dir = new_dir;
        next_pos = new_pos;
        if board.walls.contains(&next_pos) {
            break;
        }
    }
    (cur, direction)
}

fn part1(board: &Board, instructions: &Vec<String>) -> i32 {
    solve(board, instructions, &get_next_wrap)
}

fn part2(board: &Board, instructions: &Vec<String>) -> i32 {
    solve(board, instructions, &get_next_cube)
}


fn tests(board: &Board){
    let (direction, p )= get_next_cube(Point::new(149, 0), Dir::Right, board)  ;
    assert! (direction == Dir::Left && Point::new(99, 149) == p);
    let (direction, p )= get_next_cube(Point::new(149, 49), Dir::Right, board);
    assert! (direction == Dir::Left && Point::new(99, 100) == p);

    let (direction, p )= get_next_cube(Point::new(99, 50), Dir::Right, board);
    assert! (direction == Dir::Up && Point::new(100, 49) == p);
    let (direction, p )= get_next_cube(Point::new(99, 99), Dir::Right, board);
    assert! (direction == Dir::Up && Point::new(149, 49) == p);

    let (direction, p )= get_next_cube(Point::new(99, 100), Dir::Right, board);
    assert! (direction == Dir::Left && Point::new(149, 49) == p);
    let (direction, p )= get_next_cube(Point::new(99, 149), Dir::Right, board);
    assert! (direction == Dir::Left && Point::new(149, 0) == p);

    let (direction, p )= get_next_cube(Point::new(49, 150), Dir::Right, board);
    assert! (direction == Dir::Up && Point::new(50, 149) == p);
    let (direction, p )= get_next_cube(Point::new(49, 199), Dir::Right, board);
    assert! (direction == Dir::Up && Point::new(99, 149) == p);

    let (direction, p )= get_next_cube(Point::new(50, 0), Dir::Left, board);
    assert! (direction == Dir::Right && Point::new(0, 149) == p);
    let (direction, p )= get_next_cube(Point::new(50, 49), Dir::Left, board);
    assert! (direction == Dir::Right && Point::new(0, 100) == p);

    let (direction, p )= get_next_cube(Point::new(50, 50), Dir::Left, board);
    assert! (direction == Dir::Down && Point::new(0, 100) == p);
    let (direction, p )= get_next_cube(Point::new(50, 99), Dir::Left, board);
    assert! (direction == Dir::Down && Point::new(49, 100) == p);

    let (direction, p )= get_next_cube(Point::new(0, 100), Dir::Left, board);
    assert! (direction == Dir::Right && Point::new(50, 49) == p);
    let (direction, p )= get_next_cube(Point::new(0, 149), Dir::Left, board);
    assert! (direction == Dir::Right && Point::new(50, 0) == p);

    let (direction, p )= get_next_cube(Point::new(0, 150), Dir::Left, board);
    assert! (direction == Dir::Down && Point::new(50, 0) == p);
    let (direction, p )= get_next_cube(Point::new(0, 199), Dir::Left, board);
    assert! (direction == Dir::Down && Point::new(99, 0) == p);

    let (direction, p )= get_next_cube(Point::new(0, 100), Dir::Up, board);
    assert! (direction == Dir::Right && Point::new(50, 50) == p);
    let (direction, p )= get_next_cube(Point::new(49, 100), Dir::Up, board);
    assert! (direction == Dir::Right && Point::new(50, 99) == p);

    let (direction, p )= get_next_cube(Point::new(50, 0), Dir::Up, board);
    assert! (direction == Dir::Right && Point::new(0, 150) == p);
    let (direction, p )= get_next_cube(Point::new(99, 0), Dir::Up, board);
    assert! (direction == Dir::Right && Point::new(0, 199) == p);

    let (direction, p )= get_next_cube(Point::new(100, 0), Dir::Up, board);
    assert! (direction == Dir::Up && Point::new(0, 199) == p);
    let (direction, p )= get_next_cube(Point::new(149, 0), Dir::Up, board);
    assert! (direction == Dir::Up && Point::new(49, 199) == p);

    let (direction, p )= get_next_cube(Point::new(0, 199), Dir::Down, board);
    assert! (direction == Dir::Down && Point::new(100, 0) == p);
    let (direction, p )= get_next_cube(Point::new(49, 199), Dir::Down, board);
    assert! (direction == Dir::Down && Point::new(149, 0) == p);

    let (direction, p )= get_next_cube(Point::new(50, 149), Dir::Down, board);
    assert! (direction == Dir::Left && Point::new(49, 150) == p);
    let (direction, p )= get_next_cube(Point::new(99, 149), Dir::Down, board);
    assert! (direction == Dir::Left && Point::new(49, 199) == p);

    let (direction, p )= get_next_cube(Point::new(100, 49), Dir::Down, board);
    assert! (direction == Dir::Left && Point::new(99, 50) == p);
    let (direction, p )= get_next_cube(Point::new(149, 49), Dir::Down, board);
    assert! (direction == Dir::Left && Point::new(99, 99) == p);
}
fn main() {
    let input = include_str!("../../../inputs/input_22.txt");
    let (board, instructions) = parse_input(input);
    tests(&board);
    println!("Part 1: {}", part1(&board, &instructions));
    println!("Part 2: {}", part2(&board, &instructions));
}
