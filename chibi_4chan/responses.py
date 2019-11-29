from datetime import datetime
from functools import reduce

from chibi.atlas import Chibi_atlas
from chibi_requests import Response


class Thread_list( Response ):
    @property
    def native( self ):
        try:
            return self._native
        except AttributeError:
            from chibi_4chan.chibi_4chan import thread, human_thread
            native = super().native
            del self._native

            threads = reduce(
                ( lambda x, y: x + y ),
                ( page[ 'threads' ] for page in native) )

            self._native = []
            for t in threads:
                last_modified = datetime.fromtimestamp( t[ 'last_modified' ] )
                human_url = human_thread.format(
                    board=self.url.kw.board, thread_number=t[ 'no' ],
                    replies=t[ 'replies' ], last_modified=last_modified )
                self._native.append(
                    thread.format( human_url=human_url, **human_url.kw ) )
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
