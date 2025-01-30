import re


def pluralize(noun: str) -> str:
    if re.search("[sxz]$", noun):
        return re.sub("$", "es", noun)
    elif re.search("[^aeioudgkprt]h$", noun):
        return re.sub("$", "es", noun)
    elif re.search("[aeiou]y$", noun):
        return re.sub("y$", "ies", noun)
    else:
        return noun + "s"


def get_last_scraped_title(file_path: str) -> str:
    f = open(file_path, "r+", encoding="utf-8")
    last_scraped_title = f.read()
    f.close()
    return last_scraped_title


def set_last_scraped_title(file_path: str, title: str) -> None:
    f = open(file_path, "w+", encoding="utf-8")
    f.write(title)
    f.close()
