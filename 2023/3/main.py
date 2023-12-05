"""
Advent of Code 2023 day 3
"""
import sys
import logging

log = logging.getLogger()
log.setLevel(logging.ERROR)
handler = logging.StreamHandler()
formatter = logging.Formatter(fmt="%(asctime)s %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter)
log.addHandler(handler)

class Schematic():
    """
    Store the schematic as 2D matrix of chars.
    Provide some functions to extract information from that schematic
    """
    def __init__(self) -> None:
        self.matrix = []

    def add_line(self, line_str):
        """
        Add line to schematic matrix.
        This is the only method supposed to be able
        to write to the internal matrix
        """
        self.matrix.append(list(line_str.strip()))

    def get_stats(self):
        """
        Return dictionary with some statistics
        """
        stat = {'chars': {}, 'lines': len(self.matrix), 'rows': [] }
        for y, y_line in enumerate(self.matrix):
            stat['rows'].append(len(self.matrix[y]))
            for x, current_cell  in enumerate(y_line):
                current_cell = self.matrix[y][x]
                if current_cell not in stat['chars']:
                    stat['chars'][current_cell] = 0
                stat['chars'][current_cell] += 1
        return stat

    def find_stars(self):
        """
        Scan the matrix and return a list of coordinates where  '*' are

        For example

        .....
        ..*..
        ....*

        return
        [(2,1), (4,2)]
        """
        log = logging.getLogger("Schematic.find_stars")
        ret = []
        for y, y_line in enumerate(self.matrix):
            for x, current_cell  in enumerate(y_line):
                current_cell = self.matrix[y][x]
                if current_cell == '*':
                    log.debug("Star at x:%d y:%d", x, y)
                    ret.append((x,y))
        return ret

    def find_symbols(self):
        """
        Scan the matrix and return a list of coordinates where
        something different from a number or dot is found.

        For example

        .1...
        ..#..
        ..44*

        return
        [(2,1), (4,2)]
        """
        log = logging.getLogger("Schematic.find_symbols")
        ret = []
        for y, y_line in enumerate(self.matrix):
            for x, current_cell  in enumerate(y_line):
                current_cell = self.matrix[y][x]
                if not current_cell.isdigit() and current_cell != '.':
                    log.debug("Symbol at x:%d y:%d", x, y)
                    ret.append((x,y))
        return ret

    def find_numbers(self):
        """
        Scan the matrix and return a list of start/stop coordinates where numbers are

        For example

        .....
        ..42.
        ....1

        return
        [
            {'begin':(2,1), 'end':(3,1)},
            {'begin':(4,2), 'end':(4,2)}
        ]
        """
        log = logging.getLogger("Schematic.find_numbers")
        ret = []
        for y, y_line in enumerate(self.matrix):
            log.info("Line %s  --> %s", y, y_line)
            state_in_number = False
            start_number = (None, None)
            end_number = (None, None)
            for x, current_cell  in enumerate(y_line):
                current_cell = self.matrix[y][x]
                log.debug("current_cell[%s][%s]:%s   ---   state_in_number:%s",
                          x, y, current_cell, state_in_number)
                if current_cell.isdigit():
                    log.info("IS DIGIT current_cell[%s][%s]:%s   ---   state_in_number:%s",
                             x, y, current_cell, state_in_number)
                    if state_in_number:
                        log.info("Number started in x:%s y:%s is continuing here",
                                 start_number[0], start_number[1])
                        end_number = (x,y)
                    else:
                        log.info("Number start here in x:{%s} y:{%s}", x, y)
                        end_number = start_number = (x,y)
                        state_in_number = True
                else:
                    if state_in_number:
                        state_in_number = False
                        ret.append({'begin': start_number, 'end': end_number})
            log.debug("Exit from line %d loop. Found %d numbers. state_in_number:%s start_number:%s end_number:%s",
                      y, len(ret), state_in_number, start_number, end_number)
            if state_in_number:
                log.debug("Add numbers that terminates at the end of the line")
                ret.append({'begin': start_number, 'end': end_number})
            log.debug(ret)
        return ret

    def is_adiacent(self, object_coordinate, other_object_coordinate):
        """
        Return True if two cells are adiacent
        """
        log = logging.getLogger("Schematic.is_adiacent")
        log.debug("is_adiacent delta_x:%d delta_y:%d", abs(object_coordinate[0]-other_object_coordinate[0]), abs(object_coordinate[1]-other_object_coordinate[1]))
        return (abs(object_coordinate[0]-other_object_coordinate[0]) <= 1) and (abs(object_coordinate[1]-other_object_coordinate[1]) <= 1)

    def get_number_coordinates(self, number_coordinate):
        """
        Giving
            {'begin':(2,1), 'end':(5,1)}
        return
            [(2,1), (3,1), (4,1), (5,1)]
        """
        ret = []
        y = number_coordinate['begin'][1]
        for x in range(number_coordinate['begin'][0], number_coordinate['end'][0] + 1):
            ret.append((x,y))
        return ret

    def is_part(self, number_coordinate):
        """
        Giving beginning and end coordinate of a number
        it looks all adiacent cells for a not number nor dot
        """
        log = logging.getLogger("Schematic.is_part")
        #log.debug(self.matrix)
        log.debug("Begin:%s End:%s", number_coordinate['begin'], number_coordinate['end'])
        sym_list = self.find_symbols()
        adiacent_list = []
        for digit_coordinate in self.get_number_coordinates(number_coordinate):
            for sym in sym_list:
                log.debug("Check if symbol %s is adiacent to number digit %s", sym, digit_coordinate)
                adiacent_list.append(self.is_adiacent(digit_coordinate, sym))
        return any(adiacent_list)

    def is_gear(self, star_coordinate):
        """
        Giving a coordinate of a star
        it looks all adiacent cells for numbers.
        It return (True, gear_ratio) if there are two numbers
        """
        log = logging.getLogger("Schematic.is_gear")
        #log.debug(self.matrix)
        log.debug("Star is in %s", star_coordinate)
        num_list = self.find_numbers()
        numbers_touching = 0
        gear_ratio = 1
        for number_coordinate in num_list:
            log.debug("Check number %s", number_coordinate)
            is_this_num_near = []
            for digit_coordinate in self.get_number_coordinates(number_coordinate):
                log.debug("Check digit %s of number %s", digit_coordinate, number_coordinate)
                is_this_num_near.append(self.is_adiacent(digit_coordinate, star_coordinate))
            log.debug("Has number %s at least one digit touching the star? %s", number_coordinate, any(is_this_num_near))
            if any(is_this_num_near):
                numbers_touching += 1
                gear_ratio *= self.get_number(number_coordinate)
        return (numbers_touching == 2, gear_ratio)

    def get_number(self, number_coordinate):
        """
        Giving begin and end coordinate of a number, extract the string and
        return the corresponding integer
        """
        log = logging.getLogger("Schematic.get_number")
        log.debug("number_coordinate:%s", number_coordinate)
        log.debug("Get number from line %d  line:%s",
                  number_coordinate['begin'][1], self.matrix[number_coordinate['begin'][1]])
        substring = self.matrix[number_coordinate['begin'][1]][number_coordinate['begin'][0]:number_coordinate['end'][0] + 1]
        log.debug("substring:%s", substring)
        return int(''.join(substring))


def main():
    schematic = []

    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        score = [0, 0]
        schematic = Schematic()
        for line in f.readlines():
            log.debug("line:%s", line.strip())
            schematic.add_line(line)
        log.info("--- MATRIX STATISTIC: %s", schematic.get_stats())
        for this_coordinates in schematic.find_numbers():
            log.debug("Search sorraunding of %s", this_coordinates)
            if schematic.is_part(this_coordinates):
                log.debug("Number in schematic at %s is a part and value is %s",
                          this_coordinates, schematic.get_number(this_coordinates))
                score[0] += schematic.get_number(this_coordinates)
        for stars_pos in schematic.find_stars():
            res = schematic.is_gear(stars_pos)
            if res[0]:
                score[1] += res[1]


    print("Part1:" + str(score[0]))
    print("Part2:" + str(score[1]))


if __name__ == "__main__":
    main()
