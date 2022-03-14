import logging
from datetime import datetime
import math

import ckan.plugins as p

log = logging.getLogger(__name__)

def freshness_score(last_modified_dts):
    '''
    Simple scoring mechanism based on the most recently modified resource
    A score of 5 is given where last updated resource is < 180 days old
    A score falls in increments of 180 days (i.e a score of 1 for > 720 days or ~ 2 years)
    '''
    newest = last_modified_dts[0]
    age = (datetime.now() - newest).days

    score = 5 - math.floor(age / 180)
    if score < 1:
        score = 1
    
    return int(score)

def get_freshness_score(pkg):
    ''' 
    Read the freshness score from the pkg dict
    Used by the helper function h.freshness_score
    '''
    return pkg['freshness_score'] if 'freshness_score' in pkg else 0


class FreshnessPlugin(p.SingletonPlugin):
    p.implements(p.IPackageController)
    p.implements(p.ITemplateHelpers)
    
    # ------- IPackageController method implementations ------- #
    
    def read(self, entity):
        # Called after IPackageController.before_view inside package_show.
        pass

    def create(self, entity):
        # Called after the dataset had been created inside package_create.
        pass

    def edit(self, entity):
        # Called after the dataset had been updated inside package_update.
        pass

    def delete(self, entity):
        # Called before commit inside package_delete.
        pass

    def after_create(self, context, pkg_dict):
        # Extensions will receive the validated data dict after the dataset has been created (Note that the create method will return a dataset domain object, which may not include all fields). Also the newly created dataset id will be added to the dict.
        pass

    def after_update(self, context, pkg_dict):
        # Extensions will receive the validated data dict after the dataset has been updated.
        pass

    def after_delete(self, context, pkg_dict):
        # Extensions will receive the data dict (typically containing just the dataset id) after the dataset has been deleted.
        pass

    def after_show(self, context, pkg_dict):
        # Extensions will receive the validated data dict after the dataset is ready for display.
        pass

    def before_search(self, search_params):
        # Extensions will receive a dictionary with the query parameters, and should return a modified (or not) version of it.
        # search_params will include an extras dictionary with all values from fields starting with ext_, so extensions can receive user input from specific fields.
        return search_params

    def after_search(self, search_results, search_params):
        # Extensions will receive the search results, as well as the search parameters, and should return a modified (or not) object with the same structure:
        # {'count': '', 'results': '', 'facets': ''}
        # Note that count and facets may need to be adjusted if the extension changed the results for some reason.
        # search_params will include an extras dictionary with all values from fields starting with ext_, so extensions can receive user input from specific fields.
        return search_results

    def before_index(self, pkg_dict):
        # Extensions will receive what will be given to Solr for indexing. This is essentially a flattened dict (except for multi-valued fields such as tags) of all the terms sent to the indexer. The extension can modify this by returning an altered version.
        return pkg_dict

    def before_view(self, pkg_dict):
        ''' 
        Adds freshness score to the pkg_dict for display in the UI
        '''
        resources = pkg_dict['resources']
        
        # No resources -> don't provide a freshness score
        if len(resources) < 1:
            return pkg_dict
        
        # Find and sort the last modified dates for all dataset resources
        last_modified_dts = []
        for res in resources:
            if 'last_modified' in res and res['last_modified'] is not None:
                try:
                    date_format = "%Y-%m-%dT%H:%M:%S.%f"
                    dt = datetime.strptime(res['last_modified'], date_format)
                    last_modified_dts.append(dt)
                except:
                    # Skip resources whose last modified property is empty or cannot be parsed using date_format
                    pass
        
        if len(last_modified_dts) >= 1:
            last_modified_dts = sorted(last_modified_dts, reverse=True)
            pkg_dict['freshness_score'] = freshness_score(last_modified_dts)
            
        return pkg_dict
    

    # ------- ITemplateHelpers method implementations ------- #
    
    def get_helpers(self):
        ''' 
        Helper function to extract the freshness score from the package dict
        '''
        return {'freshness_score': get_freshness_score}
