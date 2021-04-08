"""Takes a phrase as input and Googles it.
If Google thinks the phrase should be different, print Google's phrase to standard out,
otherwise print the input phrase to standard out"""

import sys
import requests
from bs4 import BeautifulSoup


def main():
    """Main logic that prints to standard out"""
    search_request = parse_search_request()

    # Check if output is terminal, if so output newline for readablity
    # If not, do not output a newline
    if sys.stdout.isatty():
        end_char = "\n"
    else:
        end_char = ""

    # print(get_google_spelling(search_request), end=end_char)


def get_google_spelling(phrase):
    """Return how google would spell the phrase"""
    page = get_page(phrase)

    spell_tag = get_spell_tag(page)

    # If the spell tag does not exist or if the text is empty then the input is
    # spelled correctly as far as Google is concerned so we output the input
    if spell_tag is None or spell_tag.text == "":
        return phrase
    else:
        return spell_tag.text


def get_spell_tag(page):
    """Get out the tag that has the Google spelling or is empty"""
    soup = BeautifulSoup(page.text, 'html.parser')
    spell_tag = soup.find('i')
    return spell_tag


def get_page(search):
    """Get Google html page that has Google spelling and/or same spelling"""
    url = 'http://google.com/search?hl=ru&q=' + search + "&meta=&gws_rd=ssl"
    page = requests.get(url)

    return page


def parse_search_request():
    """Parses stdin first, if None then parses command line arguments to get search request for Google spell checking"""
    if sys.stdin.isatty():
        return ' '.join(sys.argv[1:])
    stdin_list = sys.stdin.readlines()
    stdin = ''.join(stdin_list)
    return stdin


def has_stdin():
    if select.select([sys.stdin, ], [], [], 0.0)[0]:
        return True
    else:
        return False

if __name__ == '__main__':
    main()

