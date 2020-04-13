############################################################
####               All single functions                #####
############################################################

from vscollections import get_collection, create_new_collection
from vscollections import get_all_items_of_collection, delete_all_items_of_collection
from vscollections import delete_collection, add_all_items_to_collection
from connections import connect, close_connection
from users import get_userid_from_name, get_user_selection

## Copy a collection to a single user
def copy_single_mode(args):

    ## Connect to Video Station database
    print("    Connecting to Synology VideoStation database...")
    conn, cur = connect()
    if(conn == None): exit(-1)
    print("[x] Connected successfully")

    ## Get admin and its ID
    admin_id = get_user_selection('admin_only')[1]

    ## Get the collection information
    collection_info = get_collection(cur, args.playlist, admin_id)
    if(collection_info == None):
        close_connection(conn, cur)
        exit(-1)
    print("[x] Get the playlist information")

    ## Get the userID of the passed username
    user_id = get_userid_from_name(args.user)
    if(user_id == None):
        close_connection(conn, cur)
        exit(-1)
    print("[x] Get the UserID of the passed user")

    ## Get all items of the collection
    items = get_all_items_of_collection(cur, collection_info)
    if(items == None):
        close_connection(conn, cur)
        exit(-1)
    print("[x] Get all items of the playlist")

    ## Create the new collection
    new_collection_id = create_new_collection(conn, cur, collection_info, user_id)
    if(new_collection_id == None):
        close_connection(conn, cur)
        exit(-1)
    print("[x] Inserted the new playlist successfully")

    ## Add all items to the new collection
    add_all_items_to_collection(conn, cur, items, new_collection_id)
    if(items == None):
        close_connection(conn, cur)
        exit(-1)
    print("[x] Added all items to the new playlist")

    ## Close connection
    close_connection(conn, cur)

## Delete a collection from a single user
def delete_single_mode(args):

    ## Connect to Video Station database
    print("    Connecting to Synology VideoStation database...")
    conn, cur = connect()
    if(conn == None): exit(-1)
    print("[x] Connected successfully")

    ## Get the userID of the passed username
    user_id = get_userid_from_name(args.user)
    if(user_id == None):
        close_connection(conn, cur)
        exit(-1)
    print("[x] Get the UserID of the passed user")

    ## Get the collection information
    collection_info = get_collection(cur, args.playlist, user_id)
    if(collection_info == None):
        close_connection(conn, cur)
        exit(-1)
    print("[x] Get the playlist information")

    ## Delete all items of a collection
    delete_all_items_of_collection(conn, cur, collection_info)
    print("[x] Delete all items of the playlist")

    ## Delete the collection itself
    delete_collection(conn, cur, collection_info)
    print("[x] Delete the playlist itself")

    ## Close connection
    close_connection(conn, cur)
