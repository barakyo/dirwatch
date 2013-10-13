try:
    import pyinotify
except ImportError:
    print("Missing pyitnotify library")
    sys.exit(0)
from subprocess import call

class EventHandler(pyinotify.ProcessEvent):
    ext_map = {}

    def __init__(self, extensions):
        self.ext_map = extensions

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