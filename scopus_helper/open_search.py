"""Implements a simple opensearch function"""

from .api_cycler import ElsevierApiKeyCycler, ApiKeyException
import requests


@ElsevierApiKeyCycler
def open_search(current_request, api_key=None):
    more_pages_available = True
    results = []
    if current_request['search-results']['opensearch:totalResults'] == '0':
        return []

    while more_pages_available:
        try:
            results.extend(current_request['search-results']['entry'])

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

    return results
