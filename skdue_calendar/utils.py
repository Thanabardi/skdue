def generate_slug(name):
    """A valid 'slug' consisting of letters, numbers, underscores or hyphens."""
    temp = ""
    for a in name:
        if(a.isalnum() or a in [' ', '-']):
            temp += a
    return '-'.join(temp.lower().split())

def generate_tag(name):
    """A valid 'tag' consisting of letters, numbers, underscores or hyphens."""
    temp = ""
    for text in name:
        if text.isalnum():
            temp += text
    return temp.lower()