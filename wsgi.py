from daspanel_web import create_app

# http://stackoverflow.com/questions/14810795/flask-url-for-generating-http-url-instead-of-https
class ReverseProxied(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        scheme = environ.get('HTTP_X_FORWARDED_PROTO')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        else:
            environ['wsgi.url_scheme'] = 'https'
        return self.app(environ, start_response)


app = create_app()
app.wsgi_app = ReverseProxied(app.wsgi_app)

if __name__ == "__main__":
    from werkzeug.serving import run_simple

    run_simple('0.0.0.0',
               5000,
               app,
               threaded=True,
               use_reloader=True,
               use_debugger=True)
