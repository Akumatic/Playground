# Utils

## DupeFinder
#### Description
DupeFinder iterates over all given folders, creating md5 hashes of every file and storing them in a list.

It removes duplicate files and outputs the path of deleted file as well as the path of the first found file with same hash.
#### Usage
Call DupeFinder in a terminal with ```python DupeFinder.py <args>```. 

\<args\> is optional. If provided, it should be paths to one or more directories. If no directory is specified, DupeFinder will check the current working directory.