#-*- coding: utf-8 -*-
from whoosh.fields import Schema, STORED, ID, KEYWORD, TEXT
from whoosh.index import create_in, open_dir, exists_in
from whoosh.qparser import QueryParser
from jieba.analyse import ChineseAnalyzer


class YLSearch(object):
    '''
        search
    '''

    index_dir = 'F:/tmp/index'

    def __init__(self, dir):
        self._analyzer = ChineseAnalyzer()
        schema = Schema(title=STORED, content=TEXT(
            stored=True, analyzer=self._analyzer), command=STORED)
        if exists_in(self.index_dir):
            self._index = open_dir(self.index_dir)
        else:
            self._index = create_in(self.index_dir, schema)

    def add(self, title, content, command):
        writer = self._index.writer()
        writer.add_document(title=title, content=content, command=command)
        writer.commit()

    def search(self, content):
        try:
            searcher = self._index.searcher()
            query = QueryParser(
                'content', self._index.schema).parse(content)
            results = searcher.search(query)
            return results
        except Exception, e:
            pass
        # finally:
        #     searcher.close()

if __name__ == '__main__':
    search = YLSearch(1)
    # search.add(u'power_on', u'open light', u'power_on')
    # search.add(u'power_off', u'open close light', u'power_off')
    # search.add(u'power_off', u'我的好朋友是李明;我爱北京天安门;IBM和Microsoft;', u'power_off')
    print search.search(u'好朋友')[0]
    print search.search(u'好朋友')[0]
    print search.search(u'好朋友')[0]
    print search.search(u'好朋友')[0]
    print search.search(u'好朋友')[0]
    print search.search(u'好朋友')[0]
