import sqlite3
from datetime import datetime
import sqlitecloud

def get_db_connection():
    conn = sqlitecloud.connect("sqlitecloud://cx7eygq1hz.g4.sqlite.cloud:8860/ragdb.sqlite3?apikey=AAUKO0qpbN6GCHtxqSOuJiMVvdBbUTWlueWtgO2SlDc")
    #conn.row_factory = sqlite3.Row
    return conn

def create_application_logs():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS application_logs
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     session_id TEXT,
                     user_query TEXT,
                     gpt_response TEXT,
                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.close()

def create_document_store():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS document_store
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     filename TEXT,
                     upload_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.close()


def insert_application_logs(session_id, user_query, gpt_response):
    conn = get_db_connection()
    conn.execute('INSERT INTO application_logs (session_id, user_query, gpt_response) VALUES (?, ?, ?)',
                 (session_id, user_query, gpt_response))
    conn.commit()
    conn.close()

def get_chat_history(session_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT user_query, gpt_response FROM application_logs WHERE session_id = ? ORDER BY created_at', (session_id,))
    messages = []
    for row in cursor.fetchall():
        messages.extend([
        {"role": "human", "content": row[0]},
        {"role": "ai", "content": row[1]}
    ])
    conn.close()
    return messages

def insert_document_record(filename):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO document_store (filename) VALUES (?)', (filename,))
    file_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return file_id

def delete_document_record(file_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM document_store WHERE id = ?', (file_id,))
    conn.commit()
    conn.close()
    return True

def get_all_documents():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, filename, upload_timestamp FROM document_store ORDER BY upload_timestamp DESC')
    documents = cursor.fetchall()
    conn.close()
    return [dict(doc) for doc in documents]

create_application_logs()
create_document_store()