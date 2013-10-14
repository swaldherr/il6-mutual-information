import SCons.Script
import os
from collections import defaultdict

docbase = '/Users/waldherr/Documents'

task_targets = defaultdict(lambda: [])

def add_targets(target, source, env):
    t = os.path.basename(str(target[0]))[:-4]
    target.extend([os.path.join("results", t, i) for i in task_targets[t]])
    return target, source
bld = Builder(action = "python run.py --task $TARGET --log --export=png --memoize",
                 suffix = '.log',
                 src_suffix = '.py',
                 emitter = add_targets)

env = Environment(ENV={"TEXINPUTS":os.environ.get("TEXINPUTS",""), "HOME":os.environ["HOME"], "PATH":os.environ["PATH"],
                       "PYTHONPATH":os.environ["PYTHONPATH"],
		       "TARFLAGS":"-c -z",},
    		  BUILDERS = {'Pytask' : bld})

texdocs = Glob("docs/*.tex")
docbuilds = []
for f in texdocs:
    docbuilds.append(env.PDF(target=str(f)[:-4]+".pdf", source=f))
