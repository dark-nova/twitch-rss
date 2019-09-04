import sqlite3

from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from selenium import webdriver

import db


URL = 'https://twitch.amazon.com/tp/loot'


def get_as_html():
    """Gets the true source of the URL."""
    # Choose your own webdriver if desired
    options = webdriver.firefox.options.Options()
    options.headless = True
    browser = webdriver.Firefox(options = options)
    browser.get(URL)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    # with open('example.html', 'w') as f:
    #     f.write(soup.prettify())
    return soup


def get_all_loot(fg: FeedGenerator, soup = None):
    """Gets all loot from page.

    Loot can be categorized as either 'in-game' or 'games'.

    Args:
        fg (FeedGenerator): the feed to add entries
        soup (optional): the soup to use; defaults to None

    Returns:
        None

    """

    if soup is None:
        with open('example.html', 'r') as example:
            soup = BeautifulSoup(example, 'html.parser')

    for loot in soup.find_all('div', 'offer-list__content'):
        category = loot.find('h3').text.strip()
        get_loot(fg, loot, category)

    return


def get_loot(fg: FeedGenerator, loot, category: str):
    """Gets loot for a given `loot` type.

    Called by `get_all_loot`.

    Args:
        fg (FeedGenerator): the feed to add entries
        loot: the loot to parse
        category (str): either 'In-Game Loot and More'
            or 'Games with Prime'

    Returns:
        None

    """
    for offer in loot.find_all('div', 'offer'):
        entry = fg.add_entry()
        entry.title(offer.find('span').text.strip())
        entry.category(
            category = {
                'label': category
                }
            )
        try:
            link = offer.find('a')['href']
            entry.link(href = link)
            entry.guid(link)
        except TypeError:
            entry.link(href = URL)
            entry.guid(URL)

    return


if __name__ == '__main__':
    fg = FeedGenerator()
    fg.title('Twitch Prime Games and Loot')
    fg.author({'name': 'Twitch Prime'})
    fg.description('Twitch Prime Games and Loot')
    fg.link(
        href = URL,
        rel = 'alternate'
        )
    # Change the below URL when self-hosting.
    fg.link(
        href = 'https://dark-nova.me/twitchprime.xml',
        rel = 'self'
        )
    # Change the below URL when self-hosting.
    fg.logo('https://dark-nova.me/twitchprime.png')
    fg.language('en-US')
    get_all_loot(fg, get_as_html())


    #get_as_html()
