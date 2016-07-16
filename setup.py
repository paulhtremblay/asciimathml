import sys, os
from distutils.core import setup
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

script_name1 =  os.path.join('scripts', 'asciimath2fo.py')
script_name2 =  os.path.join('scripts', 'asciimath2html.py')


setup(name="asciitomathml",
    version= "1.0" ,
    description="Module converts ASCII math to Mathml",
    long_description=read('README'),
    author="Paul Tremblay",
    author_email="Paul Henry Tremblay <paultremblay@users.sourceforge.net> ",
    license = 'BSD',
    url = "https://sourceforge.net/projects/asciimathpython/",
    classifiers=[
        "Topic :: Documentation",
        "Topic :: Software Development :: Documentation",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
    ],
    platforms='any',
    packages=['asciitomathml'],
    scripts=[script_name1, script_name2],
    )
