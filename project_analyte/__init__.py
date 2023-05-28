from .celery import app as celery_app

__all__ = ['celery_app']

#
#
# # from os import environ
# # from dotenv import load_dotenv
# #
# #
# #
# # load_dotenv(dotenv_path='./project_analyte/.env')
# #
# # is_devel = environ.get('DEVELOPMENT_MODE', False)
# #
# #
# # from .settings import devel as devel_sets
# # settings = devel_sets
# #
# # if is_devel == 't':
# #     print('Development mode. Please disable it in production')
# #     settings.DEBUG = True
# # else:
# #
# #     settings.DEBUG = True
