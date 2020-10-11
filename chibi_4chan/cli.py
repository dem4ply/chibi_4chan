# -*- coding: utf-8 -*-
import argparse
import datetime
import logging
import sys

from babel.dates import format_timedelta
from prettytable import PrettyTable

from chibi_4chan import boards
from chibi_4chan.boards import boards as human_boards
from chibi_4chan.chibi_4chan import thread as thread_url
from chibi.file import Chibi_path


logger_formarter = '%(levelname)s %(name)s %(asctime)s %(message)s'

logger = logging.getLogger( 'chibi_4chan.cli' )


def prepare_parser():
    parser = argparse.ArgumentParser(
        description="simple reader of 4chan",
        fromfile_prefix_chars='@' )
    parser.add_argument( 'board', help="board of 4chan" )

    parser.add_argument( 'threads', nargs='*', help="thread number" )
    parser.add_argument(
        '--dest', '-d', dest='dest', type=Chibi_path,
        help="folder where is going to download the images" )

    parser.add_argument(
        "--log_level", dest="log_level", default="INFO",
        help="log level", )
    args = parser.parse_args()
    return args


def download_thread( board, thread_number, folder ):
    url = thread_url.format( board=board, thread_number=thread_number  )
    posts = url.get().native
    if 'title' in posts[0]:
        title = posts[0].title
    else:
        title = thread_number
    dest = folder + title
    if not dest.exists:
        dest.mkdir()
    for post in posts:
        if post.has_image:
            image_dest = dest + post.image_url.base_name
            if image_dest.exists:
                logger.info( f"se encontro '{image_dest}'" )
                continue
            post.image_url.download( image_dest )


def print_board( board ):
    board = boards[ board ]
    threads = board.get()

    table = PrettyTable()
    table.field_names = [
        'thread number', 'replies', 'last modified', 'message', 'url' ]
    for thread in threads.native:
        if 'title' in thread:
            title = thread.title
        else:
            title = ''

        delta = thread.last_modified - datetime.datetime.now()
        last_modified = format_timedelta( delta, locale='es_MX' )
        table.add_row( [
            thread.id, thread.replies, last_modified,
            title, str( thread.url ) ] )
    print( table )


def print_list_of_boards():
    table = PrettyTable()
    table.field_names = [ 'board', 'name', ]
    for k, v in human_boards.items():
        table.add_row( [ k, v ] )
    print( table )


def main():
    args = prepare_parser()
    logging.basicConfig( level=args.log_level, format=logger_formarter )
    board = args.board
    if board == 'list':
        print_list_of_boards()
        return 0
    if board not in boards:
        logger.error( f"board {board} is not in the list" )
        return 1

    if args.threads:
        for thread_number in args.threads:
            download_thread( board, thread_number, args.dest )
    else:
        print_board( board )

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
