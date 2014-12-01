#!python3
# -*- coding: utf-8 -*-
import os, sys
import glob
import re

def parse_text(text):
    """Scan the input file one line at a time, looking for a keyword
    at the start of the line which will be one word in capital letters
    followed by a colon. This introduces a text suite, possibly over several
    lines which lasts until the next keyword or the end of the text.

    Lines which start with a hash sign (#) are treated as comments
    and are ignored.
    """
    keyword_matcher = re.compile("([A-Z]+)\:\s*(.*)")

    #
    # The text consists of a number of blocks, introduced by a keyword
    # and containing one or more paragraphs. This parser yields the keyword
    # and a list of the paragraphs. For some keywords, this list will always
    # contain exactly one string.
    #
    keyword = None
    paragraphs = []
    for line in text.splitlines():
        if line.startswith("#"):
            continue
        match = keyword_matcher.match(line)
        if match:
            if keyword:
                yield keyword, paragraphs
            keyword, text = match.groups()
            paragraphs = [text.strip()]
        else:
            paragraphs.append(line.strip())

    #
    # If we fall out of the loop with a keyword & text
    # remaining (which is the most likely case) then yield
    # both
    #
    if keyword and paragraphs:
        yield keyword, paragraphs

def process_default(texts):
    """For every item not specified, return a single string
    containing the space-concatenated strings in the list
    """
    return " ".join(text)

def process_title(texts):
    """Take a title with an optional subtitle in brackets and
    yield both as TITLE / SUBTITLE
    """
    text = " ".join(texts)
    #
    # Match as many non-left-bracket characters as possible
    # Then, optionally, match text in brackets
    #
    title, subtitle = re.match(r"([^(]+)\s*(?:\(([^)]+)\))?", text, flags=re.UNICODE).groups()
    yield "TITLE", title
    yield "SUBTITLE", subtitle

def process_gospel(texts):
    """Take a gospel quote prefixed by a chapter-and-verse reference
    """
    print("About to process gospel:", "\n".join(ascii(t) for t in texts))
    text = " ".join(texts)
    #
    #
    #
    citation, gospel = re.match("((?:Mt|Mk|Lk|Jn)\s[0-9:.-�]+)\s+(.*)", text).groups()
    yield "CITATION", citation
    yield "GOSPEL", gospel

def process_comments(text):
    """The comments field is processed specially so that blocks which are
    tagged as italic or bold (surrounded by _ or *) can be broken out into
    separate blocks and tagged as such.
    """
    pass

#
# Each processor takes a list of paragraphs and yields
# tuples of keyword, paragraphs. This allows a single source
# line to become more than one keyword / text. eg a title
# which looks like this:
#   TITLE: This is a title (With a subtitle)
# can yield:
#  TITLE, This is a title
#  SUBTITLE, With a subtitle
#
PROCESSORS = {
    "TITLE" : process_title,
    "GOSPEL" : process_gospel,
    "COMMENTS" : process_comments
}

def process_one_file(filepath):
    items = {}
    with open(filepath, encoding="utf-8") as f:
        for keyword, paragraphs in parse_text(f.read()):
            items.update(PROCESSORS.get(keyword, process_default)(paragraphs))
    return items

def process_one_folder(dirpath):
    text = {}
    for filepath in glob.glob(os.path.join(dirpath, "*.txt")):
        print(filepath)
        filename = os.path.basename(filepath)
        name, ext = os.path.splitext(filename)
        text[name] = dict(process_one_file(filepath))
    return text

def main(dirpath="."):
    return process_one_folder(dirpath)

if __name__ == '__main__':
    print(main(*sys.argv[1:]))
