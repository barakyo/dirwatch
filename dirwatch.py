#!/usr/bin/python

import pyinotify
import argparse
from subprocess import call

parser = argparse.ArgumentParser(
    description='''Will watch files in the specified 
    directory for updates and run compile commands 
    based on their extensions''')
parser.add_argument('-r', '--recursive', action="store_true",
        default = False,
        help='Will recursively watch the dir and its subdirs')
parser.add_argument('directory', type=str,
        help='The directory to watch')
args = parser.parse_args()

wm = pyinotify.WatchManager()
# Handle updates for on create and on modify
mask = pyinotify.IN_CREATE | pyinotify.IN_MODIFY

class EventHandler(pyinotify.ProcessEvent):
    ext_map = {
        '.tex': ['pdflatex'],
        '.less': ['lessc'],
        '.scala': ['scala'],
        '.sass': ['sass'],
        '.cql': ['neo4j-shell -file']
    }

    def process_IN_CREATE(self, event):
        print "Creating: ", event.pathname

    def process_IN_MODIFY(self, event):
        print "Updating: ", event.pathname
        self.run_command(event.path, event.name)

    def run_command(self, file_path, file_name):
        # Find the extension
        ext_index  = file_name.rfind('.')
        ext = file_name[ext_index:]
        # Determine if this ext is in the map
        if ext in self.ext_map:
            print "Running Command: " + self.ext_map[ext][0] + " " + file_path + "/" +  file_name
            call(self.ext_map[ext][0] + " " + file_path + "/" + file_name, shell=True)
        else:
            print "Ext not found"

handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)
wdd = wm.add_watch(args.directory, mask, rec=args.recursive)

notifier.loop()
