import psycopg2
from psycopg2 import Error
import os
from dotenv import load_dotenv

load_dotenv()
def connect_db():
    try:
        conn = psycopg2.connect(
            host=os.getenv('POSTGRESQL_HOST'),
            user=os.getenv('POSTGRESQL_USER'),
            password=os.getenv('POSTGRESQL_PASSWORD'),
            port=os.getenv('POSTGRESQL_PORT'),
            dbname=os.getenv('POSTGRESQL_DB_NAME', 'postgres')
        )
        # .is_connected() returns True if the connection is open
        if conn.closed == 0:
            print("✅ Connection successful")
            return conn
        else:
            print("❌ Connection object created, but not connected")
            return None
    except Error as err:
        print(f"⚠️ Connection failed: {err}")
        return None
    
def close_db(conn):
    if conn is not None:
        conn.close()
        print("✅ Connection closed")


def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS articles (
            title TEXT NOT NULL,
            link TEXT NOT NULL PRIMARY KEY,
            pubDate TIMESTAMP NOT NULL,
            description TEXT,
            website TEXT NOT NULL,
            pos float DEFAULT 0,
            neg float DEFAULT 0,
            neu float DEFAULT 0,
            compound float DEFAULT 0
            )
                       """)
        conn.commit()
    except Error as err:
        print(f"⚠️ Failed to create table: {err}")
    finally:
        cursor.close()

def insert_articles(conn, entries):
    try:
        cursor = conn.cursor()
        for entry in entries:
            cursor.execute("""
                INSERT INTO articles (title, link, pubDate, description, website, pos, neg, neu, compound)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (link) DO NOTHING;
            """, (entry['title'], 
                  entry['link'], 
                  entry['pubDate'], 
                  entry['description'], 
                  entry['website'],
                  entry['pos'], 
                  entry['neg'], 
                  entry['neu'], 
                  entry['compound']))
        conn.commit()
        print("✅ Articles inserted successfully")
    except:
        print("⚠️ Failed to insert articles")
        conn.rollback()
    finally:
        cursor.close()