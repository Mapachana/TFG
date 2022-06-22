main.pdf: main.tex pseudo_clean #prepare_bibliography
	pdflatex --shell-escape main.tex
	#bibtex main
	pdflatex --shell-escape main.tex
	pdflatex --shell-escape main.tex
	#cp main.pdf ../main.pdf
	$(MAKE) pseudo_clean

pseudo_clean:
	rm -f *.aux *.blg *.log *.bbl *.toc *.out *.bcf *.xml *.synctex.gz *.snm *.nav *.vrb
	rm -f chapters/*.log
	rm -f imports/*.aux imports/*.log
	rm -rf _minted-main

clean: pseudo_clean
	

prepare_bibliography:
	python bib/prepare_bib.py
