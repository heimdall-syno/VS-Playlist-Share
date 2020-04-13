import psycopg2, pwd, grp, getpass
from psycopg2 import sql
from prints import errmsg, debugmsg

## Check whether the passed UserID is valid or not
def check_userid(conn, cur, userid):
    cur.execute(
            sql.SQL("SELECT * FROM vsuser WHERE {} = %s;").format(sql.Identifier('uid')),
            [userid]
    )
    result = cur.fetchone()
    if(result == None):
        errmsg("Could not find the userID")
        return None

    return result

## Get all users except the owner of the collection
def get_all_users_without_owner(conn, cur, owner_id):
    cur.execute(
        sql.SQL("SELECT * FROM vsuser WHERE uid <> %s;"),
        [owner_id]
    )
    result = cur.fetchall()
    if(result == None):
        errmsg("Could not get all users from the database")
        return None
    result = [r[0] for r in result]
    return result

## Get the username of the admin
def get_admin_user(all_users):
    users, admin = ([] for _ in range(2))
    for user in all_users:
        groups = [g.gr_name for g in grp.getgrall() if user[0] in g.gr_mem]
        gid = pwd.getpwnam(user[0]).pw_gid
        groups.append(grp.getgrgid(gid).gr_name)
        if "administrators" in groups:
            admin = user
        else:
            users.append(user)
    return (users, admin)

## Get all users of the Synology station
def get_user_selection(selection='users_only'):

    ## Split users and admin
    all_users = pwd.getpwall()
    all_users = [(u[0],u[2]) for u in all_users if grp.getgrgid(u[3])[0] == 'users']
    all_users = [u for u in all_users if u[0] != 'admin' and u[0] != 'guest']
    (users, admin) = get_admin_user(all_users)

    ## Users
    if selection == 'users_only':
        return users

    ## Users and admin
    elif selection == 'admin_users':
        return (users, admin)

    ## Admin only
    elif selection == 'admin_only':
        return admin
    else:
        errmsg("Could not identify user selection")
    return None

## Get the userID for a username (except admin)
def get_userid_from_name(username):
    users = get_user_selection()
    if(len(users) == 0):
        errmsg("Could not resolve the passed username (or admin)")
        return None
    user_id = [u[1] for u in users if u[0] == username]
    if(len(user_id) == 0):
        errmsg("Could not resolve the passed username (or admin)")
        return None
    return user_id[0]
