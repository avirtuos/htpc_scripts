# htpc_scripts

This is a simple collection of helper and automation scripts I've written and used to manage my own media library and thought it might be useful for others.

## rename_movies.py:

This simple script scans a source directory and re-organizes all the movies within the top-level of the source into folders like: $SOURCE/a/American_Pie/American_Pie.mkv  assuming the top level directory ($SOURCE) had a moview called American_Pie.mkv. The script is also smart enough to group nfo, -banner.jgp, etc... files with the movies.

Most of the limited functionality offered by this script is configurable by adjusting the variables at the top of the script. It is also pretty simple to modify for your own needs.I recommend running the script with is_dry_run set to true before letting it actually reorganize anything, so you can be 100% certain you like what it will do.

