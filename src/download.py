import os
import wget
import tarfile

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
