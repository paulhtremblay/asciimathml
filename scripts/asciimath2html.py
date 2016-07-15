import sys, os
temp_path = os.path.join('..', 'asciitomathml')
# sys.path.append(temp_path)
from xml.etree.ElementTree import Element, tostring
import xml.etree.ElementTree as etree
import asciitomathml.asciitomathml 
import argparse
ns = "{http://www.w3.org/1999/xhtml}"

def paragraphs(file, separator=None):
    if not callable(separator):
        def separator(line): return line == '\n'
    paragraph = []
    for line in file:
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
        if isinstance(para, str) and  sys.version_info < (3,):
            para = para.decode('utf8')
        p = Element(ns + 'p')
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
    parser = argparse.ArgumentParser(description='Convert ASCII text to FO')
    parser.add_argument('in_file', default = sys.stdin, nargs='?', 
                help = 'the file to input; default is standard in')
    args =  parser.parse_args()
    return args

def ascii_to_math_tree(the_string):
    if isinstance(the_string, str) and  sys.version_info < (3,):
        the_string = the_string.decode('utf8')
    math_obj =  asciitomathml.AsciiMathML()
    math_obj.parse_string(the_string)
    math_tree = math_obj.get_tree()
    return math_tree

def make_html_tree():
    html = Element(ns + 'html')
    html.set('xmlns:mml', 'http://www.w3.org/1998/Math/MathML')
    head = Element(ns + 'head')
    html.append(head)
    title = Element(ns + 'title')
    title.text = 'ASCIIMathml Example'
    head.append(title)
    body = Element(ns + 'body')
    html.append(body)
    return html

def main():
    xml_pi= etree.ProcessingInstruction('xml' , text='version="1.0"')
    args = get_options()
    in_file = args.in_file
    if isinstance(in_file, str):
        read_obj = open(in_file, 'r')
    else:
        read_obj = args.in_file 

    html_obj = read_file(read_obj)
    read_obj.close()
    if  sys.version_info < (3,):
        print(tostring(xml_pi))
        print(tostring(html_obj))
    else:
        print(tostring(xml_pi, encoding=str))
        print(tostring(html_obj, encoding=str))


if __name__ == '__main__':
    main()
