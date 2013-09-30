ART=lit_forensic
CLEANFILES=american_scientist.pdf american_scientist.rtf

#lit_forensic.pdf: file_type_identification.tex unicode.tex

SHELL:=$(shell which bash) 
TEX_INPUTS:=.:..:$$DOMEX_HOME/papers/npsreport/:$$DOMEX_HOME/papers/bib/:$$TEXINPUTS:$(TEX_INPUTS)
BIB_INPUTS:=.:..:$$DOMEX_HOME/papers/npsreport/:$$DOMEX_HOME/papers/bib/:$$BIBINPUTS:$(BIB_INPUTS)
BST_INPUTS:=.:..:$$DOMEX_HOME/papers/npsreport/:$$DOMEX_HOME/papers/bib/:$$BSTINPUTS:$(BST_INPUTS)

$(ART).pdf: $(ART).tex Makefile  $(ART).bib 
	if [ x$$DOMEX_HOME == x ]; then echo PLEASE SET THE DOMEX_HOME ENVIRONMENT VARIABLE; exit 1; fi
	/bin/rm -f $(ART).aux
	(export TEXINPUTS=$(TEX_INPUTS);pdflatex $(ART))
	make $(ART).bbl
	(export TEXINPUTS=$(TEX_INPUTS);pdflatex $(ART))
	(export TEXINPUTS=$(TEX_INPUTS);pdflatex $(ART))
	(export TEXINPUTS=$(TEX_INPUTS);pdflatex $(ART))
	echo ""
	echo ""
	(echo Undefined References:;cat $(ART).log) | grep -i undefin
	(echo Warnings:;cat $(ART).log) | grep -i warning

$(ART).bbl: $(ART).aux
	(export BIBINPUTS=$(BIB_INPUTS);export BSTINPUTS=$(BST_INPUTS);if grep bibdata $(ART).aux ; then bibtex $(ART); python fixerrors.py $(ART).bbl ; fi )

$(ART).rtf:		
	latex2rtf $(ART).tex

pub: $(ART).pdf
	scp $(ART).pdf www.simson.net:simson.net/
	@echo
	@echo
	@echo Draft is published to http://www.simson.net/$(ART).pdf

clean:
	rm -f $(ART).{bbl,aux,log,blg,pd,toc,pdf,toc} *.aux *~ $(CLEANFILES)

ignore:
	svn propget svn:ignore . > /tmp/$(ART)
	echo $(ART).pdf >> /tmp/$(ART)
	echo $(ART).log >> /tmp/$(ART)
	echo '*.aux' >> /tmp/$(ART)
	echo '*.bbl' >> /tmp/$(ART)
	echo '*.blg' >> /tmp/$(ART)
	echo '*.log' >> /tmp/$(ART)
	echo '*.sow' >> /tmp/$(ART)
	echo '*.spl' >> /tmp/$(ART)
	echo '*.toc' >> /tmp/$(ART)
	echo '*.zip' >> /tmp/$(ART)
	echo '*.out' >> /tmp/$(ART)
	echo '*.idx' >> /tmp/$(ART)
	sort /tmp/$(ART) | uniq | grep . | svn propset svn:ignore -F - . 
	@echo ""
	@echo Will ignore:  
	svn propget svn:ignore .
	svn update .
	@/bin/rm -f /tmp/$(ART)
