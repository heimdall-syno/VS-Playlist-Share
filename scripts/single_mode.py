from .vscollections import get_collection, create_new_collection
from .vscollections import get_all_items_of_collection, delete_all_items_of_collection
from .vscollections import delete_collection, add_all_items_to_collection
from .connections import connect, close_connection
from users import users_get_userid, users_get_selection
from prints import errmsg, debugmsg 

## Copy a collection to a single user
def copy_single_mode(args):

    ## Connect to Video Station database
    conn, cur = connect()
    if(conn == None): exit(-1)
    debugmsg("Connected successfully to Synology VideoStation database" , args.mode)

    ## Get admin and its ID
    admin_id = users_get_selection(2)[1]

    ## Get the collection information
    collection_info = get_collection(cur, args.playlist, admin_id)
    if(collection_info == None):
        close_connection(conn, cur)
        exit(-1)
    debugmsg("Get the playlist information", args.mode)

    ## Get the userID of the passed username
    user_id = users_get_userid(args.user)
    if(user_id == None):
        close_connection(conn, cur)
        exit(-1)
    debugmsg("Get the UserID of the passed user", args.mode)

    ## Get all items of the collection
    items = get_all_items_of_collection(cur, collection_info)
    if(items == None):
        close_connection(conn, cur)
        exit(-1)
    debugmsg("Get all items of the playlist", args.mode)

    ## Create the new collection
    new_collection_id = create_new_collection(conn, cur, collection_info, user_id)
    if(new_collection_id == None):
        close_connection(conn, cur)
        exit(-1)
    debugmsg("Inserted the new playlist successfully", args.mode)

    ## Add all items to the new collection
    add_all_items_to_collection(conn, cur, items, new_collection_id)
    if(items == None):
        close_connection(conn, cur)
        exit(-1)
    debugmsg("Added all items to the new playlist", args.mode)

    ## Close connection
    close_connection(conn, cur)

## Delete a collection from a single user
def delete_single_mode(args):

    ## Connect to Video Station database
    conn, cur = connect()
    if(conn == None): exit(-1)
    debugmsg("Connected successfully to Synology VideoStation database", args.mode)

    ## Get the userID of the passed username
    user_id = users_get_userid(args.user)
    if(user_id == None):
        close_connection(conn, cur)
        exit(-1)
    debugmsg("Get the UserID of the passed user", args.mode)

    ## Get the collection information
    collection_info = get_collection(cur, args.playlist, user_id)
    if(collection_info == None):
        close_connection(conn, cur)
        exit(-1)
    debugmsg("Get the playlist information", args.mode)

    ## Delete all items of a collection
    delete_all_items_of_collection(conn, cur, collection_info)
    debugmsg("Delete all items of the playlist", args.mode)

    ## Delete the collection itself
    delete_collection(conn, cur, collection_info)
    debugmsg("Delete the playlist itself", args.mode)

    ## Close connection
    close_connection(conn, cur)
