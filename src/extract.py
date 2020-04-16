import os

from tika import parser
from elasticsearch import Elasticsearch
from PyPDF2 import PdfFileWriter, PdfFileReader
from pdf2image import convert_from_path

"""
Splits an original pdf into individual pdfs of each page.
"""
def split_pdf(dirname, pdf_filename):
    pdf_file = open(dirname + '/' + pdf_filename, 'rb')
    pdf_filereader = PdfFileReader(pdf_file)

    filename_without_extension = ''.join(pdf_filename.split('.')[-2])
    os.system("rm -rf static/pdf/{}".format(filename_without_extension))
    os.system("mkdir -p static/pdf/{}".format(filename_without_extension))
    os.system("rm -rf static/img/{}".format(filename_without_extension))
    os.system("mkdir -p static/img/{}".format(filename_without_extension))
    n = pdf_filereader.numPages

    for i in range(n):
        pdf_filewriter = PdfFileWriter()
        pdf_filewriter.addPage(pdf_filereader.getPage(i))
        pdf_page_filename = 'static/pdf/{}/{}.pdf'.format(filename_without_extension, i)
        with open(pdf_page_filename, "wb") as pdf_page_file:
            pdf_filewriter.write(pdf_page_file)
        
          
    pdf_file.close()

    return n, filename_without_extension
"""
Runs apache tika on each of the pages of the pdf (after splitting) and return the contents of each indexed by page number.
"""
def parse_pdf(filename_without_extension, n):

    for i in range(n):
        filename = 'static/pdf/{}/{}.pdf'.format(filename_without_extension, i)
        raw_parse = parser.from_file(filename)
        yield i, raw_parse['content']

def convert_to_jpg(filename_without_extension, n):
    for i in range(n):
        filename = 'static/pdf/{}/{}.pdf'.format(filename_without_extension, i)
        img_page_filename = 'static/img/{}/{}.jpg'.format(filename_without_extension, i)
        imgs = convert_from_path(filename)

        for img in imgs:
            img.save(img_page_filename, 'JPEG')


"""
Builds an elastic search index from the pdf files in a directory.
"""
def extract_and_load(es, indexname, dirname):

    files = [ file for file in os.listdir(dirname) if file[0] != '.' ]
    for filename in files:
        print('Indexing {}...'.format(filename), end='', flush=True)
        num_pages, filename_no_ext = split_pdf(dirname, filename)
        convert_to_jpg(filename_no_ext, num_pages)
        for i, text in parse_pdf(filename_no_ext, num_pages):
            doc = {
                'file': filename,
                'page': i,
                'text': text
            }

            _id = "{}_{}".format(filename_no_ext, i)
            es.index(index=indexname, id=_id, body=doc)
        print('DONE')


def main():
    es = Elasticsearch()
    indexname = 'os'
    dirname = '../data/input'
    extract_and_load(es, indexname, dirname)

    print('\n------------\n')
    """
    while(True):
        print("Enter a query: ", end='')
        query = input()
        body = {
            'query': {
                'match': {
                    'text': query
                }
            }
        }

        res = es.search(index=indexname, body=body)

        for hit in res['hits']['hits'][:10]:
            print("file: %(file)s\npage:%(page)s:\ntext: %(text)s" % hit["_source"])
            next = input()
        print('\n------------\n')
    """

if __name__ == '__main__':
    main()