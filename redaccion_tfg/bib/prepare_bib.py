#!/usr/bin/env python3

filename = 'bib/library.bib'

# Read in the file
with open(filename, 'r') as file:
	filedata = file.read()

# Replace the target string
filedata = filedata.replace('{\_}', '\_')
filedata = filedata.replace('{\#}', '\#')
filedata = filedata.replace('{\%}', '\%')
filedata = filedata.replace('{~}', '~')

# Write the file out again
with open(filename, 'w') as file:
	file.write(filedata)