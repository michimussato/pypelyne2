http://www.sphinx-doc.org/en/stable/man/sphinx-apidoc.html

cd "C:\Users\michaelt\git\pypelyne2"
sphinx-apidoc -d 7 --full -H "pypelyne2" -A "Michael Mussato" -V "0" -R "0" -o "C:\Users\michaelt\git\pypelyne2\pypelyne2\doc\sphinx" ".\pypelyne2" ".\pypelyne2\payload" ".\pypelyne2\doc"

cd "C:\Users\michaelt\git\pypelyne2\pypelyne2\doc\sphinx"
make html
