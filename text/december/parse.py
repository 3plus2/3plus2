#!python3
import os, sys
import glob
import re


def get_items(text):
    """Scan the input file one line at a time, looking for a keyword
    at the start of the line which will be one word in capital letters
    followed by a colon. This introduces a text suite, possibly over several
    lines which lasts until the next keyword or the end of the text.
    
    Lines which start with a hash sign (#) are treated as comments
    and are ignored.
    """
    keyword_matcher = re.compile("([A-Z]+)\:\s*(.*)")
    current_keyword = None
    current_text = ""
    for line in text.splitlines():
        if line.startswith("#"):
            continue
        match = keyword_matcher.match(line)
        if match:
            if current_keyword:
                yield current_keyword, current_text
            current_keyword, current_text = match.groups()
        else:
            current_text += line
    if current_keyword and current_text:
        yield current_keyword, current_text

def process_gospel(text):
    """Split the text into a list of paragraphs
    """

def process_comments(text):
    """The comments field is processed specially so that blocks which are
    tagged as italic or bold (surrounded by _ or *) can be broken out into
    separate blocks and tagged as such.
    """

PROCESSORS = {
    "GOSPEL" : process_gospel,
    "COMMENTS" : process_comments
}

def parse_one_file(filepath):
    items = {}
    with open(filepath, encoding="utf-8") as f:
        for key, value in get_items(text):
            items[key] = PROCESSORS.get(key, lambda x: x)(value)
    return items
        
def main(dirpath="."):
    text = {}
    for filepath in glob.glob(os.path.join(dirpath, "*.txt")):
        print(filepath)
        filename = os.path.basename(filepath)
        name, ext = os.path.splitext(filename)
        text[name] = dict(parse_one_file(filepath))
    print(text)

if __name__ == '__main__':
    main(*sys.argv[1:])
