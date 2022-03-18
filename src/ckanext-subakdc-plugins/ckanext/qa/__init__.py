import logging

from ckanext.qa.qa_no_resources import QaNoResourcesTask, qa_no_resources_report_info
from ckanext.qa.qa_stale import QaStaleTask, qa_stale_report_info

log = logging.getLogger(__name__)

tasks = [ QaNoResourcesTask,
          QaStaleTask ]

reports = [ qa_no_resources_report_info,
            qa_stale_report_info ]

def is_sysadmin(user, _):
    return user is not None and user.sysadmin

# Force all reports to be availale only to superadmins
for report in reports:
    report['authorize'] = is_sysadmin
