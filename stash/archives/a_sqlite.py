from stash.archives.core.base import Archive

from contextlib import closing
import sqlite3


class SqliteArchive(Archive):
    __key__  = 'sqlite'

    def __init__(self, db, table):
        self.db = sqlite3.connect(db) if type(db) is str else db
        self.table = table

        # Ensure `table` exists in database
        with closing(self.db.cursor()) as c:
            c.execute('create table if not exists "%s" (key PRIMARY KEY, value)' % self.table)

        self.db.commit()

    def save(self):
        pass

    def select(self, sql, parameters=None):
        if parameters is None:
            parameters = ()

        with closing(self.db.cursor()) as c:
            return list(c.execute(sql, parameters))

    def select_one(self, sql, parameters=None):
        rows = self.select(sql, parameters)

        if not rows:
            return None

        return rows[0]

    def __delitem__(self, key):
        with closing(self.db.cursor()) as c:
            result = c.execute('delete from "%s" where key=?' % self.table, key)

            success = result.rowcount > 0

        self.db.commit()

        if not success:
            raise KeyError(key)

    def __getitem__(self, key):
        row = self.select_one('select value from "%s" where key=?' % self.table, key)

        if not row:
            raise KeyError(key)

        return row[0]

    def __iter__(self):
        raise NotImplementedError

    def __len__(self):
        row = self.select_one('select count(*) from "%s"' % self.table)

        if not row:
            return None

        return row[0]

    def __setitem__(self, key, value):
        with closing(self.db.cursor()) as c:
            c.execute('update "%s" set value=? WHERE key=?' % self.table, (value, key))
            c.execute('insert or ignore into "%s" values(?,?)' % self.table, (key, value))

        self.db.commit()
