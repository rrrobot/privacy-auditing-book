#
# BSFUtils - The Boston Software Forensics Utilities for Windows
# (C) Copyright 2010, Richard M. Smith, All rights reserved
# For more information please contact richard.m.smith@bsf-llc.com or (617) 292-1889
#

import winonly
import noironpython

from error import error

try:
	import win32com.client
	from pywintypes import com_error
	from win32com import storagecon
	from pythoncom import StgIsStorageFile, StgOpenStorage, IID_IPropertySetStorage
	import win32com.client.makepy
except:
	error.fatal("Windows COM support for Python is not installed on this computer")

def COMOpen(progID, events=None):
	try:
		if events == None:
			return win32com.client.Dispatch(progID)
		else:
			return win32com.client.DispatchWithEvents(progID, events)
	except:
		error.abortCheck()
		error.traceback()
		return None
		
makepy = win32com.client.makepy
		