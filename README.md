VS-Playlist-Share
=========
VS-Playlist-Share is a script for sharing playlists within the Synology's Video Station. It is intended to run as Scheduled Task in DSM to periodically check whether all playlists of the admin are shared with all users. Of course there is also an manual mode in case the admin wants to manually copy or delete playlists.

## Overview of the VS-Components
```
             +---------------------------------------------------------------------------------+
             |                                  Synology DSM                                   |
             +---------------------------------------------------------------------------------+
             |                  +--------------------+  +-----------------+                    |
             |                  |       Docker       |  |      Docker     |                    |
             |                  |transmission.openVpn|  |     Handbrake   |                    |
             |                  +--------------------+  +-----------------+                    |
             | +------------+   | +---------------+  |  | +-------------+ |  +---------------+ |
             | |VS-SynoIndex|   | |VS-Transmission|  |  | | VS-Handbrake| |  |VS-Notification| |
             | |   (Task)   +---->+   (Script)    +------>+   (Script)  +--->+    (Task)     | |
             | +------------+   | +---------------+  |  | +-------------+ |  +---------------+ |
             |                  +--------------------+  +-----------------+                    |
             |                                                                                 |
             | +-----------------+                                                             |
             | |VS-Playlist-Share|                                                             |
             | |     (Task)      |                                                             |
             | +-----------------+                                                             |
             +---------------------------------------------------------------------------------+
```

Check out the other components:

VS-SynoIndex:      https://github.com/heimdall-syno/VS-SynoIndex

VS-Transmission:   https://github.com/heimdall-syno/VS-Transmission

VS-Handbrake:      https://github.com/heimdall-syno/VS-Handbrake

VS-Notification:   https://github.com/heimdall-syno/VS-Notification

#### Requirements
- Python >= 3.5

## Quick Start

1. Install the dependencies (>=Python3.5 and pip3) and make sure both are in $PATH. If Python already exists execute the commands to get pip3:
  ```
  $ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
  $ sudo python3 get-pip.py
  ```

2. Clone the repository inside an abritrary path e.g. $home-directory.

3. Install the psycopg2 package for Python3
  ```
  $ sudo make
  ```

4. Check whether the script works as expected. If the help section is shown then everything will probably work fine.
  ```
  $ sudo -u postgres python3 main.py -h
  ```

5. Make sure the Scheduled task (Control Panel > Task Scheduler):
	```
    Task:       VS-Playlist-Share
    User:       root
    Schedule:   daily
    Command:    sudo -u postgres python3 /volume1/homes/user/VS-Playlist-Share/main.py --daemon
    ```


#### Manual execution

In case the admin wants to manually copy or delete playlists, the manual execution can be used as well:

- ```
  $ sudo -u postgres python3 main.py
        --playlist "<playlist name>"
        --user     "<username>"
        --mode     <copy-single|delete-single|copy-all|delete-all>
  Examples:
    Copy playlist to an user:     sudo -u postgres python3 main.py --playlist Test --user testuser --mode copy-single
    Delete playlist of an user:   sudo -u postgres python3 main.py --playlist Test --user testuser --mode delete-single
    Copy playlist to all users:   sudo -u postgres python3 main.py --playlist Test --mode copy-all
    Delete playlist of all users: sudo -u postgres python3 main.py --playlist Test --mode delete-all
  ```
