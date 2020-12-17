from loguru import logger
import urllib.parse as make_url
from newsapi import NewsApiClient
import random

from app import metadata, session


class SVC_News:

    def cmd_news(arg):
        chan = str(arg)
        text_data = ""
        channel_list = [
            "1: ABC News abc-news",
            "2: ABC News (AU) abc-news-au",
            "3: Aftenposten aftenposten",
            "4: Al Jazeera English al-jazeera-english",
            "5: ANSA.it ansa",
            "6: Argaam argaam",
            "7: Ars Technica ars-technica",
            "8: Ary News ary-news",
            "9: Associated Press associated-press",
            "10: Australian Financial Review australian-financial-review",
            "11: Axios axios",
            "12: BBC News bbc-news",
            "13: BBC Sport bbc-sport",
            "14: Bild bild",
            "15: Blasting News (BR) blasting-news-br",
            "16: Bleacher Report bleacher-report",
            "17: Bloomberg bloomberg",
            "18: Breitbart News breitbart-news",
            "19: Business Insider business-insider",
            "20: Business Insider (UK) business-insider-uk",
            "21: Buzzfeed buzzfeed",
            "22: CBC News cbc-news",
            "23: CBS News cbs-news",
            "24: CNBC cnbc",
            "25: CNN cnn",
            "26: CNN Spanish cnn-es",
            "27: Crypto Coins News crypto-coins-news",
            "28: Daily Mail daily-mail",
            "29: Der Tagesspiegel der-tagesspiegel",
            "30: Die Zeit die-zeit",
            "31: El Mundo el-mundo",
            "32: Engadget engadget",
            "33: Entertainment Weekly entertainment-weekly",
            "34: ESPN espn",
            "35: ESPN Cric Info espn-cric-info",
            "36: Financial Post financial-post",
            "37: Financial Times financial-times",
            "38: Focus focus",
            "39: Football Italia football-italia",
            "40: Fortune fortune",
            "41: FourFourTwo four-four-two",
            "42: Fox News fox-news",
            "43: Fox Sports fox-sports",
            "44: Globo globo",
            "45: Google News google-news",
            "46: Google News (Argentina) google-news-ar",
            "47: Google News (Australia) google-news-au",
            "48: Google News (Brasil) google-news-br",
            "49: Google News (Canada) google-news-ca",
            "50: Google News (France) google-news-fr",
            "51: Google News (India) google-news-in",
            "52: Google News (Israel) google-news-is",
            "53: Google News (Italy) google-news-it",
            "54: Google News (Russia) google-news-ru",
            "55: Google News (Saudi Arabia) google-news-sa",
            "56: Google News (UK) google-news-uk",
            "57: Göteborgs-Posten goteborgs-posten",
            "58: Gruenderszene gruenderszene",
            "59: Hacker News hacker-news",
            "60: Handelsblatt handelsblatt",
            "61: IGN ign",
            "62: Il Sole 24 Ore il-sole-24-ore",
            "63: Independent independent",
            "64: Infobae infobae",
            "65: InfoMoney info-money",
            "66: La Gaceta la-gaceta",
            "67: La Nacion la-nacion",
            "68: La Repubblica la-repubblica",
            "69: Le Monde le-monde",
            "70: Lenta lenta",
            "71: Lequipe lequipe",
            "72: Les Echos les-echos",
            "73: Libération liberation",
            "74: Marca marca",
            "75: Mashable mashable",
            "76: Medical News Today medical-news-today",
            "77: Metro metro",
            "78: Mirror mirror",
            "79: MSNBC msnbc",
            "80: MTV News mtv-news",
            "81: MTV News (UK) mtv-news-uk",
            "82: National Geographic national-geographic",
            "83: National Review national-review",
            "84: NBC News nbc-news",
            "85: News24 news24",
            "86: New Scientist new-scientist",
            "87: News.com.au news-com-au",
            "88: Newsweek newsweek",
            "89: New York Magazine new-york-magazine",
            "90: Next Big Future next-big-future",
            "91: NFL News nfl-news",
            "92: NHL News nhl-news",
            "93: NRK nrk",
            "94: Politico politico",
            "95: Polygon polygon",
            "96: RBC rbc",
            "97: Recode recode",
            "98: Reddit /r/all reddit-r-all",
            "99: Reuters reuters",
            "100: RT rt",
            "101: RTE rte",
            "102: RTL Nieuws rtl-nieuws",
            "103: SABQ sabq",
            "104: Spiegel Online spiegel-online",
            "105: Svenska Dagbladet svenska-dagbladet",
            "106: T3n t3n",
            "107: TalkSport talksport",
            "108: TechCrunch techcrunch",
            "109: TechCrunch (CN) techcrunch-cn",
            "110: TechRadar techradar",
            "111: The American Conservative the-american-conservative",
            "112: The Economist the-economist",
            "113: The Globe And Mail the-globe-and-mail",
            "114: The Guardian (AU) the-guardian-au",
            "115: The Guardian (UK) the-guardian-uk",
            "116: The Hill the-hill",
            "117: The Hindu the-hindu",
            "118: The Huffington Post the-huffington-post",
            "119: The Irish Times the-irish-times",
            "120: The Jerusalem Post the-jerusalem-post",
            "121: The Lad Bible the-lad-bible",
            "122: The New York Times the-new-york-times",
            "123: The Next Web the-next-web",
            "124: The Sport Bible the-sport-bible",
            "125: The Telegraph the-telegraph",
            "126: The Times of India the-times-of-india",
            "127: The Verge the-verge",
            "128: The Wall Street Journal the-wall-street-journal",
            "129: The Washington Post the-washington-post",
            "130: The Washington Times the-washington-times",
            "131: Time time",
            "132: USA Today usa-today",
            "133: Vice News vice-news",
            "134: Wired wired",
            "135: Wired.de wired-de",
            "136: Wirtschafts Woche wirtschafts-woche",
            "137: Xinhua Net xinhua-net",
            "138: Ynet ynet",
        ]
        go = 1
        try:
            chan = int(chan)
            logger.info("Converting to Integer")
        except:
            go = 0
            text_data += "The channel you selected can not be found. Please choose from one of the channels listed below: \r\n"
            text_data += str(channel_list)
            logger.info("Failed to Convert to Integer")

        if isinstance(chan, int):
            chan = chan
        else:
            go = 0
            text_data = "The channel you selected can not be found. Please choose from one of the channels listed below: \r\n"
            text_data += str(channel_list)
            logger.info("Is Not an Integer")

        if go == 1:
            if chan > 138:
                go = 0
                text_data = "The channel you selected can not be found. Please choose from one of the channels listed below: \r\n"
                text_data += str(channel_list)
                logger.info("Channel Number too High")
            else:
                logger.info("Channel Number Found: Processing.")
                channel_select = channel_list[chan - 1]
                channel_select_space = channel_select.rfind(" ")
                channel_select = channel_select[channel_select_space:]
                try:
                    choices = [1, 2]
                    use_api = random.choice(choices)
                    if use_api == 1:
                        api_key = "b7b41b1e7e86412488beaf2768eebe29"
                    else:
                        api_key = "b7b41b1e7e86412488beaf2768eebe29"

                    newsapi = NewsApiClient(
                        api_key=api_key)
                    top_headlines = newsapi.get_top_headlines(
                        sources=channel_select)
                    x = top_headlines
                    text_data += (
                        "You have selected your news from: " +
                        channel_list[chan - 1]
                    )
                    for key in x["articles"]:
                        content = str(key["content"])
                        text_data += "Title: " + str(key["title"]) + "[EOL]"
                        text_data += "Description: " + \
                            str(key["description"]) + "[EOL]"
                        text_data += "Content: " + \
                            content[0:254] + "[EOL]"
                        text_data += "URL: " + key["url"] + "[EOL]"
                        if len(key["url"]) > 10:
                            text_data += "Link Code: " + SVC_News.proc_link(
                                key["url"], metadata, session
                            )
                        text_data += (
                            "[EOL]"
                            + "***********************************************"
                            + "[EOL]"
                        )
                except Exception as e:
                    text_data += "The news channel you have selected is not available at this time. \r\n"
                    text_data += str(e)
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

    def int_to_base36(num):
        """Converts a positive integer into a base36 string."""
        assert num >= 0
        digits = "0123456789abcdefghijklmnopqrstuvwxyz"
        res = ""
        while not res or num > 0:
            num, i = divmod(num, 36)
            res = digits[i] + res
        return res

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
            link_code = SVC_News.int_to_base36(link_id)
            # Got B36 Encoding, update link_code
            links = Table("links", metadata, autoload=True)
            upd = (
                links.update()
                .values(link_code=link_code)
                .where(links.c.link_id == link_id)
            )
            session.execute(upd)
            session.commit()

    def proc_link(link_url, metadata, session):
        # Find URL in DB
        status = SVC_News.link_exists(link_url, metadata)
        if status[0] == True:
            logger.debug("Link Exists, pulling the existing link_code")
            link_code = status[1]
        else:
            logger.debug(
                "Link Does Not Exists, entering the link into the DB and recovering the code"
            )
            links = Table("links", metadata, autoload=True)
            i = insert(links)
            i = i.values({"link_url": link_url})
            session.execute(i)
            session.commit()
            SVC_News.link_codes(metadata, session)
            status = SVC_News.link_exists(link_url, metadata)
            link_code = status[1]
        return link_code

    def url_encode(phrase):
        data = make_url.quote(phrase)
        return data
