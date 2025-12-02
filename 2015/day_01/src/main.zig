const std = @import("std");
const day_01 = @import("day_01");
var input: []const u8 = @embedFile("input.txt");

pub fn main() !void {
    var stdout_buffer: [1024]u8 = undefined;
    var stdout_writer = std.fs.File.stdout().writer(&stdout_buffer);
    const stdout = &stdout_writer.interface;

    var res: i32 = 0;
    res = day_01.part_1(input);
    try stdout.print("Part1:{d}\n", .{res});
    res = day_01.part_2(input);
    try stdout.print("Part2:{d}\n", .{res});
    try stdout.flush();
}
