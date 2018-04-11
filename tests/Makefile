# tests require netpbm to be installed
all: font_test.scr size_test.scr

font_test.scr: font_test.tex
	pdflatex -halt-on-error font_test.tex
	pdftoppm -r 1200 font_test.pdf | pnmtopng > font_test.png
	../image2eagle.py font_test.png font_test.scr -d 1200 -n -w 2.5
	pdftoppm -r 400 font_test.pdf | ppmtopgm | pgmtopbm -threshold | \
	          ppmtobmp -bpp 1 > font_test.bmp

size_test.scr: size_test.tex
	pdflatex -halt-on-error size_test.tex
	pdftoppm -r 1200 size_test.pdf | pnmtopng > size_test.png
	../image2eagle.py size_test.png size_test.scr -d 1200 -n -w 2.5
	pdftoppm -r 400 size_test.pdf | ppmtopgm | pgmtopbm -threshold | \
	          ppmtobmp -bpp 1 > size_test.bmp

clean:
	 rm -f *~ *.aux *.log *.pdf *.png *.scr *.bmp
