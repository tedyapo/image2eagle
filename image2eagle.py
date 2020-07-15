#!/usr/bin/env python3
#
# image2eagle.py: convert image to Eagle line or rectangle primitives 
#                 generates an eagle command script (*.scr) which
#                 must be run in Eagle to import image

from PIL import Image, ImageOps
import sys
import argparse
import logging

def emit(file, code):
  file.write(code)

def render_run(file, style, line_width, x0, y0, x1, y1):
  if style == 'r':
    emit(file, "RECT (%f %f) (%f %f);\n" % (x0, y0, x1, y1))
  else:
    emit(file, "WIRE %f (%f %f) (%f %f);\n" % (line_width, x0, y0, x1, y1))

def x_coord(col, dpi):
  """x-coordinate in mils"""
  return 1000.*col/dpi

def y_coord(row, rows, line_width):
  """ y-coordinate in mils"""
  return (rows - row - 1)*line_width

def main():
  logging.basicConfig(format='%(levelname)s:%(message)s')
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
  parser.add_argument('-m', '--mirror',
                      help = 'mirror image (useful for bottom side)',
                      action = 'store_true')  
  parser.add_argument('-n', '--invert',
                      help = 'invert input image (black <-> white)',
                      action = 'store_true')
  args = parser.parse_args()

  if args.primitive not in {'l', 'r'}:
    logging.warning('Unknown primitive type: %s\n\n', args.primitive)
    parser.print_help()
    sys.exit(2)

  # read image and process as required
  try:
    image = Image.open(args.image)
  except IOError:
    logging.warning('Cannot open input file "%s"\n', args.image)
    sys.exit(1)
  image = ImageOps.grayscale(image)
  if args.invert:
    image = ImageOps.invert(image)
  if args.mirror:
    image = ImageOps.mirror(image)    

  # rescale image so pixels are line_width tall
  orig_cols, orig_rows = image.size
  cols = orig_cols
  rows = int((orig_rows / args.input_dpi) / (args.line_width / 1000.))
  image = image.resize((cols, rows), Image.LANCZOS)

  try:
    outfile = open(args.scr, 'w')
  except IOError:
    logging.warning('Cannot open output file "%s" for writing\n', args.scr)
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
      elif in_run:
        in_run = False
        render_run(outfile, args.primitive, args.line_width, 
                   x_coord(start_col, args.input_dpi),
                   y_coord(row, rows, args.line_width),
                   x_coord(col, args.input_dpi),
                   y_coord(row+1, rows, args.line_width))
    # render any run that ends at end of row
    if in_run:
      render_run(outfile, args.primitive, args.line_width, 
                 x_coord(start_col, args.input_dpi),
                 y_coord(row, rows, args.line_width),
                 x_coord(col, args.input_dpi),
                 y_coord(row+1, rows, args.line_width))

  # restore previous grid units
  emit(outfile, "GRID last;\n")
  outfile.close()
  sys.stderr.write('\n')

if __name__ == '__main__': main()
