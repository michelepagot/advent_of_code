"""
Advent of Code 2023 day 3
"""
import sys
import logging

log = logging.getLogger()
log.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter(fmt="%(asctime)s %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter)
log.addHandler(handler)

class Schematic():
    def __init__(self) -> None:
        self.matrix = []

    def add_line(self, line_str):
        self.matrix.append(list(line_str.strip()))

    def get_stats(self):
        stat = {'chars': {}, 'lines': len(self.matrix), 'rows': [] }
        for y, y_line in enumerate(self.matrix):
            stat['rows'].append(len(self.matrix[y]))
            for x, current_cell  in enumerate(y_line):
                current_cell = self.matrix[y][x]
                if current_cell not in stat['chars']:
                    stat['chars'][current_cell] = 0
                stat['chars'][current_cell] += 1
        return stat

    def find_numbers(self):
        """
        Scan the matrix and return a list of start/stop coordinates where numbers are

        For example

        .....
        ..42.
        ....1

        return
        [
            {'start':(1,2), 'stop':(1,3)},
            {'start':(2,4), 'stop':(2,4)}
        ]
        """
        log = logging.getLogger("Schematic.find_numbers")
        ret = []
        for y, y_line in enumerate(self.matrix):
            log.info('-' * 50)
            log.info("Line %s  --> %s", y, y_line)
            state_in_number = False
            start_number = (None, None)
            end_number = (None, None)
            for x, current_cell  in enumerate(y_line):
                current_cell = self.matrix[y][x]
                log.debug("current_cell[%s][%s]:%s   ---   state_in_number:%s", x, y, current_cell, state_in_number)
                if current_cell.isdigit():
                    log.info("IS DIGIT  :::  current_cell[%s][%s]:%s   ---   state_in_number:%s", x, y, current_cell, state_in_number)
                    if state_in_number:
                        log.info("Number started in x:%s y:%s is continuing here", start_number[0], start_number[1])
                        end_number = (x,y)
                    else:
                        log.info("Number start here in x:{%s} y:{%s}", x, y)
                        end_number = start_number = (x,y)
                        state_in_number = True
                else:
                    if state_in_number:
                        state_in_number = False
                        ret.append({'start': start_number, 'end': end_number})
            log.debug(f"Exit from line {x} loop. Found {len(ret)} numbers. state_in_number:{state_in_number} start_number:{start_number} end_number:{end_number}")
            if state_in_number:
                log.debug("Add numbers that terminates at the end of the line")
                ret.append({'start': start_number, 'end': end_number})
            log.debug(ret)
        return ret


    def is_part(self, number_coordinate):
        """
        Giving beginning and end coordinate of a number
        it looks all adiacent cells for a not number nor dot
        """
        log.debug(self.matrix)
        log.debug("Start:%s End:%s", number_coordinate['start'], number_coordinate['end'])

        log.debug("check the line above if it exist")
        y = number_coordinate['start'][1] -1
        if y >= 0:
            start_x = max(0,number_coordinate['start'][0] -1)
            end_x = min(number_coordinate['end'][0] + 1, len(self.matrix[y]) - 1)
            log.debug(f"Check the line above that start from x:{start_x} y:{y} and end at x:{end_x} y:{y}.")
            for x in range(start_x, end_x + 1):
                log.debug(f"Check x:{x} y:{y}")
                check = self.matrix[y][x]
                log.debug(f"x:{x} y:{y} --> {check}")
                if not check.isdigit() and check != '.':
                    log.debug('SYMBOL')
                    return True
        else:
            log.debug(f"Line {number_coordinate['start'][1]} does not have above line")

        log.debug("check the line below if it exist")
        y = number_coordinate['start'][1] + 1
        if y < len(self.matrix):
            start_x = max(0,number_coordinate['start'][0] -1)
            end_x = min(number_coordinate['end'][0] + 1, len(self.matrix[y]) -1)
            log.debug(f"Check the line below that start from x:{start_x} y:{y} and end at x:{end_x} y:{y}.")
            for x in range(start_x, end_x + 1):
                log.debug(f"Check x:{x} y:{y}")
                check = self.matrix[y][x]
                log.debug(f"x:{x} y:{y} --> {check}")
                if not check.isdigit() and check != '.':
                    log.debug('SYMBOL')
                    return True
        else:
            log.debug(f"Line {number_coordinate['start'][1]} does not have below line")

        log.debug("check the cell before the number if it exist")
        y = number_coordinate['start'][1]
        x = number_coordinate['start'][0] - 1
        if x >= 0:
            check = self.matrix[y][x]
            log.debug(f"x:{x} y:{y} --> {check}")
            if not check.isdigit() and check != '.':
                log.debug('SYMBOL')
                return True
        else:
            log.debug(f"Number starting at x:{number_coordinate['start'][0]}  y:{y} does not have cell on the left")

        log.debug("check the cell after the number if it exist")
        y = number_coordinate['start'][1]
        x = number_coordinate['end'][0] + 1
        if x < len(self.matrix[y]):
            check = self.matrix[y][x]
            log.debug(f"x:{x} y:{y} --> {check}")
            if not check.isdigit() and check != '.':
                log.debug('SYMBOL')
                return True
        else:
            log.debug(f"Number ending at x:{number_coordinate['end'][0]}  y:{y} does not have cell on the righ")

        return False
    
    def get_number(self, number_coordinate):
        log.debug("number_coordinate:%s", number_coordinate)
        log.debug("Get number from line %s  line:%s", number_coordinate['start'][1], self.matrix[number_coordinate['start'][1]])
        substring = self.matrix[number_coordinate['start'][1]][number_coordinate['start'][0]:number_coordinate['end'][0] + 1]
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
                log.debug("Number in schematic at %s is a part and value is %s", this_coordinates, schematic.get_number(this_coordinates))
                score[0] += schematic.get_number(this_coordinates)

    print("Part1:" + str(score[0]))
    print("Part2:" + str(score[1]))


if __name__ == "__main__":
    main()
