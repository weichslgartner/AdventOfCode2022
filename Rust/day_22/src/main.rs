use std::collections::hash_map::Entry::Vacant;
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
    RIGHT,
    DOWN,
    LEFT,
    UP,
}

struct Board {
    walls: HashSet<Point>,
    min_max_line: HashMap<i32, (i32, i32)>,
    min_max_row: HashMap<i32, (i32, i32)>,
    width: i32,
    height: i32,
    side_sz: i32,
}

fn do_turn(cur_dir: Dir, turn: &str) -> Dir {
    if turn.is_empty() || !turn.chars().all(|c| c == 'L' || c == 'R') {
        return cur_dir;
    }
    match cur_dir {
        Dir::RIGHT => {
            if turn == "L" {
                Dir::UP
            } else {
                Dir::DOWN
            }
        }
        Dir::DOWN => {
            if turn == "L" {
                Dir::RIGHT
            } else {
                Dir::LEFT
            }
        }
        Dir::LEFT => {
            if turn == "L" {
                Dir::DOWN
            } else {
                Dir::UP
            }
        }
        Dir::UP => {
            if turn == "L" {
                Dir::LEFT
            } else {
                Dir::RIGHT
            }
        }
    }
}

fn add_to_min_max(min_max: &mut HashMap<i32, (i32, i32)>, key: i32, value: i32) {
    if let Vacant(e) = min_max.entry(key) {
        e.insert((value, value));
        return;
    }
    let (min, max) = min_max[&key];
    min_max.insert(key, (min.min(value), max.max(value)));
}

fn parse_input(lines: &str) -> (Board, Vec<String>) {
    let (grid, instructions) = lines.split_once("\n\n").unwrap();
    let mut width = 0;
    let mut height = 0;
    let mut walls = HashSet::new();
    let mut min_max_line = HashMap::new();
    let mut min_max_row = HashMap::new();

    for (y, line) in grid.split('\n').enumerate() {
        height = height.max(y as i32);
        for (x, c) in line.chars().enumerate() {
            width = width.max(x as i32);
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
    let instructions: Vec<String> = instructions
        .split(|c: char| !c.is_numeric())
        .filter(|s| !s.is_empty())
        .map(String::from)
        .collect();
    width += 1;
    height += 1;
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
            width,
            height,
            side_sz,
        },
        instructions,
    )
}

fn get_next_wrap(p: Point, direction: Dir, board: &Board) -> (Dir, Point) {
    if direction == Dir::RIGHT {
        let mut x_new = p.x + 1;
        if x_new > board.min_max_line[&p.y].1 {
            x_new = board.min_max_line[&p.y].0;
        }
        return (direction, Point { x: x_new, y: p.y });
    }
    if direction == Dir::DOWN {
        let mut y_new = p.y + 1;
        if y_new > board.min_max_row[&p.x].1 {
            y_new = board.min_max_row[&p.x].0;
        }
        return (direction, Point { x: p.x, y: y_new });
    }
    if direction == Dir::LEFT {
        let mut x_new = p.x - 1;
        if x_new < board.min_max_line[&p.y].0 {
            x_new = board.min_max_line[&p.y].1;
        }
        return (direction, Point { x: x_new, y: p.y });
    }
    if direction == Dir::UP {
        let mut y_new = p.y - 1;
        if y_new < board.min_max_row[&p.x].0 {
            y_new = board.min_max_row[&p.x].1;
        }
        return (direction, Point { x: p.x, y: y_new });
    }
    unreachable!()
}

