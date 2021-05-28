#!/usr/bin/env python3
# Built for Python 3.7.3
# Take any input file and run it through the best command to losslessly optimize file size.

# DEPENDENCIES:
#   python3
#   python-magic (pip3 install magic-python) https://github.com/ahupp/python-magic
#
#   7zip (https://www.7-zip.org/)
#   AdvanceCOMP Utilities (https://www.advancemame.it/comp-readme)
#       Contains both advzip and advpng.
#   cwebp (https://developers.google.com/speed/webp/docs/cwebp)
#   flac (https://xiph.org/flac/)
#   jpegoptim (https://github.com/tjko/jpegoptim)
#   optipng (http://optipng.sourceforge.net/)
#   pngcrush (not yet used)
#
# OPTIONAL:
#   file

from pathlib import Path
from sys import argv, exit, platform
from subprocess import run
import gzip


### BEGIN ARGUMENTS
def define_arguments():
# https://docs.python.org/3/howto/argparse.html
# https://docs.python.org/3/library/argparse.html
	import argparse
	parser = argparse.ArgumentParser(
		description="Automate lossless optimization of many file types.",
		prog="optpymize")
	
	# Gather input files.
	parser.add_argument("files",
		help="List files to be processed.",
		# Adding "+" to nargs means input must have at least one variable.
		# Use "*" if none are necessary.
		nargs="*")

	# Search directories recursively.
	# https://gist.github.com/89465127/5273149
	parser.add_argument("-r", "--recursive",
		help="Search recursively through directories for files to process.",
		action="store_true",
		dest="use_recursion")

	# Convert gzip to 7zip. Default is to do nothing.
	parser.add_argument("-g", "--convert-gzip",
		help="Recompress gzipped files as 7zip.",
		action="store_true",
		dest="convert_gzip")

	# Strip metadata from JPGs
	parser.add_argument("-j", "--strip-jpg", "--strip-jpeg",
		help="Strip metadata from JPGs. Otherwise JPGs left untouched.",
		# "store_true" will make the variable True when the flag is set. Otherwise, defaults to False.
		action="store_true",
		dest="strip_jpg")

	# Convert PNGs to WebP instead of using the usual PNG compression method
	parser.add_argument("-p", "--convert-png",
		help="Convert PNG files to WebP.",
		action="store_true",
		dest="convert_png")

	# Convert wav to FLAC. Default is to do nothing.
	parser.add_argument("-w", "--convert-wav",
		help="Convert wav files to FLAC.",
		action="store_true",
		dest="convert_wav")
	
	# Delete thumbnails from ODT and similar files where it is unnecessary.
	parser.add_argument("--delete_thumbnails",
		help="Delete unnecessary thumbnails embedded in ODT files. (Does nothing right now.)",
		action="store_true",
		dest="delete_thumbnails"
		)

	#parser.add_argument("-7", "--optimize-7z-contents",
		#help="Optimize contents of 7zip files before recompressing.",
		#action="store_true",
		#dest="optimize_7z_contents")

	#parser.add_argument("-z", "--optimize-zip-contents",
		#help="Optimize contents of zip files before recompressing.",
		#action="store_true",
		#dest="optimize_zip_contents")

	# Shortcut to 
	parser.add_argument("-A", "--all-optimizations",
		help="Enable all conversion optimizations (same as -jw). Use twice to enable less common conversion optimizations and destructive optimizations (-gjpw).",
		action="count",
		default=0,
		dest="all_optimizations")

	# Return the variable holding the arguments. Assign it where called for later use.
	return parser.parse_args()


### BEGIN SUPPORT FUNCTIONS

# Console colors using ANSI escape. Use with print(f"{WARNING}Your text here{ENDC}")
if platform.startswith("win32"):
	# Colors do not work on Windows in CMD or PowerShell.
	OKGREEN = ''
	WARNING = ''
	ERROR = ''
	ENDC = ''
	#BOLD = ''
	#UNDERLINE = ''
else:
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	ERROR = '\033[91m'
	ENDC = '\033[0m'
	#BOLD = '\033[1m'
	#UNDERLINE = '\033[4m'


