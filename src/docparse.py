from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import LSHForest
import cPickle as pickle
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from lda import LDA

class Paper:
    def __init__(self, xml):
        f = file(xml)
        self.title = extract_tag(f, "title")[:-1]
        self.authors = extract_tag(f, "author").replace("and",",")[:-1].split(",")
        self.authors = [author.strip() for author in self.authors]
        # f = file(xml)
        self.body = extract_section(f)
        # self.body = f.read()
    def __repr__(self):
        return "Title: {0}\nAuthors: {1}\nBody:\n {2}...[TRUNCATED]\n".format(
            self.title, self.authors, self.body[:500])
    def __str__(self):
        return "Title: {0}\nAuthors: {1}\nBody:\n {2}...[TRUNCATED]\n".format(
            self.title, self.authors, self.body[:500])

def extract_tag(f, tag):
    opening = "<{0}".format(tag)
    closing = "</{0}".format(tag)
    # print opening, closing
    in_block = False
    lines = []
    for line in f:
        if closing in line:
            break
        if in_block:
            lines.append(line)
        if opening in line:
            in_block = True
    return "".join(lines).replace("\n"," ")

def extract_section(f):
    # header = extract_tag(f, "sectionHeader")
    end = False
    sections = []
    while not end:
        body = extract_tag(f, "bodyText")
        if body:
            sections.append( "".join(body).replace("- ","").replace("&apos;", " "))
        end = body == ""
    return ''.join(sections)
    # return header, "".join(body).replace("-\n","").replace("\n"," ").replace("&apos;", " ").replace("")


corpus_dir = "../resources/xmls/"

class Corpus:
    def __init__(self, corp_dir = corpus_dir):
        self.corpus = load_corpus()
        self.texts = None
    def get_texts(self):
        if not self.texts:
            self.texts = [paper.body for paper in self.corpus]
        return self.texts

def get_tfidf(corpus):
    tfidf = TfidfVectorizer(sublinear_tf=True, stop_words = "english", min_df=.08)
    return tfidf.fit_transform(corpus.get_texts())
def get_counts(corpus):
    tfidf = CountVectorizer(stop_words="english", min_df = .15, max_df = .8)
    return tfidf.fit_transform(corpus.get_texts())

def load_corpus():
    corp =  os.listdir(corpus_dir)
    corp = [(corpus_dir+doc) for doc in corp if ".xml" in doc]
    paps = [Paper(doc) for doc in corp]
    return paps

def load_body(f):
    sections = []
    section = None

    in_sec = False
    in_body = False
    inner_block = 0
    for line in f:
        if "<\sectionHeader" in line:
            sections.append(section)
            section = []
        if "<sectionHeader" in line:
            in_sec = True

def contains_any(string, terms):
    return all((term.lower() in string.lower() for term in terms))

def query(corpus, terms):
    terms = terms.split()
    docs = [(i,doc) for (i,doc) in enumerate(corpus.corpus)
            if contains_any(doc.title, terms)]
    for i, doc in docs[:10]:
        print i,doc.title
    return docs

def recomend_similar(corpus, doc_id, nn, tfdf):
    _, ids = nn.kneighbors(tfdf[doc_id], 10)
    ids = ids[0]
    for id_ in ids:
        print id_, corpus.corpus[id_].title
    return ids

class Recommender:
    def __init__(self, corpus=None, mtx = None, nn = None):
        self.corpus = corpus
        self.mtx = mtx
        self.nn = nn
    def set_mtx(self,mtx, nn = LSHForest()):
        self.mtx = mtx
    def fit_nn(self, nn=LSHForest()):
        self.nn = nn
        self.nn.fit(self.mtx)
    def recomend(self, doc_id, show=True):
        _, [ids] = self.nn.kneighbors(self.mtx[doc_id])
        if show:
            for id_ in ids:
                print id_, self.corpus.corpus[id_].title
        return ids
    def search(self, query_str):
        terms = query_str.replace("*","")
        return query(self.corpus, terms)
    def backup(self, outfile = "RecommenderBackup"):
        pickle.dump(self, file(outfile, mode="w"))
