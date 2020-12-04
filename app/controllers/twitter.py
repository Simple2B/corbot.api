import re
import requests
from loguru import logger
import bs4 as BeautifulSoup
from sqlalchemy import *

from app import metadata, session


def cmd_twitter(phrase):
    search_url = "https://twitter.com/search-home"
    url = "https://twitter.com/sarah_hyland"
    feed_text = get_feed(url)
    return feed_text


def get_feed(url):
    get_page = requests.get(
        url,
        headers={
            "User-agent": "Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/70.0"
        },
    )
    page_data = str(get_page.text)
    soup = BeautifulSoup.BeautifulSoup(page_data, "lxml")
    file_data = soup.text
    # Clean Up
    file_data = file_data.replace("Log in", "")
    file_data = file_data.replace("Sign up", "")
    file_data = file_data.replace(
        "You are on Twitter Mobile because you are using an old version of Chrome. Learn more here",
        "",
    )
    file_data = file_data.replace("Settings", "")
    file_data = file_data.replace("Help", "")
    file_data = file_data.replace("Load older Tweets", "")
    file_data = file_data.replace("View details", "")
    file_data = file_data.replace("Enter a topic, @name, or fullname", "")
    file_data = file_data.replace("Back to top · Turn images off", "")
    file_data = file_data.replace('{"page":"profile"}', "")
    text = re.sub(r"[^\x00-\x7F]+", "*", file_data)
    text_data = ""
    file_data_lines = text.split(chr(10))
    for line in file_data_lines:
        if len(line) > 1:
            text_data += line.strip() + chr(13) + chr(10)
    return text_data


def parse_twitter(link_url):
    tweets = []
    the_url = str(link_url)
    the_url = the_url.replace("https://", "https://mobile.")
    # the_url = "https://mobile.twitter.com/realdonaldtrump"

    try:
        body_text = ""
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0",
            "X-Requested-With": "XMLHttpRequest",
        }
        get_page = requests.get(the_url, headers)
        page_data = str(get_page.text)
        logger.debug("Now fetching: " + the_url)
    except:
        logger.debug("Error  - get fail : " + the_url)

    soup = BeautifulSoup.BeautifulSoup(page_data, "lxml")
    body = soup.find("body")
    try:
        ol_tweets = body.find("div", attrs={"class": "timeline"})
        for tweets in ol_tweets.find_all("table", attrs={"class": "tweet"}):
            tweets_by = tweets.find_all(
                "tr", attrs={"class": "tweet-header"})
            tweets_name = tweets.find_all(
                "td", attrs={"class": "user-info"}
            )  # gets name
            name = re.findall('fullname">(.*?)<', str(tweets_name))
            tweet_timing = tweets.find_all(
                "td", attrs={"class": "timestamp"})
            timing = re.findall('">(.*?)<', str(tweet_timing))
            tweet_text = tweets.find_all("div", attrs={"class": "dir-ltr"})

            for tweets_text1 in tweet_text:
                # body_text += ("Tweeted by: " + str(name) + " About " + str(timing) + " ago" + "\r\n")
                body_text += (
                    "Tweeted by: "
                    + str(name)
                    + " About "
                    + str(timing)
                    + " ago"
                    + str(tweets_text1.text)
                )
                body_text += (
                    "\r\n***************************************************\r\n"
                )
    except:
        body_text = "Twitter request has failed."

    return body_text


def strip_spaces(temp_data):
    spam_fried = False
    stripped_string = ""
    if len(temp_data) < 2:
        return temp_data
    for elem in temp_data[0: len(temp_data): 1]:
        if ord(elem) > 32 and ord(elem) <= 125:
            stripped_string = stripped_string + elem
            spam_fried = False
        elif ord(elem) == 32 and spam_fried == False:
            stripped_string = stripped_string + " "
            spam_fried = True
    return stripped_string
