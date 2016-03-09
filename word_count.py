import gzip
import warc
import sys
import os
import string
import time
from gzipstream import GzipStreamFile
from collections import Counter

class parser:

    def __init__(self):
        self.curr_doc_id = 0
        self.urls = open('index/table_','w+')
        self.tuple_file = open('tmp/_sortedTuples','w')
        self.docid_lengths = open('index/docid_lengths','w')

    def __del__(self):
        self.urls.close()
        self.tuple_file.close()
        self.docid_lengths.close()

    def stem_tokens(self, tokens):
        stemmed = []
        for item in tokens:
            stemmed.append(self.stemmer.stem(item))
        return stemmed

    def process_record(self, record):
        if record['Content-Type'] != 'text/plain':
            return
        data = record.payload.read()
        self.urls.write(record["WARC-Target-URI"]+"\n")
        # print "processing %s" % record["WARC-Target-URI"]
        data = data.decode('utf-8').strip().lower()
        tokens = data.split()
        self.docid_lengths.write("%d\t%d\n" % (self.curr_doc_id, len(tokens)))
        # tokens = word_tokenize(data)
        tokens = [i.strip() for i in tokens if i.isalnum()]
        # stems = self.stem_tokens(tokens)
        for word, count in Counter(tokens).iteritems():
            word = word.encode("ascii", 'ignore')
            if word.strip() == "" or len(word) > 50 or len(word) < 3:
                continue
            self.tuple_file.write("%s\t%d\t%d\n" % (word, self.curr_doc_id, count))
        self.curr_doc_id += 1

    def process_wet_file(self, f):
        for i, record in enumerate(f):
            self.process_record(record)

if __name__ == '__main__':
    t0 = time.time()
    p = parser()
    with open('wet_file_paths') as f:
        for line in f:
            f = warc.WARCFile(fileobj=gzip.open(os.path.abspath(line.strip())))
            print "processing %s file" % line.strip()
            try:
                p.process_wet_file(f)
            except Exception, e:
                print "error processing file %s "  % line.strip()
                pass
    t1 = time.time()

    total = t1-t0
    print "time to parse files %d" % total