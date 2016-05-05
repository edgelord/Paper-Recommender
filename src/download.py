import wget
import tarfile

names_file  = "../resources/files.txt"
names_file  = "../resources/download_names.txt"
base_str = r"http://acl-arc.comp.nus.edu.sg/archives/acl-arc-160301-parscit/{0}.tgz"
tar_dir = "../resources/tars"

str = r"http://acl-arc.comp.nus.edu.sg/archives/acl-arc-160301-parscit/{0}.tgz".format("A00")


def download_files(filename = names_file):
    f = file(filename)
    for name in f:
        name = name[:-1]
        print "Downloading: {0}".format(name)
        wget.download(base_str.format(name), out=tar_dir)

