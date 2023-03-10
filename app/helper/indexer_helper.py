import os.path
import pickle

from app.utils import StringUtils, ExceptionUtils
from app.utils.commons import singleton
from config import Config


@singleton
class IndexerHelper:
    _indexers = []

    def __init__(self):
        self.init_config()

    def init_config(self):
        try:
            with open(os.path.join(Config().get_inner_config_path(),
                                   "sites.dat"),
                      "rb") as f:
                self._indexers = pickle.load(f)
        except Exception as err:
            ExceptionUtils.exception_traceback(err)

    def get_all_indexers(self):
        return self._indexers

    def get_indexer(self,
                    url,
                    cookie=None,
                    name=None,
                    rule=None,
                    public=None,
                    proxy=False,
                    parser=None,
                    ua=None,
                    render=None,
                    language=None,
                    pri=None):
        if not url:
            return None
        for indexer in self._indexers:
            if not indexer.get("domain"):
                continue
            if StringUtils.url_equal(indexer.get("domain"), url):
                return IndexerConf(datas=indexer,
                                   cookie=cookie,
                                   name=name,
                                   rule=rule,
                                   public=public,
                                   proxy=proxy,
                                   parser=parser,
                                   ua=ua,
                                   render=render,
                                   builtin=True,
                                   language=language,
                                   pri=pri)
        return None


class IndexerConf(object):

    def __init__(self,
                 datas=None,
                 cookie=None,
                 name=None,
                 rule=None,
                 public=None,
                 proxy=False,
                 parser=None,
                 ua=None,
                 render=None,
                 builtin=True,
                 language=None,
                 pri=None):
        if not datas:
            return
        # ID
        self.id = datas.get('id')
        # ??????
        self.name = datas.get('name') if not name else name
        # ??????????????????
        self.builtin = builtin
        # ??????
        self.domain = datas.get('domain')
        # ??????
        self.search = datas.get('search', {})
        # ???????????????????????????????????????????????????????????????
        self.batch = self.search.get("batch", {}) if builtin else {}
        # ?????????
        self.parser = parser if parser is not None else datas.get('parser')
        # ??????????????????
        self.render = render if render is not None else datas.get("render")
        # ??????
        self.browse = datas.get('browse', {})
        # ????????????
        self.torrents = datas.get('torrents', {})
        # ??????
        self.category = datas.get('category', {})
        # Cookie
        self.cookie = cookie
        # User-Agent
        self.ua = ua
        # ????????????
        self.rule = rule
        # ??????????????????
        self.public = public
        # ??????????????????
        self.proxy = proxy
        # ????????????????????????
        self.language = language
        # ??????????????????
        self.pri = pri if pri else 0
