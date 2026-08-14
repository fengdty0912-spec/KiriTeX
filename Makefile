.PHONY: all a4 pad clean

all: a4 pad

a4:
	xelatex -interaction=nonstopmode -halt-on-error demo-a4.tex
	xelatex -interaction=nonstopmode -halt-on-error demo-a4.tex

pad:
	xelatex -interaction=nonstopmode -halt-on-error demo-pad.tex
	xelatex -interaction=nonstopmode -halt-on-error demo-pad.tex

clean:
	rm -f *.aux *.log *.out *.toc *.pdf *.synctex.gz

# Future multi-format targets (via pandoc):
# html: ...
# md: ...
# pptx: ...
