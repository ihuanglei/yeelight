#-*- coding: utf-8 -*-
import os
import uuid
import logging
from whoosh.fields import Schema, STORED, ID, KEYWORD, TEXT
from whoosh.index import create_in, open_dir, exists_in
from whoosh.qparser import QueryParser
from whoosh import query
from jieba.analyse import ChineseAnalyzer


class YLCMDSearcher(object):
    '''Searcher'''

    def __init__(self, dir):
        self._analyzer = ChineseAnalyzer()
        schema = Schema(id=ID(unique=True, stored=True), title=STORED, content=TEXT(
            stored=True, analyzer=self._analyzer), command=STORED)
        self._index_dir = dir + '/yl_cmd_index'
        os.path.exists(self._index_dir) or os.makedirs(self._index_dir)
        if exists_in(self._index_dir):
            self._index = open_dir(self._index_dir)
        else:
            self._index = create_in(self._index_dir, schema)

    def add(self, title, content, command):
        '''add document'''
        id = unicode(uuid.uuid1())
        writer = self._index.writer()
        writer.add_document(id=id, title=title,
                            content=content, command=command)
        writer.commit()

    def remove(self, id):
        '''remove index by id'''
        writer = self._index.writer()
        writer.delete_by_term('id', id)
        writer.commit()

    def search(self, content, page=1, pagelen=50):
        '''search'''
        try:
            searcher = self._index.searcher()
            if content == '*':
                q = query.Every()
            else:
                q = QueryParser(
                    'content', self._index.schema).parse(content)
            logging.debug('-- YLSearcher query %s', q)
            results = searcher.search_page(q, page, pagelen)
            hits = []
            for hit in results:
                hits.append(hit.fields())

            return {
                'page_total': results.pagecount,
                'page_num': results.pagenum,
                'page_len': results.pagelen,
                'count': results.total,
                'hits': hits
            }

        except Exception, e:
            logging.error('-- YLSearcher query %s', e)
        finally:
            searcher.close()

if __name__ == '__main__':
    search = YLCMDSearcher('F:/tmp/')
    # search.add(u'1', u'open light', u'power_on')
    # search.add(u'2', u'open close light', u'power_off')
    # search.add(u'3', u'我的好朋友是李明;我爱北京天安门;IBM和Microsoft;', u'power_off')
    # search.remove('e8b0a180-2338-11e7-8885-fcaa14d480a2')
    # print search.all()
    print search.search(u'*', page=1, pagelen=1)
    # print search.search(u'好朋友')
