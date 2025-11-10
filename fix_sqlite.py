"""
Fix SQLite version issue for ChromaDB
This script replaces the built-in sqlite3 module with pysqlite3
"""
import sys

# Replace sqlite3 with pysqlite3
__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

print("SQLite patched successfully", flush=True)
