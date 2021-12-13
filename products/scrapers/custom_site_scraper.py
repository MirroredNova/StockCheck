import requests
from lxml import html

# @param url: String representation of the site URL
# @param xpath: String representation of the watched element's XPath
# @param element: String representation of the content of the watched element (optional, blank string if not given)
# @return: Returns true if watched element found, false otherwise
# @throws: ValueError if repeats of the watched element found
# @throws: Appropriate requests errors if http request fails
def custom_site_scraper(url, xpath, element):
    HEADERS = ({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)}'
                              'AppleWebKit/537.36 (KHTML, like Gecko))'
                              'Chrome/44.0.2403.157 Safari/537.36',
                'Accept-Language': 'en-US, en;q=0.5'})

    # Many browsers put in a "tbody" tag that doesn't actually exist, so this should pull it out
    xpath_clean = xpath.replace('tbody', '').replace('//', '/')

    # Ensure that some sort of scheme is provided
    if not (url.__contains__("https://") or url.__contains__("http://")):
        url_clean = "https://" + url

    # We want to manage this with a valid SSL certificate, but some trustworthy sites get an error with verification
    # This is a hacky solution and probably not the safest, but for the purposes of this we'll use it
    try:
        r = requests.get(url_clean, headers=HEADERS, stream=True)
    except requests.exceptions.SSLError:
        r = requests.get(url_clean, headers=HEADERS, verify=False, stream=True)

    # Raise a known exception if the HTTP request failed
    r.raise_for_status()

    r.raw.decode_content = True
    tree = html.parse(r.raw)
    elements = tree.xpath(xpath_clean)
    site_changed = False

    if len(elements) == 0:
        site_changed = True
    elif len(elements) == 1:
        # Appears unchanged
    else:
        raise ValueError("Too many of the specified element found")

    # If the contents of the element were provided and the xpath was found, check that its contents are unchanged
    if (len(elements) == 1) and len(element) > 0:
        if not (html.tostring(elements[0], pretty_print=False).decode() == element):
            site_changed = True

    return site_changed