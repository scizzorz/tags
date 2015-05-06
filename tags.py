#!/usr/bin/env python

import argparse
import os

from datetime import datetime

class Tag:
  def __init__(self, string=None, tag=None, timestamp=None):
    if string is not None:
      temp = string.split()
      self.tag = temp[0]
      self.datetime = datetime.fromtimestamp(int(temp[1]))

    elif tag is not None:
      self.tag = tag
      if timestamp is None:
        self.datetime = datetime.utcnow()
      else:
        self.datetime = timestamp

  def __str__(self):
    return '{} {}'.format(self.tag, int(self.datetime.timestamp()))

  def __repr__(self):
    return 'Tag(tag={!r}, datetime={!r})'.format(self.tag, self.datetime)


def main(args):
  # read tag file
  try:
    with open(os.path.expanduser(args.file)) as tag_file:
      tags = [Tag(line) for line in tag_file]
  except FileNotFoundError:
    tags = []

  # add tags from arguments
  for tag in args.tags:
    tags.append(Tag(tag=tag))

  # filter based on the search (-s)
  display_tags = filter(lambda x: args.search in x.tag, tags)

  # filter based on the number (-n)
  if args.search != 0:
    display_tags = list(display_tags)[-args.number:]

  # display tags
  for tag in display_tags:
    print(repr(tag))

  # write tag file
  with open(os.path.expanduser(args.file), 'w') as tag_file:
    tag_file.write('\n'.join(str(tag) for tag in tags))

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.set_defaults(func=main)

  parser.add_argument('-n', '--number', type=int, default=10, help='Limit number of tags.')
  parser.add_argument('-s', '--search', type=str, default='', help='Search within tags.')
  parser.add_argument('-f', '--file', type=str, default='~/.tags', help='The file to load tags from.')
  parser.add_argument('tags', type=str, nargs='*', help='The tags to record.')

  args = parser.parse_args()
  args.func(args)
