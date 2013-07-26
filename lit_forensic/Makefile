ART=lit_forensic
CLEANFILES=american_scientist.pdf american_scientist.rtf
include ../Makefile.latex
lit_forensic.pdf: file_type_identification.tex unicode.tex

as: american_scientist.pdf american_scientist.rtf

american_scientist.pdf: american_scientist.tex Makefile introduction.tex lit_forensic.bib
	pdflatex american_scientist
	pdflatex american_scientist
	(export BIBINPUTS=$(BIB_INPUTS);export BSTINPUTS=$(BST_INPUTS);	bibtex american_scientist)
	python ../../npsreport/fixerrors.py american_scientist.bbl
	pdflatex american_scientist

american_scientist.rtf: american_scientist.pdf american_scientist.tex
	latex2rtf american_scientist.tex
