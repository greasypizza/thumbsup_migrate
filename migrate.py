#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gmusicapi import Mobileclient

export_api = Mobileclient()
import_api = Mobileclient()

# create/use app specific passwords.
export_user = ''
export_pw = ''
import_user = ''
import_pw = ''

if not export_api.login(export_user, export_pw, Mobileclient.FROM_MAC_ADDRESS):
  print "export login failed"
  exit()

if not import_api.login(import_user, import_pw, Mobileclient.FROM_MAC_ADDRESS):
  print "import login failed"
  exit()

print "logged in"

all_tracks = export_api.get_all_songs()
print "found %d tracks" % len(all_tracks)

promoted_tracks = export_api.get_promoted_songs()
print "found %d promoted tracks" % len(promoted_tracks)

promoted_rated = [track for track in promoted_tracks if track.has_key('rating')]
print "found %d promoted rated tracks" % len(promoted_rated)

promoted_thumbs_up = [track for track in promoted_rated if track['rating'] == '5']
print "found %d promoted thumbsup tracks" % len(promoted_thumbs_up)

store_tracks = [track for track in all_tracks if track.has_key('storeId')]
print "found %d store tracks" % len(store_tracks)

rated_tracks = [track for track in store_tracks if track.has_key('rating')]
print "found %d rated store tracks" % len(rated_tracks)

thumbs_up = [track for track in rated_tracks if track['rating'] == '5']
thumbs_down = [track for track in rated_tracks if track['rating'] == '1']
print "found %d thumbs up tracks" % len(thumbs_up)
print "found %d thumbs down tracks" % len(thumbs_down)

import_api_promoted_tracks = import_api.get_promoted_songs()
import_thumbsup = [track['storeId'] for track in import_api_promoted_tracks]

# When I was writing this, attempting to import songs from a specific artist would always break shit
skip_artists = []

for track in promoted_thumbs_up:
  print "importing %(artist)s - %(title)s" % track
  if track['storeId'] in import_thumbsup:
    print 'already imported, skipping'
    continue
  if track['artist'] in skip_artists:
    print 'skipping'
    continue
  id = import_api.add_store_tracks(track['storeId'])
  song = import_api.get_track_info(track['storeId'])
  song['rating'] = '5'
  import_api.change_song_metadata(song)
  
