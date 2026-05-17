import re
import sys
import json
from calendar import month_name

import jinja2
import jinja2.sandbox
from pybtex.database.input import bibtex


MONTHS = {
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "may": 5,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "sep": 9,
    "oct": 10,
    "nov": 11,
    "dec": 12,
}


def author_fmt(author):
    return " ".join(author.first_names + author.middle_names + author.last_names)


def and_list(items, sep=", ", sep_last=", and ", sep_two=" and "):
    if len(items) <= 1:
        return "".join(items)
    if len(items) == 2:
        return sep_two.join(items)
    return sep.join(items[:-1]) + sep_last + items[-1]


def author_list(authors):
    return and_list([author_fmt(author) for author in authors])


def author_names(authors):
    return [author_fmt(author) for author in authors]


def yaml_value(value):
    if value is None or isinstance(value, jinja2.Undefined):
        value = ""
    return json.dumps(value, ensure_ascii=True)


def venue_type(entry):
    if entry.type == "inbook":
        return "Chapter in "
    if entry.type == "techreport":
        return "Technical Report "
    if entry.type == "phdthesis":
        return "Ph.D. thesis, {}".format(entry.fields["school"])
    return ""


def venue(entry):
    fields = entry.fields
    if entry.type == "article":
        value = fields["journal"]
        if fields.get("volume") and fields.get("number"):
            value += " {0}({1})".format(fields["volume"], fields["number"])
        return value
    if entry.type == "inproceedings":
        value = fields["booktitle"]
        if fields.get("series"):
            value += " ({})".format(fields["series"])
        return value
    if entry.type == "inbook":
        return fields["title"]
    if entry.type == "techreport":
        return "{0}, {1}".format(fields["number"], fields["institution"])
    if entry.type == "phdthesis":
        return ""
    return "Unknown venue (type={})".format(entry.type)


def title(entry):
    value = entry.fields["chapter"] if entry.type == "inbook" else entry.fields["title"]
    return value.translate(str.maketrans("", "", "{}"))


def main_url(entry):
    for field in ("url", "ee"):
        if field in entry.fields:
            return entry.fields[field]
    return None


def extra_urls(entry):
    urls = {}
    for key, value in entry.fields.items():
        if not key.endswith("_url"):
            continue
        url_type = key[:-4].replace("_", " ")
        urls[url_type] = value
    return urls


def grant_list(entry):
    value = entry.fields.get("scs_grants", "")
    grants = []
    for item in re.split(r"[,;]\s*", value):
        item = item.strip()
        if not item:
            continue
        grant_id = item.replace("CNS-", "").strip()
        label = f"NSF CNS-{grant_id}"
        url = f"https://www.nsf.gov/awardsearch/showAward?AWD_ID={grant_id}"
        grants.append({"id": grant_id, "label": label, "url": url})
    return grants


def grant_ids(entry):
    return [grant["id"] for grant in grant_list(entry)]


def month_match(month):
    if re.match("^[0-9]+$", month):
        return int(month)
    return MONTHS[month.lower()[:3]]


def monthname(month_number):
    try:
        return month_name[int(month_number)]
    except Exception:
        return ""


def sort_key(entry):
    fields = entry.fields
    key = "{:04d}".format(int(fields["year"]))
    if "month" in fields:
        key += "{:02d}".format(month_match(fields["month"]))
    else:
        key += "00"
    return key


def main(bibfile, template):
    env = jinja2.sandbox.SandboxedEnvironment()
    env.filters["author_fmt"] = author_fmt
    env.filters["author_list"] = author_list
    env.filters["author_names"] = author_names
    env.filters["yaml"] = yaml_value
    env.filters["title"] = title
    env.filters["venue_type"] = venue_type
    env.filters["venue"] = venue
    env.filters["main_url"] = main_url
    env.filters["extra_urls"] = extra_urls
    env.filters["grant_list"] = grant_list
    env.filters["grant_ids"] = grant_ids
    env.filters["monthname"] = monthname

    with open(template) as handle:
        tmpl = env.from_string(handle.read())

    with open(bibfile) as handle:
        db = bibtex.Parser().parse_stream(handle)

    for key, entry in db.entries.items():
        entry.fields["key"] = key

    entries = sorted(db.entries.values(), key=sort_key, reverse=True)
    rendered = tmpl.render(entries=entries)
    sys.stdout.write("\n".join(line.rstrip() for line in rendered.splitlines()) + "\n")


if __name__ == "__main__":
    main(*sys.argv[1:])
