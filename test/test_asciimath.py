import sys
# from StringIO import StringIO
from io import StringIO
from xml.etree.ElementTree import Element, tostring
import xml.etree.ElementTree as etree
import xml.sax.handler
from xml.sax.handler import feature_namespaces
import asciitomathml.asciitomathml 

class CopyTree(xml.sax.ContentHandler):
    """
    A simple class that copies a tree. Used for testing two xml strings.

    """


    def __init__(self):
        self.__characters = ''
        self.__xml_string = ''
        self.__default_ns = None
        self.__mathml_ns = 'http://www.w3.org/1998/Math/MathML'


    def characters (self, characters): 
        self.__characters += characters


    def startElementNS(self, name, qname, attrs):
        self.__write_text()
        ns = name[0]
        el_name = name[1]
        root = None
        self.__xml_string += '<'
        if self.__default_ns == None:
            if ns != self.__mathml_ns:
                raise ValueError('wrong namespace "%s"' % (ns))
            self.__default_ns = self.__mathml_ns
            root = True
        elif ns != self.__mathml_ns:
            raise ValueError('wrong namespace')
        self.__xml_string += el_name
        if root:
            self.__xml_string += ' xmlns="%s"' % ns

        the_keys = list(attrs.keys())
        the_keys.sort()
        counter = 1
        for the_key in the_keys:
            counter +=1
            ns_att = the_key[0]
            att_name = the_key[1]
            value = attrs[the_key]
            if ns_att and ns_att != ns:
                self.__xml_string += ' xmlns:ns%s="%s"' % (counter,ns_att)
            if ns_att and ns_att == ns:
                self.__xml_string += ' ns1:%s="%s"' % (att_name, value)
            elif ns_att:
                self.__xml_string += ' ns%s:%s="%s"' % (counter,att_name, value)
            else:
                self.__xml_string += ' %s="%s"' % (att_name, value)
        self.__xml_string += '>'

    def __write_text(self):
        text =  xml.sax.saxutils.escape(self.__characters)
        # text = text.encode('utf8')
        self.__xml_string += text
        self.__characters = ''

    def endElementNS(self, name, qname):
        self.__write_text()
        ns = name[0]
        el_name = name[1]
        self.__xml_string += '</%s>' % el_name

    def get_xml_string(self):
        return self.__xml_string
    

def xml_copy_tree(xml_string, encoding='utf8'):
    """
    Makes a simple copy of an XML string. Only used for testing purposes.

    Two identical XML strings may have different syntax:

    <TEI xmlns="http://www.tei-c.org/ns/1.0"><p/></TEI>

    is identical to 

    <tei:TEI xmlns:tei="http://www.tei-c.org/ns/1.0"><tei:p xmlns:tei="http://www.tei-c.org/ns/1.0"/></tei:TEI>

    All XML parsers read these strings as the same. However, when testing
    modules in Python, the strings need to have the same syntax. This function
    achieves will create two equal strings by passing each to it and comparing
    the return value. 

    string1 = xml_copy_tree(<'TEI xmlns="http://www.tei-c.org/ns/1.0"><p/></TEI>')
    string2 = xml_copy('<tei:TEI xmlns:tei="http://www.tei-c.org/ns/1.0"><tei:p xmlns:tei="http://www.tei-c.org/ns/1.0"/></tei:TEI>')

    string1 == string2
    True

    """
    if sys.version_info < (3,0):
        if isinstance(xml_string, str):
            xml_string = xml_string.decode(encoding)
    else:
        if isinstance(xml_string, bytes):
            xml_string = xml_string.decode(encoding)
    read_obj = StringIO(xml_string)
    the_handle=CopyTree()
    parser = xml.sax.make_parser()
    parser.setFeature(feature_namespaces, 1)
    parser.setContentHandler(the_handle)
    parser.setFeature("http://xml.org/sax/features/external-general-entities", True)
    parser.parse(read_obj)             
    read_obj.close()
    new_xml_string = the_handle.get_xml_string()
    return new_xml_string

# indents XML Needed to make a uniform XML string
def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def ascii_to_math_tree(the_string):
    if isinstance(the_string, str) and  sys.version_info < (3,):
        the_string = the_string.decode('utf8')
    math_obj =  asciitomathml.asciitomathml.AsciiMathML()
    math_obj.parse_string(the_string)
    math_tree = math_obj.get_tree()
    return math_tree

def test_xml():
    the_tree = etree.parse('test.xml')
    for test in the_tree.getiterator('test'):
        name = test.get('name')
        if not name:
            raise ValueError('test element does not have a name attribute')
        the_string = ''
        for string in test.getiterator('string'):
            the_string += string.text
        test_xml = ascii_to_math_tree(the_string)
        indent(test_xml)
        if sys.version_info < (3,0):
            test_xml_string = tostring(test_xml).encode('utf8')
        else:
            test_xml_string = tostring(test_xml, encoding=str)
        standard_test_xml_string = xml_copy_tree(test_xml_string)
        match = None
        for result in test.getiterator('result'):
            math_tree = result[0]
            indent(math_tree)
            xml_string = tostring(math_tree)
            standard_result_xml_string = xml_copy_tree(xml_string)
            if standard_test_xml_string == standard_result_xml_string:
                match = True
                break
        if not match:
            sys.stderr.write('Error for test "%s"\n' % (name))
            if isinstance(standard_test_xml_string, str) and  sys.version_info > (3,0):
                sys.stderr.write(standard_test_xml_string)
            else:
                sys.stderr.write(standard_test_xml_string.encode("utf8"))
            sys.stderr.write('\ndoes not match\n')
            if isinstance(standard_test_xml_string, str) and  sys.version_info > (3,0):
                sys.stderr.write(standard_result_xml_string)
            else:
                sys.stderr.write(standard_result_xml_string.encode("utf8"))
    # other tests
    # Needs to not just match a tree
    math_obj =  asciitomathml.asciitomathml.AsciiMathML()
    the_string = 'x'
    math_obj.parse_string(the_string)
    xml_string = math_obj.to_xml_string(encoding="utf8", no_encoding_string = True) 
    needed = '<math xmlns="http://www.w3.org/1998/Math/MathML"><mstyle><mi>x</mi></mstyle></math>'
    if xml_string != needed:
        sys.stderr.write('Error for test "no_encoding_string"\n')
        sys.stderr.write('"{0}" != "{1}"'.format(needed, xml_string))

if __name__ == '__main__':
    test_xml()
