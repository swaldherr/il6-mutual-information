#!/usr/bin/env python
# Time-stamp: <Last change 2018-10-12 08:30:10 by Steffen Waldherr>

from optparse import OptionParser
import os

from tasks import il6_mutualinfo2
import scripttool
import scripttool.script

scripttool.set_output_dir("results")

def main():
    usage = """%prog [options]"""
    parser = OptionParser(usage)
    parser.add_option("-v","--verbose", action="store_true", help="print messages")
    parser.add_option("-d","--data", action="store", help="choose data directory")
    options, args = parser.parse_args()
    scripttool.set_output_dir(os.path.join("results", options.data))
    scripttool.script.ensure_output_dir()
    task = il6_mutualinfo2.StatMutualInfo(data=options.data, rawdata=True)
    task.run()

    
if __name__ == "__main__":
    main()

