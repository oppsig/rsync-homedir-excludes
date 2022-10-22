from os import path
import re

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

    create_file_exclude_no_comments(final_list) 
    create_file_backintime_new(final_list, config_contents)

def create_file_exclude_no_comments(final_list):
    with open(exclude_no_comments, 'w', encoding='utf-8') as f:
        for line in final_list: 
            f.write(format_exclude_no_comments(line))
            #f.write('\n')

def create_file_backintime_new(final_list, config_contents):
    has_matched = False
    tmp = []
    counter = 1
    for line in config_contents:
        m = re.search("profile[%s].snapshots.exclude.[0-9]+.value=" % profile, line)
        if not m:
            tmp.append(line)
        if m and not has_matched:
            has_matched = True
            counter = 1
            for line in final_list:
                value = format_exclude(line, counter)
                counter += 1
                tmp.append(value)
    with open(backintime_config_new, 'w', encoding='utf-8') as f:
        for line in tmp:
            f.write(line)
            #f.write('\n')

def format_exclude(line, counter):
    if not re.search("^($|[:space:]*#)", line) and not re.search("^([/])", line): 
        value = f"profile{profile}.snapshots.exclude.{counter}.value=/home/*/{line}"
    if re.search("^([/].*)", line):
        value = f"profile{profile}.snapshots.exclude.{counter}.value={line}"
    return value

def format_exclude_no_comments(line):
    if not re.search("^($|[:space:]*#)", line) and not re.search("^([/])", line): 
        value = f"/home/*/{line}"
    if re.search("^([/].*)", line):
        value = f"{line}"
    return value


if __name__ == "__main__":
    backintime_config_root = "/root/.config/backintime/config"
    backintime_config_old = "./backintime_config_old" 
    backintime_config_new = "./backintime_config_new" 
    exclude_no_comments = "./exclude_no_comments"

    if path.exists(backintime_config_root):
        configfile = backintime_config_root
    elif path.exists(backintime_config_old):
        configfile = path.relpath(backintime_config_old) # backintime config file

    excludefile = path.relpath("./exclude") # exclude file
    profile = 1 # backintime profile

    parse_config(configfile)
