Hi Simson,

Attached are two ZIP files.  Src.zip contains the interesting source code
for my metadump utility. I left out a few dozen Python files that provide
the infrastructure for my toolkit that are not relevant to metadata
extraction process.   The bin.zip contains a compile executable for Windows.
Check out also the /table switch.

Using the IID_IPropertySetStorage interface does illustrate a couple of
issues:  1).  The utility only works on Windows and 2).  It does not support
the newer Office file formats such as .docx, .xlsx, etc.  To support the
newer formats requires a different approach.  The easiest is to parse the
appropriate XML file of a .DOCX file using ElementTree and extract the
content of metadata tags.

Richard
