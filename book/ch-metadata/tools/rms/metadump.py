#
# BSFUtils - The Boston Software Forensics Utilities for Windows
# (C) Copyright 2009, Richard M. Smith, All rights reserved
# For more information please contact richard.m.smith@bsf-llc.com or (617) 292-1889
#

import setpath
import sys

import iolib
import wincom
from _main import _main
from cmdline import cmdline
from bsfutils import *
from macros import expandMacros, standardMacros
from docprops import docProps,wordRevLog
from tsv import TSVRow
from error import error 

helpMsg = \
"""

metadump - Dump metadata from a Microsoft Office file (.DOC, .XLS, .PPT, etc.)

metadump <filename> ... [<options>]

   /s                Search for files in subdirectories
   /z                Search for files inside of Zip files
   /-q               Non-quiet mode -- Show all error messages [defualt]
   /q                Quiet mode -- suppress non-critical error messages
   /nomd5            Do not output MD5 hash values for files [default]
   /md5              Output MD5 hash value for files
   /table            Produce a table output file
   /out:name         Specify the name of the output file
   /relpath          Show relative file paths [default]
   /fullpath         Show full file paths

See also: exetype, exifdump, filever

Category: FileInspect
"""

OUT_NORMAL = 0
OUT_TSV = 1

def main(argv):
	if cmdline.askedForHelp("metadump", helpMsg, argv):
		return
	options = cmdlParse(argv)
	options.outClass = outClasses[options.outFormat]
	options.outClass.startOutput(options)
	for path in options.filenames:
		path = expandMacros(path, options.locals)
		if path == None:
			continue
		iolib.findFiles(path, processFile, options)
	options.outClass.endOutput(options)
	return

def cmdlParse(argv):
	options = cmdline.defaultOptions()
	options.filenames = []
	options.outFormat = OUT_NORMAL
	options.outFile = None
	options.outRedirector = iolib.outRedirector()
	options.quietf = False
	options.md5f = False
	options.fullpathf = False
	scanner = cmdline.scanner(argv)
	while scanner.isMore():
		scanner.getNext()
		if scanner.isPositionalArg():
			arg = scanner.getValue()
			if not arg.startswith("@"):
				options.filenames.append(arg)
			else:
				newfiles = cmdline.processIncludeFile(arg[1:])
				if newfiles == None:
					return None
				options.filenames.extend(newfiles)
		elif error.switches(scanner):
			pass
		elif scanner.match("/s"):
			options.recursef = True	
		elif scanner.match("/z"):
			options.walkZipsf = True	
		elif scanner.match("/table"):
			options.outFormat = OUT_TSV
		elif scanner.match("/out:"):
			options.outFile = scanner.getValue()
		elif scanner.match("/q"):
			options.quietf = True
		elif scanner.match("/-q"):
			options.quietf = False
		elif scanner.match("/md5"):
			options.md5f = True
		elif scanner.match("/-md5"):
			options.md5f = False
		elif scanner.match("/fullpath"):
			options.fullpathf = True
		elif scanner.match("/relpath"):
			options.fullpathf = False
		else:
			scanner.unknownSwitch()
	if len(options.filenames) == 0:
		error.fatal("Missing file name", ())
	return options

def processFile(entry, options):
	if entry.attributes & iolib.FILE_ATTRIBUTE_DIRECTORY:
		return
	filename = entry.path
	filename2 = filename
	tempFilename = None
	if iolib.webfile.isWebPath(filename) or iolib.zipfile.isZipPath(filename):
		tempFilename = iolib.makeTempCopy(filename)
		if tempFilename == None:
			return
		filename2 = tempFilename
	oldStdout = options.outRedirector.redirect(entry, options)
	if oldStdout == None:
		iolib.removeTempCopy(tempFilename)
		return
	if not wincom.StgIsStorageFile(filename2):
		error.signal("File %s is not a Micorosft Office document file", (filename))
		iolib.removeTempCopy(tempFilename)
		return
	try:
		props = docProps.getFromFile(filename2)
		props.path = filename
	except:
		error.exception("Unable to access file %s", (filename))
		iolib.removeTempCopy(tempFilename)
		return
	try:
		revLog = wordRevLog(filename2)
	except:
		error.abortCheck()
		revLog = None
	entry.md5 = None
	if options.md5f:
		entry.md5 = md5file(filename2)
	iolib.removeTempCopy(tempFilename)
	options.outClass.showMetadata(entry, props, revLog, options)
	options.outRedirector.restore(oldStdout)
	return

class normalOutput:

	@staticmethod
	def startOutput(options):
		return

	@staticmethod
	def endOutput(options):
		return

	@staticmethod
	def showMetadata(entry, props, revLog, options):
		print
		print
		print "Metadata of file %s" % (entry.path if options.fullpathf else entry.relPath)
		print
		print "File date/time:      %s" % (entry.lastModifiedTimestamp)
		print "File size:           %s" % (bytesFormat(entry.size))
		if options.md5f:
			print "MD5:                 %s" % (entry.md5)
		print "Title:               %s" % (props.title)
		print "Author:              %s" % (props.author)
		print "Organization:        %s" % (props.company)
		print "Last person to edit: %s" % (props.lastAuthor)
		print "Subject:             %s" % (props.subject)
		print "Keywords:            %s" % (props.keywords)
		print "Comments:            %s" % (props.comments)
		print "Template:            %s" % (props.template)
		if props.createdTime != None:
			print "Created:             %s" % (props.createdTime)
		if props.lastPrintedTime != None:
			print "Last printed:        %s" % (props.lastPrintedTime)
		if props.lastEditTime != None:
			print "Last edit:           %s" % (props.lastEditTime)
		if props.lastSavedTime != None:
			print "Last saved:          %s" % (props.lastSavedTime)
		if revLog == None or len(revLog) == 0:
			return
		print
		print "Revision log"
		print
		for entry in revLog:
			print "\"%s\" editted \"%s\"" % (entry.person, entry.filePath)
		return

class TSVOutput:

	@staticmethod
	def startOutput(options):
		columnNames = iolib.fileEntry.columnNames[:-1]
		columnNames.append("path" if options.fullpathf else "relPath")
		if options.md5f:
			columnNames.append("md5")
		columnNames.extend(docProps.columnNames[1:])
		print "\t".join(columnNames)
		return

	@staticmethod
	def endOutput(options):
		return

	@staticmethod
	def showMetadata(entry, props, revLog, options):
		line = iolib.fileEntry.toTSVString(entry, fullpathf=options.fullpathf)
		if options.md5f:
			line += "\t" + TSVRow.toTSVString([entry.md5])
		line += "\t" + props.toTSVString(nopathf=True)
 		print line
		return

outClasses = [normalOutput, TSVOutput]

if __name__ == "__main__":
	_main(main)
