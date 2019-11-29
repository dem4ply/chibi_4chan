from chibi_requests import Chibi_url
from .boards import boards as boards_atlas
from chibi.atlas import Chibi_atlas
from chibi_4chan.responses import Thread_list, Post


threads = Chibi_url(
    'http://a.4cdn.org/{board}/threads.json', response_class=Thread_list )
thread = Chibi_url(
    'http://a.4cdn.org/{board}/thread/{thread_number}.json',
    response_class=Post )

image = Chibi_url( 'http://i.4cdn.org/{board}/{image}{ext}' )

human_thread = Chibi_url(
    'http://boards.4channel.org/{board}/thread/{thread_number}' )


boards = Chibi_atlas( {
    board: threads.format( board=board )
    for board in boards_atlas.keys() } )
