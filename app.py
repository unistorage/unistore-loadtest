import redis
import uwsgi
import urlparse
from werkzeug.wrappers import Request, Response
from werkzeug.utils import redirect

import settings


def spawn_connections():
    global r
    r = redis.StrictRedis(host='localhost', port=6379, db=0)

uwsgi.post_fork_hook = spawn_connections


@Request.application
def app(request):
    id = r.get(request.url)
    if id:
    	unistore_url = urlparse.urljoin(settings.UNISTORE_SERVE_URL, id)
    	return redirect(unistore_url, code=302)
    else:
    	return Response(status=404)


if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('localhost', 3000, app, use_debugger=True, use_reloader=True)