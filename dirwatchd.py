import sys
try:
    import pyinotify
except ImportError:
    print("Missing pyinotify library")
    sys.exit(0)
try:
    import Pyro4
except ImportError:
    print("Missing Pyro4 library")
    sys.exit(0)
import json

from event_handler import EventHandler

class DirWatchDaemon():

    def __init__(self):
        # Dictionary of all the paths being watched
        self.wm_dict = dict()
        # Watch manager object
        self.watch_mgr = pyinotify.WatchManager()
        # Masks used to watch
        self.mask = pyinotify.IN_CREATE | pyinotify.IN_MODIFY
        # Notifier
        self.notifiers = list()

    def add_dir(self, name):
        # Look for config.json file in directory
        try:
            # Try to get the config file
            json_config = open(name + "/config.json")
        except IOError:
            # Let user know it wasn't found
            raise IOError("config.json cannot be found for " + name)
        else:
            # If found, process and create a new event handler for this dir
            handler = EventHandler(json_config)
            # Create a ThreadedNotifier for the handle
            t_notifier = pyinotify.ThreadedNotifier(self.watch_mgr, handler)
            # Start the notifier
            t_notifier.start()
            # Append to list of notifiers
            self.notifiers.append(t_notifier)
            # Update watch manager dict
            self.wm_dict = dict((self.wm_dict.items() + 
                (self.watch_mgr.add_watch(name, self.mask).items())))
            print("Adding " + name)

    def remove_dir(self, name):
        # Find the directory in the dictionary
        try:
            # Try to remove key from dictionary
            rm_dir = self.wm_dict.pop(name)
        except KeyError:
            raise KeyError("Cannot remove " + name 
                + " since it is not being watched")
        else:
            # Remove dir from watch manager
            self.watch_mgr.rm_watch(rm_dir)
            print(name + " has been removed from the watch list")

    def get_dirs(self):
        return self.wm_dict


def main():
    dirwatch = DirWatchDaemon()
    Pyro4.Daemon.serveSimple({
        dirwatch: "dirwatch"
    }, port=9009, ns=False)

if __name__ == "__main__":
    main()
