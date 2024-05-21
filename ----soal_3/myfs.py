#!/usr/bin/env python3

from fuse import FUSE, FuseOSError, Operations
import os
import shutil

class MyFS(Operations):
    def __init__(self, source_dir, target_dir):
        self.source_dir = source_dir
        self.target_dir = target_dir

    def readdir(self, path, fh):
        dirents = ['.', '..']
        dirents.extend(os.listdir(self.source_dir))
        return dirents

    def getattr(self, path, fh=None):
        full_path = self._full_path(path)
        st = os.lstat(full_path)
        return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                     'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))

    def read(self, path, size, offset, fh):
        full_path = self._full_path(path)
        with open(full_path, 'rb') as f:
            f.seek(offset)
            return f.read(size)

    def _full_path(self, partial):
        if partial.startswith("/"):
            partial = partial[1:]
        path = os.path.join(self.source_dir, partial)
        return path

def main(mountpoint, source_dir, target_dir):
    FUSE(MyFS(source_dir, target_dir), mountpoint, nothreads=True, foreground=True)

if __name__ == '__main__':
    main('./[nama_bebas]', './relics', './report')

