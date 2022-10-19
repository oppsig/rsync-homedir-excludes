from os import path
import re

if path.exists("/root/.config/backintime/config"):
    configfile = "/root/.config/backintime/config"
else:
    configfile = path.relpath("./config") # backintime config file

excludefile = path.relpath("./exclude") # exclude file
profile = 1 # backintime profile

# parse backintime config file.
def parse_config(config):
    with open(config) as f:
        config_contents = f.readlines()

    # create a list of excludes from config file.
    config_list = []

    for line in config_contents:
        m = re.search("profile[%s].snapshots.exclude.[0-9]+.value=" % profile, line)
        if m:
            x = line.split("value=")[1]
            config_list.append(x)
    
   
    # create a list of excludes from local exclude list.
    
    exclude_list = []
    with open(excludefile) as f:
        exclude_contents = f.readlines() 
    for line in exclude_contents:
        if not re.search("^($|[:space:]*#)", line) and not re.search("^([/])", line): 
            exclude_list.append(line)
        if re.search("^([/].*)", line):
            exclude_list.append(line)
    final_list = []
    final_list.extend(config_list)
    final_list.extend(exclude_list)

    # print out a list of duplicates
    import collections
    print ("list of duplicates found:")
    x = [item for item, count in collections.Counter(final_list).items() if count > 1]
    if len(x) > 0:
            print(x)

    # remove duplicates
    final_list = [*set(final_list)]
    final_list.sort()
    
    # print
    print("length of excludes: %s" % len(final_list))
    for line in final_list:
        pass
        #print(line, end="")
    
    # now start creating new backintime config file
    has_matched = False
    for line in config_contents:
        m = re.search("profile[%s].snapshots.exclude.[0-9]+.value=" % profile, line)
        if not m:
            print(line, end="")
        if m and not has_matched:
            has_matched = True
            counter = 1
            for line in final_list:
                format_exclude(line, counter)
                counter += 1

def format_exclude(line, counter):
    if not re.search("^($|[:space:]*#)", line) and not re.search("^([/])", line): 
        value = f"profile{profile}.snapshots.exclude.{counter}.value=/home/*/{line}"
    if re.search("^([/].*)", line):
        value = f"profile{profile}.snapshots.exclude.{counter}.value={line}"

    print(value, end="")




if __name__ == "__main__":
    parse_config(configfile)
