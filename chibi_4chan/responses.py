from chibi_requests import Response, Chibi_url
from chibi.atlas import Chibi_atlas
from functools import reduce
from datetime import datetime


class Thread_list( Response ):
    @property
    def native( self ):
        try:
            return self._native
        except AttributeError:
            from chibi_4chan.chibi_4chan import thread
            native = super().native
            del self._native

            threads = reduce(
                ( lambda x, y: x + y ),
                ( page[ 'threads' ] for page in native) )

            self._native = [
                thread.format(
                    board=self.url.kw.board, thread_number=t[ 'no' ],
                    replies=t[ 'replies' ],
                    last_modified=datetime.fromtimestamp( t[ 'last_modified' ] ) )
                for t in threads ]
            return self._native


class Post( Response ):
    @property
    def native( self ):
        try:
            return self._native
        except AttributeError:
            from chibi_4chan.chibi_4chan import image
            native = super().native
            del self._native
            results = []
            for post in native.posts:
                result = Chibi_atlas( **post )
                result.time = datetime.fromtimestamp( result.time )
                result.has_image = 'filename' in result
                results.append( result )

                if result.has_image:
                    result.image_url = image.format(
                        board=self.url.kw.board, image=post[ 'tim' ],
                        ext=post[ 'ext' ] )
            self._native = results
            return self._native
