import re
import json
import html2text
from loguru import logger
import requests
import http
from .google import proc_link
from .twitter import parse_twitter
from sqlalchemy import *


from app import metadata, session


def cmd_link(code_or_url):
    # Check for a comma, and determine page count, unfinished...
    page_count = 3
    pos1 = str(code_or_url).find(",")
    if pos1 > 0:
        phrase = str(code_or_url)[:pos1]
        page_count = str(code_or_url)[pos1 + 1:].strip()
        try:
            page_count = int(page_count)
            logger.warning("Page Count Specified: " + str(page_count))
        except:
            logger.warning("Error. Multilink Not Enabled")
            page_count = 3
    else:
        phrase = str(code_or_url)
    pos1 = phrase.find(".")
    if pos1 >= 0:
        logger.debug("Using URL")
        # Do URL Magic Here
        link_code = proc_link(phrase, metadata, session)
        logger.debug("Link Code: " + link_code)
    else:
        logger.debug("Using Link Code")
        link_code = phrase
    # Link Code has been established by this point
    link_url = ""
    links = Table("links", metadata, autoload=True)
    qry = links.select().where(links.c.link_code == link_code)
    results = qry.execute()
    # headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0"}

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        # "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "If-None-Match": 'W/"2d948-yE4NiwNgR4dh3fmcnU5LR8bysMg"',
        "Cache-Control": "max-age=0",
    }
    text_data = ""
    rowcount = len(results._saved_cursor._result.rows)
    if rowcount == 0:
        logger.warning("Link Code " + link_code + " can not be found.")
        link_text = (
            "Link Code for: "
            + link_code
            + " can not be found. Please check the link and try again."
        )
    else:
        for x in results:
            link_row = list(x)
            link_url = link_row[2]
        logger.debug("Now fetching: " + link_code + " | " + link_url)
        file_ext_dot = link_url.rfind(".") + 1
        file_ext = link_url[file_ext_dot: file_ext_dot + 3]
        logger.debug("Filetype found: " + file_ext)
        if file_ext == "pdf":
            logger.debug("PDF Filetype Detected. Aborting.")
            link_text = (
                "Apologies. You have requested a PDF file, which is not supported by your end. "
                "We are working on a solution to allow the reading of PDF files, but this feature is not yet available"
            )
        else:
            try:
                logger.debug("Getting URL: " + link_url)
                r = requests.get(link_url, headers=headers, timeout=5)
                r.raise_for_status()
                link_text = r.text
            except requests.exceptions.HTTPError as errh:
                link_text = "Http Error: " + str(errh)
            except requests.exceptions.ConnectionError as errc:
                link_text = "Error Connecting: " + str(errc)
            except requests.exceptions.Timeout as errt:
                link_text = "Timeout Error: " + str(errt)
            except requests.exceptions.RequestException as err:
                link_text = "OOps: Something went wrong: " + str(err)
            except:
                link_text = "OOps: Something went wrong: Unknown Error"
            if link_text[:3] == "%PDF":
                link_text = (
                    "Apologies. You have requested a PDF file, which is not supported by your end. "
                    "We are working on a solution to allow the reading of PDF files, but this feature is not yet available"
                )
    pos1 = link_url.find("amazon.com")
    pos2 = link_url.find("/dp/")
    pos3 = link_url.find("://twitter.com/")
    # Filter Link Returns
    if (pos1 >= 0) and (pos2 >= 0):
        logger.debug("Using Amazon Filter")
        # try to find asin to use api
        asin = link_url[pos2+4:]
        pos1 = asin.find(r"/")
        asin = asin[:pos1]

        # ScrapeHero Code ----------------
        conn = http.client.HTTPSConnection("get.scrapehero.com")
        conn.request(
            "GET", "/amz/product-details/?x-api-key=SXOFpa27z4vriRCOlfQC7IZOdxYWo9Xj&asin=" + asin + "&country_code=US")
        res = conn.getresponse()
        data = res.read()
        json_data = json.loads(data.decode("utf-8"))
        prod_data = dict(json_data)
        show = ''
        end = '[EOL]' + chr(13) + chr(10)
        for k, v in prod_data.items():
            try:
                show += k + ': ' + v + end
            except:
                pass
        amz_details = show
        # --------------------------

        body_text = to_text(str(amz_details), rehtml=True)
    elif pos3 >= 0:
        logger.debug("Using Twitter Filter")
        body_text = parse_twitter(link_url)
    else:
        logger.debug("Not Using Filters")
        body_text = "URL: " + link_url + "\r\n"
        body_text += (
            "Link Code: " + link_code + " \r\n" +
            to_text(link_text)
        )
    return body_text, page_count


def to_text(html_src, rehtml=True):
    html_data = str(html_src)
    html_data = html_data.replace("\t", " ")
    while (html_data.find("  ")) >= 0:
        html_data = html_data.replace("  ", " ")
    while (html_data.find(chr(9))) >= 0:
        html_data = html_data.replace(chr(9), " ")
    parser = html2text.HTML2Text()
    parser.wrap_links = True
    parser.unicode_snob = True
    parser.skip_internal_links = True
    parser.inline_links = True
    parser.ignore_anchors = True
    parser.ignore_images = True
    parser.ignore_emphasis = True
    parser.ignore_links = True
    try:
        text = parser.handle(html_data)
    except Exception as e:
        logger.warning('HTML2Text Failed')
        logger.info(str(e))
        text = str(html_data)
    if rehtml:
        text = text.replace("\\", "")
    text = re.sub(r"â", r"'", text)
    text = re.sub(r"Â»", r">>", text)
    text = re.sub(r"’", "'", text)
    text = re.sub(r"‘", "'", text)
    text = re.sub(r"©", "(c)", text)
    text = low_ascii(text)
    text = text.replace("\r", "[EOL]")
    text = text.replace("\n", "[EOL]")
    for x in range(0, 30):
        text = text.replace("[EOL]        [EOL]", "[EOL]")
        text = text.replace("[EOL]       [EOL]", "[EOL]")
        text = text.replace("[EOL]      [EOL]", "[EOL]")
        text = text.replace("[EOL]     [EOL]", "[EOL]")
        text = text.replace("[EOL]    [EOL]", "[EOL]")
        text = text.replace("[EOL]   [EOL]", "[EOL]")
        text = text.replace("[EOL]  [EOL]", "[EOL]")
        text = text.replace("[EOL] [EOL]", "[EOL]")
        text = text.replace("[EOL][EOL]", "[EOL]")
    text = text.replace("[EOL]", "\r\n")
    return text


def low_ascii(in_text):
    text_data = str(in_text)
    new_str = ""
    for char in text_data:
        ascii_code = ord(char)
        if ascii_code > 126:
            new_str += "*"
        else:
            new_str += char
    return new_str
