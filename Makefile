textbook.pdf: textbook.tex bib/textbook.bib Makefile $(wildcard *.tex)
	pdflatex textbook
	makeindex textbook -s StyleInd.ist
	biber textbook
	pdflatex textbook
	pdflatex textbook

g:
	pdflatex textbook
	open textbook.pdf

plainbook: plainbook.pdf

pb: plainbook.pdf

plainbook.pdf: plainbook.tex 
	pdflatex plainbook
	bibtex plainbook
	pdflatex plainbook
	pdflatex plainbook

clean:
	/bin/rm -f *.{aux,bbl,bcf,blg,log,idx,ptc,run.xml,toc}
	/bin/rm -f main.pdf plainbook.pdf textbook.pdf
