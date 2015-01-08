from beets.plugins import BeetsPlugin
from beets import ui, config, library

from os import system, fsync
from os.path import isdir, isfile, join, relpath
from tempfile import NamedTemporaryFile

def get_playlist_items(lib, playlist):
    if not config['syncpl']['playlist_dir'].get():
        raise ui.UserError(u'no playlist_dir specified')

    if not isdir(config['syncpl']['playlist_dir'].get()):
        raise ui.UserError(u'invalid playlist_dir')

    pl_path = join(config['syncpl']['playlist_dir'].get(), playlist)

    if not isfile(pl_path):
        raise ui.UserError(u'playlist not found: ' + playlist)

    items = set()

    with open(pl_path, 'r') as f:
        for path in f.readlines():
            full_path = join(config['directory'].get(),
                             path.strip('\n').decode('utf-8'))
            items.update(lib.items(query=u'path:"%s"' % full_path))

    return items

def get_query_items(lib, query):
    return set(lib.items(query=query))

def syncpl(lib, opts, args):
    if args:
        config['syncpl']['dest'] = args[0]

    if not config['syncpl']['dest']:
        raise ui.UserError(u'no destination path specified')

    if not isdir(config['syncpl']['dest'].get()):
        raise ui.UserError(u'invalid destination path')

    if not config['syncpl']['playlists'].get() and \
       not config['syncpl']['queries'].get():
        raise ui.UserError(u'nothing to sync')

    items = set()
    paths = set()

    # Retrieve the playlist items to sync
    for playlist in config['syncpl']['playlists'].as_str_seq():
        items.update(get_playlist_items(lib, playlist))

        if config['syncpl']['include_playlist']:
            paths.add(playlist.encode('utf-8'))

    # Retrieve the query items to sync
    for query in config['syncpl']['queries'].as_str_seq():
        items.update(get_query_items(lib, query))

    # Retrieve the track and album art paths
    for item in items:
        paths.add(relpath(item.path, config['directory'].get().encode('utf-8')))

        if item.get_album().artpath:
            paths.add(relpath(item.get_album().artpath,
                              config['directory'].get()))

    # Write the paths to a reference file for rsync
    with NamedTemporaryFile() as tmp:
        tmp.write('\n'.join(paths))
        tmp.flush()
        fsync(tmp.fileno())

        src = join(config['directory'].get(), '')

        if config['syncpl']['playlist_dir']:
            src += ' ' + join(config['syncpl']['playlist_dir'].get(), '')

        system('rsync -amv --include="*/" --include-from=%s --exclude="*" \
                --delete-excluded %s %s' %
                        (tmp.name, src, config['syncpl']['dest'].get()))

class SyncplPlugin(BeetsPlugin):
    def __init__(self):
        super(SyncplPlugin, self).__init__()
        self.config.add({
            u'dest': None,
            u'playlist_dir': None,
            u'include_playlist': True,
            u'playlists': [],
            u'queries': [],
        })

    def commands(self):
        cmd = ui.Subcommand('syncpl', help='sync music files to a folder')
        cmd.func = syncpl
        return [cmd]
