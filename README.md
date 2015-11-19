# Scopus Helper

This Python package makes easier to access Scopus API (http://dev.elsevier.com/) from Pyhon.

# Functionality

- Search for authors and get profile information
- Given a profile identifier, get all publications
- Given publication identifier, get all citations
- Cycle through a list of API keys when request limits are reached

# Example

```python
import scopus_helper as sh
# before using the function you need to specify the list of API keys that you have available
sh.ElsevierApiKeyCycler.key_list = []
# get dictionary with data returned by the Scopus API
profile = sh.get_profile('8868165800')
```


# Author

- Daniel E. Acuna
