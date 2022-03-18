from datetime import datetime
import logging
import math

from ckanext.qa.interfaces import IQaTask, IQaReport
from ckanext.qa.qa_actions import QaHideDatasetsAction

log = logging.getLogger(__name__)

QA_PROPERTY_NAME = 'qa_stale'
QA_ACTIONS = [ QaHideDatasetsAction ]
QA_STALESNESS_THRESHOLD = 720 # in days


class QaStaleTask(IQaTask):
    qa_property_name = QA_PROPERTY_NAME
    
    @classmethod
    def evaluate(cls, pkg):
        # The `metadata_updated` attribute of both the package and resources gets updated whenever
        # the QA tasks run, so should not be used to judge staleness. This leaves the `last_modified`
        # attribute on resources as the sole method for determining if a dataset is stale (we use
        # the same logic for the freshness plugin)
        try:
            resources = pkg['resources']
        
            # No resources -> evaluate False
            if len(resources) < 1:
                return { 'is_stale': False}
            
            # Find the last_modified (or created) datetimes for each resource in the package
            last_modified_dts = []
            for res in resources:
                dt = None
                datetime_format = "%Y-%m-%dT%H:%M:%S"
                if 'last_modified' in res and res['last_modified'] is not None:
                    try:
                        lm = res['last_modified'].split('.')[0] # Ignore milliseconds
                        dt = datetime.strptime(lm, datetime_format)
                    except ValueError as e:
                        log.error(f"Cannot parse resource last_modified datetime in QaStaleTask: {e}")
                        
                else:
                    try:
                        created = res['created'].split('.')[0] # Ignore milliseconds
                        dt = datetime.strptime(created, datetime_format)
                    except ValueError as e:
                            log.error(f"Cannot parse resource created datetime in QaStaleTask: {e}")
                
                if dt is not None:                 
                    last_modified_dts.append(dt)
            
            # If at least one datetime is found and the most recent datetime is older than threshold,
            # then evaluate as True
            if len(last_modified_dts) >= 1:
                last_modified_dts = sorted(last_modified_dts, reverse=True)
                age = (datetime.now() - last_modified_dts[0]).days
                
                if age > QA_STALESNESS_THRESHOLD:
                    return { 'is_stale': True, 'age': age }
            
            return { 'is_stale': False }
                
        except Exception as e:
            log.error(f"Could not evaluate pkg in QaStaleTask: {e}")
            return { 'is_stale': False }
            
            
class QaStaleReport(IQaReport):
    qa_property_name = QA_PROPERTY_NAME
    qa_actions = QA_ACTIONS
    
    @classmethod
    def generate(cls):
        action_is_running = cls.run_action()
        
        fields = ['id', 'title', 'num_resources']
        computed_fields = { 'age': cls.get_age}
       
        report = cls.build(fields, computed_fields, action_is_running=action_is_running)
       
        report['table'].sort(key=lambda x: x['age'], reverse=True)
        return report
   
    @classmethod
    def get_age(cls, pkg):
        try:
            return pkg['subak_qa'][QA_PROPERTY_NAME]['age']
        except ValueError:
            return None
    
    @classmethod
    def should_show_in_report(cls, value):
        # Only show in report if value `is_stale` item is set to true
        return value.get('is_stale', False)


qa_stale_report_info = {
    'name': 'stale-datasets',
    'description': f"This report lists stale datasets where the newest resource was added/updated more than {math.ceil(QA_STALESNESS_THRESHOLD / 365)} years ago",
    'option_defaults': None,
    'option_combinations': None,
    'generate': QaStaleReport.generate,
    'template': 'report/qa_stale.html'
}