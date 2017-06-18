from datetime import datetime
from weakref import WeakValueDictionary
from sqlalchemy import inspect
from sqlalchemy.orm import aliased
from sqlalchemy.orm.collections import InstrumentedList

from . import db

class MetaBaseModel(db.Model.__class__):

    def __init__(cls, *args):
        super().__init__(*args)
        cls.aliases = WeakValueDictionary()

    def __getitem__(cls, key):
        try:
            alias = cls.aliases[key]
        except KeyError:
            alias = aliased(cls)
            cls.aliases[key] = alias
        return alias

class BaseModel():

    print_filter = ()
    to_json_filter = ()

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, {
            column: value
            for column, value in self._to_dict().items()
            if column not in self.print_filter
        })

    @property
    def json(self):

        json_obj = {}
        for column, value in self._to_dict().items():
            if column not in self.to_json_filter:
                if isinstance(value, datetime):
                    json_obj[column] = value.strftime('%Y-%m-%d')
                elif isinstance(value, InstrumentedList):
                    json_obj[column] = [v.json for v in value]
                else:
                    json_obj[column] = value
        return json_obj

    def _to_dict(self):
        return {
            column.key: getattr(self, column.key)
            for column in inspect(self.__class__).attrs
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
