import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


class SubakdcPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)

    # ------- IConfigurer method implementations ------- #
    def update_config(self, config):
        toolkit.add_template_directory(config, 'templates')
        toolkit.add_public_directory(config, 'public')
        toolkit.add_resource('./assets', 'ckanext-subakdc')
