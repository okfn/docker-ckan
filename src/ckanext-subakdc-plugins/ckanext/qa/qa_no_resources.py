import logging

from ckanext.qa.interfaces import IQaTask, IQaReport, IQaAction

log = logging.getLogger(__name__)

QA_PROPERTY_NAME = 'qa_no_resources'


class QaNoResourcesTask(IQaTask):
    qa_property_name = QA_PROPERTY_NAME
    
    @classmethod
    def evaluate(cls, pkg):
        # True if no resources, False if 1 or more resources
        try:
            return len(pkg['resources']) == 0
        except Exception as e:
            log.error(f"Could not evaluate pkg in QaNoResourcesTask: {e}")
            return False
            
            
class QaNoResourcesReport(IQaReport):    
    @classmethod
    def generate(cls):
       fields = ['id', 'title', 'num_resources']
       return cls.build(QA_PROPERTY_NAME, fields)
    
    @classmethod
    def should_show_in_report(cls, value):
        # Only show in report if value is set to true
        if value is None:
            return False
        else:
            return value
        
    @classmethod
    def get_qa_actions(cls):
        # TODO add some actions (e.g. remove dataset or set to private visibility)
        return []
    
qa_no_resources_report_info = {
    'name': 'datasets-with-no-resources',
    'description': 'Datasets with no resources',
    'option_defaults': None,
    'option_combinations': None,
    'generate': QaNoResourcesReport.generate,
    'template': 'report/qa_no_resources.html'
}