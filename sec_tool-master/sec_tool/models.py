from mongoengine import Document, StringField, ListField, ReferenceField, IntField, BooleanField, DecimalField
from urllib import parse


class Author(Document):
    fullname = StringField()
    firstname = StringField()
    middlename = StringField()
    lastname = StringField()
    affiliation = StringField()
    affiliation_country = StringField()
    affiliation_id = StringField()
    dblp_url = StringField()
    eid_list = ListField(IntField())
    city = StringField()
    subject_areas = ListField(IntField())
    # If, in any point of the pipeline, the author fails a search/parse,
    # mark it with 'exact' = False
    exact = BooleanField(default=True)
    committee_mentions_ratio = DecimalField()
    committee_mentions = IntField()
    total_mentions = IntField() 

    def getattr(self, key, default=""):
        '''
        Returns the attribute if it not None, `default` otherwise
        '''
        return (default if self.__getattribute__(key) is None else
                self.__getattribute__(key))


class AuthorIndex(Document):
    eid = IntField(primary_key=True)
    author = ReferenceField(Author)


class Paper(Document):
    scopus_id = StringField()

    def getattr(self, key, default=""):
        '''
        Returns the attribute if it not None, `default` otherwise
        '''
        return (default if self.__getattribute__(key) is None else
                self.__getattribute__(key))


class Conference(Document):
    fullname = StringField()  # CHECK: do i still need it?
    name = StringField()
    year = IntField()
    location = StringField()  # IMPROVE: use location info
    acronym = StringField()
    wikicfp_id = StringField()
    # not_processed, committee_extracted, papers_extracted, complete
    processing_status = StringField(default='not_processed')
    _wikicfp_url = StringField(db_field='wikicfp_url')

    def __init__(self, *args, **kwargs):
        kwargs['_wikicfp_url'] = None
        if kwargs.get('wikicfp_url'):
            kwargs['_wikicfp_url'] = kwargs.pop('wikicfp_url')
        Document.__init__(self, *args, **kwargs)
        self.wikicfp_url = kwargs['_wikicfp_url']

    @property
    def wikicfp_url(self):
        return self._wikicfp_url

    @wikicfp_url.setter
    def wikicfp_url(self, url):
        if not url:
            return
        self._wikicfp_url = url
        self.wikicfp_id = parse.parse_qs(parse.urlparse(url).query)['eventid'][0]

    def getattr(self, key, default=""):
        '''
        Returns the attribute if it not None, `default` otherwise
        '''
        return (default if self.__getattribute__(key) is None else
                self.__getattribute__(key))
