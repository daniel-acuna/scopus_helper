__all__ = ['ApiKeyException',
           'ElsevierApiKeyCycler']


class ApiKeyException(Exception):
    """Raise this exception when the API key fail for any reason. Provide the response as an additional message"""
    def __init__(self, message, json_response):
        super(Exception, self).__init__(message)
        self.json_response = json_response


class ElsevierApiKeyCycler(object):
    """"Decorator for cycling through API keys. The decorated function must accept `api_key` keyword"""
    key_idx = 0
    key_list = []

    def __init__(self, f):
        self.f = f

    @staticmethod
    def add_key(api_key):
        """Add a key to the list"""
        ElsevierApiKeyCycler.key_list.append(api_key)

    @staticmethod
    def set_key_list(key_list):
        """Sets the key list and sets the index to 0"""
        ElsevierApiKeyCycler.key_list = key_list
        ElsevierApiKeyCycler.key_idx = 0

    def __call__(self, *args, **kwargs):
        initial_idx = ElsevierApiKeyCycler.key_idx
        while True:
            try:
                return self.f(*args, api_key=ElsevierApiKeyCycler.key_list[ElsevierApiKeyCycler.key_idx], **kwargs)
            except ApiKeyException as e:
                # Examine Elsevier's API response
                # TODO: Check if the reponse indicates that we ran out of keys
                print("API exhausted")
                if 'service-error' in e.json_response and \
                        (e.json_response['service-error']['status']['statusCode'] == 'QUOTA_EXCEEDED' or
                         e.json_response['service-error']['status']['statusCode'] == 'AUTHORIZATION_ERROR'):
                    # move to next key
                    ElsevierApiKeyCycler.key_idx += 1
                    if ElsevierApiKeyCycler.key_idx >= len(ElsevierApiKeyCycler.key_list):
                        ElsevierApiKeyCycler.key_idx = 0
                    if ElsevierApiKeyCycler.key_idx == initial_idx:
                        # whole rotation done, throw error
                        raise Exception("No API keys left")
                else:
                    raise Exception('Unknown API message: %s' % str(e.json_response))
