import re
import wikipedia
import html2text
from loguru import logger
from .link import SVC_Link


class SVC_Wikipedia:
    def cmd_wiki(arg):
        try:
            logger.debug("Wikipedia User Search Phrase: " + arg)
            wiki_pages = wikipedia.search(arg)
            wiki_text = (
                "The following is a list of other Wikipedia page titles that came back in your search,"
                " if you see what you are looking for here, and not in the below content, "
                "then please submit a new request for the correct page title from this list: "
            )
            wiki_text += str(wiki_pages)
            wiki_text = SVC_Link.to_text(wiki_text, rehtml=True)
            # If Some Results are Found
            if len(wiki_pages) > 0:
                selected = wiki_pages[0]
                wiki_text += "\r\n Wikipage Selected: " + selected + "\r\n"
                wiki_content = wikipedia.page(selected)
                wiki_text += wiki_content.content
            # If No Results are Found
            else:
                page1 = (
                    "There are no Wikipedia results for this search phrase: \r\n"
                    + str(arg)
                    + "\r\n"
                    + "Wikipedia requires exact spelling for page requests, you may have better luck using the Google "
                    "Service first, to get the exact spelling. And of course you can retrieve pages from the Google "
                    "search results with the link feature as well."
                )
        except Exception as e:
            page1 = (
                "An Error Occurred Wikipedia results for this search phrase: \r\n"
                + str(arg)
                + "\r\n"
                + "Wikipedia requires exact spelling for page requests, you may have better luck using the Google "
                "Service first, to get the exact spelling. And of course you can retrieve pages from the Google "
                "search results with the link feature as well."
            )
            logger.warning("Wikipedia Error: " + str(e))
        return wiki_text

    def text_wiki(html_src, rehtml=True):
        html_data = str(html_src)
        html_data = html_data.replace("\n", "[EOL]")
        # html_data = html_data.replace('===', '[EOL]')
        # html_data = html_data.replace('==', '[EOL]')
        parser = html2text.HTML2Text()
        parser.wrap_links = True
        parser.unicode_snob = True
        parser.skip_internal_links = True
        parser.inline_links = True
        parser.ignore_anchors = True
        parser.ignore_images = True
        parser.ignore_emphasis = True
        parser.ignore_links = True
        text = parser.handle(html_data)
        text = re.sub(r"â", r"'", text)
        text = re.sub(r"Â»", r">>", text)
        text = re.sub(r"’", "'", text)
        text = re.sub(r"‘", "'", text)
        text = re.sub(r"©", "(c)", text)
        text = SVC_Link.low_ascii(text)
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
        return text
