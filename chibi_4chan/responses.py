from datetime import datetime
from functools import reduce

from chibi.atlas import Chibi_atlas
from chibi_requests import Response
from .serializer import (
    Thread,
    Post as Post_serializer,
    Catalog as Catalog_serializer
)


class Thread_list( Response ):
    serializer = Thread


class Post( Response ):
    serializer = Post_serializer

    @property
    def native_is_many( self ):
        return True
        parse = self.parse_content_type()
        return isinstance( parse, list )


class Catalog( Response ):
    serializer = Catalog_serializer
