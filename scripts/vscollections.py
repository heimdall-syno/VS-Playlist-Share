import os, sys, psycopg2
from psycopg2 import sql

## Import from submodule VS-Utils
cur_dir = os.path.dirname(os.path.abspath(__file__))
par_dir = os.path.abspath(os.path.join(cur_dir, os.path.pardir))
sys.path.append(os.path.join(par_dir, "VS-Utils"))
from prints import errmsg, debugmsg

## Get the collection with the passed collection name
def get_collection(cur, playlist, user=None):
    if(user == None):
        cur.execute(
            sql.SQL("SELECT * FROM collection WHERE title = %s AND (title != %s AND title != %s);"),
            [playlist, "syno_watchlist", "syno_favorite"]
        )
        result = cur.fetchall()
    else:
        cur.execute(
            sql.SQL("SELECT * FROM collection WHERE title = %s AND uid = %s AND (title != %s AND title != %s);"),
            [playlist, str(user), "syno_watchlist", "syno_favorite"]
        )
        result = cur.fetchone()
    if(result == None):
        errmsg("Could not find the playlist")
        return None
    return(result)

## Get the collection of a single user
def get_collections_of_user(cur, user):
    if(user == None):
        errmsg("get_collections_of_user() failed - User missing"); exit()
    else:
        cur.execute(
            sql.SQL("SELECT * FROM collection WHERE uid = %s AND (title != %s AND title != %s AND title != %s);"),
            [str(user), "syno_watchlist", "syno_favorite", "syno_default_shared"]
        )
        result = cur.fetchall()
    if(result == None):
        errmsg("User does not have any playlist information")
        return None
    return(result)

## Create the new collection for the passed UserID
def create_new_collection(conn, cur, collection_info, userid):
    if(int(userid) == int(collection_info[1])):
        errmsg("The ownerID and the userID are equal")
        return None

    ## Insert the collection
    collection_name = collection_info[2]
    try:
        cur.execute(
            sql.SQL("INSERT INTO collection (uid,title) VALUES (%s,%s);"), [userid, collection_name])
        conn.commit()

    except psycopg2.IntegrityError:
        errmsg("Could not insert the new playlist, the playlist already exists (%s)", userid)
        return None

    ## Get the ID of the new created collection
    cur.execute(
        sql.SQL("SELECT * FROM collection WHERE uid = %s AND title = %s;"),
        [userid, collection_name]
    )
    result = cur.fetchone()
    if(result == None):
        errmsg("Could not insert the new playlist, the playlist already exists")
        return None
    return result[0]

## Delete a collection
def delete_collection(conn, cur, collection_info):

    ## Delete all items
    collection_id = collection_info[0]
    cur.execute(
        sql.SQL("DELETE FROM collection WHERE id = %s;"),
        [collection_id]
    )
    conn.commit()

## Get all items in the collection to be copied
def get_all_items_of_collection(cur, collection_info):
    collection_id = collection_info[0]

    ## Get all items
    cur.execute(
        sql.SQL("SELECT * FROM collection_map WHERE collection_id = %s;"), [collection_id]
    )
    result = cur.fetchall()

    ## Parse the mapper_id and collection_id
    result = [r[1:3] for r in result]
    if(result == None or len(result) == 0):
        errmsg("The playlist is empty")
        return None
    return(result)

## Delete all items of a collection
def delete_all_items_of_collection(conn, cur, collection_info):

    ## Delete all items
    collection_id = collection_info[0]
    cur.execute(
        sql.SQL("DELETE FROM collection_map WHERE collection_id = %s;"),
        [collection_id]
    )
    conn.commit()

## Add all items to the new collection
def add_all_items_to_collection(conn, cur, items, new_collection_id):

    items = [(mapper_id,new_collection_id) for mapper_id, collection_id in items]
    try:
        values = ', '.join(map(str, items))
        sql_query = ("INSERT INTO collection_map (mapper_id, collection_id) VALUES {}").format(values)
        cur.execute(
            sql.SQL(sql_query)
        )
        conn.commit()
    except psycopg2.IntegrityError:
        errmsg("Could not insert the items to the new playlist")
        return None
