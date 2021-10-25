def generate_slug(name):
    """A valid 'slug' consisting of letters, numbers, underscores or hyphens."""
    temp = ""
    for a in name:
        if(a.isalnum() or a in [' ', '-']):
            temp += a
    return '-'.join(temp.lower().split())
