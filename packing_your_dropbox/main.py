#!/usr/bin/env python
# coding: utf-8

#
# The "Packing your Dropbox" problem.
# https://www.dropbox.com/jobs/challenges#packing-your-dropbox
# by Leo Vasilyev (chin@shaftsoft.ru)
#

import sys

#--------------------------------------#
#    Drawing and joining functions     #
#--------------------------------------#
BOX_SPACE = " "


def draw_box(w, h):
    '''
    Draw box as char matrix.
    INPUT:
      w - integer, width of a box
      h - integer, height of a box.
    OUTPUT:
      box - list of lists with chars
    '''
    if h == 1: # just a row
        return [[BOX_SPACE] + (['+'] * w)]
    if w == 1: # just a column
        return [[BOX_SPACE] + ['+'] for i in xrange(h)]
    box = []
    # subtract 1 from w because of space prefix
    first_line = last_line = [BOX_SPACE] + ['+'] + ([' ', '-', ' '] * (w-1)) + ['+']
    box.append(first_line)
    for i in xrange(h-2):
        # w must be multiplied by 3 because we use string ' - ' as a width unit.
        box.append([BOX_SPACE] + ['|'] + [' ' * ((w-1)*3)] + ['|'])
    box.append(last_line)
    return box


def format_box(box):
    '''
    Format box as string ready for printing.
    INPUT:
      box - matrix with box
    OUTPUT:
      s - string, ready for printing
    '''
    s = ""
    for i in range(len(box)):
        s += ''.join(box[i])
        s += '\n'
    return s


def join(box1, box2):
    '''
    Join box2 to box1 at the right-top.
    '''
    result_box = []
    box1_height = len(box1)
    box2_height = len(box2)
    if box1_height != box2_height:
        for i in xrange(max(box1_height, box2_height)):
            if i >= len(box1):
                row = [BOX_SPACE] * len(box1[0])
            else:
                row = []
                row += box1[i]
            if i >= len(box2):
                row.extend([BOX_SPACE] * len(box2[0]))
            else:
                row.extend(box2[i])
            result_box.append(row)
    else:
        for i in xrange(box1_height):
            result_box.append(box1[i] + box2[i])
    return result_box

#------------------#
#    OO Classes    #
#------------------#
class Box(object):
    '''
    A box
    '''

    HORIZONTAL_SHAPE = 0
    VERTICAL_SHAPE = 1

    def __init__(self, width, height):
        if width <= 0 or not isinstance(width, int):
            raise TypeError("width must be a positive integer")
        if height <= 0 or not isinstance(height, int):
            raise TypeError("height must be a positive integer")
        self._width = width
        self._height = height

    @property
    def shape(self):
        if self.width >= self.height:
            return self.HORIZONTAL_SHAPE
        else:
            return self.VERTICAL_SHAPE

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def rotate(self):
        return self.__class__(self._height, self._width)

    def __str__(self):
        return format_box(draw_box(self._width, self._height))

    def __repr__(self):
        return "<Box %sx%s instance at %s>" % (self._width, self._height, hex(id(self)))


class Shelf(object):
    '''
    Horizontally packed boxes or just a shelf
    '''
    def __init__(self, width, height):
        self._w = width
        self._h = height
        self._boxes = []

    def is_fits_in(self, box):
        if box.width + sum(b.width for b in self._boxes) > self._w:
            return False
        elif box.height > self._h:
            return False
        else:
            return True

    def add_box(self, box):
        if not self.is_fits_in(box):
            raise ValueError("Box %r is to large" % box)
        self._boxes.append(box)

    @property
    def size(self):
        return sum(b.width for b in self._boxes), max(b.height for b in self._boxes)

    def __str__(self):
        if not len(self._boxes):
            return ''
        return format_box(reduce(join, [draw_box(b.width, b.height) for b in self._boxes]))

    def __repr__(self):
        return "<%s instance. Size is %s with %s boxes at %s>" % (
            self.__class__.__name__,
            self.size,
            len(self._boxes),
            hex(id(self))
        )

#------------------#
#    Main logic    #
#------------------#
def main():
    '''
    Note that this problem is NP-hard :-)
    Here we use gready heuristic approarch, based on the shelf algorithm.

    1. Sort boxes by non descreasing min(height, width).
       (we have to use min because we can rotate boxes)
    2. Insert box into a shelf:
       2a. A box that initializes a new shelf is always horizontally oriented.
           (to keep as low as possible the vertical occupancy of the corresponding shelf)
       2b. When a box is inserted into existing shelf, if both orientations are OK then
           the vertical one is selected.
           (to keep as low as possible the horizontal occupancy of the shelf)
    3. The area of enclosing box computed as the max box width multipled by sum of shelf's heights.
    '''
    n = int(raw_input())
    if n <= 0:
        raise ValueError("n must be > 0")
    boxes = []
    for i in range(n):
        w, h = [int(x) for x in raw_input().split()]
        boxes.append(Box(w, h))
    boxes.sort(key=lambda b: min([b.width, b.height]), reverse=True)
    max_w = max(b.width for b in boxes)
    shelfs = []
    for b in boxes:
        rb = b.rotate()
        fits = False
        for cur_s in shelfs:
            box_to_add = None
            if b.shape == b.VERTICAL_SHAPE:
                if cur_s.is_fits_in(b):
                    box_to_add = b
                    fits = True
                elif cur_s.is_fits_in(rb):
                    box_to_add = rb
                    fits = True
            else:
                if cur_s.is_fits_in(rb):
                    box_to_add = rb
                    fits = True
                elif cur_s.is_fits_in(b):
                    box_to_add = b
                    fits = True
            if fits:
                cur_s.add_box(box_to_add)
                break
        if not fits:
            if b.shape != b.HORIZONTAL_SHAPE:
                b = b.rotate()
            s = Shelf(max_w, b.height)
            s.add_box(b)
            shelfs.append(s)

    total_width = max(s.size[0] for s in shelfs)
    total_height = sum(s.size[1] for s in shelfs)

    print total_width * total_height

    sys.stderr.write("%sx%s\n" % (total_width, total_height))
    for s in shelfs:
        sys.stderr.write(str(s))

if __name__ == "__main__":
    main()
