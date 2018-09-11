import SCons.Script
import os
from collections import defaultdict

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
		       "TARFLAGS":"-c -z",},
    		  BUILDERS = {'Pytask' : bld})

testdatafiles = Glob("data/test-data/*.txt")
testdata = env.Command("data/test-data/data.db", testdatafiles + ["src/load_data.py",], "python src/load_data.py -d test")


t = env.Pytask("results/mutual-info2-test/mutual-info2-test.log", "tasks/il6_mutualinfo2.py")
Depends(t, "src/mutualinfo.py")
Depends(t, testdata)

