textbook.pdf: textbook.tex textbook.bib Makefile
	pdflatex textbook
	echo makeindex textbook -s StyleInd.ist
	biber textbook
	pdflatex textbook
	pdflatex textbook

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
