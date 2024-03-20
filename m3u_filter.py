input_file = "input.m3u"
output_file = "output.m3u"

include_patterns = ["DE: "]
exclude_patterns = ["OSOKOYO", "VIP-DE", "XXX"]


# maybe need to edit the get_tvg_name function to match your m3u file;
# the tvg-name attribute is not always included in the m3u file
def get_tvg_name(line: str):
    return line.split('tvg-name="')[1].split('"')[0]


def rename_channel(line: str, patterns: list):
    for pattern in patterns:
        line = line.replace(pattern, "")
    return line


def filter_m3u(
    input_file: str, output_file: str, inc_patterns: list, exc_patterns: list
):
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        lines = infile.readlines()

        outfile.write("#EXTM3U\n")
        filtered_pairs = []
        line_pairs = [(lines[i], lines[i + 1]) for i in range(1, len(lines), 2)]

        for pair in line_pairs:
            if not (any(pattern in pair[0] for pattern in inc_patterns)):
                continue
            if any(pattern in pair[0] for pattern in exc_patterns):
                continue
            filtered_pairs.append(pair)

        renamed_pairs = []

        for pair in filtered_pairs:
            renamed_pairs.append((rename_channel(pair[0], inc_patterns), pair[1]))

        sorted_pairs = sorted(renamed_pairs, key=lambda pair: get_tvg_name(pair[0]))
        for line_pair in sorted_pairs:
            for line in line_pair:
                outfile.write(line)


filter_m3u(
    "./" + input_file,
    output_file,
    include_patterns,
    exclude_patterns,
)
