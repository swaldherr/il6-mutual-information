#!/usr/bin/env python
# Time-stamp: <Last change 2013-10-23 13:37:01 by Steffen Waldherr>

from optparse import OptionParser

import pandas
import csv
import shelve
import glob
import os
import numpy as np

def get_data_20131014():
    db = shelve.open(os.path.join("data","2013-10-14-results-ba-boehmert","data.db"))
    if not "all" in db:
        raise Exception("Combined data from 2013-10-14 not found in database, maybe it was not loaded previously?")
    return db["all"]

def load_data_20131014(filename, storedb=None):
    ident = os.path.basename(filename)[:-4].split("_")
    df = pandas.read_csv(filename)
    del df["Unnamed: 0"]
    del df["Unnamed: 6"]
    df.insert(0, "stim", ident[4])
    df.insert(0, "marker", ident[3])
    df.insert(0, "cell", ident[2])
    df.insert(0, "tech-repl", ident[1])
    df.insert(0, "bio-repl", ident[0])
    if storedb is not None:
        storedb["_".join(ident)] = df
    return ident, df

def combine_data_20131014(storedb):
    df = reduce(lambda df1, df2: df1.append(df2, ignore_index=True), (storedb[i] for i in storedb.keys() if i.startswith("V")))
    storedb["all"] = df
    return df

def main():
    usage = """%program [options]"""
    parser = OptionParser(usage)
    parser.add_option("-v","--verbose", action="store_true", help="print messages")
    parser.add_option("-d","--data", action="store", help="choose data directory")
    options, args = parser.parse_args()
    if options.data == "2013-10-14":
        files = glob.glob(os.path.join("data","2013-10-14-results-ba-boehmert","*","*.txt"))
        db = shelve.open(os.path.join("data","2013-10-14-results-ba-boehmert","data.db"))
        for f in files:
            printv("Loading data from %s." % f, options)
            load_data_20131014(f, db)
        combine_data_20131014(db)
        db.close()

def printv(message, opt):
    if opt.verbose:
        print message

if __name__ == "__main__":
    main()


