name=`echo $1 | sed 's/\.[^\.]*$//'`
platex $name.tex
bibtex $name
platex $name.tex
platex $name.tex
dvipdfmx $name.dvi
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome $name.pdf