def keep_smaller_file(original_file, new_file):
	# Compare the size of each file. Remove the larger file.
	if Path(new_file).stat().st_size < Path(original_file).stat().st_size:
		print("New file was smaller in size.")
		Path(original_file).unlink()
	else:
		# Not deleting old file under all other else conditions is fail safe.
		print("Original file was smaller or equal in size.")
		Path(new_file).unlink()
	
	print("Smaller file will be kept.")
	
	# If original file was removed and new_file still exists, rename to remove temp extension.
	# TODO: This will rename it to have the wrong file extension sometimes?
	# Cannot just use the original file to rename because it may have been in a different format.
	if Path(new_file).exists():
		Path(new_file).rename(new_file.with_suffix(""))
	# If original file still exists, then nothing to do. New file should have been removed if it was larger.


def compress_to_7z(file):
	print("Creating 7zip container...")
	run([x7z, 'a', '-t7z', '-m0=lzma2', '-mx=9', '-myx=9', '-mqs=on', '-ms=on', f'{file}.7z', file])


### END SUPPORT FUNCTIONS


### BEGIN OPTIMIZATION FUNCTIONS

# Commands to optimize files.
optimize_msg = "Optimizing {} file."


def optimize_7z(file, optimize_7z_contents=False):
	print(optimize_msg.format("7zip"))
	print("7zip not yet supported. Sorry. :c")

	# TODO: Everything
	# Extract the files to a known directory.
	# Unpack
	# Lack of space after switch is intentional. 7z's command line interface is bad.
	#7z x -o"${file%.7[zZ]}" "$file"
	
	# new_file = f'{file.rsplit(".", 1)[0]}.7z.tmp'
	#run(['7z', 'x', f'-o"{new_file}', file])
	
	# Provides a predictable destination for extracted files. Use this because 7z doesn't have a nice way of getting them otherwise.  ./${file%.7[zZ]}/*
	
	# Does not delete original archive. Do at end if new size smaller.
	
	# Optionally optimize archive contents.
	#if optimize_7z_contents:
		# Optimize everything in the directory.
		#optimize_file(extracted, recursion=True)
	#else:
	#	print("Skipping individual file optimization.")
	
	# Repack
	#compress_7z("./${file%.7[zZ]}/")
	
	# Confirm repack smaller than original
	#keep_smaller_file(file, new_file)

#def optimize_archive_contents(file, destructive=False):
	# Delete unecessary resource fork in archives created on Mac computers.
	# https://en.wikipedia.org/wiki/Resource_fork
	# https://superuser.com/questions/104500/what-is-macosx-folder
	#if destructive:
		# Delete _MACOSX directory.
		#shutil.rmtree("_MACOSX")
		# Delete .DS_Store files.
		#Path.unlink(".DS_Store")


def optimize_gz(file, convert_gzip=False):
	print(optimize_msg.format("gzipped"))

	if convert_gzip:
		# Decompress
		decompressed_file = Path(file).with_suffix('')

		# Open and write out decompressed gz file.
		with open(decompressed_file, 'wb') as f:
			with gzip.open(file, 'rb') as g:
				f.write(g.read())
		# Close files to prevent memory leaks in PyPy.
				g.close()
			f.close()
		
		# Recompress to 7zip
		# TODO: Will cannibalize any files that have the filename.7z
		compress_to_7z(decompressed_file)
		
		# Cleanup
		remove(decompressed_file)
		
		# Check that 7zip file is smaller than original
		keep_smaller_file(file, f'{decompressed_file}.7z')
	else:
		print(f"Skipping {file}. Converting gzip to 7zip not enabled.")


def optimize_flac(file):
	print(optimize_msg.format("FLAC"))
	print(f"Re-compressing {file}...")
	
	# Set filename for new file.
	new_file = Path(file).with_suffix('.flac.tmp')
	
	# Use appropriate command for appropriate system.
	try:
		# Compress FLAC at maximum compression.
		run([flac, file, '-f', '-V', '--compression-level-8', '-o', new_file])
	except:
		print("Please install `flac` to continue.")
	
	# Compare file size, delete the smaller one, rename if necessary.
	try:
		keep_smaller_file(file, new_file)
	except:
		print("Could not compare file size between wav and FLAC.")


