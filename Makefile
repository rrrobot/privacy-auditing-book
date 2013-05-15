textbook.pdf: textbook.tex
	pdflatex textbook
	bibtex textbook
	pdflatex textbook
	pdflatex textbook
