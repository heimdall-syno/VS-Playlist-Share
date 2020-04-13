from .vscollections import get_collection, create_new_collection
from .vscollections import add_all_items_to_collection, delete_all_items_of_collection
from .vscollections import delete_collection, get_all_items_of_collection
from .connections import connect, close_connection
from .users import get_user_selection
from prints import errmsg, debugmsg

## Add a colletion to all users
def copy_all_mode(args):

    ## Connect to Video Station database
    conn, cur = connect()
    if(conn == None): exit(-1)
    debugmsg("Connected successfully to Synology VideoStation database", args.mode)

    ## Get admin and its ID
    admin_id = get_user_selection('admin_only')[1]

    ## Get the collection information
    collection_info = get_collection(cur, args.playlist, admin_id)
    if(collection_info == None):
        close_connection(conn, cur)
        exit(-1)
    debugmsg("Get the playlist information", args.mode)

    ## Get all users except the owner of the collection
    users_id = [u[1] for u in get_user_selection()]
    if(len(users_id) == 0):
        close_connection(conn, cur)
        exit(-1)
    debugmsg("Get all user information", args.mode)

    ## Get all items of the collection
    items = get_all_items_of_collection(cur, collection_info)
    if(items == None):
        close_connection(conn, cur)
        exit(-1)
    debugmsg("Get all items of the playlist", args.mode)

    for user in sorted(users_id):
        ## Create the new collection
        new_collection_id = create_new_collection(conn, cur, collection_info, str(user))
        if(new_collection_id == None):
                close_connection(conn, cur)
                exit(-1)
        debugmsg("Inserted the new playlist successfully for user", args.mode, (user,))

        ## Add all items to the new collection
        add_all_items_to_collection(conn, cur, items, new_collection_id)
        if(items == None):
                close_connection(conn, cur)
                exit(-1)
        debugmsg("Added all items to the new playlist for user", args.mode, (user,))
        new_collection_id = None

    ## Close connection
    close_connection(conn, cur)

## Delete a collection from all users except the admin
def delete_all_mode(args):

    ## Connect to Video Station database
    conn, cur = connect()
    if(conn == None): exit(-1)
    debugmsg("Connected successfully to Synology VideoStation database", args.mode)

    ## Get admin and its ID
    admin_id = get_user_selection('admin_only')[1]

    ## Get all corresponding collection information
    collection_info = get_collection(cur, args.playlist)
    if(collection_info == None):
        close_connection(conn, cur)
        exit(-1)
    collection_info = [c for c in collection_info if c[1] != admin_id]
    debugmsg("Get all playlist information", args.mode)

    for collection in collection_info:
        ## Delete all items of a collection
        delete_all_items_of_collection(conn, cur, collection)
        debugmsg("Delete all items of the playlist for user", args.mode, (collection[1],))

        ## Delete the collection itself
        delete_collection(conn, cur, collection)
        debugmsg("Delete the playlist itself for user", args.mode, (collection[1],))

    ## Close connection
    close_connection(conn, cur)
