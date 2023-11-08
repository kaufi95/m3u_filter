from datetime import date
import re

input_file = "input.m3u"
include_adult = False

patterns = [",AT |", ",DE |"]
adult_pattern = ",XXX |"

def process_pattern_name(pattern_name):
    return re.sub(r"[^a-zA-Z]", "", pattern_name)


def get_pattern_names(patterns):
    pattern_names = []
    for pattern_name in patterns:
        pattern_names.append(process_pattern_name(pattern_name))
    return "_".join(pattern_names)


def create_file_name(patterns):
    return date.today().strftime("%Y-%m-%d") + "_" + get_pattern_names(patterns) + ".m3u"


def filter_m3u(input_file, output_file, patterns: list):
    if include_adult:
        patterns.append(adult_pattern)
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        lines = infile.readlines()
        keep_next_line = False

        for line in lines:
            if line.startswith("#EXTM3U"):
                outfile.write(line)
                continue
            if any(pattern in line for pattern in patterns):
                outfile.write(line)
                keep_next_line = True
            elif keep_next_line:
                outfile.write(line)
                keep_next_line = False


filter_m3u("./" + input_file, create_file_name(patterns), patterns)

# edit the script so it prepares two output lists, one with XXX and one without
