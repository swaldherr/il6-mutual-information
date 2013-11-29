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

datafiles = Glob("data/2013-10-14-results-ba-boehmert/*/*.txt")
data20131014 = env.Command("data/2013-10-14-results-ba-boehmert/data.db", datafiles + ["src/load_data.py",], "python src/load_data.py -d 2013-10-14")
data20131104 = env.Command("data/2013-11-04-results-ba-boehmert/data.db", datafiles + ["src/load_data.py",], "python src/load_data.py -d 2013-11-04")

t = env.Pytask("results/stat_mutualinfo/stat_mutualinfo.log", "tasks/il6_mutualinfo.py")
Depends(t, "src/mutualinfo.py")
Depends(t, data20131014)

t = env.Pytask("results/stat_mutualinfo_20131104/stat_mutualinfo_20131104.log", "tasks/il6_mutualinfo.py")
Depends(t, "src/mutualinfo.py")
Depends(t, data20131104)

env.Zip("il6-heterogeneity-mutualinfo.zip", datafiles)
env.Zip("il6-heterogeneity-mutualinfo.zip", "src/__init__.py")
env.Zip("il6-heterogeneity-mutualinfo.zip", "src/mutualinfo.py")
env.Zip("il6-heterogeneity-mutualinfo.zip", "src/load_data.py")
env.Zip("il6-heterogeneity-mutualinfo.zip", "tasks/__init__.py")
env.Zip("il6-heterogeneity-mutualinfo.zip", "tasks/il6_mutualinfo.py")
env.Zip("il6-heterogeneity-mutualinfo.zip", "run.py")
