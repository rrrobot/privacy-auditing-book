all:
	echo 'make what?'

clean:
	find . -name '*~' -exec rm {} +
	(cd book;make clean)