def optimize_jpeg(file, strip_jpg=False):
	print(optimize_msg.format("JPEG image"))

	if strip_jpg:
		run([jpegoptim, '--strip-all', file])
	else:
		print(f"{WARNING}Option `--strip-jpg` not set. Metadata will be untouched.{ENDC}")
		run([jpegoptim, file])


def optimize_odt(file, delete_thumbnail=False):
	print(optimize_msg.format("OpenDocument Text"))
	
	# Delete bulky thumbnail from file.
	#if delete_thumbnail:
		# Contents are inside a zip file. Extract it.
		# Delete the auto-generated thumbnail image.
		# Optimize image files and such embedded in the document?
	
	# Recompress it with ADVzip with .odt extension.
	print("Optimizing ODT zip compression.")
	optimize_zip(file)

#def optimize_pdf(file):
	# Probably use Ghostscript or something.
	# https://stackoverflow.com/questions/10450120/optimize-pdf-files-with-ghostscript-or-other
	# https://askubuntu.com/questions/113544/how-can-i-reduce-the-file-size-of-a-scanned-pdf-file
	# http://tuxdiary.com/2015/04/07/compress-pdf-files-linux/
	# Offer OCR?  ocrmypdf


def optimize_png(file, convert_png=False):
	# TODO: APNGs will be completely broken by the optimizers. Need a way to identify them before it reaches here and skip them.
	# Consider also: https://sourceforge.net/projects/apng/files/APNG_Optimizer/
	# And to convert to animated WebP: https://github.com/Benny-/apng2webp
	# Will need to write something custom to search the file for an Animation Control Chunk.
	#  - https://stackoverflow.com/questions/47104481/bash-script-check-if-image-is-animated-png-apng
	#  - https://wiki.mozilla.org/APNG_Specification
	
	print(optimize_msg.format("PNG image"))
	
	if convert_png:
		print("Converting PNG to WebP...")
		optimize_webp(file)
	else:
		print("Optimizing PNGs...")
		
		# TODO: Consider adding PNGCrush. It hasn't given good results though.
		
		try:
			print("Using OptiPNG...")
			run([optipng, '-o7', '-fix', file])
		except:
			print("Please install OptiPNG to improve compression. (http://optipng.sourceforge.net/)")
		
		# AdvPNG should be run last.
		try:
			print("Using AdvPNG...")
			run([advpng, '-z4', file])
		except:
			print("Please install AdvanceCOMP Utilities to use AdvPNG. (https://www.advancemame.it/comp-readme)")


def optimize_wav(file, convert_wav=False):
	print(optimize_msg.format("WAV"))
	
	if convert_wav:
		print("Converting wav file to FLAC...")
		
		try:
			optimize_flac(file)
		except TypeError:
			print("Failed to convert wav to FLAC.")
		
		# Delete original wav file if flac was created successfully.
		if Path(file).with_suffix('.flac').exists():
			Path(file).unlink()
	else:
		print("Leaving WAV as is.")


#def optimize_rar(file):
	# TODO: If cbr, convert to cbz. Else, convert to 7z.


#def optimize_txt(file):
	# TODO: Strip trailing white-space off the ends of lines.


def optimize_webp(file):
	print(optimize_msg.format("WebP image"))

	# Set filename for new file.
	new_file = Path(file).with_suffix('.webp.tmp')

	try:
		run([cwebp, '-z', '9', file, '-o', new_file])
	except:
		print("Please install `cwebp` and try again.")
	
	# Compare file size, delete the smaller one, rename if necessary.
	if Path(new_file).exists():
			keep_smaller_file(file, new_file)


def optimize_zip(file, optimize_zip_contents=False):
	print(optimize_msg.format("Zip container"))
	
	#if optimize_zip_contents:
		# Extract zip file
		
		# Optimize contents
		#optimize_file('extracted-file-directory')
	
	try:
		run([advzip, '-z4', file])
	except:
		print("Please install the AdvanceCOMP utilities and try again.\n",
			"https://www.advancemame.it/comp-readme")

