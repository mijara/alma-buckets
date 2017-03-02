def build_url(host, secure):
    return "%s://%s" % ('https' if secure else 'http', host)
