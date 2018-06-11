import os
import pymysql.cursors
from dotenv import load_dotenv
from progressbar import progressbar
from pymongo import MongoClient

import sys
sys.path.append('./src')

from db import insert_wp_page, insert_category_associations, insert_link_contexts
from process_pages import process_seed_pages
from redirects import get_redirects_lookup


def main():
  load_dotenv(dotenv_path='.env')
  EL_DATABASE_NAME = os.getenv("EL_DBNAME")
  ENWIKI_DATABASE_NAME = os.getenv("ENWIKI_DBNAME")
  DATABASE_USER = os.getenv("DBUSER")
  DATABASE_PASSWORD = os.getenv("DBPASS")
  DATABASE_HOST = os.getenv("DBHOST")

  client = MongoClient()
  dbname = 'enwiki'
  print('Reading from mongodb db', dbname)
  db = client[dbname]
  pages_db = db['pages']
  num_seed_pages = 10000
  print('Fetching WP pages using', num_seed_pages, 'seed pages')
  initial_pages_to_fetch = list(pages_db.aggregate([{'$sample': {'size': num_seed_pages}}]))
  print('Building redirects lookup')
  redirects_lookup = get_redirects_lookup()
  print('Processing WP pages')
  processed_pages = process_seed_pages(pages_db, redirects_lookup, initial_pages_to_fetch, depth=1)

  el_connection = pymysql.connect(host=DATABASE_HOST,
                                  user=DATABASE_USER,
                                  password=DATABASE_PASSWORD,
                                  db=EL_DATABASE_NAME,
                                  charset='utf8mb4',
                                  use_unicode=True,
                                  cursorclass=pymysql.cursors.DictCursor)
  enwiki_connection = pymysql.connect(host=DATABASE_HOST,
                                      user=DATABASE_USER,
                                      password=DATABASE_PASSWORD,
                                      db=ENWIKI_DATABASE_NAME,
                                      charset='utf8mb4',
                                      use_unicode=True,
                                      cursorclass=pymysql.cursors.DictCursor)
  try:
    with el_connection.cursor() as el_cursor:
      el_cursor.execute("SET NAMES utf8mb4;")
      el_cursor.execute("SET CHARACTER SET utf8mb4;")
      el_cursor.execute("SET character_set_connection=utf8mb4;")
      with enwiki_connection.cursor() as enwiki_cursor:
        enwiki_cursor.execute("SET NAMES utf8mb4;")
        enwiki_cursor.execute("SET CHARACTER SET utf8mb4;")
        enwiki_cursor.execute("SET character_set_connection=utf8mb4;")
        print('Inserting processed pages')
        source = 'wikipedia'
        for processed_page in progressbar(processed_pages):
          insert_wp_page(enwiki_cursor, el_cursor, processed_page, source)
          el_connection.commit()
          insert_category_associations(el_cursor, processed_page, source)
          el_connection.commit()
          insert_link_contexts(enwiki_cursor, el_cursor, processed_page, source)
          el_connection.commit()
  finally:
    el_connection.close()
    enwiki_connection.close()


if __name__ == "__main__": main()
