import datetime
from unittest import TestCase, skip
from vcr_unittest import VCRTestCase
from chibi_4chan import boards
from chibi_requests import Chibi_url
from chibi.atlas import Chibi_atlas


class Test_threads( VCRTestCase ):
    def test_all_boards_is_a_atlas( self ):
        self.assertIsInstance( boards, Chibi_atlas )
        for name, url in boards.items():
            self.assertIsInstance( name, str )
            self.assertIsInstance( url, Chibi_url )

    def test_should_get_threads_from_wallpapers( self ):
        response = boards.w.get()
        self.assertEqual( response.status_code, 200 )
        for thread in response.native:
            self.assertIsInstance( thread, Chibi_url )
            self.assertIn( 'board', thread.kw )
            self.assertIn( 'last_modified', thread.kw )
            self.assertIn( 'replies', thread.kw )
            self.assertIn( 'thread_number', thread.kw )

            self.assertEqual( thread.kw.board, 'w' )
            self.assertIsInstance( thread.kw.last_modified, datetime.datetime )


    def test_each_tread_should_get_the_post( self ):
        response = boards.w.get()
        self.assertEqual( response.status_code, 200 )
        for thread in response.native[:5]:
            thread_response = thread.get()
            for post in thread_response.native:
                self.assertIsInstance( post.time, datetime.datetime )
                if post.has_image:
                    self.assertIsInstance( post.image_url, Chibi_url )
                else:
                    self.assertIsNone( post.image_url )
