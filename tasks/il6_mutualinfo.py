"""
Analysis of mutual information in IL6/Stat signalling
"""
# Time-stamp: <Last change 2013-11-29 15:47:29 by Steffen Waldherr>

import numpy as np
import itertools
from scipy import stats

import scripttool

from src import mutualinfo
from src import load_data

compute_mutual_information = scripttool.memoize.filecache(mutualinfo.compute_mutual_information)

class StatMutualInfo(scripttool.Task):
    """
    Compute mutual information between Stat and pStat
    """
    customize = {"data": "20131014",
                 }

    def run(self):
        if self.data == "20131014":
            dataframe = load_data.get_data_20131014()
        elif self.data == "20131104":
            dataframe = load_data.get_data_20131104()
        bioreps = set(dataframe["bio-repl"])
        techreps = set(dataframe["tech-repl"])
        cell = set(dataframe["cell"])
        stim = set(dataframe["stim"])
        mi_il6 = []
        mi_hyperil6 = []
        for b, t, c, s in itertools.product(bioreps, techreps, cell, stim):
            selection = ((dataframe["bio-repl"] == b) * (dataframe["tech-repl"] == t)
                         * (dataframe["cell"] == c) * (dataframe["stim"] == s))
            if sum(selection) <= 1:
                continue
            label1 = "APC-A"
            data1 = dataframe[selection][label1]
            label2 = "FITC-A" if not np.isnan(dataframe[selection]["FITC-A"][0]) else "PE-A"
            data2 = dataframe[selection][label2]
            mi = compute_mutual_information(data1, data2)
            if s == "stim IL6":
                mi_il6.append(mi)
            if s == "stim Hyper IL6":
                mi_hyperil6.append(mi)
            self.printf("MI for %s_%s_%s_%s: %*s %.5f bit" % (b, t, c, s, 30 - len("_".join((b,t,c,s))), " ", mi))
            fig, ax = self.make_ax(name="%s-%s_" % (label1, label2) + "_".join((b,t,c,s)),
                               xlabel=label1,
                               ylabel=label2,
                               title="%s vs. %s in dataset " % (label1, label2) + "_".join((b,t,c,s)))
            ax.plot(data1, data2, "b.")
        self.printf("Mutual information for stim IL6:")
        self.printf("Mean = %g, std = %g" % (np.mean(mi_il6), np.std(mi_il6)), indent=1)
        self.printf("Mutual information for stim Hyper IL6:")
        self.printf("Mean = %g, std = %g" % (np.mean(mi_hyperil6), np.std(mi_hyperil6)), indent=1)
        t, p1, p2 = compute_t_stat(np.asarray(mi_il6), np.asarray(mi_hyperil6))
        self.printf("Welch's t-test for different means of IL6 and Hyper IL6 stimulation:")
        self.printf("t = %g, p-one-sided = %g, p-two-sided = %g" % (t, p1, p2), indent=1)

# creation of my experiments
scripttool.register_task(StatMutualInfo(), ident="stat_mutualinfo")
scripttool.register_task(StatMutualInfo(data="20131104"), ident="stat_mutualinfo_20131104")

# code from http://stackoverflow.com/questions/10038543/tracking-down-the-assumptions-made-by-scipys-ttest-ind-function
def compute_t_stat(pop1,pop2):

    num1 = pop1.shape[0];
    num2 = pop2.shape[0];

    # The formula for t-stat when population variances differ.
    t_stat = (np.mean(pop1) - np.mean(pop2))/np.sqrt( np.var(pop1)/num1 + np.var(pop2)/num2 )

    # ADDED: The Welch-Satterthwaite degrees of freedom.
    df = ((np.var(pop1)/num1 + np.var(pop2)/num2)**(2.0))/(   (np.var(pop1)/num1)**(2.0)/(num1-1) +  (np.var(pop2)/num2)**(2.0)/(num2-1) ) 

    # Am I computing this wrong?
    # It should just come from the CDF like this, right?
    # The extra parameter is the degrees of freedom.

    one_tailed_p_value = 1.0 - stats.t.cdf(t_stat,df)
    two_tailed_p_value = 1.0 - ( stats.t.cdf(np.abs(t_stat),df) - stats.t.cdf(-np.abs(t_stat),df) )    

    return t_stat, one_tailed_p_value, two_tailed_p_value

