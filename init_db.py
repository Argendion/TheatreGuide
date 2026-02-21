import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Shows table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS shows (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        theatre TEXT,
        dates TEXT,
        genre TEXT,
        mood TEXT,
        keywords TEXT,  -- Store as comma-separated string
        source_url TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# Users table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,  -- In real app, hash this!
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# Ratings table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ratings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        show_id INTEGER,
        rating INTEGER CHECK(rating >= 1 AND rating <= 5),
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (show_id) REFERENCES shows (id),
        UNIQUE(user_id, show_id)
    )
''')

# Seen shows table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS seen_shows (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        show_id INTEGER,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (show_id) REFERENCES shows (id),
        UNIQUE(user_id, show_id)
    )
''')

# User keyword preferences (our "learning" table!)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_keywords (
        user_id INTEGER,
        keyword TEXT,
        score INTEGER DEFAULT 0,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id),
        PRIMARY KEY (user_id, keyword)
    )
''')

conn.commit()
conn.close()

print("Database initialized successfully!")