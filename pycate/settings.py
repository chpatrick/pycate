# Scrapy settings for pycate project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'pycate'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['pycate.spiders']
NEWSPIDER_MODULE = 'pycate.spiders'
DEFAULT_ITEM_CLASS = 'pycate.items.PycateItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

