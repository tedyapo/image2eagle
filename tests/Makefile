all: font_test.scr

font_test.scr: font_test.tex
	pdflatex -halt-on-error font_test.tex
	pdftoppm -r 1200 font_test.pdf | pnmtopng > font_test.png
	../image2eagle.py font_test.png font_test.scr -d 1200 -n -w 2.5
