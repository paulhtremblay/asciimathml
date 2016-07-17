import sys, os
temp_path = os.path.join('..', 'asciitomathml')
sys.path.append(temp_path)
from xml.etree.ElementTree import Element, tostring
import xml.etree.ElementTree as etree
import asciitomathml.asciitomathml 
import argparse
ns = "{http://www.w3.org/1999/XSL/Format}"

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

def insert_text(fo_obj, text):
    if not text:
        return
    flow = fo_obj[1][0]
    # print(flow[-1])
    block = flow[-1]
    exists_text = block.text
    if not exists_text:
        exists_text = ''
    if len(block) != 0:
        append = block[-1]
        append.tail = text
    else:
        block.text = exists_text + text


def insert_math(block, line):
    instream = Element(ns + 'instream-foreign-object')
    block.append(instream)
    math_obj =  asciitomathml.asciitomathml.AsciiMathML(mstyle={'scriptlevel': '-2'})
    math_obj.parse_string(line)
    math_tree = math_obj.get_tree()
    instream.append(math_tree)


def read_file(file_obj):
    it_obj = paragraphs(file_obj)
    fo_obj = make_fo_tree()
    flow = fo_obj[1][0]
    for para in it_obj:
        block = Element(ns + 'block')
        block.set('space-before', '12pt')
        flow.append(block)
        the_string = para
        while the_string:
            the_index = the_string.find('`')
            if the_index > -1:
                start = the_string[:the_index]
                insert_text(fo_obj, start)
                the_string = the_string[the_index + 1:]
                the_index = the_string.find('`')
                if the_index > -1:
                    math = the_string[:the_index]
                    the_string = the_string[the_index + 1:]
                    insert_math(block, math)
                else:
                    math = the_string
                    insert_math(block, math)
                    break
            else:
                insert_text(fo_obj, the_string)
                break
    return fo_obj

def get_options():
    parser = argparse.ArgumentParser(description='Convert ASCII text to FO')
    parser.add_argument('in_file', default = sys.stdin, nargs='?', 
                help = 'the file to input; default is standard in')
    args =  parser.parse_args()
    return args

def ascii_to_math_tree(the_string):
    math_obj =  asciitomathml.AsciiMathML()
    math_obj.parse_string(the_string)
    math_tree = math_obj.get_tree()
    return math_tree

def make_fo_tree():
    fo = Element(ns + 'root')
    fo.set('font-family', 'STIXGeneral,CharisSIL')
    lo_master = Element(ns + 'layout-master-set')
    fo.append(lo_master)
    sim_page_ms = Element(ns + 'simple-page-master', 
            **{'master-name':'A4',
                'page-height':'11in',
                'page-width':'8.5in',
                'margin-top':'0.5in',
                'margin-left':'0.5in',
                'margin-bottom':'.5in',
                'margin-right':'.5in'
                }
            )
    lo_master.append(sim_page_ms)
    reg_bd = Element(ns + 'region-body', **{'margin-top':'1in'})
    sim_page_ms.append(reg_bd)
    ps = Element(ns + 'page-sequence',  **{'master-reference':'A4'})
    fo.append(ps)
    flow = Element(ns + 'flow', **{'flow-name':'xsl-region-body'})
    ps.append(flow)
    return fo

    print(tostring(fo))

def main():
    args = get_options()
    in_file = args.in_file
    if isinstance(in_file, str):
        read_obj = open(in_file, 'r')
    else:
        read_obj = args.in_file 

    fo_obj = read_file(read_obj)
    read_obj.close()
    print(tostring(fo_obj))


if __name__ == '__main__':
    main()
