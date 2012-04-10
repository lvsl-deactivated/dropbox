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
#    OO Classes    #
#------------------#
class Box(object):
    '''
    A box
    '''

    SQUARE_SHAPE = 0
    HORIZONTAL_SHAPE = 1
    VERTICAL_SHAPE = 2

    def __init__(self, width, height):
        if width <= 0 or not isinstance(width, int):
            raise TypeError("width must be a positive integer")
        if height <= 0 or not isinstance(height, int):
            raise TypeError("height must be a positive integer")
        self._width = width
        self._height = height

    @property
    def shape(self):
        if self.width > self.height:
            return self.HORIZONTAL_SHAPE
        elif self.width < self.height:
            return self.VERTICAL_SHAPE
        else:
            return self.SQUARE_SHAPE

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def area(self):
        return self.width * self.height

    def rotate(self):
        self._width, self._height = self._height, self._width

    def __str__(self):
        return format_box(draw_box(self._width, self._height))

    def __repr__(self):
        return "<Box %sx%s instance at %s>" % (self._width, self._height, hex(id(self)))


class Package(object):
    '''
    A package of boxes.
    '''
    def __init__(self):
        self._boxes = []
        self._pack_size = 0
        self.G = None

    def add_box(self, box):
        if not isinstance(box, Box):
            raise TypeError("box must be an instance of Box.")
        if box in self._boxes:
            raise ValueError("Box %r already in package." % box)
        self._boxes.append(box)
        self._boxes.sort(key=lambda b: b.area)
        self.shake_down()

    def remove_box(self, box):
        if not isinstance(box, Box):
            raise TypeError("box must be an instance of Box.")
        if box not in self._boxes:
            raise ValueError("Box %r not in this packages." % box)
        self._boxes.remove(box)
        self.shake_down()

    def shake_down(self):
        def rec_width(a, b, t):
            if isinstance(a, tuple):
                wa = rec_width(*a)
            else:
                wa = a.width

            if isinstance(b, tuple):
                wb = rec_width(*b)
            else:
                wb = b.width

            if t == 'right':
                return sum([wa, wb])
            elif t == 'bottom':
                return max([wa, wb])
            else:
                raise ValueError("WTF: %s!?" % t)

        def rec_height(a, b, t):
            if isinstance(a, tuple):
                ha = rec_height(*a)
            else:
                ha = a.height

            if isinstance(b, tuple):
                hb = rec_height(*b)
            else:
                hb = b.height

            if t == 'right':
                return max([ha, hb])
            elif t == 'bottom':
                return sum([ha, hb])
            else:
                raise ValueError("WTF: %s!?" % t)

        if not self._boxes: # empty pack
            self._pack_size = 0
        elif len(self._boxes) == 1: # only one box
            self._pack_size = self._boxes[0].area
        else:
            cb = self._boxes[0]
            t = None
            for nb in self._boxes[1:]:
                # TODO: add box rotation
                if not t:
                    dw = abs(cb.width - nb.width)
                    dh = abs(cb.height - nb.height)
                    rb = Box(nb.width, nb.height)
                    rb.rotate()
                    rdw = abs(cb.width - rb.width)
                    rdh = abs(cb.height - rb.height)
                    if dw >= dh and dw >= rdw:
                        t = (nb, cb, 'right')
                    elif dw >= rdw:
                        t = (rb, cb, 'right')
                    elif dh >= rdh:
                        t = (nb, cb, 'bottom')
                    else:
                        t = (rb, cb, 'bottom')
                else:
                    w = rec_width(*t)
                    h = rec_height(*t)
                    dw = abs(w - nb.width)
                    dh = abs(h - nb.height)
                    rb.rotate()
                    rdw = abs(w - rb.width)
                    rdh = abs(h - rb.height)
                    if dw >= dh and dw >= rdw:
                        t = (t, nb, 'right')
                    elif dw >= rdw:
                        t = (t, rb, 'right')
                    elif dh >= rdh:
                        t = (t, nb, 'bottom')
                    else:
                        t = (t, rb, 'bottom')
            self.G = t

    @property
    def boxes(self):
        return self._boxes[:] # make copy to avoid modifications

    @property
    def width(self):
        pass

    @property
    def height(self):
        pass

    @property
    def area(self):
        return self._pack_size

    def __contains__(self, item):
        return item in self._boxes

    def __len__(self):
        return len(self._boxes)

    def __str__(self):
        def rec_join(a, b, t):
            if isinstance(a, tuple):
                a = rec_join(*a)
            elif isinstance(a, Box):
                a = draw_box(a.width, a.height)

            if isinstance(b, tuple):
                b = rec_join(*b)
            elif isinstance(b, Box):
                b = draw_box(b.width, b.height)

            if t == 'right':
                j = right_join(a, b)
            elif t == 'bottom':
                j = bottom_join(a, b)
            else:
                raise ValueError("WTF: %w!?" % t)

            return j

        if not self._boxes:
            return ''
        elif len(self._boxes) == 1:
            r = draw_box(self._boxes[0].width, self._boxes[0].height)
        else:
            r = rec_join(*self.G)
        return format_box(r)

    def __repr__(self):
        return "<Package instance with %s boxes at %s>" % (len(self._boxes), hex(id(self)))


#------------------------------------------------#
#    Backtracking algorithm for packing boxes    #
#------------------------------------------------#
def pack_boxes(boxes):
    boxes = sorted(boxes, key=lambda b: b[0]*b[1], reverse=True)

#------------------#
#    Main logic    #
#------------------#
def main():
    n = int(raw_input())
    p = Package()
    for i in range(n):
        box = [int(x) for x in raw_input().split()]
        p.add_box(Box(*box))
    print p

if __name__ == "__main__":
    main()
