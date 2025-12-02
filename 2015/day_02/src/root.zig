//! By convention, root.zig is the root source file when making a library.
const std = @import("std");

const Vec3 = struct { l: u32, w: u32, h: u32 };

fn smaller(i: Vec3) u32 {
    if ((i.l < i.w) and (i.l < i.h)) {
        return i.l;
    } else if (i.w < i.h) {
        return i.w;
    }
    return i.h;
}

test "Smaller" {
    try std.testing.expectEqual(2, smaller(Vec3{ .l = 2, .w = 3, .h = 4 }));
    try std.testing.expectEqual(2, smaller(Vec3{ .l = 4, .w = 2, .h = 3 }));
    try std.testing.expectEqual(2, smaller(Vec3{ .l = 3, .w = 4, .h = 2 }));
    try std.testing.expectEqual(2, smaller(Vec3{ .l = 2, .w = 2, .h = 2 }));
    try std.testing.expectEqual(1, smaller(Vec3{ .l = 1, .w = 1, .h = 10 }));
}

fn area(i: Vec3) u32 {
    const areas = Vec3{ .l = i.l * i.h, .w = i.h * i.w, .h = i.w * i.l };
    return 2 * (areas.l + areas.h + areas.w) + smaller(areas);
}

test "Area" {
    try std.testing.expectEqual(58, area(Vec3{ .l = 2, .w = 3, .h = 4 }));
    try std.testing.expectEqual(43, area(Vec3{ .l = 1, .w = 1, .h = 10 }));
}

fn length(i: Vec3) u32 {
    const half_perim = Vec3{ .l = i.l + i.h, .w = i.h + i.w, .h = i.w + i.l };
    return 2 * smaller(half_perim) + (i.l * i.h * i.w);
}

test "Length" {
    try std.testing.expectEqual(34, length(Vec3{ .l = 2, .w = 3, .h = 4 }));
    try std.testing.expectEqual(14, length(Vec3{ .l = 1, .w = 1, .h = 10 }));
}

fn line_parser(line: []const u8) !Vec3 {
    var x_n: u8 = 0;
    var res = Vec3{ .l = 2, .w = 3, .h = 4 };

    var it = std.mem.tokenizeScalar(u8, line, 'x');
    while (it.next()) |token| {
        if (x_n == 0) {
            res.l = try std.fmt.parseInt(u32, token, 10);
        } else if (x_n == 1) {
            res.w = try std.fmt.parseInt(u32, token, 10);
        } else if (x_n == 2) {
            res.h = try std.fmt.parseInt(u32, token, 10);
        }
        x_n += 1;
        std.log.debug("res:{}", .{res});
    }
    return res;
}

test "parse line" {
    try std.testing.expectEqualDeep(Vec3{ .l = 2, .w = 3, .h = 4 }, line_parser("2x3x4"));
    try std.testing.expectEqual(Vec3{ .l = 30, .w = 4, .h = 5 }, line_parser("30x4x5"));
    try std.testing.expectEqual(Vec3{ .l = 3, .w = 400, .h = 5 }, line_parser("3x400x5"));
    try std.testing.expectEqual(Vec3{ .l = 3, .w = 4, .h = 5000 }, line_parser("3x4x5000"));
    try std.testing.expectEqual(Vec3{ .l = 30, .w = 400, .h = 5000 }, line_parser("30x400x5000"));
    try std.testing.expectEqual(Vec3{ .l = 1, .w = 1, .h = 10 }, line_parser("1x1x10"));
}

pub fn part_1(today_input: []const u8) !u32 {
    var pack: Vec3 = .{ .l = 0, .h = 0, .w = 0 };
    var tot: u32 = 0;
    std.log.debug("part_1", .{});

    var it = std.mem.tokenizeScalar(u8, today_input, '\n');
    while (it.next()) |token| {
        pack = try line_parser(token);
        tot += area(pack);
    }
    return tot;
}

test "part_1" {
    const str1 =
        \\2x3x4
        \\
    ;
    try std.testing.expectEqual(58, part_1(str1));
    const str2 =
        \\2x3x4
        \\1x1x10
        \\
    ;
    try std.testing.expectEqual(58 + 43, part_1(str2));
}

pub fn part_2(today_input: []const u8) !u32 {
    var x_start: u32 = 0;
    var x_end: u32 = 0;
    var pack: Vec3 = .{ .l = 0, .h = 0, .w = 0 };
    var tot: u32 = 0;
    std.log.debug("part_2", .{});
    for (today_input) |byte| {
        std.log.debug("part_2::FOR START x_start:{} x_end:{} today_input[{}]={}", .{ x_start, x_end, x_end, today_input[x_end] });
        if (byte == 10 or byte == 13) {
            std.log.debug("part_1::EOL START x_start:{} x_end:{} today_input[{}]={}", .{ x_start, x_end, x_end, today_input[x_end] });
            pack = try line_parser(today_input[x_start..x_end]);
            tot += length(pack);
            x_start = x_end + 1;
            std.log.debug("part_2::EOL END x_start:{} x_end:{} pack:{} tot:{}", .{ x_start, x_end, pack, tot });
        }
        x_end += 1;
        std.log.debug("part_2::FOR END x_start:{} x_end:{}", .{ x_start, x_end });
    }
    return tot;
}

test "part_2" {
    const str1 =
        \\2x3x4
        \\
    ;
    try std.testing.expectEqual(34, part_2(str1));
    const str2 =
        \\2x3x4
        \\1x1x10
        \\
    ;
    try std.testing.expectEqual(34 + 14, part_2(str2));
}
