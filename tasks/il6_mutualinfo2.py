"""
Analysis of mutual information in IL6/Stat signalling
"""
# Time-stamp: <Last change 2015-06-15 13:36:43 by Steffen Waldherr>

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
                data1 = dataframe[selection][label1]
                data2 = dataframe[selection][label2]
                if np.any(np.isnan(data1)) or np.any(np.isnan(data2)):
                    continue
                this_mi = compute_mutual_information(data1, data2)
                ident = (exp, stim, conc, cell, label1, label2)
                identstr = "%d_%s_%.2f_%s_%s_%s" % ident
                mi[ident] = this_mi
                self.printf("MI for %s: %.5f bit" % (identstr, this_mi))
                fig, ax = self.make_ax(name="%s-%s_" % (label1, label2) + "_" + identstr,
                                   xlabel=label1,
                                   ylabel=label2,
                                   title="%s vs. %s in dataset " % (label1, label2) + identstr)
                ax.plot(data1, data2, "b.")

# creation of my experiments
scripttool.register_task(StatMutualInfo(), ident="mutual-info2-test")

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

