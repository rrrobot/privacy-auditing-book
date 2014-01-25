all:
	(cd book;make)

clean:
	find . -name '*~' -exec rm {} +
	(cd book;make clean)

