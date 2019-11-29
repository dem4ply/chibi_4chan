# -*- coding: utf-8 -*-
import argparse
import datetime
import logging
import sys

from babel.dates import format_timedelta
from prettytable import PrettyTable

from chibi_4chan import boards
from chibi_4chan.boards import boards as human_boards


logger_formarter = '%(levelname)s %(name)s %(asctime)s %(message)s'

logger = logging.getLogger( 'chibi_4chan.cli' )


def prepare_parser():
    parser = argparse.ArgumentParser(
        description="simple reader of 4chan",
        fromfile_prefix_chars='@' )
    parser.add_argument( 'board', help="board of 4chan" )

    parser.add_argument(
        "--log_level", dest="log_level", default="INFO",
        help="log level", )
    args = parser.parse_args()
    return args


def print_board( board ):
    board = boards[ board ]
    threads = board.get()

    table = PrettyTable()
    table.field_names = [
        'thread number', 'replies', 'last modified', 'message', 'url' ]
    for thread in threads.native:
        posts = thread.get()
        post_first = posts.native[0]

        if 'sub' in post_first:
            sub = post_first.sub
        else:
            sub = ''

        if 'com' in post_first and sub != post_first.com:
            sub += f"\n{post_first.com}"

        delta = thread.kw.last_modified - datetime.datetime.now()
        last_modified = format_timedelta( delta, locale='es_MX' )
        table.add_row( [
            thread.kw.thread_number, thread.kw.replies, last_modified,
            sub, str( thread.kw.human_url ) ] )
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

    print_board( board )

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
