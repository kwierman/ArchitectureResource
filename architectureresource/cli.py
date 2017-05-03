# -*- coding: utf-8 -*-

import click
import logging
import sys
import logging
import signal
import sys


@click.command()
@click.argument('file_list', nargs=-1)
def print_images(file_list):
  logging.basicConfig(level=logging.DEBUG)
  from architectureresource.image_writer import ImageWriter
  for _file in file_list:
    writer = ImageWriter(_file)
    writer.get_all_particle_images()


@click.command()
def get_resource_for_network():
  logging.basicConfig(level=logging.DEBUG)
  from architectureresource.resource import NetworkAnalyzer
  


if __name__ == "__main__":
    main()