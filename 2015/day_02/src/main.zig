const std = @import("std");
const day_02 = @import("day_02");
var input: []const u8 = @embedFile("input.txt");

pub fn main() !void {
    var stdout_buffer: [1024]u8 = undefined;
    var stdout_writer = std.fs.File.stdout().writer(&stdout_buffer);
    const stdout = &stdout_writer.interface;

    var res: u32 = 0;
    res = try day_02.part_1(input);
    try stdout.print("Part1:{d}\n", .{res});
    res = try day_02.part_2(input);
    try stdout.print("Part2:{d}\n", .{res});
    try stdout.flush();
}
