"""Functions for accessing publications"""

import requests

from api_cycler import ElsevierApiKeyCycler, ApiKeyException
from open_search import open_search


__all__ = ['get_publications',
           'get_citation_matrix',
           'get_citations',
           ]


@ElsevierApiKeyCycler
def get_publications(author_id, api_key=None):
    initial_request = requests.get('http://api.elsevier.com/content/search/scopus',
                                   params={'query': 'au-id(%s)'
                                                    % author_id,
                                           'count': 100},
                                   headers={'Accept': 'application/json',
                                            'X-ELS-APIKey': api_key}).json()
    all_results = open_search(initial_request)
    return all_results


@ElsevierApiKeyCycler
def get_citation_matrix(scopus_id, api_key=None):
    results = requests.get('http://api.elsevier.com/content/abstract/citations',
                           params={'scopus_id': scopus_id},
                           headers={'Accept': 'application/json',
                                    'X-ELS-APIKey': api_key}).json()
    return results


@ElsevierApiKeyCycler
def get_citations(doi, per_page=25, api_key=None):
    """Get the citations for a particular document"""
    initial_citation_res = requests.get('http://api.elsevier.com/content/abstract/citation-count?doi=%s' % doi,
                                        headers={'Accept': 'application/json', 'X-ELS-APIKey': api_key}).json()
    try:
        possible_initial_citation_link = [l['@href'] for l in
                                          initial_citation_res['citation-count-response']['document']['link']
                                          if l['@rel'] == 'citedby']
        if len(possible_initial_citation_link) == 1:
            initial_citation_link = possible_initial_citation_link[0]

        next_link = initial_citation_link + ('&count=%d' % per_page)
        citations = []
        more_citations_available = True
    except Exception as e:
        raise ApiKeyException(e.message, json_response=initial_citation_res)

    while more_citations_available:
        try:
            citation_res = requests.get(next_link,
                                        headers={'Accept': 'application/json', 'X-ELS-APIKey': api_key}).json()
            citations.append(citation_res['search-results']['entry'])

            possible_next_link = [l['@href'] for l in citation_res['search-results']['link'] if l['@ref'] == 'next']
            if len(possible_next_link) == 1:
                next_link = possible_next_link[0]
                more_citations_available = True
            else:
                more_citations_available = False
        except Exception as e:
            raise ApiKeyException(e.message, json_response=citation_res)

    return [initial_citation_res, citations]


if __name__ == '__main__':
    # Retrieve authors from PLOS ONE
    # from sqlalchemy import create_engine
    # import pandas as pd
    # engine = create_engine(r'postgresql://postgres:root@localhost:5432/wos')
    # engine.connect()
    # author_metrics = pd.read_sql('select * from plos_one.author_metrics', engine)
    # publications = get_publications(author_metrics.iloc[3].scopus_id[10:])
    publications = get_publications('7006576183')
