#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

# import os
# import sys

# if __name__ == "__main__":
#     os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
#     try:
#         from django.core.management import execute_from_command_line
#     except ImportError as exc:
#         raise ImportError(
#             "Couldn't import Django. Are you sure it's installed and "
#             "available on your PYTHONPATH environment variable? Did you "
#             "forget to activate a virtual environment?"
#         ) from exc
#     execute_from_command_line(sys.argv)

# # Añadir este bloque para configurar HTTPS en el servidor de desarrollo
# import django.core.servers.basehttp
# from django.core.wsgi import get_wsgi_application

# application = get_wsgi_application()

# django.core.servers.basehttp.WSGIServer.allow_reuse_address = False
# django.core.servers.basehttp.WSGIRequestHandler.protocol_version = "HTTP/1.1"

# from wsgiref.simple_server import make_server, WSGIRequestHandler

# class SSLWSGIRequestHandler(WSGIRequestHandler):
#     def makefile(self, *args, **kwargs):
#         return super(SSLWSGIRequestHandler, self).makefile(*args, **kwargs, errors='ignore')

# if __name__ == "__main__":
#     import ssl
#     httpd = make_server(
#         'localhost',
#         8000,
#         application,
#         ssl_context=(r'path\to\mysite.crt', r'path\to\mysite.key'),
#         handler_class=SSLWSGIRequestHandler
#     )
#     print("Starting server at https://localhost:8000")
#     httpd.serve_forever()
