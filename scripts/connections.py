############################################################
####           All connection functions                #####
############################################################

import psycopg2

## Try to connection to the Video Station database server
def connect():
    try:
        conn = psycopg2.connect("dbname='video_metadata' user='postgres'")
    except:
        print("[-] Could not connect to the database, try to run as follows: sudo -u postgres python")
        return (None,None)

    cur = conn.cursor()
    return (conn, cur)

## Close the connection to the Video Station database server
def close_connection(conn, cur):
    cur.close()
    conn.close()
