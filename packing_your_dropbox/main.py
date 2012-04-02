#!/usr/bin/env python
# coding: utf-8

#
# The "Packing your Dropbox" problem.
# https://www.dropbox.com/jobs/challenges#packing-your-dropbox
# by Leo Vasilyev (chin@shaftsoft.ru)
#

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


def right_join(box1, box2):
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


def bottom_join(box1, box2):
    '''
    Join box2 to box1 at the bottom-left.
    '''
    result_box = []
    box1_width = len(box1[0])
    box2_width = len(box2[0])
    if box1_width != box2_width:
        if box1_width > box2_width:
            result_box += box1
        else:
           delta = [BOX_SPACE] * (box2_width - box1_width)
           for i in xrange(len(box1)):
               row = box1[i] + delta
               result_box.append(row)

        if box1_width > box2_width:
           delta = [BOX_SPACE] * (box1_width - box2_width)
           for i in xrange(len(box2)):
               row = box2[i] + delta
               result_box.append(row)
        else:
           result_box += box2
    else:
       result_box += box1
       result_box += box2
    return result_box

#------------------#
# OO Classes       #
#------------------#
class Box(object):
    '''
    A box
    '''
    def __init__(self, width, height):
        if width <= 0 or not isinstance(width, int):
            raise TypeError("width must be a positive integer")
        if height <= 0 or not isinstance(height, int):
            raise TypeError("height must be a positive integer")
        self._width = width
        self._height = height

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def area(self):
        return self.width * self.height

    def __str__(self):
        return format_box(draw_box(self.width, self.height))

    def __repr__(self):
        return "<Box %sx%s instance at %s>" % (self.width, self.height, hex(id(self)))


class Package(object):
    '''
    A package of boxes.
    '''
    def __init__(self, boxes=None):
        if not boxes:
            self._boxes = []
            return
        if not all(isinstance(b, Box) for b in boxes):
            raise TypeError("Boxes must be an iterable with Box instances.")
        self._boxes = list(boxes)

    def add_box(self, box):
        if not isinstance(box, Box):
            raise TypeError("box must be an instance of Box.")
        if box in self.boxes:
            raise ValueError("Box %r already in package." % box)
        self._boxes.append(box)

    def remove_box(self, box):
        if not isinstance(box, Box):
            raise TypeError("box must be an instance of Box.")
        if box not in self.boxes:
            raise ValueError("Box %r not in this packages.")
        self._boxes.remove(box)

    def shake_down(self):
        pass

    @property
    def boxes(self):
        return self._boxes[:] # make copy to avoid modifications

    @property
    def area(self):
        pass

    def __contains__(self, item):
        return item in self.boxes

    def __len__(self):
        return len(self.boxes)

    def __str__(self):
        r = draw_box(self.boxes[0].width, self.boxes[0].height)
        for i in range(1, len(self)):
            b = self.boxes[i]
            # TODO: more clever joining
            r = right_join(r, draw_box(b.width, b.height))
        return format_box(r)

    def __repr__(self):
        return "<Package instance with %s boxes at %s>" % (len(self.boxes), hex(id(self)))

#------------------#
#    Main logic    #
#------------------#
def main():
    n = int(raw_input())
    boxes = []
    for i in range(n):
        box = [int(x) for x in raw_input().split()]
        boxes.append(box)

if __name__ == "__main__":
    main()
