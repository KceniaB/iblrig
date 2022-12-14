import logging

from confapp import conf

logger = logging.getLogger(__name__)

conf += "iblpybpod.pyforms_generic_editor.settings"

# # load the user settings in case the file exists
# try:
# 	import pyforms_generic_editor_user_settings
#
# 	conf += pyforms_generic_editor_user_settings
# except Exception as err:
# 	logger.debug('No user_settings available', exc_info=True)
