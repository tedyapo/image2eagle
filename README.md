# image2eagle
Eagle image importer

image2eagle is a replacement for the "import-bmp" user-language program (ULP) that comes with Autodesk EAGLE.  Its enhanced features include:
* Reading multiple image formats
* Conversion from color or grayscale to bitmap
* Faster than import-bmp
* May allow higher resolution while maintianing minimum linewidth (see below)
* Default settings optimized for use with OSH Park silkscreen
* Outputs line or rectangle primitives (lines have rounded ends; rectangles are square)
* Doesn't change your grid after importing!

image2eagle accepts high-resolution input images and resizes only in the vertical dimension to use the specified linewidth.  In the horizontal dimension, the output coordinates retain the original image resolution.  Here, you can see the difference on the same text rendered using 2.5mil rectangles.  The top image was produced by image2eagle and the bottom by import-bmp.  

![400 DPI comparison](/docs/400dpi_comparison.png)

Here is the result fabricated by OSH Park:

![OSH Park Sample](/docs/pcb_art_proof.jpg)

Depending on your board manufacturer, these differences may vary.

# Usage
    usage: image2eagle.py [-h] [-w LINE_WIDTH] [-d INPUT_DPI] [-l LAYER]
                           [-t THRESHOLD] [-p PRIMITIVE] [-n]
                           image scr

    Convert image to Eagle line or rectangle primitives. Resulting script must be
    run in Eagle to import image.

    positional arguments:
      image                 input image
      scr                   output script

    optional arguments:
      -h, --help            show this help message and exit
      -w LINE_WIDTH, --line-width LINE_WIDTH
                            rendered line width in mils (default = 2.5)
      -d INPUT_DPI, --input-dpi INPUT_DPI
                            input image resolution in dots per inch
      -l LAYER, --layer LAYER
                            eagle layer number (default = 21)
      -t THRESHOLD, --threshold THRESHOLD
                            image threshold (default = 127)
      -p PRIMITIVE, --primitive PRIMITIVE
                            eagle primitive: r = rect (default), l = line
      -n, --invert          invert input image (black <-> white)

## Importing
Once you have created the Eagle scr file, you can import the graphic by running it from the "File/Execute Script.." menu in Eagle.

## See Also
For some more info, [check out the project on hackaday.io](https://hackaday.io/project/152693-eagle-image-importer)
