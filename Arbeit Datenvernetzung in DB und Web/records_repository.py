import sqlite3
from contextlib import contextmanager

class RecordsRepository:
    def __init__(self, db_path="schallplatten.db"):
        """Initialize the repository with SQLite database"""
        self.db_path = db_path
        self._init_db()

    @contextmanager
    def _get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def _init_db(self):
        """Initialize the database with the records table if it doesn't exist"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    artist TEXT NOT NULL,
                    year INTEGER,
                    genre TEXT,
                    condition TEXT DEFAULT 'Good'
                )
            ''')
            
            # Check if table is empty and add sample data if needed
            cursor.execute('SELECT COUNT(*) FROM records')
            if cursor.fetchone()[0] == 0:
                cursor.executemany('''
                    INSERT INTO records (title, artist, year, genre, condition)
                    VALUES (?, ?, ?, ?, ?)
                ''', [
                    ("Abbey Road", "The Beatles", 1969, "Rock", "Excellent"),
                    ("Thriller", "Michael Jackson", 1982, "Pop", "Very Good")
                ])

    def get_all(self):
        """Get all records"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM records')
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def get(self, record_id):
        """Get a specific record by ID"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM records WHERE id = ?', (record_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def create(self, title, artist, year=None, genre=None, condition="Good"):
        """Create a new record"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO records (title, artist, year, genre, condition)
                VALUES (?, ?, ?, ?, ?)
            ''', (title, artist, year, genre, condition))
            
            record_id = cursor.lastrowid
            # Fetch the newly inserted row using the same connection (not yet committed until context exits)
            cursor.execute('SELECT * FROM records WHERE id = ?', (record_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def update(self, record_id, title=None, artist=None, year=None, genre=None, condition=None):
        """Update an existing record"""
        record = self.get(record_id)
        if not record:
            return None

        # Build update query dynamically
        updates = []
        values = []
        
        if title is not None:
            updates.append('title = ?')
            values.append(title)
        if artist is not None:
            updates.append('artist = ?')
            values.append(artist)
        if year is not None:
            updates.append('year = ?')
            values.append(year)
        if genre is not None:
            updates.append('genre = ?')
            values.append(genre)
        if condition is not None:
            updates.append('condition = ?')
            values.append(condition)

        if not updates:
            return record

        values.append(record_id)
        query = f"UPDATE records SET {', '.join(updates)} WHERE id = ?"

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, values)

        return self.get(record_id)

    def delete(self, record_id):
        """Delete a record by ID"""
        record = self.get(record_id)
        if not record:
            return False

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM records WHERE id = ?', (record_id,))

        return True
