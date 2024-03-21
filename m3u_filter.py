import re

input_file = "input.m3u"
output_file = "output.m3u"

include_patterns = ["DE: "]
exclude_patterns = ["OSOKOYO", "VIP-DE", "XXX"]
quality_patterns = [" 4K", " FHD", " HD", " HEVC", " SD"]
rename_patterns = include_patterns + quality_patterns


# maybe need to edit the get_tvg_name function to match your m3u file;
# the tvg-name attribute is not always included in the m3u file
def get_tvg_name(line: str):
    return line.split('tvg-name="')[1].split('"')[0]


def rename_channel(line: str, patterns: list):
    for pattern in patterns:
        line = line.replace(pattern, "")
    return line


def get_quality(line):
    # Extracts the quality from a line using regular expressions
    match = re.search(r"\b(4K|FHD|HD|HEVC|SD)\b", line)
    if match:
        return match.group(1)
    else:
        return None


def filter_by_quality(line_pairs, quality_patterns):
    # Filters line pairs by quality
    filtered_pairs = []
    channel_dict = {}
    for pair in line_pairs:
        quality = get_quality(pair[0])
        name = get_tvg_name(pair[0])
        if name not in channel_dict:
            channel_dict[name] = (quality, pair)
        else:
            existing_quality, _ = channel_dict[name]
            if any(
                quality.strip() == pattern.strip()
                and existing_quality.strip() != pattern.strip()
                for pattern in quality_patterns
            ):
                channel_dict[name] = (quality, pair)
    filtered_pairs = [pair for _, pair in channel_dict.values()]
    return filtered_pairs


def filter_m3u(
    input_file: str,
    output_file: str,
    inc_patterns: list,
    exc_patterns: list,
    quality_patterns: list,
    rename_patterns: list,
):
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        lines = infile.readlines()

        outfile.write("#EXTM3U\n")

        line_pairs = [(lines[i], lines[i + 1]) for i in range(1, len(lines), 2)]

        # filtered_pairs = filter_by_quality(line_pairs, quality_patterns)
        filtered_pairs = line_pairs

        filtered_pairs = [
            pair
            for pair in filtered_pairs
            if any(pattern in pair[0] for pattern in inc_patterns)
        ]
        filtered_pairs = [
            pair
            for pair in filtered_pairs
            if not any(pattern in pair[0] for pattern in exc_patterns)
        ]

        renamed_pairs = [
            (rename_channel(pair[0], rename_patterns), pair[1])
            for pair in filtered_pairs
        ]

        sorted_pairs = sorted(renamed_pairs, key=lambda pair: get_tvg_name(pair[0]))
        for pair in sorted_pairs:
            for line in pair:
                outfile.write(line)


filter_m3u(
    "./" + input_file,
    output_file,
    include_patterns,
    exclude_patterns,
    quality_patterns,
    include_patterns,  # replace by rename_patterns if you want to rename the channels
)
