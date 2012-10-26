import base64
import glob
import json
import logging
import mutagen
import os
import re
import settings
import urllib

from django.views.decorators.cache import cache_page
from django.http import (HttpResponseRedirect,
                        HttpResponseServerError,
                        HttpResponse)
from django.template import Context, loader
from django.utils.translation import ugettext as _, activate

log = logging.getLogger(__name__)

BASE_PATH = settings.MUSIC_APP_ROOT
PATH_LEN = len(BASE_PATH)

def song_info(request, song=None):
    """ Read id3 tags """

    a = {}
    song = os.path.join(BASE_PATH, _decode(song))

    log.warn(song)
    log.warn(os.path.exists(song))

    if (os.path.exists(song)):
        a = mutagen.File(song, easy=True)

    d = os.path.split(song)[0]
    d += "/*.jpg"

    # glob doesn't like some chars, so replace with ?
    restricted_char = r'[][]'
    d = re.sub(restricted_char, '?', d)

    image = glob.glob(d)

    if image:
        image = image[0][PATH_LEN:]
        log.warn(image)
        if not image.startswith('/'):
            image = "/" + image
    else:
        image = "/album.jpg"

    y = dict(zip(a.keys(), a.values()))

    y['image'] = image
    y['search_path'] = d
    y['song'] = song

    return HttpResponse(json.dumps(y))


#@cache_page(60 * 15)
def ajax_file_view(request, dir=None):

    if dir:
        dir = _decode(dir)
    else:
        dir = os.path.join(BASE_PATH, 'music')

    r = []

    r = file_list_gen(r, dir, 0)

    #r.pop()  # remove extra </ul>

    return HttpResponse(json.dumps({
        'dir': dir,
        'files': r,
    }))


@cache_page(60 * 15)
def ajax_playlist_view(request, pl_file=None):
    ### Im not sure how this should work

    if pl_file:
        #Test that pl_file is valid
        pl_file = _decode(urllib.unquote_plus(pl_file))
        if not os.path.exists(pl_file):
            return HttpResponseServerError(
                json.dumps('pl_file: ' + str(pl_file) + ' doesnt exist')
            )

        y = pl_file.split('/')
        y.pop()
        d = '/'.join(y)

        r = {
            'playlist_file': pl_file,
            'files': [],
        }

        f = open(pl_file)
        x = f.readlines()
        f.close()

        count = 0

        for fl in x:
            if fl.startswith('#') or fl == "" or fl == "\n":
                continue
            count += 1
            fp = os.path.join(d, fl)
            fp = fp.rstrip('\r\n')
            r['files'].append({
                'song_path': fp[PATH_LEN:],
                'id': _encode(fp),
                'track_number': count
            })

    else:
        search_path = os.path.join(BASE_PATH, 'music')
        playlists = []
        playlists = pl_list_gen(playlists, search_path)

        r = {
            'search_path': search_path,
            'playlists': playlists,
        }

    return HttpResponse(json.dumps(r))


def pl_list_gen(p, d):
    try:
        for i in os.listdir(d):
            fi = os.path.join(d,i)
            if (fi.endswith('.m3u')):
                p.append({
                    'path': fi,
                    'id': _encode(fi),
                    'file': fi.split('/')[-1],
                    'directory': fi.split('/')[-2],
                })
            elif os.path.isdir(fi):
                pl_list_gen(p, fi)
    except Exception, e:
        log.error('bad stuff')

    return p


def file_list_gen(r, d, recursive=1):
    log.info("Starting file_list_gen() with - " + str(d))
    try:
        for f in os.listdir(d):
            ff = os.path.join(d, f)
            # fix this
            if (not f.endswith('.AppleDouble')
                and not f.endswith('.jpg')
                and not f.endswith('.nfo')
                and not f.endswith('.m3u')
                and not f.endswith('.sfv')
                and not f.endswith('.txt')
                and not f.endswith('.JPG')):

                if os.path.isdir(ff):
                    r.append({
                        'type': 'directory',
                        'id': _encode(ff),
                        'path': ff[PATH_LEN:],
                        'name': f
                    })
                    if recursive:
                        log.info("Recursing to - " + str(ff))
                        r = file_list_gen(r, ff)
                        log.info("Done recursing for - " + str(ff))
                else:
                    file_extensions = [
                            '.mp3',
                            '.mp4',
                            '.ogg',
                            '.flac',
                            '.wav',
                            '.m4a'
                    ]
                    if filter(f.endswith, file_extensions):
                        # get .ext and remove dot
                        e = os.path.splitext(f)[1][1:]
                        r.append({
                            'type': 'file',
                            'id': _encode(ff),
                            'path': ff[PATH_LEN:],
                            'name': f,
                            })
    except Exception, e:
        log.error(str(e))
        r.append('Could not load directory: %s' % str(e))

    log.info("finishing file_list_gen()")
    return r


# _encode and _decode are helpers to remove padding chars from base64 encoded
# strings because jquery doesn't like having '=' in selectors.
#
def _decode(string):
    string = (string + "===")[0: len(string) + (len(string) % 4)]

    try:
        return base64.b64decode(string)
    except TypeError as e:
        log.warn('incorrect padding for %s' % string)
        return HttpResponseServerError()


def _encode(string):
    return base64.b64encode(string).replace('=', '')
