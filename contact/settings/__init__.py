from contact.settings.default import *

try:
    from contact.settings.production import *
except ImportError:
    from contact.settings.development import *
