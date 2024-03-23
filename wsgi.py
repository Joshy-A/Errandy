from app import app (as wsgi_app)
import socketio

socketio = socketio.Server(async_mode='gevent')
socketio.wrap_app(wsgi_app)