### END OPTIMIZATION FUNCTIONS


### START

# Check if python-magic can be imported. Use `is_magic` to track if it succeeded.
try:
	import magic
	is_magic = True
except ImportError:
	# TODO: Clean up error messages.
	print("It appears python-magic is not installed.")
	is_magic = False
	
	# Offer to attempt installing automatically.
	print("Python can attempt to install the required files automatically.")
	magic_install_choice = confirm()
	
	if magic_install_choice in accept_options:
		# Import some extras to aid with installing.
		from sys import executable
		from subprocess import check_call
		
		try:
			# The preferred way to use pip is through subprocess.
			# check_call will ensure the process completes successfully before continuing.
			# Using the system executable variable is a path to the currently running version of Python, ensuring a compatible version is installed. Works cross-platform.
			check_call([executable, '-m', 'pip', 'install', 'python-magic'])
			
			# If on Windows, install the necessary binary as well.
			if platform.startswith('win32'):
				check_call([executable, '-m', 'pip', 'install', 'python-magic-bin==0.4.14'])
		except:
			print("Could not install. Please ensure pip or Python is installed to PATH and try again.")
		
		try:
			# Try importing again
			import magic
			is_magic = True
		except:
			print("Could not install. Please ensure pip is installed and try again.")
			is_magic = False
	else:
		print("Please install `python-magic` with pip.")
		if platform.endswith('win32'):
			print("On Windows, also install the binaries for Magic with `pip3.exe install python-magic-bin==0.4.14`")


# Set all the executable locations because Windows is a special duck.
# Defining these outside of a function makes them automatically global variables.
if platform.startswith('win32'):
	# Special extra windows junk
	from shutil import which
	from os import getenv
	
	# Install/import winreg
	try:
		import winreg
	except ImportError:
		print("Installing winreg...")
		check_call([executable, '-m', 'pip', 'install', 'winreg'])
	finally:
		try:
			import winreg
		except ImportError:
			print("Unable to install winreg module. Please ensure pip is installed.")	
	
	
	# Get local system variables
	localappdata = getenv("LocalAppData")
	programfiles = getenv("ProgramFiles")  # Alternate maybe?  %ProgramW6432%
	programfiles32 = getenv("ProgramFiles(x86)")
	
	
	# Check if installed things exist where expected.
	def check_paths(*paths) -> str:
		#print(paths)
		for path in paths:
			try:
				# Pathlib can't handle a None type. Check before it so it is never reached.
				# An empty path returns True. Don't want that.
				if path != None and path != "" and Path(path).exists():
					return path
			except TypeError:
				print(f"{ERROR}Pathlib is probably acting up. Please report this message.{ENDC}")
		return None  # Redundant?
	
	
	# Attempt to find where a program is installed through the registry.
	def check_registry_location(program) -> str:
		try:
			regkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, fr"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\{program}")
			return winreg.QueryValue(regkey, None)
		except FileNotFoundError:
			return ""  # NoneType will cause errors in pathlib. Use empty string instead.
	
	
	# Find if programs exist on the system path or expected default locations, then add them.
	x7zip = check_paths(
		# 7zFM.exe may be registered, but not 7z.exe. They're likely in the same directory.
		check_registry_location("7zFM.exe").replace("7zFM.exe", "7z.exe"),
		which("7z.exe"), 
		f"{programfiles}\\7-Zip\\7z.exe",
		f"{localappdata}\\7-Zip\\7z.exe",
		f"{programfiles32}\\7-Zip\\7z.exe"
	)
	# TODO: Update everything below with real paths. Current are filler.
	flac = check_paths(
		which('flac.exe'),	
		#check_registry_location('flac.exe'),
		f"{programfiles}\\flac\\win64\\flac.exe", 
		f"{localappdata}\\flac\\win64\\flac.exe",
		f"{programfiles32}\\flac\\win32\\flac.exe"
	)
	jpegoptim = check_paths(
		which('jpegoptim.exe'), 
		#check_registry_location('jpegoptim.exe'),
		f"{programfiles}\\jpegoptim\\jpegoptim.exe", 
		f"{localappdata}\\jpegoptim\\jpegoptim.exe",
		f"{programfiles32}\\flac\\bin\\flac.exe"
	)
	optipng = check_paths(
		which('optipng.exe'), 
		#check_registry_location('optipng.exe'),
		f"{programfiles32}\\optipng\\optipng.exe", 
		f"{programfiles}\\optipng\\optipng.exe", 
		f"{localappdata}\\optipng\\optipng.exe"
	)
	advpng = check_paths(
		which('advpng.exe'), 
		#check_registry_location('advpng.exe'),
		f"{programfiles}\\advancecomp\\advpng.exe", 
		f"{localappdata}\\advancecomp\\advpng.exe",
		f"{programfiles32}\\flac\\bin\\flac.exe"
	)
	cwebp = check_paths(
		which('cwebp.exe'), 
		#check_registry_location('cwebp.exe'),
		f"{programfiles}\\libwebp\\bin\\cwebp.exe", 
		f"{localappdata}\\libwebp\\bin\\cwebp.exe",
		f"{programfiles32}\\flac\\bin\\flac.exe"
	)
	advzip = check_paths(
		which('advzip.exe'), 
		#check_registry_location('advzip.exe'),
		f"{programfiles}\\advancecomp\\advzip.exe", 
		f"{localappdata}\\advancecomp\\advzip.exe",
		f"{programfiles32}\\flac\\bin\\flac.exe" 
	)
