"""
template task for scripttool
"""
# Time-stamp: <Last change 2012-04-23 18:48:58 by Steffen Waldherr>

import numpy as np

import scripttool

class Task(scripttool.Task):
    """
    Task documentation
    """
    customize = {"taskoption":"default"}

    def run(self):
        
        self.printf("Task logging feature.")
        fig, ax = self.make_ax(name="figurename",
                               xlabel="x",
                               ylabel="y",
                               title="")

# creation of my experiments
scripttool.register_task(Task(taskoption=["custom"]), ident="task_custom")
scripttool.register_task(Task(), ident="task_default")
