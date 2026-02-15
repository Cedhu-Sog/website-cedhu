from django.urls import get_resolver

def get_named_urls():
    resolver = get_resolver()
    urls = []

    def extract(patterns, prefix=""):
        for p in patterns:
            if hasattr(p, "url_patterns"):
                extract(p.url_patterns, prefix)
            elif p.name:
                urls.append((p.name, p.name))

    extract(resolver.url_patterns)
    return sorted(urls)
