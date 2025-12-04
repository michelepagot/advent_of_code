//! By convention, root.zig is the root source file when making a library.
const std = @import("std");

pub fn part_1(today_input: []const u8) i32 {
    var floor: i32 = 0;
    for (today_input) |byte| {
        if (byte == '(') {
            floor += 1;
        } else if (byte == ')') {
            floor -= 1;
        }
    }
    return floor;
}

pub fn part_2(today_input: []const u8) i32 {
    var floor: i32 = 0;
    var step: i32 = 1;
    for (today_input) |byte| {
        if (byte == '(') {
            floor += 1;
        } else if (byte == ')') {
            floor -= 1;
        }
        if (floor == -1) {
            break;
        }
        step += 1;
    }
    return step;
}
