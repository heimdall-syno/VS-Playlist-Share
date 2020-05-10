
import os, sys
from .vscollections import get_collections_of_user, get_all_items_of_collection
from .vscollections import create_new_collection, add_all_items_to_collection
from .vscollections import delete_all_items_of_collection, delete_collection
from .connections import connect, close_connection
from users import users_get_selection
from prints import errmsg, debugmsg

def daemon_collections_same(user_collections, admin_collections):
    uc = set(sorted([uc[2] for uc in user_collections]))
    ac = set(sorted([ac[2] for ac in admin_collections]))
    if not ac.issubset(uc):
        new_collections = list(ac.difference(uc))
        new_collections = [i for i in admin_collections if i[2] in new_collections]
        return new_collections
    return []

def daemon_items_same(conn, cur, user_collection, admin_collection):

    ## Get all items of the collection
    user_items = get_all_items_of_collection(cur, user_collection)
    admin_items = get_all_items_of_collection(cur, admin_collection)
    if(user_items == None or admin_items == None):
        errmsg("Could not get items of admin collection")
        close_connection(conn, cur)
        exit(-1)
    if (set([u[0] for u in user_items]) == set([u[0] for u in admin_items])):
        return True
    return False

def daemon_collection_add_to_user(conn, cur, collection_info, user):
    new_collection_id = create_new_collection(conn, cur, collection_info, str(user[1]))
    if(new_collection_id == None):
        errmsg("Could not find collection of admin")
        close_connection(conn, cur)
        exit(-1)

    ## Get all items of the collection
    items = get_all_items_of_collection(cur, collection_info)
    if(items == None):
        errmsg("Could not get items of admin collection")
        close_connection(conn, cur)
        exit(-1)

    ## Add all items to the new collection
    add_all_items_to_collection(conn, cur, items, new_collection_id)
    if(items == None):
        close_connection(conn, cur)
        errmsg("Could not add items to user collection")
        exit(-1)

## Add a colletion to all users
def daemon_mode(args):

    debugmsg("Started execution", "Daemon mode")

    ## Connect to Video Station database
    conn, cur = connect()
    if (conn == None):
        errmsg("Could not connect to database"); exit(-1)
    debugmsg("Connected successfully to Synology Video Station database", "Daemon mode")

    ## Get the admin ID
    users, admin = users_get_selection(1)

    ## Get all collection information of the admin
    admin_collections = get_collections_of_user(cur, admin[1])
    if(admin_collections == None):
        close_connection(conn, cur)
        exit(-1)

    changes = False
    for user in users:
        ## Check whether user has all admin collections
        user_collections = get_collections_of_user(cur, user[1])
        new_collections = daemon_collections_same(user_collections, admin_collections)
        for collection_info in new_collections:
            daemon_collection_add_to_user(conn, cur, collection_info, user)
            debugmsg("Add another playlist to the user", "Daemon mode", (user[0], collection_info[2]))
            changes = True

        ## Check whether all items in every collection is synced
        for collection_info in admin_collections:
            user_collection = [uc for uc in user_collections if uc[2] == collection_info[2]]
            if user_collection:
                user_collection = user_collection[0]
                if not daemon_items_same(conn, cur, user_collection, collection_info):
                    delete_all_items_of_collection(conn, cur, user_collection)
                    delete_collection(conn, cur, user_collection)
                    daemon_collection_add_to_user(conn, cur, collection_info, user)
                    debugmsg("Renew playlist due to admin's playlist was updated", "Daemon mode", (user[0], collection_info[2]))
                    changes = True
    if not changes:
        debugmsg("Finish daemon mode without any changes", "Daemon mode")
    return
