import json
from bs4 import BeautifulSoup
import re

MAGIC_STR = r"Compose email to "
BS_NAME_REGEX = re.compile(MAGIC_STR + r"(.+)")
BS_ID_REGEX = re.compile(r"EmailUser\(([0-9]+)\)")
EMAIL_REGEX = re.compile(r"(s[0-9]+@connect\.np\.edu\.sg)")


def is_student_anchor(a_tag) -> bool:
    title = a_tag.get('title')
    if title is None:
        return False
    return MAGIC_STR in title


def get_name(a_tag) -> str:
    title = a_tag.get('title')
    match = BS_NAME_REGEX.match(title)
    if match is None:
        raise Exception(f"Brightspace ID not found for {a_tag}")
    return match.group(1)


def get_bs_id(a_tag) -> str:
    bs_id = a_tag.get('onclick')
    match = BS_ID_REGEX.match(bs_id)
    if match is None:
        raise Exception(f"Brightspace ID not found for {a_tag}")
    return match.group(1)


def get_emails(label_tags) -> list[str]:
    email_label_tags = filter(
        lambda x: EMAIL_REGEX.match(x.text) is not None, label_tags)
    emails = list(
        map(lambda x: EMAIL_REGEX.match(x.text).group(1), email_label_tags))
    return emails[1::2]


def get_student_info(emails: list[str],
                     student_names: list[str],
                     student_bs_ids: list[str],
                     tutorial_group: str) -> list[list[str]]:
    if len(emails) != len(student_names) or len(emails) != len(student_bs_ids):
        raise Exception(f"list length mismatch {len(emails)} {
                        len(student_names)} {len(student_bs_ids)}")
    ls = []
    for i in range(len(emails)):
        ls.append([tutorial_group, student_names[i],
                  emails[i], student_bs_ids[i]])
    return ls


with open("reference/p01.html", "r") as f:
    soup = BeautifulSoup(f.read(), 'html.parser')
    label_tags = soup.find_all('label')
    emails = get_emails(label_tags)

    a_tags = soup.find_all('a')
    student_a_tags = list(filter(is_student_anchor, a_tags))
    student_names = list(map(get_name, student_a_tags))
    student_bs_ids = list(map(get_bs_id, student_a_tags))
    tutorial_group = 'T01'

    students = get_student_info(
        emails, student_names, student_bs_ids, tutorial_group)
    with open(f"{tutorial_group}_classlist.json", "w") as f2:
        f2.write(json.dumps(students))
