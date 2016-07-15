python to_3.py  asciitomathml/asciitomathml.py  > temp.py
cp asciitomathml/asciitomathml.py asciitomathml/asciitomathml.bac.py
mv temp.py asciitomathml/asciitomathml.py
2to3 -w asciitomathml/asciitomathml.py
rm asciitomathml/asciitomathml.bac.py
rm asciitomathml/asciitomathml.py.bak
