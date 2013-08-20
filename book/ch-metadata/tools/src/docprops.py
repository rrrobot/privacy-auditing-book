#
# BSFUtils - The Boston Software Forensics Utilities for Windows
# (C) Copyright 2009, Richard M. Smith, All rights reserved
# For more information please contact richard.m.smith@bsf-llc.com or (617) 292-1889
#

#
# docprops.py - Python classes for extracting document properties (metadata) from Microsoft Office files
#
# Copyright (C) 2007 Richard M. Smith
#


import win32extras
import wincom
from bsfutils import *
from tsv import *
from error import error

# Property IDs for the SummaryInformation Property Set

PIDSI_TITLE               = 0x00000002  # VT_LPSTR
PIDSI_SUBJECT             = 0x00000003  # VT_LPSTR
PIDSI_AUTHOR              = 0x00000004  # VT_LPSTR
PIDSI_KEYWORDS            = 0x00000005  # VT_LPSTR
PIDSI_COMMENTS            = 0x00000006  # VT_LPSTR
PIDSI_TEMPLATE            = 0x00000007  # VT_LPSTR
PIDSI_LASTAUTHOR          = 0x00000008  # VT_LPSTR
PIDSI_REVNUMBER           = 0x00000009  # VT_LPSTR
PIDSI_EDITTIME            = 0x0000000a  # VT_FILETIME (UTC)
PIDSI_LASTPRINTED         = 0x0000000b  # VT_FILETIME (UTC)
PIDSI_CREATE_DTM          = 0x0000000c  # VT_FILETIME (UTC)
PIDSI_LASTSAVE_DTM        = 0x0000000d  # VT_FILETIME (UTC)
PIDSI_PAGECOUNT           = 0x0000000e  # VT_I4
PIDSI_WORDCOUNT           = 0x0000000f  # VT_I4
PIDSI_CHARCOUNT           = 0x00000010  # VT_I4
PIDSI_THUMBNAIL           = 0x00000011  # VT_CF
PIDSI_APPNAME             = 0x00000012  # VT_LPSTR
PIDSI_DOC_SECURITY        = 0x00000013  # VT_I4

# Property IDs for the DocSummaryInformation Property Set

PIDDSI_CATEGORY          = 0x00000002 # VT_LPSTR
PIDDSI_PRESFORMAT        = 0x00000003 # VT_LPSTR
PIDDSI_BYTECOUNT         = 0x00000004 # VT_I4
PIDDSI_LINECOUNT         = 0x00000005 # VT_I4
PIDDSI_PARCOUNT          = 0x00000006 # VT_I4
PIDDSI_SLIDECOUNT        = 0x00000007 # VT_I4
PIDDSI_NOTECOUNT         = 0x00000008 # VT_I4
PIDDSI_HIDDENCOUNT       = 0x00000009 # VT_I4
PIDDSI_MMCLIPCOUNT       = 0x0000000A # VT_I4
PIDDSI_SCALE             = 0x0000000B # VT_BOOL
PIDDSI_HEADINGPAIR       = 0x0000000C # VT_VARIANT | VT_VECTOR
PIDDSI_DOCPARTS          = 0x0000000D # VT_LPSTR | VT_VECTOR
PIDDSI_MANAGER           = 0x0000000E # VT_LPSTR
PIDDSI_COMPANY           = 0x0000000F # VT_LPSTR
PIDDSI_LINKSDIRTY        = 0x00000010 # VT_BOOL


FMTID_UserDefinedProperties = "{F29F85E0-4FF9-1068-AB91-08002B27B3D9}"
FMTID_SummaryInformation = "{F29F85E0-4FF9-1068-AB91-08002B27B3D9}"
FMTID_DocSummaryInformation = "{D5CDD502-2E9C-101B-9397-08002B2CF9AE}"


allSummaryInformation = (PIDSI_TITLE, PIDSI_SUBJECT, PIDSI_AUTHOR, PIDSI_KEYWORDS, PIDSI_COMMENTS, PIDSI_TEMPLATE, PIDSI_LASTAUTHOR, PIDSI_REVNUMBER, PIDSI_EDITTIME, PIDSI_LASTPRINTED, PIDSI_CREATE_DTM, PIDSI_LASTSAVE_DTM, PIDSI_PAGECOUNT, PIDSI_WORDCOUNT, PIDSI_CHARCOUNT, PIDSI_APPNAME, PIDSI_DOC_SECURITY)
allDocSummaryInformation = (PIDDSI_CATEGORY, PIDDSI_PRESFORMAT,	PIDDSI_BYTECOUNT, PIDDSI_LINECOUNT, PIDDSI_PARCOUNT, PIDDSI_SLIDECOUNT, PIDDSI_NOTECOUNT, PIDDSI_HIDDENCOUNT, PIDDSI_MMCLIPCOUNT, PIDDSI_SCALE, PIDDSI_HEADINGPAIR, PIDDSI_DOCPARTS, PIDDSI_MANAGER, PIDDSI_COMPANY, PIDDSI_LINKSDIRTY)

WIN95_IDENT = 0xA5DC
WIN97_IDENT = 0xA5EC

