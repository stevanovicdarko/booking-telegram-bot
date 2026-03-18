from peewee import SqliteDatabase

# Initialize the SQLite database instance.
# 'telegramm_hotels.db' will be created in the root directory upon first connection.

db = SqliteDatabase('telegramm_hotels.db')

