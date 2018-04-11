#!/usr/bin/env python
#
# image2eagle.py: convert image to Eagle line or rectangle primitives 
#                 generates an eagle command script (*.scr) which
#                 must be run in Eagle to import image

from PIL import Image, ImageOps
import math
import sys
import argparse

def emit(file, code):
  file.write(code)

def render_run(file, style, line_width, x0, y0, x1, y1):
  if style == 'r':
    emit(file, "RECT (%f %f) (%f %f);\n" % (x0, y0, x1, y1))
  else:
    emit(file, "WIRE %f (%f %f) (%f %f);\n" % (line_width, x0, y0, x1, y1))

# x-coordinate in mils
def x_coord(col, dpi):
  return 1000.*col/dpi

# y-coordinate in mils
def y_coord(row, rows, line_width):
  return (rows - row - 1)*line_width

# command-line parsing
parser = argparse.ArgumentParser(description = 'Convert image to Eagle line' +
                                 ' or rectangle primitives.  Resulting ' +
                                 'script must be run in Eagle to import image.')
parser.add_argument('image', help = 'input image', type = str)
parser.add_argument('scr', help = 'output script', type = str)
parser.add_argument('-w', '--line-width',
                    help = 'rendered line width in mils (default = 2.5)',
                    type = float,
                    default = 2.5)
parser.add_argument('-d', '--input-dpi',
                    help = 'input image resolution in dots per inch',
                    type = float)
parser.add_argument('-l', '--layer',
                    help = 'eagle layer number (default = 21)',
                    type = int,
                    default = 21)
parser.add_argument('-t', '--threshold',
                    help = 'image threshold (default = 127)',
                    type = int,
                    default = 127)
parser.add_argument('-p', '--primitive',
                    help = 'eagle primitive: r = rect (default), l = line',
                    type = str,
                    default = 'r')
parser.add_argument('-n', '--invert',
                    help = 'invert input image (black <-> white)',
                    action = 'store_true')
args = parser.parse_args()

if args.primitive != 'l' and args.primitive != 'r':
  sys.stderr.write('Unknown primitive type: %s\n\n' % args.primitive)
  parser.print_help()
  sys.exit(2)

# process image as required
image = Image.open(args.image)
image = ImageOps.grayscale(image)
if args.invert:
  image = ImageOps.invert(image)

# rescale image so pixels are line_width tall
(orig_cols, orig_rows) = image.size
cols = orig_cols
rows = int((orig_rows / args.input_dpi) / (args.line_width / 1000.))
image = image.resize((cols, rows), Image.LANCZOS)

try:
  outfile = open(args.scr, 'w')
except IOError:
  sys.stderr.write('Cannot open output file "%s" for writing\n' % args.scr)
  sys.exit(1)

emit(outfile, "GRID mil;\n")
emit(outfile, "LAYER %d;\n" % args.layer)

# find horizontal runs of pixels and emit a corresponding 
#   rectangle or line command
for row in range(0, rows):
  sys.stderr.write('processing row %d/%d\r' % (row, rows))
  in_run = False
  for col in range(0, cols):
    if image.getpixel((col, row)) > args.threshold:
      if not in_run:
        in_run = True
        start_col = col
    else:
      if in_run:
        in_run = False
        render_run(outfile, args.primitive, args.line_width, 
                   x_coord(start_col, args.input_dpi),
                   y_coord(row, rows, args.line_width),
                   x_coord(col-1, args.input_dpi),
                   y_coord(row+1, rows, args.line_width))
  # render any run that ends at image boundary
  if in_run:
    render_run(outfile, args.primitive, args.line_width, 
               x_coord(start_col, args.input_dpi),
               y_coord(row, rows, args.line_width),
               x_coord(col-1, args.input_dpi),
               y_coord(row+1, rows, args.line_width))

# restore previous grid units
emit(outfile, "GRID last;\n")
outfile.close()
sys.stderr.write('\n')
