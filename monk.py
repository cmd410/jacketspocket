"""Script that can encode numbers
and messages into Cistercian number system.
Result is outputed as an svg image.

Requires:
    svgwrite
"""

from argparse import ArgumentParser

try:
    from svgwrite import Drawing
    from svgwrite.container import Group
    from svgwrite.shapes import Line
except ModuleNotFoundError:
    print('svgwrite is not installed.\nRun command:\n\tpip install svgwrite')
    quit(1)


parser = ArgumentParser()

parser.add_argument(
    '-i',
    metavar='INTS',
    type=int,
    nargs='+',
    default=[],
    help='Integers to encode'
    )

parser.add_argument(
    '-m',
    metavar='MESSAGE',
    type=str,
    default='',
    help='Text string to encode'
)

parser.add_argument(
    '-o',
    metavar='OUTPUT',
    type=str,
    default='',
    help='Output file name'
)


def line(start: tuple, end: tuple) -> Line:
    return Line(start, end, stroke='black', style='stroke-linecap:round;stroke-width:2px;')


def zero():
    return line((0, 0),(0, 30))


def one():
    return line((0, 0), (10, 0))


def two():
    return line((0, 10),(10, 10))


def three():
    return line((0, 0), (10, 10))


def four():
    return line((0, 10), (10, 0))


def five():
    five = Group()
    five.add(four())
    five.add(one())
    return five


def six():
    return line((10, 0), (10, 10))


def seven():
    seven = Group()
    seven.add(six())
    seven.add(one())
    return seven


def eight():
    eight = Group()
    eight.add(six())
    eight.add(two())
    return eight


def nine():
    nine = Group()
    nine.add(eight())
    nine.add(one())
    return nine


draw_functions = [
    zero,
    one,
    two,
    three,
    four,
    five,
    six,
    seven,
    eight,
    nine
]

offsets = [
    (0, 0),
    (-10, 0),
    (0, 30),
    (-10, 30)
]

def number(num: int) -> Line:
    if 0 > num > 9999:
        raise RuntimeError('Cistercian numbers can only represent numbers from 0 to 9999')

    num_drawing = Group()
    num_drawing.add(zero())
    if num != 0:
        for i, digit in enumerate(reversed(str(num))):
            digit_drawing = draw_functions[int(digit)]()
            offset = offsets[i]
            try:
                isnt_flat = bool(digit_drawing['y1'] - digit_drawing['y2'])
            except KeyError:
                isnt_flat = True
            if offset[1] and isnt_flat:
                offset = (offset[0], offset[1] - 10)
            digit_drawing.translate(offset)
            if i % 2 != 0:
                digit_drawing.scale((-1, 1))
                digit_drawing.translate((-10, 0))
            if i > 1:
                if isnt_flat:
                    digit_drawing.scale((1, -1))
                    digit_drawing.translate((0, -10))
                elif digit == '2':
                    digit_drawing.translate((0, -20))
            num_drawing.add(digit_drawing)

    num_drawing.translate((20, 20))
    return num_drawing


def draw_numbers(*args):
    numbers = Group()
    for i, num in enumerate(args):
        assert isinstance(i, int)
        num_drawing = number(num)
        num_drawing.translate((35 * i, 0))
        numbers.add(num_drawing)
    return numbers


def encode_message(message: str) -> Group:
    return draw_numbers(*[ord(i) for i in message])


def encode_bytes(b: bytes) -> Group:
    return draw_numbers(*[i for i in b])


def validate_filename(name: str) -> str:
    for i in '<>:\"/\\|?*':
        name = name.replace(i, '_')
    return name


def main():
    args = parser.parse_args()
    if not any([args.i, args.m]):
        print('Please, provide some integers or a text message to encode.\n')
        parser.print_help()
        quit(1)

    ints = args.i
    message = args.m

    ints_output_file = args.o or '-'.join([str(i) for i in ints]) + '.svg'
    message_output_file = args.o or validate_filename(message) + '.svg'

    if ints:
        d = Drawing(
            filename=ints_output_file,
            profile='tiny',
            size=(f'{10 + len(ints)*35}px', '70px'))
        d.add(draw_numbers(*ints))
        d.save()
    if message:
        d = Drawing(
            filename=message_output_file,
            profile='tiny',
            size=(f'{10 + len(message)*35}px', '70px'))
        d.add(encode_message(message))
        d.save()


if __name__ == '__main__':
    main()
