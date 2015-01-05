
from django.conf import settings
import importlib

def menuItem(title,url):
    return MenuItem(title,url)

def menu_context_processor(request):
    return {'MENU_ITEMS':__menu_items()}

def __menu_items():
    menu = ()
    for app_name in settings.INSTALLED_APPS:
        try:
            mod = importlib.import_module(app_name+'.menu')
            menu = menu + mod.menu_items
        except ImportError:
            pass
    return menu 

class MenuItem:
    
    def __init__(self, title,url):
        self.title = title
        self.url = url