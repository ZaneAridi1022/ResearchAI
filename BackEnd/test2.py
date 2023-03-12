

#get seeMoreUrl of data
def get_all_urls(response):
    sources = response["item"]['messages'][1]['sourceAttributions']
    print(sources)
    all_urls = []
    for source in sources:
        all_urls.append(source["seeMoreUrl"])
    all_urls = list(set(all_urls))
    return all_urls


print(get_all_urls(data))