import os
import wget
import tarfile
from subprocess import call
import untangle
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
names_file  = "../resources/files.txt"
names_file  = "../resources/download_names.txt"
base_str = r"http://acl-arc.comp.nus.edu.sg/archives/acl-arc-160301-parscit/{0}.tgz"
tar_dir = "../resources/tars/"
xml_dir = "../resources/xmls/"

str = r"http://acl-arc.comp.nus.edu.sg/archives/acl-arc-160301-parscit/{0}.tgz".format("A00")


def download_files(filename = names_file):
    f = file(filename)
    for name in f:
        name = name[:-1]
        print "Downloading: {0}".format(name)
        wget.download(base_str.format(name), out=tar_dir)

def extract_tars(dirname = xml_dir):
    files = os.listdir(tar_dir)
    tars = [tar_dir+f for f in files if "tgz" in f]
    for tar in tars:
        tf = tarfile.open(tar)
        tf.extractall(xml_dir)
    return tars

def flatten_dir(dirname):
    os.system("find {0} -mindepth 2 -type f -exec mv -i '{{}}' {0} ';'".format(dirname))
    os.system("find {0} -depth -type d -exec rmdir {{}} \;".format(dirname))

import xmltodict

def as_dict(xml):
    with open(xml) as fd:
        doc = xmltodict.parse(fd.read())
    return doc

def notags(xml):
    tree = ET.parse(xml)
    notags = ET.tostring(tree, encoding='utf8', method='text')
    print(notags)



from xml.parsers.expat import ParserCreate

def char_data(data):
    if data.strip(): # skip empty text if you want
        print data



parser = ParserCreate()
parser.CharacterDataHandler = char_data

import xml.etree.ElementTree as ET
def rem_tags(xml):
    mystring = file(xml).read()
    element = ET.XML(mystring)
    print element.text
