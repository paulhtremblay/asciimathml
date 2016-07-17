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
        xml_string = math_obj.to_xml_string(as_string = True) 
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
        xml_string = math_obj.to_xml_string(as_string = True)
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
        xml_string = math_obj.to_xml_string(as_string = True)
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
        xml_string = math_obj.to_xml_string(as_string = True)
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
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mi>α</mi>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_simple_addition(self):
        math_obj =  asciitomathml.asciitomathml.AsciiMathML()
        the_string = '1 + 1'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mn>1</mn>
               <mo>+</mo>
               <mn>1</mn>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_simple_fraction(self):
        math_obj =  asciitomathml.asciitomathml.AsciiMathML()
        the_string = '1/2'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mfrac>
                  <mn>1</mn>
                  <mn>2</mn>
               </mfrac>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_double_fraction(self):
        math_obj =  asciitomathml.asciitomathml.AsciiMathML()
        the_string = '1/2/3/4'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mfrac>
                  <mfrac>
                     <mn>1</mn>
                     <mn>2</mn>
                  </mfrac>
                  <mfrac>
                     <mn>3</mn>
                     <mn>4</mn>
                  </mfrac>
               </mfrac>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_tripple_fraction(self):
        math_obj =  asciitomathml.asciitomathml.AsciiMathML()
        the_string = '1/2/3/4/5/6'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mfrac>
                  <mfrac>
                     <mn>1</mn>
                     <mn>2</mn>
                  </mfrac>
                  <mfrac>
                     <mfrac>
                        <mn>3</mn>
                        <mn>4</mn>
                     </mfrac>
                     <mfrac>
                        <mn>5</mn>
                        <mn>6</mn>
                     </mfrac>
                  </mfrac>
               </mfrac>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))


    def test_parenthesis(self):
        math_obj =  asciitomathml.asciitomathml.AsciiMathML()
        the_string = '(6)'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mfenced close=")" open="(" separators="">
                  <mn>6</mn>
               </mfenced>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_left_parenthesis(self):
        math_obj =  asciitomathml.asciitomathml.AsciiMathML()
        the_string = '(6'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mo>(</mo>
               <mn>6</mn>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_right_parenthesis(self):
        math_obj =  asciitomathml.asciitomathml.AsciiMathML()
        the_string = '6)'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mn>6</mn>
               <mo>)</mo>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_fraction_needs_parenthesis(self):
        math_obj =  asciitomathml.asciitomathml.AsciiMathML()
        the_string = '(a + b)/c'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mfrac>
                  <mrow class="nominator">
                     <mi>a</mi>
                     <mo>+</mo>
                     <mi>b</mi>
                  </mrow>
                  <mi>c</mi>
               </mfrac>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_simple_superscript(self):
        math_obj =  asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'b^2'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <msup>
                  <mi>b</mi>
                  <mn>2</mn>
               </msup>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_superscript_with_complex_fraction(self):
        math_obj =  asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'b^((c + d)/(e + f))'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <msup>
                  <mi>b</mi>
                  <mrow class="superscript">
                     <mfrac>
                        <mrow class="nominator">
                           <mi>c</mi>
                           <mo>+</mo>
                           <mi>d</mi>
                        </mrow>
                        <mrow class="denominator">
                           <mi>e</mi>
                           <mo>+</mo>
                           <mi>f</mi>
                        </mrow>
                     </mfrac>
                  </mrow>
               </msup>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_single_double_bar(self):
        math_obj =  asciitomathml.asciitomathml.AsciiMathML()
        the_string = '||'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mfenced close="" open="&#x2016;" separators=""></mfenced>
            </mstyle>
         </math>
         """
        t = xml_compare_strings(xml_string, needs)
        if not t:
            needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mo>‖</mo>
            </mstyle>
         </math>
             """
            self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_double_bar_with_addition(self):
        math_obj =  asciitomathml.asciitomathml.AsciiMathML()
        the_string = '|| 4 + 5 ||'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mfenced close="&#x2016;" open="&#x2016;" separators="">
                  <mn>4</mn>
                  <mo>+</mo>
                  <mn>5</mn>
               </mfenced>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_complex_double_bar(self):
        math_obj =  asciitomathml.asciitomathml.AsciiMathML()
        the_string = '|| (a + b)/(c+d) ||^2'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <msup>
                  <mfenced close="&#x2016;" open="&#x2016;" separators="">
                     <mfrac>
                        <mrow class="nominator">
                           <mi>a</mi>
                           <mo>+</mo>
                           <mi>b</mi>
                        </mrow>
                        <mrow class="denominator">
                           <mi>c</mi>
                           <mo>+</mo>
                           <mi>d</mi>
                        </mrow>
                     </mfrac>
                  </mfenced>
                  <mn>2</mn>
               </msup>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_simple_sub_super(self):
        math_obj =  asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'a_b^2'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <msubsup>
                  <mi>a</mi>
                  <mi>b</mi>
                  <mn>2</mn>
               </msubsup>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_simple_sum(self):
        math_obj =  asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'sum'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mo>∑</mo>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_sum_with_base(self):
        math_obj =  asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'sum_b'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <munder>
                  <mo>∑</mo>
                  <mi>b</mi>
               </munder>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_sum_with_super(self):
        math_obj =  asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'sum^6'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mover>
                  <mo>∑</mo>
                  <mn>6</mn>
               </mover>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_sum_with_munder_and_mover(self):
        math_obj =  asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'sum_(n=1)^oo = 1/2 + 1/4 + 1/8 + ...'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <munderover>
                  <mo>∑</mo>
                  <mrow class="munder">
                     <mi>n</mi>
                     <mo>=</mo>
                     <mn>1</mn>
                  </mrow>
                  <mo>∞</mo>
               </munderover>
               <mo>=</mo>
               <mfrac>
                  <mn>1</mn>
                  <mn>2</mn>
               </mfrac>
               <mo>+</mo>
               <mfrac>
                  <mn>1</mn>
                  <mn>4</mn>
               </mfrac>
               <mo>+</mo>
               <mfrac>
                  <mn>1</mn>
                  <mn>8</mn>
               </mfrac>
               <mo>+</mo>
               <mo>...</mo>
            </mstyle>
         </math>
         """
        t = xml_compare_strings(xml_string, needs)
        if not t:
            needs ="""
        <math xmlns="http://www.w3.org/1998/Math/MathML">
          <mstyle>
            <munderover>
              <mo>∑</mo>
              <mrow class="munder">
                <mi>n</mi>
                <mo>=</mo>
                <mn>1</mn>
              </mrow>
              <mo>∞</mo>
            </munderover>
            <mo>=</mo>
            <mfrac>
              <mn>1</mn>
              <mn>2</mn>
            </mfrac>
            <mo>+</mo>
            <mfrac>
              <mn>1</mn>
              <mn>4</mn>
            </mfrac>
            <mo>+</mo>
            <mfrac>
              <mn>1</mn>
              <mn>8</mn>
            </mfrac>
            <mo>+</mo>
            <mo>…</mo>
          </mstyle>
        </math>
            """
            self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_product_with_munder_and_mover(self):
        math_obj =  asciitomathml.asciitomathml.AsciiMathML()
        the_string = '∏_b^2'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <munderover>
                  <mo>∏</mo>
                  <mi>b</mi>
                  <mn>2</mn>
               </munderover>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_hat_with_munder_and_mover(self):
        math_obj =  asciitomathml.asciitomathml.AsciiMathML()
        the_string = '^^^_b^2'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <munderover>
                  <mo>⋀</mo>
                  <mi>b</mi>
                  <mn>2</mn>
               </munderover>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_big_vvv_with_munder_and_mover(self):
        math_obj =  asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'vvv_b^2'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <munderover>
                  <mo>⋁</mo>
                  <mi>b</mi>
                  <mn>2</mn>
               </munderover>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_nnn_with_munder_and_mover(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'nnn_b^2'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <munderover>
                  <mo>⋂</mo>
                  <mi>b</mi>
                  <mn>2</mn>
               </munderover>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_uuu_with_munder_and_mover(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'uuu_b^2'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <munderover>
                  <mo>⋃</mo>
                  <mi>b</mi>
                  <mn>2</mn>
               </munderover>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_min_with_under_and_over(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'min_b^2'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <munderover>
                  <mo>min</mo>
                  <mi>b</mi>
                  <mn>2</mn>
               </munderover>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_max_with_munder_and_mover(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'max_b^2'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <munderover>
                  <mo>max</mo>
                  <mi>b</mi>
                  <mn>2</mn>
               </munderover>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_simple_brackets(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = '{a + b}'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mfenced close="}" open="{" separators="">
                  <mi>a</mi>
                  <mo>+</mo>
                  <mi>b</mi>
               </mfenced>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_brackets_with_fraction(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = '({x + 5}/{x -5})'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mfenced close=")" open="(" separators="">
                  <mfrac>
                     <mrow class="nominator">
                        <mi>x</mi>
                        <mo>+</mo>
                        <mn>5</mn>
                     </mrow>
                     <mrow class="denominator">
                        <mi>x</mi>
                        <mo>-</mo>
                        <mn>5</mn>
                     </mrow>
                  </mfrac>
               </mfenced>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_brackets_with_square(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = '[x -5]^2'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <msup>
                  <mfenced close="]" open="[" separators="">
                     <mi>x</mi>
                     <mo>-</mo>
                     <mn>5</mn>
                  </mfenced>
                  <mn>2</mn>
               </msup>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_parenthesis_colon(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = '(: x + y :)'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mfenced close="〉" open="〈" separators="">
                  <mi>x</mi>
                  <mo>+</mo>
                  <mi>y</mi>
               </mfenced>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_parenthesis_colon_with_fraction(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = '(: x + y :)/ (: x - y :)'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mfrac>
                  <mfenced close="〉" open="〈" separators="">
                     <mi>x</mi>
                     <mo>+</mo>
                     <mi>y</mi>
                  </mfenced>
                  <mfenced close="〉" open="〈" separators="">
                     <mi>x</mi>
                     <mo>-</mo>
                     <mi>y</mi>
                  </mfenced>
               </mfrac>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_gt_with_fraction(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = '<< x + y >>/ << x - y >>'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mfrac>
                  <mfenced close="〉" open="〈" separators="">
                     <mi>x</mi>
                     <mo>+</mo>
                     <mi>y</mi>
                  </mfenced>
                  <mfenced close="〉" open="〈" separators="">
                     <mi>x</mi>
                     <mo>-</mo>
                     <mi>y</mi>
                  </mfenced>
               </mfrac>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_brackets_colon(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = '{: 5 + 7 :}'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mrow class="invisible">
                  <mn>5</mn>
                  <mo>+</mo>
                  <mn>7</mn>
               </mrow>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_superscript_with_brackets(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'B^{: 5 + 7 :}'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <msup>
                  <mi>B</mi>
                  <mrow class="superscript">
                     <mn>5</mn>
                     <mo>+</mo>
                     <mn>7</mn>
                  </mrow>
               </msup>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_hat_5(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'hat 5'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mover class="hat">
                  <mn>5</mn>
                  <mo>^</mo>
               </mover>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_hat_with_double_base(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'hat (5 6)'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mover class="hat">
                  <mrow class="mover">
                     <mn>5</mn>
                     <mn>6</mn>
                  </mrow>
                  <mo>^</mo>
               </mover>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_bar_with_double_base(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'bar (5 6)'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mover class="bar">
                  <mrow class="mover">
                     <mn>5</mn>
                     <mn>6</mn>
                  </mrow>
                  <mo>¯</mo>
               </mover>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_vec_with_double_base(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'vec (5 6)'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mover class="vec">
                  <mrow class="mover">
                     <mn>5</mn>
                     <mn>6</mn>
                  </mrow>
                  <mo>→</mo>
               </mover>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_dot_with_double_base(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'dot (5 6)'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mover class="dot">
                  <mrow class="mover">
                     <mn>5</mn>
                     <mn>6</mn>
                  </mrow>
                  <mo>.</mo>
               </mover>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_ddot_with_double_base(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'ddot (5 6)'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mover class="ddot">
                  <mrow class="mover">
                     <mn>5</mn>
                     <mn>6</mn>
                  </mrow>
                  <mo>..</mo>
               </mover>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_ul_with_double_base(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'ul (5 6)'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <munder class="ul">
                  <mrow class="munder">
                     <mn>5</mn>
                     <mn>6</mn>
                  </mrow>
                  <mo>̲</mo>
               </munder>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_mtext(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'text(sum vs.) sum'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mtext>sum vs.</mtext>
               <mo>∑</mo>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_mroot(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'root (2 + 1) ((b^2 - 4ac)/b)'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mroot>
                  <mrow class="base">
                     <mfrac>
                        <mrow class="nominator">
                           <msup>
                              <mi>b</mi>
                              <mn>2</mn>
                           </msup>
                           <mo>-</mo>
                           <mn>4</mn>
                           <mi>a</mi>
                           <mi>c</mi>
                        </mrow>
                        <mi>b</mi>
                     </mfrac>
                  </mrow>
                  <mrow class="index">
                     <mn>2</mn>
                     <mo>+</mo>
                     <mn>1</mn>
                  </mrow>
               </mroot>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_frac(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'frac a (b - a)'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mfrac>
                  <mi>a</mi>
                  <mrow class="denominator">
                     <mi>b</mi>
                     <mo>-</mo>
                     <mi>a</mi>
                  </mrow>
               </mfrac>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_sqrt(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'sqrt(a^2 - 4ac) + 4'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <msqrt>
                  <mrow class="radical">
                     <msup>
                        <mi>a</mi>
                        <mn>2</mn>
                     </msup>
                     <mo>-</mo>
                     <mn>4</mn>
                     <mi>a</mi>
                     <mi>c</mi>
                  </mrow>
               </msqrt>
               <mo>+</mo>
               <mn>4</mn>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_max_underover_as_function(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'max_i^j(x)'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <munderover>
                  <mo>max</mo>
                  <mi>i</mi>
                  <mi>j</mi>
               </munderover>
               <mfenced close=")" open="(" separators="">
                  <mi>x</mi>
               </mfenced>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_lim(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'lim_i^j(x)'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <munderover>
                  <mo>lim</mo>
                  <mi>i</mi>
                  <mi>j</mi>
               </munderover>
               <mfenced close=")" open="(" separators="">
                  <mi>x</mi>
               </mfenced>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_lim2(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'Lim_(i + 1)^j x'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <munderover>
                  <mo>Lim</mo>
                  <mrow class="munder">
                     <mi>i</mi>
                     <mo>+</mo>
                     <mn>1</mn>
                  </mrow>
                  <mi>j</mi>
               </munderover>
               <mi>x</mi>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_sin(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'sin (x + 5)'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mo>sin</mo>
               <mfenced close=")" open="(" separators="">
                  <mrow class="function">
                     <mi>x</mi>
                     <mo>+</mo>
                     <mn>5</mn>
                  </mrow>
               </mfenced>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_cos(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'cos (x + 5)'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mo>cos</mo>
               <mfenced close=")" open="(" separators="">
                  <mrow class="function">
                     <mi>x</mi>
                     <mo>+</mo>
                     <mn>5</mn>
                  </mrow>
               </mfenced>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_tan(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'tan (x + 5)'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mo>tan</mo>
               <mfenced close=")" open="(" separators="">
                  <mrow class="function">
                     <mi>x</mi>
                     <mo>+</mo>
                     <mn>5</mn>
                  </mrow>
               </mfenced>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_open_matrix(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = '|x|= {(x , if x ge 0 text(,)),(-x , if x < 0.):}'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mfenced close="|" open="|" separators="">
                  <mi>x</mi>
               </mfenced>
               <mo>=</mo>
               <mfenced class="invisible" close="" open="{" separators="">
                  <mtable>
                     <mtr>
                        <mtd>
                           <mi>x</mi>
                        </mtd>
                        <mtd>
                           <mspace width="1ex"></mspace>
                           <mo>if</mo>
                           <mspace width="1ex"></mspace>
                           <mi>x</mi>
                           <mo>≥</mo>
                           <mn>0</mn>
                           <mtext>,</mtext>
                        </mtd>
                     </mtr>
                     <mtr>
                        <mtd>
                           <mo>-</mo>
                           <mi>x</mi>
                        </mtd>
                        <mtd>
                           <mspace width="1ex"></mspace>
                           <mo>if</mo>
                           <mspace width="1ex"></mspace>
                           <mi>x</mi>
                           <mo>&lt;</mo>
                           <mn>0.</mn>
                        </mtd>
                     </mtr>
                  </mtable>
               </mfenced>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_simple_matrix(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = '((1,2),(1,2))'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mfenced close=")" open="(" separators="">
                  <mtable>
                     <mtr>
                        <mtd>
                           <mn>1</mn>
                        </mtd>
                        <mtd>
                           <mn>2</mn>
                        </mtd>
                     </mtr>
                     <mtr>
                        <mtd>
                           <mn>1</mn>
                        </mtd>
                        <mtd>
                           <mn>2</mn>
                        </mtd>
                     </mtr>
                  </mtable>
               </mfenced>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_bar_with_non_maching(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = '(a,b]={x in RR | a < x <= b}'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mo>(</mo>
               <mi>a</mi>
               <mo>,</mo>
               <mi>b</mi>
               <mo>]</mo>
               <mo>=</mo>
               <mfenced close="}" open="{" separators="">
                  <mi>x</mi>
                  <mo>∈</mo>
                  <mo>ℝ</mo>
                  <mo>|</mo>
                  <mi>a</mi>
                  <mo>&lt;</mo>
                  <mi>x</mi>
                  <mo>≤</mo>
                  <mi>b</mi>
               </mfenced>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_incomplete_fraction(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'alpha /'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mfrac>
                  <mi>α</mi>
                  <mo></mo>
               </mfrac>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_incomplete_root1(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'root 1'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mroot>
                  <mo></mo>
                  <mn>1</mn>
               </mroot>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_incomplete_root2(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'root'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mroot>
                  <mo></mo>
                  <mo></mo>
               </mroot>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_incomplete_hat(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'hat'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mover class="hat">
                  <mo></mo>
                  <mo>^</mo>
               </mover>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_incomplete_vec(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'vec'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mover class="vec">
                  <mo></mo>
                  <mo>→</mo>
               </mover>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_incomplete_dot(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'dot'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mover class="dot">
                  <mo></mo>
                  <mo>.</mo>
               </mover>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_incomplete_ddot(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'ddot'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mover class="ddot">
                  <mo></mo>
                  <mo>..</mo>
               </mover>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_incomplete_ul(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'ul'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <munder class="ul">
                  <mo></mo>
                  <mo>̲</mo>
               </munder>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_incomplete_frac(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'frac'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mfrac>
                  <mo></mo>
                  <mo></mo>
               </mfrac>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_incomplete_sum1(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'sum_'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <munder>
                  <mo>∑</mo>
                  <mo></mo>
               </munder>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_incomplete_sum2(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'sum_^'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <munder>
                  <mover>
                     <mo>∑</mo>
                     <mo></mo>
                  </mover>
                  <mo></mo>
               </munder>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_incomplete_munderover(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'sum_b^'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <munderover>
                  <mo>∑</mo>
                  <mi>b</mi>
                  <mo></mo>
               </munderover>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_incomplete_superscript(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'b^'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <msup>
                  <mi>b</mi>
                  <mo></mo>
               </msup>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_incomplete_subscript(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'b_'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <msub>
                  <mi>b</mi>
                  <mo></mo>
               </msub>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_incomplete_subsup(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'b_a^'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <msubsup>
                  <mi>b</mi>
                  <mi>a</mi>
                  <mo></mo>
               </msubsup>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_external1(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'abc-123.45^-1.1'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mi>a</mi>
               <mi>b</mi>
               <mi>c</mi>
               <mo>-</mo>
               <msup>
                  <mn>123.45</mn>
                  <mrow class="neg-num">
                     <mo>-</mo>
                     <mn>1.1</mn>
                  </mrow>
               </msup>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_incomplete_text(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'text alpha'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mtext></mtext>
               <mi>α</mi>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_text_with_curly_brackets(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'text{undefined}'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mtext>undefined</mtext>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_empty_text(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'text'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mtext></mtext>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_over_many(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'hat(ab) bar(xy) ulA vec v dotx ddot y'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mover class="hat">
                  <mrow class="mover">
                     <mi>a</mi>
                     <mi>b</mi>
                  </mrow>
                  <mo>^</mo>
               </mover>
               <mover class="bar">
                  <mrow class="mover">
                     <mi>x</mi>
                     <mi>y</mi>
                  </mrow>
                  <mo>¯</mo>
               </mover>
               <munder class="ul">
                  <mi>A</mi>
                  <mo>̲</mo>
               </munder>
               <mover class="vec">
                  <mi>v</mi>
                  <mo>→</mo>
               </mover>
               <mover class="dot">
                  <mi>x</mi>
                  <mo>.</mo>
               </mover>
               <mover class="ddot">
                  <mi>y</mi>
                  <mo>..</mo>
               </mover>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_two_matrices(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = '[[a,b],[c,d]]((n),(k))'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mfenced close="]" open="[" separators="">
                  <mtable>
                     <mtr>
                        <mtd>
                           <mi>a</mi>
                        </mtd>
                        <mtd>
                           <mi>b</mi>
                        </mtd>
                     </mtr>
                     <mtr>
                        <mtd>
                           <mi>c</mi>
                        </mtd>
                        <mtd>
                           <mi>d</mi>
                        </mtd>
                     </mtr>
                  </mtable>
               </mfenced>
               <mfenced close=")" open="(" separators="">
                  <mtable>
                     <mtr>
                        <mtd>
                           <mi>n</mi>
                        </mtd>
                     </mtr>
                     <mtr>
                        <mtd>
                           <mi>k</mi>
                        </mtd>
                     </mtr>
                  </mtable>
               </mfenced>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

    def test_least_squares(self):
        math_obj = asciitomathml.asciitomathml.AsciiMathML()
        the_string = 'hat beta = (X′X)^-1X′y (1/n sum x_i x_i′)^-1(1/n sum x_i y_i)'
        math_obj.parse_string(the_string)
        xml_string = math_obj.to_xml_string(as_string = True)
        needs = """
         <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mstyle>
               <mover class="hat">
                  <mi>β</mi>
                  <mo>^</mo>
               </mover>
               <mo>=</mo>
               <msup>
                  <mfenced close=")" open="(" separators="">
                     <mi>X</mi>
                     <mo>′</mo>
                     <mi>X</mi>
                  </mfenced>
                  <mrow class="neg-num">
                     <mo>-</mo>
                     <mn>1</mn>
                  </mrow>
               </msup>
               <mi>X</mi>
               <mo>′</mo>
               <mi>y</mi>
               <msup>
                  <mfenced close=")" open="(" separators="">
                     <mfrac>
                        <mn>1</mn>
                        <mi>n</mi>
                     </mfrac>
                     <mo>∑</mo>
                     <msub>
                        <mi>x</mi>
                        <mi>i</mi>
                     </msub>
                     <msub>
                        <mi>x</mi>
                        <mi>i</mi>
                     </msub>
                     <mo>′</mo>
                  </mfenced>
                  <mrow class="neg-num">
                     <mo>-</mo>
                     <mn>1</mn>
                  </mrow>
               </msup>
               <mfenced close=")" open="(" separators="">
                  <mfrac>
                     <mn>1</mn>
                     <mi>n</mi>
                  </mfrac>
                  <mo>∑</mo>
                  <msub>
                     <mi>x</mi>
                     <mi>i</mi>
                  </msub>
                  <msub>
                     <mi>y</mi>
                     <mi>i</mi>
                  </msub>
               </mfenced>
            </mstyle>
         </math>
         """
        self.assertTrue(xml_compare_strings(xml_string, needs))

if __name__ == '__main__':
    setup()
    unittest.main()

