import Pyro4
import sys

class DirWatchClient():
	uri = "PYRO:dirwatch@localhost:9009"
	daemon = Pyro4.Proxy(uri)

	def add_dirs(self, directories):
		if directories:
			for dir_path in directories:
				print("Adding directory: "  + dir_path)
				try:
					self.daemon.add_dir(dir_path)
				except IOError, ioe:
					print("Error: %s" % ioe)
		else:
			raise ValueError("Please provide a directory to add")

	def delete_dirs(self, directories):
		if directories:
			for dir_path in directories:
				try:
					self.daemon.remove_dir(dir_path)
				except KeyError, ke:
					print("Error %s" %ke)
		else:
			raise ValueError("Please provide a directory to remove")
			
	def list_dirs(self):
		dir_dict = self.daemon.get_dirs()
		if dir_dict:
			print("Watching the following directories: ")
			print(dir_dict)
		else:
			print("Currently no directories are being watched.")

dirwatchc = DirWatchClient()
print(sys.argv)
if "add" in sys.argv:
	# Adding
	try:
		dirwatchc.add_dirs(sys.argv[2:])
	except ValueError, ve:
		print("Error: %s" % ve)
elif "del" in sys.argv:
	# Deleting
	try:
		dirwatchc.delete_dirs(sys.argv[2:])
	except ValueError, ve:
		print("Error: %s" % ve)
elif "list" in sys.argv:
	dirwatchc.list_dirs()
else:
	# Raiser error
	print("Please use a command")


