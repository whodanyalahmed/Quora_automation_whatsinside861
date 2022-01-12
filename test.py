from os import listdir, getcwd
from os.path import isfile, join
onlyfiles = [f for f in listdir(
    getcwd() + "/images/") if isfile(join(getcwd() + "/images/", f))]
print(onlyfiles)
