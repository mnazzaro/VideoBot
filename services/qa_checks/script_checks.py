import re

tldr_re = re.compile(r'^(t|T)(l|L)(;|\s{1}|:|\,)?(d|D)(r|R)$')
link_re = re.compile(r'^https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)$')

def _remove_tldr (script: str) -> str:
    match = tldr_re.match(script)
    if match:
        return script[match.pos:]
    return script

def _remove_links (script: str) -> str:
    new = script
    for link in link_re.findall(new):
        new = new.replace(link, ',')
    return new

def run_script_qa_checks (script: str) -> str:
    s = _remove_tldr(script)
    s = _remove_links(s)
    return s
