beets-syncpl
============

*beets-syncpl* is a plugin that uses rsync to sync a selection of your music
library to a destination folder. The music selection is specified by playlists
and queries defined in the beets configuration file.

This plugin can be used, for example, to sync a selection of your music library
with a media device.

Please note, this plugin will *delete* files in the destination folder if it's
no long specified by a playlist or query. You've been warned.

Configuring
-----------

In order to use this plugin you'll first need to configure it in the beets
configuration file. The following section can be used as a reference:

```yaml
syncpl:
    dest: /mnt/sdb1
    playlist_dir: /path/to/playlists
    include_playlist: yes
    playlists: Summer.m3u Winter.m3u
    queries:
        - artist:Jaga Jazzist
        - album:Blue Lines
```

* `dest` The directory to which the music will be synchronized. This
  is optional since you can specify the destination as the command argument.
* `playlist_dir` The directory where *syncpl* can find the playlists to sync.
* `include_playlist` Also sync the playlist file to the destination (default:
  yes).
* `playlists` The list that specifies which playlists to sync.
* `quries` The list that specifies which queries to sync.

Usage
-----

After specifying which songs need to be synced in the configuration file, simply
run the following command:

```
beet syncpl [dest]
```

The `dest` argument is not needed when it is specified in the configuration
file.
