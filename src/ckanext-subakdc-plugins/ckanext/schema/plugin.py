import logging
import json
from os import path
import ckan.plugins as p

log = logging.getLogger(__name__)

def get_countries_dict(field):
    with open(path.join(path.dirname(__file__), 'countries-iso-3166.json')) as f:
        countries = json.load(f)
        
    return list(map(lambda c: { 'value': c['alpha-2'], 'label': c['name'] }, countries))

class SchemaPlugin(p.SingletonPlugin):
    p.implements(p.ITemplateHelpers)
    
    # ------- ITemplateHelpers method implementations ------- #
    
    def get_helpers(self):
        ''' 
        Helper function to extract the freshness score from the package dict
        '''
        return {'scheming_countries_choices': get_countries_dict}
