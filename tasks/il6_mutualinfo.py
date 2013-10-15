"""
Analysis of mutual information in IL6/Stat signalling
"""
# Time-stamp: <Last change 2013-10-14 21:23:33 by Steffen Waldherr>

import numpy as np
import itertools

import scripttool

from src import mutualinfo
from src import load_data

compute_mutual_information = scripttool.memoize.filecache(mutualinfo.compute_mutual_information)

class StatMutualInfo(scripttool.Task):
    """
    Compute mutual information between Stat and pStat
    """
    customize = {"taskoption":"default"}

    def run(self):
        dataframe = load_data.get_data_20131014()
        bioreps = set(dataframe["bio-repl"])
        techreps = set(dataframe["tech-repl"])
        cell = set(dataframe["cell"])
        stim = set(dataframe["stim"])
        for b, t, c, s in itertools.product(bioreps, techreps, cell, stim):
            selection = ((dataframe["bio-repl"] == b) * (dataframe["tech-repl"] == t)
                         * (dataframe["cell"] == c) * (dataframe["stim"] == s))
            if sum(selection) <= 1:
                continue
            stat = dataframe[selection]["APC-A"]
            pstat = dataframe[selection]["FITC-A"]
            mi = compute_mutual_information(stat, pstat)
            self.printf("MI for %s_%s_%s_%s: %g bit" % (b, t, c, s, mi))
            fig, ax = self.make_ax(name="pstat-stat_" + "_".join(b,t,c,s),
                               xlabel="Stat",
                               ylabel="pStat",
                               title="pStat vs. Stat in dataset " + "_".join(b,t,c,s))
            ax.plot(stat, pstat, "b.")

# creation of my experiments
scripttool.register_task(StatMutualInfo(), ident="stat_mutualinfo")
