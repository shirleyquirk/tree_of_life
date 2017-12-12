#!/usr/bin/python
import sys

expr=' '.join(sys.argv[1:])

exec('print('+expr+')')   
