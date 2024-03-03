from Errand import create_app
from flask_socketio import emit, join_room, leave_room, SocketIO
from Errand.models import *
from datetime import datetime
from flask_login import current_user


app, socket = create_app()

socket=SocketIO(app)
# COMMUNICATION MODULE
@socket.on("join-chat")
def join_chat(data):
    if "room_id" in data:
        room_id = data["room_id"]
        socket.join_room(room_id)
    else:
        print("No room_id provided in data.")

@socket.on('send-message')
def handle_send_message(data):
    sender = data['sender']
    content = data['content']
    # Broadcast the message to all users in the chat room
    socket.emit('receive-message', {'sender': sender, 'content': content}, room=data['room_id'])



@socket.on("outgoing-message")
def outgoing_message(data):
    room_id = data["room_id"]
    message_content = data["content"]
    sender_id = data["sender_id"]
    sender = User.query.get(sender_id)
    timestamp = datetime.utcnow()

    new_message = Message(content=message_content, timestamp=timestamp, sender_id=sender_id, chat_id=room_id)
    db.session.add(new_message)
    db.session.commit()

    socket.emit("incoming-message", {"content": message_content, "timestamp": timestamp, "sender_username": sender.username}, room=room_id, include_self=False)
if __name__ == '__main__':
    socket.run(app, allow_unsafe_werkzeug=True, debug=True)
    