class docProps:

	columnNames = ("path", "fileOwner", "title", "author", "subject", "keywords", "comments", "template", "lastAuthor", "revNumber",\
	"lastEditTime", "lastPrinedTime", "createdTime", "lastSavedTime", "pageCount", "wordCount", "charCount")

	def __init__(self):
		self.path = None
		self.fileOwner = None
		self.title = None
		self.author = None
		self.subject = None
		self.keywords = None
		self.comments = None
		self.template = None
		self.lastAuthor = None
		self.revNumber = None
		self.lastEditTime = None
		self.lastPrintedTime = None
		self.createdTime = None
		self.lastSavedTime = None
		self.pageCount = None
		self.wordCount = None
		self.charCount = None
		self.appName = None
		self.docSecurity = None
		return

	@staticmethod
	def getFromFile(filename):
		props = docProps()
		try:
			props.fileOwner = fileOwner(filename)
		except:
			error.abortCheck()
			props.fileOwner = None
		stg = wincom.StgOpenStorage(filename, None, wincom.storagecon.STGM_READ | wincom.storagecon.STGM_SHARE_EXCLUSIVE)
		pss = stg.QueryInterface(wincom.IID_IPropertySetStorage)
		ps = pss.Open(FMTID_SummaryInformation)
		data = ps.ReadMultiple(allSummaryInformation)
		props.path = filename
		props.title = unicodeFix(data[0])
		props.author = unicodeFix(data[2])
		props.subject = unicodeFix(data[1])
		props.keywords = unicodeFix(data[3])
		props.comments = unicodeFix(data[4])
		props.template = unicodeFix(data[5])
		props.lastAuthor = unicodeFix(data[6])
		props.revNumber = unicodeFix(data[7])
		props.lastEditTime = PyTime2datetime(data[8])
		props.lastPrintedTime = PyTime2datetime(data[9])
		props.createdTime = PyTime2datetime(data[10])
		props.lastSavedTime = PyTime2datetime(data[11])
		props.pageCount = data[12]
		props.wordCount = data[13]
		props.charCount = data[14]
		props.appName = unicodeFix(data[15])
		props.docSecurity = data[16]
		try:
			ps = pss.Open(FMTID_DocSummaryInformation)
			data = ps.ReadMultiple([PIDDSI_COMPANY])
		# except pythoncom.com_err:      No workum, use plain except instead.  Sigh.
		except:
			error.abortCheck()
			error.traceback()
			data = [""]
		props.company = unicodeFix(data[0])
		return props
	
	def toTSVString(self, nopathf=False):
		row = []
		if not nopathf:
			row.append(self.path)
		row.extend([self.fileOwner, self.title, self.author, self.subject, self.keywords, self.comments,\
		self.template, self.lastAuthor, self.revNumber, self.lastEditTime, self.lastPrintedTime,self.createdTime,self.lastSavedTime,\
		self.pageCount, self.wordCount, self.charCount])
		return TSVRow.toTSVString(row) 

def fileOwner(path):
	sd = win32extras.GetFileSecurity(path, 1)
	ownerSID = sd.GetSecurityDescriptorOwner()
	ownerName = win32extras.LookupAccountSid(None, ownerSID) 
	return unicodeFix(ownerName[1]) + "\\" + unicodeFix(ownerName[0])

def wordRevLog(filename):
	try:
		stg = wincom.StgOpenStorage(filename, None, wincom.storagecon.STGM_READ | wincom.storagecon.STGM_SHARE_EXCLUSIVE)
	except:
		error.abortCheck("Cannot open file -- %s", filename)
		return None
	try:
		stream = stg.OpenStream("WordDocument", None, wincom.storagecon.STGM_SHARE_EXCLUSIVE, 0)
		contents = stream.Read(0x02DA);
		if contents == None:
			return None
	except:
		error.abortCheck()
		return None
	filehdr = BinReader(contents)
	sign = filehdr.getWord();
	if sign != WIN95_IDENT and sign != WIN97_IDENT:
		return None
	filehdr.seek(0x02D2)
	revLogOffset = filehdr.getDWord()
	revLogSize = filehdr.getDWord()
	if revLogOffset == None or revLogSize == None or revLogSize == 0:
		return None
	try:	
		stream = stg.OpenStream("1Table", None, wincom.storagecon.STGM_SHARE_EXCLUSIVE, 0)
		contents = stream.Read(revLogOffset + revLogSize);
		if contents == None:
			return None
	except:
		error.abortCheck()
		return None
	revLog = BinReader(contents)
	revLogTable = []
	revLog.seek(revLogOffset + 2)
	count = revLog.getDWord()
	if count == None or count == 0 or count > 20 or (count % 2) != 0:
		return None
	count = count / 2
	for i in xrange(count):
		entry = SimpleStruct()
		n = revLog.getWord()
		if n == 0 or n > 512:
			break
		entry.person = revLog.getUString(n)
		n = revLog.getWord()
		if n == 0 or n > 512:
			break
		entry.filePath = revLog.getUString(n)
		revLogTable.append(entry)
	return revLogTable
