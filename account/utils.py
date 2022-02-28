def base_name_url(url):
    return url.split('//')[-1].split('/')[0].replace('www.', '')
