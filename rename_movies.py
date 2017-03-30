#!/usr/bin/python

import os
import subprocess
import shutil
import ntpath
import re
import errno  

# --------------------------------------------------------

#The top level directory to scan and then move items into folder based on the
#first relevant character of the movie title, following by a directory that is the movie name
#then all files related to the movie in that directory.
source_root = "/mnt/freenas/multimedia/Downloads/other/movies/"
target_root = "/mnt/freenas/multimedia/Movies/"


#Valid file suffixes to group into the same folder as the associated movie
suffixes = ("-trailer.mp4", "-trailer.mov","-clearart.png","-fanart.jpg","-logo.png","-poster.jpg","-thumb.jpg", ".orig.nfo", "-banner.jpg", "-disc.png", "-landscape.jpg", "thumb.jpg", ".nfo", ".srt", ".sub")

#Valid movie extensions
supported_video_extensions = (".mkv", ".avi", ".mp4", ".mov")

#words to ignore when deciding which first character to use for the folder name that the movie
#folder will go into
ignored_words = ("the","in","of","a","For")

#If True, the script won't rename or move anthying, it will just print what it would do to screen.
is_dry_run = True
# ---------------------------------------------------------


def shouldIgnore(filename):
	for nextSuffix in suffixes:
		if(filename.endswith(nextSuffix)):
			return True
	return False

def isSupportedVideo(filename):
	for nextExtension in supported_video_extensions:
		if(filename.endswith(nextExtension)):
			return True
	return False

def shouldIgnoreWord(word):
	for nextIgnoredWord in ignored_words:
		if(word == nextIgnoredWord):
			return True
	return False

def replace_last(source_string, replace_what, replace_with):
    head, _sep, tail = source_string.rpartition(replace_what)
    return head + replace_with + tail

def removeSuffix(filename):
	result = filename
	for nextSuffix in suffixes:
		result = replace_last(result, nextSuffix, "")
	return result

def mapToFolder(filename):
	filenameWithoutSuffix = removeSuffix(filename)
	movieDir= re.sub('[^a-zA-Z0-9\-]', '_', filenameWithoutSuffix)
	alphaDir = "Other"
	for word in movieDir.split('_'):
		if(not shouldIgnoreWord(word.lower())):
			return word.lower()[0] + "/" + movieDir

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

#
# Main loop
#
for root, dirs, files in os.walk(source_root):
	print root
	for name in sorted(files):
		filename, file_extension = os.path.splitext(name)
		soure_path = root + name

		if(shouldIgnore(name)):
			target_dir = target_root + mapToFolder(name)
			print "mv " + soure_path + " " + target_dir + "/" + name
			if(not is_dry_run):
				mkdir_p(target_dir)
				os.rename(soure_path, target_dir + "/" + name)
			
		elif(isSupportedVideo(name)):
			target_dir = target_root + mapToFolder(filename)
			print "mv " + soure_path + " " + target_dir + "/" + name
			if(not is_dry_run):
				mkdir_p(target_dir)
				os.rename(soure_path, target_dir + "/" + name)
		else:
			print "unable to map ", name
	#break so we only scan the top level dir
	break
