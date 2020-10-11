from chibi.atlas import Chibi_atlas
from functools import reduce
from unittest import TestCase

from marshmallow import Schema, pre_load, INCLUDE, fields, post_load
from chibi_marshmallow.fields import Timestamp

from chibi_requests import Chibi_url, Response


class Thread( Schema ):
    id = fields.Integer( data_key='no' )
    replies = fields.Integer()
    last_modified = Timestamp()

    class Meta:
        unknown = INCLUDE

    @pre_load( pass_many=True )
    def pre_load( self, data, **kw ):
        threads = reduce(
            ( lambda x, y: x + y ),
            ( page[ 'threads' ] for page in data ) )
        return threads

    @post_load
    def post_load( self, data, **kw ):
        from chibi_4chan.chibi_4chan import thread, human_thread
        url = self.context[ 'url' ]
        human_url = human_thread.format(
            board=url.kw.board, thread_number=data[ 'id' ],
            replies=data[ 'replies' ], last_modified=data[ 'last_modified' ] )
        return thread.format( human_url=human_url, **human_url.kw )


class Post( Schema ):
    id = fields.Integer( data_key='no' )
    created_at = Timestamp( data_key='time' )
    file_name = fields.String( data_key='filename' )
    comment = fields.String( data_key='com' )
    title = fields.String( data_key='sub' )

    class Meta:
        unknown = INCLUDE

    @pre_load( pass_many=True )
    def pre_load( self, data, **kw ):
        if 'posts' in data:
            return data.posts
        return data

    @post_load
    def post_load( self, data, **kw ):
        from chibi_4chan.chibi_4chan import image
        data = Chibi_atlas( data )
        data.has_image = 'file_name' in data
        url = self.context[ 'url' ]
        if data.has_image:
            data.image_url = image.format(
                board=url.kw.board, image=data.tim,
                ext=data.ext, file_name=data.file_name )
        return data


class Catalog( Schema ):
    id = fields.Integer( data_key='no' )
    created_at = Timestamp( data_key='time' )
    last_replies = fields.Nested( Post, many=True )
    last_modified = Timestamp()
    title = fields.String( data_key='sub' )
    comment = fields.String( data_key='com' )

    class Meta:
        unknown = INCLUDE

    @pre_load( pass_many=True )
    def pre_load( self, data, **kw ):
        thread = reduce(
            ( lambda x, y: x + y ),
            ( page[ 'threads' ] for page in data ) )
        return thread

    @post_load
    def post_load( self, data, **kw ):
        from chibi_4chan.chibi_4chan import thread, human_thread
        data = Chibi_atlas( data )
        url = self.context[ 'url' ]
        human_url = human_thread.format(
            board=url.kw.board, thread_number=data[ 'id' ],
            replies=data[ 'replies' ], last_modified=data[ 'last_modified' ] )
        data.url = thread.format( human_url=human_url, **human_url.kw )
        return data
