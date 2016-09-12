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
		       "TARFLAGS":"-c -z",},
    		  BUILDERS = {'Pytask' : bld})

texdocs = Glob("docs/*.tex")
docbuilds = []
for f in texdocs:
    docbuilds.append(env.PDF(target=str(f)[:-4]+".pdf", source=f))

def build_sbml(source, target, env, for_signature):
    bname = os.path.basename(target[0].get_path())
    antimonyout = bname[:bname.rfind(".xml")] + "_il6m7_sbml.xml"
    return "antimony2sbml '%s'; mv '%s' '%s'" % (source[0], antimonyout, target[0])
env.sbml = SCons.Script.Builder(generator = build_sbml, suffix = '.xml', src_suffix='.txt')
env.Append(BUILDERS = {'sbml' : env.sbml})

# define builder for compiled models
def build_cython_model(source, target, env, for_signature):
    return "python bin/build_cython_model.py '%s' '%s'" % (source[0], target[0])
env.modelso = env.Builder(generator = build_cython_model, suffix = '.so', src_suffix='.xml')
env.Append(BUILDERS = {'modelso' : env.modelso})

# define models
models = Glob("models/*.txt")
modelbuilders = []
for i in models:
    a = env.sbml(i)
    xmlfile = i.get_path().replace(".txt",".xml")
    b = env.modelso(xmlfile)
    Depends(b, "bin/build_cython_model.py")
    modelbuilders.extend([a,b])

datafiles20131014 = Glob("data/2013-10-14-results-ba-boehmert/*/*.txt")
data20131014 = env.Command("data/2013-10-14-results-ba-boehmert/data.db", datafiles20131014 + ["src/load_data.py",], "python src/load_data.py -d 2013-10-14")
datafiles20131104 = Glob("data/2013-11-04-results-ba-boehmert/*/*.txt")
data20131104 = env.Command("data/2013-11-04-results-ba-boehmert/data.db", datafiles20131104 + ["src/load_data.py",], "python src/load_data.py -d 2013-11-04")
testdatafiles = Glob("data/test-data/*.txt")
testdata = env.Command("data/test-data/data.db", testdatafiles + ["src/load_data.py",], "python src/load_data.py -d test")


t = env.Pytask("results/mutual-info2-test/mutual-info2-test.log", "tasks/il6_mutualinfo2.py")
Depends(t, "src/mutualinfo.py")
Depends(t, testdata)

t = env.Pytask("results/stat_mutualinfo/stat_mutualinfo.log", "tasks/il6_mutualinfo.py")
Depends(t, "src/mutualinfo.py")
Depends(t, data20131014)

t = env.Pytask("results/stat_mutualinfo_20131104/stat_mutualinfo_20131104.log", "tasks/il6_mutualinfo.py")
Depends(t, "src/mutualinfo.py")
Depends(t, data20131104)

env.Zip("il6-heterogeneity-mutualinfo.zip", datafiles20131014)
env.Zip("il6-heterogeneity-mutualinfo.zip", datafiles20131104)
env.Zip("il6-heterogeneity-mutualinfo.zip", Glob("data/test-data/*.txt"))
env.Zip("il6-heterogeneity-mutualinfo.zip", "src/__init__.py")
env.Zip("il6-heterogeneity-mutualinfo.zip", "src/mutualinfo.py")
env.Zip("il6-heterogeneity-mutualinfo.zip", "src/load_data.py")
env.Zip("il6-heterogeneity-mutualinfo.zip", "tasks/__init__.py")
env.Zip("il6-heterogeneity-mutualinfo.zip", "tasks/il6_mutualinfo.py")
env.Zip("il6-heterogeneity-mutualinfo.zip", "tasks/il6_mutualinfo2.py")
env.Zip("il6-heterogeneity-mutualinfo.zip", "run.py")
