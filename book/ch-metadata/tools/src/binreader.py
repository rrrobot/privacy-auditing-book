#
# BSFUtils - The Boston Software Forensics Utilities for Windows
# (C) Copyright 2009, Richard M. Smith, All rights reserved
# For more information please contact richard.m.smith@bsf-llc.com or (617) 292-1889
#

#
# binreader.py - BinReader class for extracting binary values and strings from a byte array
#
# Copyright (C) 2007 Richard M. Smith
#

import struct

class BinReader(object):

	def __init__(self, contents):
		self.contents = contents
		self.offset = 0
		return

	def seek(self, offset, direction = 0):
		if direction == 0:
			newoffset = offset
		elif direction == 1:
			newoffset = self.offset + offset
		elif direction == 2:
			newoffset = len(self.contents) + offset
		else:
			raise ValueError, "Bad direction parameter \"%d\" passed to BinReader.seek()" % (direction)
		if newoffset < 0 or newoffset > len(self.contents):
			raise ValueError, "Bad seek offset 0x%08X passed in to BinReader.seek().  Max offset is 0x%08X" % (offset, len(self.contents))
		self.offset = newoffset
		return 

	def size(self):
		return len(self.contents)
		
	def isEOF(self):
		return self.offset >= len(self.contents)

	def getByte(self):
		try:
			value = struct.unpack("B", self.contents[self.offset:self.offset+1])[0]
			self.offset += 1
			return value
		except:
			return None
	
	def getWord(self):
		try:
			value = struct.unpack("H", self.contents[self.offset:self.offset+2])[0]
			self.offset += 2
			return value
		except:
			return None

	def getBIWord(self):
		try:
			value = struct.unpack(">H", self.contents[self.offset:self.offset+2])[0]
			self.offset += 2
			return value
		except:
			return None
	
	def get3ByteNumber(self):
		try:
			value = struct.unpack("H", self.contents[self.offset:self.offset+2])[0]	+ 65536 * struct.unpack("B", self.contents[self.offset+2:self.offset+3])[0]
			self.offset += 3
			return value
		except:
			return None
	
	def getDWord(self):
		try:
			value = struct.unpack("L", self.contents[self.offset:self.offset+4])[0]
			self.offset += 4
			return value
		except:
			return None

	def getBIDWord(self):
		try:
			value = struct.unpack(">L", self.contents[self.offset:self.offset+4])[0]
			self.offset += 4
			return value
		except:
			return None
	
	def getQWord(self):
		try:
			value = struct.unpack("Q", self.contents[self.offset:self.offset+8])[0]
			self.offset += 8
			return value
		except:
			return None

	def getBIQWord(self):
		try:
			value = struct.unpack(">Q", self.contents[self.offset:self.offset+8])[0]
			self.offset += 8
			return value
		except:
			return None
	
	def getSByte(self):
		try:
			value = struct.unpack("b", self.contents[self.offset:self.offset+1])[0]
			self.offset += 1
			return value
		except:
			return None
	
	def getSWord(self):
		try:
			value = struct.unpack("h", self.contents[self.offset:self.offset+2])[0]
			self.offset += 2
			return value
		except:
			return None
	
	def getSDWord(self):
		try:
			value = struct.unpack("l", self.contents[self.offset:self.offset+4])[0]
			self.offset += 4
			return value
		except:
			return None
	
	def getSQWord(self):
		try:
			value = struct.unpack("q", self.contents[self.offset:self.offset+8])[0]
			self.offset += 8
			return value
		except:
			return None
	
	def getIntByWidth(self, width):
		try:
			if width == 1:
				return self.getSByte()
			if width == 2:
				return self.getSWord()
			if width == 4:
				return self.getSDWord()
			if width == 8:
				return self.getSQWord()
			no = self.getUIntByWidth(width)
			if no == None:
				return None  
			mask = long(1) << (width * 8 - 1)
			if no & mask:
				no = no - (mask << 1)
			return no
		except:
			return None
	
	def getUIntByWidth(self, width):
		try:
			if width == 1:
				return self.getByte()
			if width == 2:
				return self.getWord()
			if width == 3:
				return self.get3ByteNumber()
			if width == 4:
				return self.getDWord()
			if width == 5:
				l = self.getByte()
				h = self.getDWord()
				return (long(h) << 8) + l
			if width == 6:
				l = self.getWord()
				h = self.getDWord()
				return (long(h) << 16) + l
			if width == 7:
				l = self.getByte()
				m = self.getWord()
				h =	self.getDWord()
				return (long(h) << 24) + (m << 8) + l
			if width == 8:
				return self.getQWord()
			return None
		except:
			return None
	
	def getString(self, length):
		if length == None:
			return None
		try:
			value = self.contents[self.offset:self.offset + length]
			self.offset += length
			return value
		except:
			return None
	
	def getCString(self):
		try:
			i = self.contents.index('\0', self.offset)
			value = self.contents[self.offset:i]
			self.offset = i + 1
			return value
		except:
			return None
	
	def getUCString(self):
		outstr = ""
		i = self.offset
		while i < len(self.contents) - 1:
			ch = ord(self.contents[i]) + 256 * ord(self.contents[i + 1])
			if ch == 0:
				break
			outstr += unichr(ch)
			i += 2
		self.offset += (len(outstr) + 1) * 2
		return outstr
	
	def getUString(self, count):
		if count == None:
			return None
		outstr = ""
		for i in xrange(self.offset, len(self.contents), 2):
			if count <= 0:
				break
			ch = ord(self.contents[i]) + 256 * ord(self.contents[i + 1])
			outstr += unichr(ch)
			count -= 1
		self.offset += len(outstr) * 2
		return outstr
		
	def getUTF8String(self, length):
		if length == None:
			return None
		try:
			value = self.contents[self.offset:self.offset + length]
			self.offset += length
			return unicode(value, "utf-8", "replace")
		except:
			return None

