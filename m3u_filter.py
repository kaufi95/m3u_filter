from datetime import date
import re

input_file = "input.m3u"
filters = [",AT |", ",DE |"]


def process_filter_name(filter_name):
    return re.sub(r"[^a-zA-Z]", "", filter_name)


def get_filter_names(filters):
    filter_names = []
    for filter_name in filters:
        filter_names.append(process_filter_name(filter_name))
    return "_".join(filter_names)


def create_file_name(filters):
    return date.today().strftime("%Y-%m-%d") + "_" + get_filter_names(filters) + ".m3u"


def filter_m3u(input_file, output_file, patterns):
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


filter_m3u("./" + input_file, create_file_name(filters), filters)
