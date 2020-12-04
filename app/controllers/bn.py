import re
from loguru import logger
import requests
import bs4 as BeautifulSoup
from urllib.parse import quote_plus

from app import metadata, session


class SVC_BN:
    def cmd_bn(keyword):
        key_phrase = keyword
        text_data = "Here is you Barne's and Nobel Search Results:" + "\r\n"
        keyword = quote_plus(keyword)
        url = f"https://www.barnesandnoble.com/s/{keyword}"
        # url = 'https://www.barnesandnoble.com/s/science+fiction/_/N-8q8?_requestid=2486782'
        response = requests.get(
            url,
            headers={
                "User-agent": "Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/70.0"
            },
        )
        soup = BeautifulSoup.BeautifulSoup(response.content, "lxml")

        product_raw = soup.find_all(
            "div", class_="product-shelf-info product-info-view text--left"
        )
        try:
            for product in product_raw:
                titles = re.findall("title=.*><span", str(product_raw))
                book_link = re.findall('href="/w.*onclick', str(product_raw))
            title_count = 0
            list_title = []
            for each_title in titles:
                each_title = each_title.replace("title=", "")
                each_title = each_title.replace("><span", "")
                title_count += 1
                list_title.append(each_title)
            url_count = 0
            url_list = []
            for each_book_link in book_link:
                each_book_link = each_book_link.replace("onclick", "")
                each_book_link = each_book_link.replace(" ", "")
                each_book_link = each_book_link.replace(
                    "href=", "https://www.barnesandnoble.com"
                )
                each_book_link = each_book_link.replace('"', "")
                final_book_link = re.findall(".*\d;", each_book_link)
                url_list.append(str(final_book_link))
            url_list2 = []

            for non_dup in url_list:
                if non_dup not in url_list2:
                    url_count += 1
                    url_list2.append(non_dup)

            for authors in product_raw:
                authors = re.findall("matchall.*div>", str(product_raw))
            count = 0
            list_author = []
            for author in authors:
                author = author.replace('matchall">', "")
                author = author.replace("</a></div>", "")
                count += 1
                list_author.append(author)
            raw_prices = soup.find_all("div", {"class": "current"})

            for prices in raw_prices:
                prices = re.findall(
                    "\d{1,3}.\d\d</span>\n</a>", str(raw_prices))
            price_count = 0
            list_price = []

            for price in prices:
                price = price.replace("</span>\n</a>", "")
                price_count += 1
                list_price.append(price)
            # print(price_count)
            cnt = 0
            list_len = len(list_title)

            while cnt < list_len:
                # Fix Author Link Issue
                failed = 0
                try:
                    author = list_author[cnt]
                    link_found = author.find("</a>")
                    if link_found > 0:
                        author = author[:link_found]
                except:
                    author = ""
                    failed = 1
                # Fix Link
                try:
                    link_url = url_list2[cnt]
                    link_url = link_url[2:-3]
                    link_code = SVC_BN.proc_link(link_url, metadata, session)
                    link_code = str(link_code)
                except:
                    link_url = ""
                    link_code = ""
                    failed = 1
                try:
                    show_title = list_title[cnt]
                except:
                    show_title = ""
                    failed = 1
                try:
                    price = list_price[cnt]
                except:
                    price = ""
                    failed = 1
                if failed == 0:
                    text_data += "Title: " + show_title + "\r\n"
                    text_data += "Author: " + author + "\r\n"
                    text_data += "Price: $" + price + "\r\n"
                    text_data += "URL:  " + link_url + "\r\n"
                    text_data += "Link Code:  " + link_code + "\r\n"
                    text_data += "\r\n"
                cnt += 1
        except:
            text_data = (
                "We were unable to locate any search results for the search phrase: "
                + key_phrase
                + "\r\n"
            )
            text_data += "Please check the spelling of the book title, or author's name, and try again."
        # text_data = (list(zip(list_title, list_author, list_price)))
        return text_data

    def link_exists(link_url, metadata):
        links = Table("links", metadata, autoload=True)
        qry = links.select().where(links.c.link_url == link_url)
        results = qry.execute()
        rowcount = len(results._saved_cursor._result.rows)
        if rowcount > 0:
            found = True
            for x in results:
                link_code = x[1]
        else:
            found = False
            link_code = ""
        return found, link_code

    def proc_link(link_url, metadata, session):
        # Find URL in DB
        safe_link = str(link_url)
        safe_link = safe_link[:511]
        status = SVC_BN.link_exists(link_url, metadata)
        if status[0] == True:
            logger.debug("Link Exists, pulling the existing link_code")
            link_code = status[1]
        else:
            logger.debug(
                "Link Does Not Exists, entering the link into the DB and recovering the code"
            )
            links = Table("links", metadata, autoload=True)
            i = insert(links)
            i = i.values({"link_url": safe_link})
            session.execute(i)
            session.commit()
            SVC_BN.link_codes(metadata, session)
            status = SVC_BN.link_exists(link_url, metadata)
            link_code = status[1]
        return link_code

    def link_codes(metadata, session):
        links = Table("links", metadata, autoload=True)
        qry = links.select().where(links.c.link_code == None)
        res = qry.execute()
        rowcount = len(res._saved_cursor._result.rows)
        link_rows = {}
        cnt = 0
        for row in res:
            link_rows[cnt] = dict(row)
            link_row = link_rows[cnt]
            logger.info(link_rows[cnt])
            cnt += 1
            link_id = link_row["link_id"]
            link_code = SVC_BN.int_to_base36(link_id)
            # Got B36 Encoding, update link_code
            links = Table("links", metadata, autoload=True)
            upd = (
                links.update()
                .values(link_code=link_code)
                .where(links.c.link_id == link_id)
            )
            session.execute(upd)
            session.commit()

    def int_to_base36(num):
        """Converts a positive integer into a base36 string."""
        assert num >= 0
        digits = "0123456789abcdefghijklmnopqrstuvwxyz"
        res = ""
        while not res or num > 0:
            num, i = divmod(num, 36)
            res = digits[i] + res
        return res
