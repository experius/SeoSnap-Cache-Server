def lremove(s, pattern) -> str:
    if s.startswith(pattern):
        s = s[len(pattern):]
    return s


def rremove(s, pattern) -> str:
    if s.endswith(pattern):
        s = s[:-len(pattern)]
    return s