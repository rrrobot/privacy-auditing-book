#
# Book without orange. It just wasn't working

CLEANFILES=$(wildcard *.{aux,bbl,blg,idx,ilg,ind,log,out,run.xml,toc}) main.pdf plainbook.pdf book.pdf

book.pdf: book.tex ../bib/textbook.bib Makefile $(wildcard *.tex) $(wildcard */*.tex) $(wildcard */*.py)
	pdflatex book
	makeindex book -s orange/StyleInd.ist
	bibtex8 book
	pdflatex book
	pdflatex book

g:
	pdflatex book
	open book.pdf

plainbook: plainbook.pdf

pb: plainbook.pdf

plainbook.pdf: plainbook.tex 
	pdflatex plainbook
	bibtex plainbook
	pdflatex plainbook
	pdflatex plainbook

clean:
	/bin/rm -f $(CLEANFILES)
