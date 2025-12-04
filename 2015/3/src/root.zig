//! By convention, root.zig is the root source file when making a library.
const std = @import("std");

const Vec2 = struct { x: i32, y: i32 };

fn pos_update(byte: u8, pos: *Vec2) void {
    if (byte == '>') {
        pos.x += 1;
    } else if (byte == '<') {
        pos.x -= 1;
    } else if (byte == '^') {
        pos.y += 1;
    } else if (byte == 'v') {
        pos.y -= 1;
    }
}

fn add(list: *std.ArrayList(Vec2), allocator: std.mem.Allocator, pos: Vec2) !void {
    for (list.items) |item| {
        if ((pos.x == item.x) and (pos.y == item.y)) {
            std.log.debug("add::skip {}", .{pos});
            return;
        }
    }
    std.log.debug("add::append {}", .{pos});
    try list.append(allocator, pos);
}

pub fn part_1(today_input: []const u8) !usize {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    const allocator = gpa.allocator();
    var house_log = try std.ArrayList(Vec2).initCapacity(allocator, 1);
    defer house_log.deinit(allocator);
    var pos = Vec2{ .x = 0, .y = 0 };
    try add(&house_log, allocator, pos);

    for (today_input) |byte| {
        pos_update(byte, &pos);
        std.log.debug("part_1::'{c}' {}", .{ byte, pos });
        try add(&house_log, allocator, pos);
    }
    return house_log.items.len;
}

test "part_1" {
    std.log.debug("TEST1 --- START '<'", .{});
    try std.testing.expectEqual(2, part_1("<"));
    std.log.debug("TEST1 --- END", .{});

    std.log.debug("TEST2 --- START '>>'", .{});
    try std.testing.expectEqual(3, part_1(">>"));
    std.log.debug("TEST2 --- END", .{});

    // delivers presents to 4 houses in a square,
    // including twice to the house at his starting/ending location.
    std.log.debug("TEST3 --- START '^>v<'", .{});
    try std.testing.expectEqual(4, part_1("^>v<"));
    std.log.debug("TEST3 --- END", .{});

    //  delivers a bunch of presents to some very lucky children at only 2 houses.
    std.log.debug("TEST4 --- START '^v^v^v^v^v'", .{});
    try std.testing.expectEqual(2, part_1("^v^v^v^v^v"));
    std.log.debug("TEST4 --- END", .{});

    std.log.debug("TEST5 --- START '><'", .{});
    try std.testing.expectEqual(2, part_1("><"));
    std.log.debug("TEST5 --- END", .{});
}

pub fn part_2(today_input: []const u8) !usize {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    const allocator = gpa.allocator();
    var house_log = try std.ArrayList(Vec2).initCapacity(allocator, 1);
    defer house_log.deinit(allocator);

    var pos: [2]Vec2 = .{ Vec2{ .x = 0, .y = 0 }, Vec2{ .x = 0, .y = 0 } };
    var index: usize = 0;
    try add(&house_log, allocator, pos[0]);

    for (today_input) |byte| {
        index += 1;
        pos_update(byte, &pos[index % 2]);
        std.log.debug("part_2::'{c}' {}", .{ byte, pos[index % 2] });
        try add(&house_log, allocator, pos[index % 2]);
    }
    return house_log.items.len;
}

test "part_2" {
    std.log.debug("TEST1 --- START '<'", .{});
    try std.testing.expectEqual(2, part_2("<"));
    std.log.debug("TEST1 --- END", .{});

    std.log.debug("TEST2 --- START '>>'", .{});
    try std.testing.expectEqual(2, part_2(">>"));
    std.log.debug("TEST2 --- END", .{});

    std.log.debug("TEST3 --- START '^v'", .{});
    try std.testing.expectEqual(3, part_2("^v"));
    std.log.debug("TEST3 --- END", .{});

    std.log.debug("TEST4 --- START '^>v<'", .{});
    try std.testing.expectEqual(3, part_2("^>v<"));
    std.log.debug("TEST4 --- END", .{});

    std.log.debug("TEST5 --- START '^v^v^v^v^v'", .{});
    try std.testing.expectEqual(11, part_2("^v^v^v^v^v"));
    std.log.debug("TEST5 --- END", .{});
}
