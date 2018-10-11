"""
Analysis of mutual information in IL6/Stat signalling
"""
# Time-stamp: <Last change 2018-10-11 14:41:18 by Steffen Waldherr>

import numpy as np
import itertools
from scipy import stats

import scripttool

from src import mutualinfo
from src import load_data

compute_mutual_information = mutualinfo.compute_mutual_information

class StatMutualInfo(scripttool.Task):
    """
    Compute mutual information between Stat and pStat
    """
    customize = {"data": "test-data",
                 "labels": set(("STAT3", "pSTAT3", "SSC", "DAPI")),
                 }

    def run(self):
        dataframe = load_data.get_data(self.data)
        exps = set(dataframe["Exp"])
        cells = set(dataframe["Cell"])
        stims = set(dataframe["Stim"])
        concs = set(dataframe["Conc"])
        mi = {}
        for exp, cell, stim, conc in itertools.product(exps, cells, stims, concs):
            selection = ((dataframe["Exp"] == exp) & (dataframe["Cell"] == cell)
                         & (dataframe["Stim"] == stim) & (dataframe["Conc"] == conc))
            if sum(selection) <= 1:
                continue
            for label1, label2 in itertools.combinations(self.labels, 2):
                ident = (exp, stim, conc, cell, label1, label2)
                identstr = ("%d_%s_%s_%s_%s_%s" % ident).replace("/","_")
                print "Starting computation for %s ..." % str(ident)
                data1 = dataframe[selection][label1]
                data2 = dataframe[selection][label2]
                if np.any(np.isnan(data1)) or np.any(np.isnan(data2)):
                    print "Found NaN data, aborting computation."
                    continue
                this_mi = compute_mutual_information(data1, data2)
                mi[ident] = this_mi
                self.printf("MI for %s: %.5f bit" % (identstr, this_mi))
                print "MI for %s: %.5f bit" % (identstr, this_mi)
                fig, ax = self.make_ax(name="%s-%s_" % (label1, label2) + "_" + identstr,
                                   xlabel=label1,
                                   ylabel=label2,
                                   title="%s vs. %s in dataset " % (label1, label2) + identstr)
                ax.plot(data1, data2, "b.")

# creation of my experiments
scripttool.register_task(StatMutualInfo(), ident="mutual-info2-test")