else:
	# Every other system is nice and simple.
	x7z = '7z'
	flac = 'flac'
	jpegoptim = 'jpegoptim'
	optipng = 'optipng'
	advpng = 'advpng'
	cwebp = 'cwebp'
	advzip = 'advzip'



def get_mimetype(file) -> str:
	# Check if magic-python imported successfully.
	if is_magic == True:
		# Check if input is a file or directory before passing to magic.
		# python-magic will fail if given a directory.
		if Path(file).is_dir():
			type = 'inode/directory'
		else:
			# *~ M a g i c ~*
			try:
				# Get the mime-type from a file using magic.
				type = magic.from_file(file, mime=True)
			except IsADirectoryError:
				# This should be redundant with the above if statement, but it's here just in case to catch.
				type = 'inode/directory'

	elif is_magic == False:
		if platform.startswith('linux'):
			print("Falling back to using native `file` command to detect mime-type.")
			
			# The output of stdout is not clean. Need to clean it.
			# Solution: https://python-forum.io/Thread-paramiko-read-stdout
			type = run(['file', '-b', '--mime-type', file], capture_output=True).stdout.decode('ascii').strip("\n")
			# The line above is ridiculous but it works.
		else:
			print("This script can use Python's default mimetypes module in place of python-magic. Results may be less accurate.\n",
				"Continue with default mimetypes module?")
			mimetype_module_choice = confirm()
			
			if mimetype_module_choice in accept_options:
				print("Falling back to default Python mimetypes module.")
				
				# https://docs.python.org/3/library/mimetypes.html
				import mimetypes
				
				# This uses file extensions to guess, which fails if there's no extension, or has the wrong extension. Unreliable.
				type = mimetypes.guess_type(file)
			else:
				print("Stopping script.")
				# Exit, because this can't do anything if it can't identify file types.
				exit()

	print(f"Discovered mime-type to be '{type}'.")
	return type


