#
# Book without orange. It just wasn't working

CLEANFILES=main.pdf plainbook.pdf book.pdf *.{aux,bbl,blg,idx,ilg,ind,log,out,run.xml,toc}
TEXFILES=$(wildcard *.tex)

book.pdf: book.tex ../bib/textbook.bib Makefile $(TEXFILES) $(wildcard */*.tex) $(wildcard */*.py) book-body.tex
	/bin/rm -f $(CLEANFILES)
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
