import logging

from ckanext.qa.interfaces import IQaAction

log = logging.getLogger(__name__)


class QaHideDatasetsAction(IQaAction):
    name = 'hide_datasets'
    form_button_text = 'Hide selected datasets'
    
    @classmethod
    def run(cls, dataset_ids):
        log.debug(dataset_ids)