def optimize_file(*files, 
		#optimize_7z_contents=False, 
		convert_gzip=False, 
		delete_thumbnails=False,
		strip_jpg=False, 
		convert_png=False, 
		convert_wav=False, 
		#optimize_zip_contents=False, 
		recursion=False):

	for file in files:
		print(f'{OKGREEN}\nCurrent file is "{file}".{ENDC}')
		
		# Get the file's mimetype so we can handle it correctly.
		# Path objects must be converted to strings to work with Magic.
		type = get_mimetype(str(file))
		
		# Choose the correct optimizer to use.
		# Python does not support case statements. :c
		if   type == 'application/x-7z-compressed': optimize_7z(file, optimize_7z_contents=optimize_7z_contents)
		elif type in ('application/gzip', 'application/x-gzip'): optimize_gz(file, convert_gzip=convert_gzip)
		elif type in ('audio/flac', 'audio/x-flac'): optimize_flac(file)
		elif type == 'image/jpeg': optimize_jpeg(file, strip_jpg=strip_jpg)
		elif type == 'application/vnd.oasis.opendocument.text': optimize_odt(file, delete_thumbnail=delete_thumbnails)
		#elif type == 'application/pdf': optimize_pdf(file)
		elif type == 'image/png': optimize_png(file, convert_png=convert_png)
		#elif type == 'application/x-rar': optimize_rar(file)
		#elif type == 'text/plain': optimize_txt(file)
		elif type == 'audio/x-wav': optimize_wav(file, convert_wav=convert_wav)
		elif type == 'image/webp': optimize_webp(file)
		elif type in ('application/zip', 'application/epub+zip'): optimize_zip(file, optimize_zip_contents=optimize_zip_contents)
		elif type == 'inode/x-empty':
			print(f'File "{file}" is empty. Nothing to do.')
		elif type == 'inode/directory':
			print(f"{file} is a directory.")
			# Recursive function to handle all directories as they come.
			# TODO: Ensure this will not follow symlinks/shortcuts!
			if recursion:
				print(f"Optimizing contents of {file}")
				new_files = [
					# Create a list of each item in the directory prepended with relative path.
					new for new in Path(file).iterdir()
					]
				
				optimize_file(*new_files,
					#optimize_7z_contents=optimize_7z_contents,
					convert_gzip=convert_gzip,
					strip_jpg=strip_jpg,
					convert_png=convert_png,
					convert_wav=convert_wav,
					#optimize_zip_contents=optimize_zip_contents,
					recursion=recursion
					)
			else:
				print(f"Skipping {file}. Use `-r` to recursively optimize files inside directories.")
		elif type == '':
			print(f"{ERROR}This file has no mime-type. This shouldn't be possible.{ENDC}")
		else:
			print(f"No optimizer available for file type '{type}'")



# If script is run as the main file, gather arguments to use.
# Will not activate if imported as a module.
# https://realpython.com/python-main-function/
if __name__ == "__main__":
	# Set up command line arguments so they can be processed.
	args = define_arguments()
	
	if args.all_optimizations == 1:
		args.strip_jpg = True
		args.convert_wav = True
		#args.optimize_zip_contents = True
		#args.optimize_7z_contents = True
	elif args.all_optimizations >= 2:
		args.convert_gzip = True
		args.delete_thumbnails = True
		args.strip_jpg = True
		args.convert_png = True
		args.convert_wav = True
		#args.optimize_zip_contents = True
		#args.optimize_7z_contents = True
	
	
	# Pass all required argument options to the optimize function so global vars are not needed.
	optimize_file(*args.files, 
		#optimize_7z_contents=args.optimize_7z_contents,
		convert_gzip=args.convert_gzip,
		strip_jpg=args.strip_jpg,
		convert_png=args.convert_png,
		convert_wav=args.convert_wav,
		#optimize_zip_contents=args.optimize_zip_contents,
		recursion=args.use_recursion
		)
		
	### DONE! ###
	if not args.files:
		print("No files given. If you'd like to optimize all files in the current directory, use a wildcard.\n")
		if platform.startswith('linux'):
			print("In Bash, use the * character.")
		if platform.startswith('win32'):
			print("In Powershell, use (get-item *) to pass multiple files at once with a wildcard. (CMD does not support wildcard expansion.)\nExample: py -3 optimize.py (get-item *.jpg)")
			print("You may also drag-and-drop multiple files onto the script at once.")
		print("\n\tTip: Select all files with the same extension using *.png\n")
		print("Use `-h` or `--help` to view the help.\n")
	
	if platform.startswith('linux') or platform.startswith('win32'):
		print(f"\n{OKGREEN}Optimizations completed.{ENDC}")
	else:
		print(f"\n{WARNING}Unsupported system. Sorry. Did it complete?{ENDC}")
