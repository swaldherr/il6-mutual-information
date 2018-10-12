#!/usr/bin/env python
# Time-stamp: <Last change 2018-10-12 08:19:02 by Steffen Waldherr>

from optparse import OptionParser

import pandas
import csv
import shelve
import glob
import os
import numpy as np

def get_data(datadir):
    db = shelve.open(os.path.join("data",datadir,"data.db"))
    if not "all" in db:
        raise Exception("Combined data '%s' not found in database, maybe it was not loaded previously?" % datadir)
    return db["all"]

def get_data2(datadir):
    db = shelve.open(os.path.join(datadir,"data.db"))
    if not "all" in db:
        raise Exception("Combined data '%s' not found in database, maybe it was not loaded previously with src/load_data.py ?" % datadir)
    return db["all"]

def load_data2(filename, storedb=None):
    df = pandas.read_csv(filename, sep='\t')
    ident = hash(filename)
    if storedb is not None:
        storedb[str(ident)] = df
    return ident, df

def load_data_excel(filename, storedb=None):
    ef = pandas.ExcelFile(filename)
    df = pandas.read_excel(ef, sheetname=ef.sheet_names[0])
    ident = hash(filename)
    if storedb is not None:
        storedb[str(ident)] = df
    return ident, df
    
def load_data(filename, storedb=None):
    ident = os.path.basename(filename)[:-4].split("_")
    df = pandas.read_csv(filename, sep='\t')
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

def combine_data(storedb):
    df = reduce(lambda df1, df2: df1.append(df2, ignore_index=True), (storedb[i] for i in storedb.keys() if i.startswith("V")))
    storedb["all"] = df
    return df

def combine_data2(storedb):
    df = reduce(lambda df1, df2: df1.append(df2, ignore_index=True), (storedb[i] for i in storedb.keys()))
    storedb["all"] = df
    return df

def get_data_20131014():
    return get_data("2013-10-14-results-ba-boehmert")

def get_data_20131104():
    return get_data("2013-11-04-results-ba-boehmert")

def main():
    usage = """%prog [options]"""
    parser = OptionParser(usage)
    parser.add_option("-v","--verbose", action="store_true", help="print messages")
    parser.add_option("-d","--data", action="store", help="choose data directory")
    parser.add_option("-x","--excel", action="store_true", help="read .xlsx files instead of .txt")
    options, args = parser.parse_args()
    if options.data == "test":
        files = glob.glob(os.path.join("data","test-data","*.txt"))
        db = shelve.open(os.path.join("data","test-data","data.db"))
        for f in files:
            printv("Loading data from %s." % f, options)
            load_data2(f, db)
        combine_data2(db)
        db.close()
    else:
        if options.excel:
            files = glob.glob(os.path.join(options.data,"*.xlsx"))
        else:
            files = glob.glob(os.path.join(options.data,"*.txt"))
        db = shelve.open(os.path.join(options.data,"data.db"))
        for f in files:
            printv("Loading data from %s." % f, options)
            if options.excel:
                load_data_excel(f, db)
            else:
                load_data2(f, db)
        combine_data2(db)
        db.close()

    
def printv(message, opt):
    if opt.verbose:
        print message

if __name__ == "__main__":
    main()