fn get_next_cube(p: Point, direction: Dir, board: &Board) -> (Dir, Point) {
    if direction == Dir::RIGHT {
        let mut x_new = p.x + 1;
        if x_new > board.min_max_line[&p.y].1 {
            if p.y < board.side_sz {
                return (
                    Dir::LEFT,
                    Point {
                        x: 2 * board.side_sz - 1,
                        y: (3 * board.side_sz - 1) - p.y,
                    },
                );
            } else if p.y < 2 * board.side_sz {
                let mut direction = Dir::UP;
                return (
                    direction,
                    Point {
                        x: 2 * board.side_sz + (p.y - board.side_sz),
                        y: board.side_sz - 1,
                    },
                );
            } else if p.y < 3 * board.side_sz {
                let mut direction = Dir::LEFT;
                return (
                    direction,
                    Point {
                        x: 3 * board.side_sz - 1,
                        y: (3 * board.side_sz - 1) - p.y,
                    },
                );
            } else if p.y < 4 * board.side_sz {
                let mut direction = Dir::UP;
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
    if direction == Dir::DOWN {
        let mut y_new = p.y + 1;
        if y_new > board.min_max_row[&p.x].1 {
            if p.x < board.side_sz {
                return (
                    Dir::DOWN,
                    Point {
                        x: 2 * board.side_sz + p.x,
                        y: 0,
                    },
                );
            } else if p.x < 2 * board.side_sz {
                return (
                    Dir::LEFT,
                    Point {
                        x: board.side_sz - 1,
                        y: 3 * board.side_sz + p.x - board.side_sz,
                    },
                );
            } else if p.x < 3 * board.side_sz {
                return (
                    Dir::LEFT,
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
    if direction == Dir::LEFT {
        let mut x_new = p.x - 1;
        if x_new < board.min_max_line[&p.y].0 {
            if p.y < board.side_sz {
                return (
                    Dir::RIGHT,
                    Point {
                        x: 0,
                        y: (3 * board.side_sz - 1) - p.y,
                    },
                );
            } else if p.y < 2 * board.side_sz {
                let mut direction = Dir::DOWN;
                return (
                    direction,
                    Point {
                        x: p.y - board.side_sz,
                        y: 2 * board.side_sz,
                    },
                );
            } else if p.y < 3 * board.side_sz {
                let mut direction = Dir::RIGHT;
                return (
                    direction,
                    Point {
                        x: board.side_sz,
                        y: (3 * board.side_sz - 1) - p.y,
                    },
                );
            } else if p.y < 4 * board.side_sz {
                let mut direction = Dir::DOWN;
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
    if direction == Dir::UP {
        let mut y_new = p.y - 1;
        if y_new < board.min_max_row[&p.x].0 {
            if p.x < board.side_sz {
                return (
                    Dir::RIGHT,
                    Point {
                        x: board.side_sz,
                        y: board.side_sz + p.x,
                    },
                );
            } else if p.x < 2 * board.side_sz {
                return (
                    Dir::RIGHT,
                    Point {
                        x: 0,
                        y: 3 * board.side_sz + p.x - board.side_sz,
                    },
                );
            } else if p.x < 3 * board.side_sz {
                return (
                    Dir::RIGHT,
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

fn solve(board: &Board, instructions: &Vec<String>, next_fun: &dyn Fn(Point, Dir, &Board) -> (Dir, Point)) -> i32 {
    let mut cur = Point { y: 0, x: board.min_max_line[&0].0 };
    let mut direction = Dir::RIGHT;
    for i in (0..instructions.len()-1).step_by(2) {
        direction = do_turn(direction, &instructions[i]);
        let length = instructions[i + 1].parse::<i32>().unwrap();
        (cur, direction) = do_move(cur, direction, length, &board, next_fun);
    }
    return 1000 * (cur.y + 1) + 4 * (cur.x + 1) + direction as i32;
}

fn do_move(mut cur: Point, mut direction: Dir, length: i32, board: &Board, next_fun: &dyn Fn(Point, Dir, &Board) -> (Dir, Point)) -> (Point, Dir) {
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

fn main() {
    let input = include_str!("../../../inputs/input_22.txt");
    let (board, instructions) = parse_input(input);
    println!("Part 1: {}", part1(&board,&instructions));
    println!("Part 2: {}", part2(&board,&instructions));
}
