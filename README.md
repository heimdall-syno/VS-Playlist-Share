VS-Playlist-Share
=========
VS-Playlist-Share is a script for sharing playlists within the VideoStation of synology because the VideoStation doesn't support it. It enables the copying of a single playlist owning by the admin to a single user or to all users of the VideoStation. The playlists can be deleted analogously.

The script is executed by an admin user via SSH on the diskstation.

#### Requirements
- Python 2.7 (Default of DSM 6.x)
- pip (curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && sudo python get-pip.py)
- psycopg2 (sudo pip install psycopg2/psycopg2-binary)

#### Getting started
- ```
  $ make
  $ sudo -u postgres python main.py 
        -p | --playlist "<playlist name>"
		-u | --user 	"<username>"
		-m | --mode 	<copy-single|delete-single|copy-all|delete-all>
  ```
		
#### Example
- ```
  $ sudo -u postgres python main.py -m delete-all "Test-Playlist"
  ```

