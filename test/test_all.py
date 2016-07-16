import sys
import os
import unittest
import xml.etree.ElementTree as ET

def _check_dir():
    cur_dir = os.path.curdir
    all_paths = os.listdir(cur_dir)
    path_to_test = os.path.join('test', 'test_all.py')
    if not os.path.isfile(path_to_test):
        return False
    if os.path.abspath(path_to_test) != os.path.abspath(__file__):
        return False
    return True

def setup():
    if not _check_dir():
        sys.stderr.write("Please be in home directory to run\n")
        sys.exit(1)
sys.path.insert(0, ".")
import asciitomathml.asciitomathml


def convert_string_to_tree(xmlString):
    return ET.fromstring(xmlString)

def xml_compare_strings(x1, x2):
    x1 = convert_string_to_tree(x1)
    x2 = convert_string_to_tree(x2)
    t = xml_compare(x1, x2)
    return t

def xml_compare(x1, x2, excludes=[]):
    """
    Compares two xml etrees
    :param x1: the first tree
    :param x2: the second tree
    :param excludes: list of string of attributes to exclude from comparison
    :return:
        True if both files match
    """

    if x1.tag != x2.tag:
        return False
    for name, value in x1.attrib.items():
        if not name in excludes:
            if x2.attrib.get(name) != value:
                return False
    for name in x2.attrib.keys():
        if not name in excludes:
            if name not in x1.attrib:
                return False
    if not text_compare(x1.text, x2.text):
        return False
    if not text_compare(x1.tail, x2.tail):
        return False
    cl1 = x1.getchildren()
    cl2 = x2.getchildren()
    if len(cl1) != len(cl2):
        return False
    i = 0
    for c1, c2 in zip(cl1, cl2):
        i += 1
        if not c1.tag in excludes:
            if not xml_compare(c1, c2, excludes):
                return False
    return True

def text_compare(t1, t2):
    """
    Compare two text strings
    :param t1: text one
    :param t2: text two
    :return:
        True if a match
    """
    if not t1 and not t2:
        return True
    if t1 == '*' or t2 == '*':
        return True
    return (t1 or '').strip() == (t2 or '').strip()

class MyTest(unittest.TestCase):

    def setUp(self):
        pass


    def test_tree_compare1(self):
        x1 = """<root>   </root>
        """
        x2 = """<root> </root> """
        t =  xml_compare_strings( x1, x2)
        self.assertTrue(t)

    def test_simple_variable(self):
        math_obj =  asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'x'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True) # xml_string is an XML string
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mi>x</mi>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_simple_number(self):
        math_obj =  asciitomathml.asciitomathml.AsciiMathML()
        the_string = '1'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True) # xml_string is an XML string
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mn>1</mn>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_simple_negative_number(self):
        math_obj =  asciitomathml.asciitomathml.AsciiMathML()
        the_string = '-1'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True) # xml_string is an XML string
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mo>-</mo>
               <mn>1</mn>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_simple_operator(self):
        math_obj =  asciitomathml.asciitomathml.AsciiMathML()
        the_string = '+'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True) # xml_string is an XML string
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mo>+</mo>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_simple_ascii_symbol(self):
        math_obj =  asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'alpha'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True) # xml_string is an XML string
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mi>α</mi>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))


    def test_x_squared(self):
        math_obj =  asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'x^2'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True) # xml_string is an XML string
        needs = """<math xmlns="http://www.w3.org/1998/Math/MathML"><mstyle><msup><mi>x</mi><mn>2</mn></msup></mstyle></math>"""
        self.assertTrue(xml_compare_strings(xml_string, needs))


if __name__ == '__main__':
    setup()
    unittest.main()

