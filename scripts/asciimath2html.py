import sys, os
temp_path = os.path.join('..', 'asciitomathml')
# sys.path.append(temp_path)
from xml.etree.ElementTree import Element, tostring
import xml.etree.ElementTree as etree
import asciitomathml.asciitomathml
import argparse
import codecs

def paragraphs(file_obj, separator=None):
    if not callable(separator):
        def separator(line): return line == '\n'
    paragraph = []
    for line in file_obj:
        if line.startswith(u'\ufeff'):
            line = line[1:]
        if separator(line):
            if paragraph:
                yield ''.join(paragraph)
                paragraph = []
        else:
            paragraph.append(line)
    if paragraph: yield ''.join(paragraph)

def insert_text(html_obj, text):
    if not text:
        return
    body = html_obj[1]
    p = body[-1]
    exists_text = p.text
    if not exists_text:
        exists_text = ''
    if len(p) != 0:
        append = p[-1]
        append.tail = text
    else:
        p.text = exists_text + text


def insert_math(p, line):
    math_obj =  asciitomathml.asciitomathml.AsciiMathML(mstyle={'displaystyle':'true'})
    math_obj.parse_string(line)
    math_tree = math_obj.get_tree()
    p.append(math_tree)


def read_file(file_obj):
    it_obj = paragraphs(file_obj)
    html_obj = make_html_tree()
    body = html_obj[1]
    for para in it_obj:
        p = Element('p')
        body.append(p)
        the_string = para
        while the_string:
            the_index = the_string.find('`')
            if the_index > -1:
                start = the_string[:the_index]
                insert_text(html_obj, start)
                the_string = the_string[the_index + 1:]
                the_index = the_string.find('`')
                if the_index > -1:
                    math = the_string[:the_index]
                    the_string = the_string[the_index + 1:]
                    insert_math(p, math)
                else:
                    math = the_string
                    insert_math(p, math)
                    break
            else:
                insert_text(html_obj, the_string)
                break
    return html_obj

def get_options():
    parser = argparse.ArgumentParser(description='Convert ASCII text to HTML')
    parser.add_argument('in_file', default = sys.stdin, nargs='?',
                help = 'the file to input; default is standard in')
    args =  parser.parse_args()
    return args

def ascii_to_math_tree(the_string):
    math_obj =  asciitomathml.AsciiMathML()
    math_obj.parse_string(the_string)
    math_tree = math_obj.get_tree()
    return math_tree

def make_html_tree():
    html = Element('html')
    head = Element('head')
    html.append(head)
    title = Element('title')
    title.text = 'ASCIIMathml Example'
    head.append(title)
    body = Element('body')
    html.append(body)
    return html

def main():
    args = get_options()
    in_file = args.in_file
    if isinstance(in_file, str):
        read_obj = open(in_file, 'r')
    else:
        read_obj = args.in_file
    html_obj = read_file(read_obj)
    read_obj.close()
    final_string = tostring(html_obj, encoding="unicode")
    print(final_string)


if __name__ == '__main__':
    main()

