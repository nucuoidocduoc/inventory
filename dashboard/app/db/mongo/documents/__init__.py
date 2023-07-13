# -*- coding: utf-8 -*-
import math

from bson import ObjectId
from mongoengine.queryset import QuerySet
from mongoengine import (Document,
                         EmbeddedDocument,
                         BooleanField,
                         DateTimeField,
                         StringField)

from app.common.utils import get_now
from app.common.dict_utils import filter_keys
from app.common.constants import STRING_LENGTH


class Pagination(object):

    def __init__(self, iterable, page, per_page):

        if page < 1:
            page = 1

        self.iterable = iterable
        self.page = page
        self.per_page = per_page

        if isinstance(iterable, QuerySet):
            self.total = iterable.count()
        else:
            self.total = len(iterable)

        start_index = (page - 1) * per_page
        end_index = page * per_page

        self.items = iterable[start_index:end_index]
        if isinstance(self.items, QuerySet):
            self.items = self.items.select_related()

    @property
    def pages(self):
        """The total number of pages"""
        return int(math.ceil(self.total / float(self.per_page)))

    def prev(self, error_out=False):
        """Returns a :class:`Pagination` object for the previous page."""
        assert self.iterable is not None, ('an object is required '
                                           'for this method to work')
        iterable = self.iterable
        if isinstance(iterable, QuerySet):
            iterable._skip = None
            iterable._limit = None
        return self.__class__(iterable, self.page - 1, self.per_page)

    @property
    def prev_num(self):
        """Number of the previous page."""
        return self.page - 1

    @property
    def has_prev(self):
        """True if a previous page exists"""
        return self.page > 1

    def next(self, error_out=False):
        """Returns a :class:`Pagination` object for the next page."""
        assert self.iterable is not None, ('an object is required '
                                           'for this method to work')
        iterable = self.iterable
        if isinstance(iterable, QuerySet):
            iterable._skip = None
            iterable._limit = None
        return self.__class__(iterable, self.page + 1, self.per_page)

    @property
    def has_next(self):
        """True if a next page exists."""
        return self.page < self.pages

    @property
    def next_num(self):
        """Number of the next page"""
        return self.page + 1

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        """Iterates over the page numbers in the pagination.  The four
        parameters control the thresholds how many numbers should be produced
        from the sides.  Skipped page numbers are represented as `None`.
        This is how you could render such a pagination in the templates:

        .. sourcecode:: html+jinja

            {% macro render_pagination(pagination, endpoint) %}
              <div class=pagination>
              {%- for page in pagination.iter_pages() %}
                {% if page %}
                  {% if page != pagination.page %}
                    <a href="{{ url_for(endpoint, page=page) }}">{{ page }}</a>
                  {% else %}
                    <strong>{{ page }}</strong>
                  {% endif %}
                {% else %}
                  <span class=ellipsis>…</span>
                {% endif %}
              {%- endfor %}
              </div>
            {% endmacro %}
        """
        last = 0
        for num in range(1, self.pages + 1):
            if (num <= left_edge or
                    num > self.pages - right_edge or
                    (
                            num >= self.page - left_current and num <= self.page + right_current)):
                if last + 1 != num:
                    yield None
                yield num
                last = num
        if last != self.pages:
            yield None


class NewQuerySet(QuerySet):
    def paginate(self, page, per_page, **kwargs):
        """
        Paginate the QuerySet with a certain number of docs per page
        and return docs for a given page.
        """
        return Pagination(self, page, per_page)


class Model(Document):
    _translatable_fields = None

    id = StringField(default=lambda: str(ObjectId()),
                     max_length=STRING_LENGTH['EX_SHORT'],
                     primary_key=True)
    created_at = DateTimeField(default=get_now)
    updated_at = DateTimeField()

    deleted = BooleanField(default=False)

    meta = {
        'abstract': True,
        'queryset_class': NewQuerySet,
        'indexes': [
            'created_at',
            'updated_at',
            'deleted',
        ],
    }

    def save(self, *args, **kwargs):
        self.updated_at = get_now()
        return super(Model, self).save(*args, **kwargs)

    def to_dict(self,
                excludes=None,
                includes=None
                ):
        result = self.to_mongo().to_dict()
        result['id'] = result['_id']
        return filter_keys(data=result,
                           exclude_keys=excludes,
                           include_keys=includes)

    def __repr__(self):
        model_name = self.__class__.__name__
        object_type = getattr(self, 'type', None)
        return f'<{model_name} - {self.id} - {object_type}>'


class BaseEmbeddedDocument(EmbeddedDocument):
    meta = {
        'abstract': True
    }

    def to_dict(self):
        return self.to_mongo().to_dict()
