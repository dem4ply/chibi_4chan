import datetime

from chibi.atlas import Chibi_atlas
from chibi_requests import Chibi_url
from vcr_unittest import VCRTestCase

from chibi_4chan import boards
from chibi_4chan.chibi_4chan import main, catalog


class Test_catalog_url( VCRTestCase ):
    def test_each_thread_should_have_a_url( self ):
        response = catalog.format( board='w' ).get()
        self.assertEqual( response.status_code, 200 )
        for thread in response.native:
            self.assertIn( 'url', thread )
            self.assertTrue( thread.url )
            self.assertIsInstance( thread.url, Chibi_url )

    def test_each_thread_should_have_a_title( self ):
        response = catalog.format( board='w' ).get()
        self.assertEqual( response.status_code, 200 )
        thread_with_title = list(
            thread for thread in response.native if 'title' in thread )
        self.assertTrue( thread_with_title )
        for thread in thread_with_title:
            self.assertIn( 'title', thread )
            self.assertTrue( thread.title )


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
            self.assertIsInstance( thread.url, Chibi_url )
            self.assertIn( 'last_modified', thread )
            self.assertIn( 'replies', thread )
            self.assertIn( 'id', thread )

            self.assertIsInstance( thread.last_modified, datetime.datetime )

    def test_each_tread_should_get_the_post( self ):
        response = boards.w.get()
        self.assertEqual( response.status_code, 200 )
        for thread in response.native[:5]:
            thread_response = thread.url.get()
            for post in thread_response.native:
                self.assertIsInstance( post.created_at, datetime.datetime )
                if post.has_image:
                    self.assertIsInstance( post.image_url, Chibi_url )
                else:
                    self.assertNotIn( 'image_url', post )
