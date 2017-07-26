""""Functions for getting information about profiles"""

import requests

from .api_cycler import ElsevierApiKeyCycler, ApiKeyException
from .restful_api_helpers import clean_string


__all__ = ['search_profiles',
           'get_profile',
           ]


@ElsevierApiKeyCycler
def search_profiles(first_initial, last_name, affiliation, api_key=None):
    initial_search = requests.get('http://api.elsevier.com/content/search/author',
                                  params={'query': 'authlastname(%s) and authfirst(%s) and affil(%s)'
                                                   % (clean_string(last_name),
                                                      clean_string(first_initial),
                                                      clean_string(affiliation))},
                                  headers={'Accept': 'application/json', 'X-ELS-APIKey': api_key}).json()
    try:
        return initial_search['search-results']
    except Exception as e:
        raise ApiKeyException(e.message, json_response=initial_search)


@ElsevierApiKeyCycler
def get_profile(author_id, api_key=None, additional_params={}):
    # Initial search
    initial_search = requests.get('http://api.elsevier.com/content/author/author_id/%s' % author_id,
                                  params=additional_params,
                                  headers={'Accept': 'application/json', 'X-ELS-APIKey': api_key}).json()
    try:
        return initial_search['author-retrieval-response']
    except Exception as e:
        raise ApiKeyException(e.message, json_response=initial_search)
