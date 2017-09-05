"""Implements a simple opensearch function"""

from .api_cycler import ElsevierApiKeyCycler, ApiKeyException
import requests


@ElsevierApiKeyCycler
def open_search(current_request, api_key=None):
    more_pages_available = True
    if current_request['search-results']['opensearch:totalResults'] == '0':
        yield []

    while more_pages_available:
        try:
            for r in current_request['search-results']['entry']:
                yield r

            possible_next_link = [l['@href'] for l in current_request['search-results']['link'] if l['@ref'] == 'next']
            if len(possible_next_link) == 1:
                next_link = possible_next_link[0]
                more_pages_available = True
                current_request = requests.get(next_link,
                                               headers={'Accept': 'application/json', 'X-ELS-APIKey': api_key}).json()
            else:
                more_pages_available = False
        except Exception as e:
            raise ApiKeyException(e.message, json_response=current_request)

from typing import Dict


@ElsevierApiKeyCycler
def general_query(url: str = 'http://api.elsevier.com/content/search/scopus', api_key: str = None) -> dict:
    new_request = requests.get(url, headers={'Accept': 'application/json',
                                             'X-ELS-APIKey': api_key})
    if new_request.status_code != 200:
        raise ApiKeyException(str(new_request.status_code), new_request.json())
    else:
        return new_request.json()


def arbitrary_search(url: str) -> list:
    current_request = general_query(url)
    if current_request['search-results']['opensearch:totalResults'] == '0':
        yield ''
    else:
        more_pages_available = True
        while more_pages_available:
            try:
                for r in current_request['search-results']['entry']:
                    yield str(r)

                possible_next_link = [l['@href'] for l in current_request['search-results']['link'] if l['@ref'] == 'next']
                if len(possible_next_link) == 1:
                    next_link = possible_next_link[0]
                    more_pages_available = True

                    current_request = general_query(next_link)
                else:
                    more_pages_available = False
            except Exception as e:
                raise ApiKeyException(e.message, json_response=current_request)
