
import contextlib
import logging
import os
import sqlite3

_logger = logging.getLogger(__name__)

class Image(object):
    def __init__(self, row):
        self.image_id = row[0]
        self.path = row[1]
        self.folder_id = row[2]

    def __str__(self):
        return self.path

class DbWrapper(object):
    def __init__(self, db_filename, init_script_filename):
        self.__conn = sqlite3.connect(db_filename)
        with open(init_script_filename) as script:
            self.__conn.executescript(script.read())

    @property
    @contextlib.contextmanager
    def cursor(self):
        yield self.__conn.cursor()
        self.__conn.commit()

    @property
    def read_only_cursor(self):
        return self.__conn.cursor()

    @property
    def available_folder(self):
        c = self.read_only_cursor()
        c.execute('''SELECT folder_id FROM undisplayed_folders ORDER BY random() LIMIT 1''')
        row = c.fetchone()
        if row:
            return row[0]
        else:
            return row

    @property
    def available_image(self):
        c = self.read_only_cursor()
        c.execute('''SELECT * FROM undisplayed_images ORDER BY random() LIMIT 1''')
        row = c.fetchone()
        if row:
            return Image(row)
        else:
            return row

    def get_n_images_from_folder(self, n, folder_id):
        c = self.read_only_cursor
        c.execute('''SELECT * FROM undisplayed_images WHERE folder_id=:folder_id ORDER BY random() LIMIT :n''',
                {'folder_id': folder_id, 'n': n})
        while True:
            row = c.fetchone()
            if row:
                yield Image(row)
            else:
                break

    def add_image(self, path):
        path = os.path.abspath(path)
        if not os.path.exists(path):
            raise ValueError('path must exist')
        with self.cursor as c:
            try:
                c.execute('''INSERT INTO images (path, folder_id) VALUES (:path, :folder_id)''', {
                    'path': path,
                    'folder_id': hash(os.path.dirname(path))})
            except sqlite3.IntegrityError:
                _logger.debug('"%s" already exists in DB', path)

    def add_images(self, *paths):
        paths = [os.path.abspath(p) for p in paths if os.path.exists(p)]
        with self.cursor as c:
            for path in paths:
                try:
                    c.execute('''INSERT INTO images (path, folder_id) VALUES (:path, :folder_id)''', {
                        'path': path,
                        'folder_id': hash(os.path.dirname(path))})
                except sqlite3.IntegrityError:
                    _logger.debug('"%s" already exists in DB', path)

    def add_displayed_images(self, image_ids):
        try:
            iter(image_ids)
        except TypeError:
            raise TypeError('image_ids must be an iterable')
        
        with self.cursor as c:
            for image_id in image_ids:
                c.execute('''INSERT INTO displayed_images (image_id) VALUES (?)''', (image_id,))

    def clear_displayed_images(self):
        with self.cursor as c:
            c.execute('''DELETE FROM displayed_images''')

