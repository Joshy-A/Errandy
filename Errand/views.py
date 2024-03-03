from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from flask_login import login_required, current_user, logout_user
from flask_socketio import SocketIO
from sqlalchemy import or_
from . import db
from .models import  *


views = Blueprint('views', __name__)
socket = SocketIO

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    requests = Request.query.all()
    return render_template('home.html', requests=requests, user=current_user)

@views.route("/create", methods=['POST'])
@login_required
def create():   
    """
    Creates a new request.

    Returns:
        Response: Flask response object.
    """
    title = request.form.get('title')
    description = request.form.get('description')
    
    if not title or not description:
        flash('Title and description are required fields.', category='error')
        return redirect(url_for('views.home'))

    # Create a new request associated with the current user
    new_request = Request(title=title, description=description, user_id=current_user.id)
    db.session.add(new_request)
    db.session.commit()
    
    flash('Request created successfully!', category='success')
    return redirect(url_for('views.home'))


@views.route("/chat/", methods=["GET", "POST"])
@login_required
def chat():
    """
    Renders the chat interface and displays chat messages.

    Returns:
        Response: Flask response object.
    """
    # Get the room id in the URL or set to None
    room_id = request.args.get("rid", None)

    # Get the current user's ID
    current_user_id = current_user.id

    # Get the chat list for the current user
    current_user_chats = Chat.query.filter(or_(Chat.requester_id==current_user_id, Chat.responder_id==current_user_id)).all()

    # Initialize context that contains information about the chat room
    data = []

    for chat in current_user_chats:
        # Determine the username of the other user in the chat
        if chat.requester_id == current_user_id:
            other_user_id = chat.responder_id
        else:
            other_user_id = chat.requester_id

        other_user = User.query.get(other_user_id)

        # Get the last message in the chat
        last_message = chat.messages[-1] if chat.messages else None
        last_message_content = last_message.content if last_message else "No messages yet."

        data.append({
            "username": other_user.first_name,
            "room_id": chat.id,
            "is_active": room_id == str(chat.id),
            "last_message": last_message_content,
        })

    # Get all the message history in the specified room
    messages = Message.query.filter_by(room_id=room_id).order_by(Message.timestamp).all() if room_id else []

    return render_template(
        "chat.html",
        user_data=current_user,
        room_id=room_id,
        data=data,
        messages=messages,
        user= current_user,
    )

@views.route('/message/<int:request_id>', methods=['POST'])
@login_required
def send_message(request_id):
    # Retrieve the request associated with the given request_id
    request = Request.query.get_or_404(request_id)

    # Check if the current user is authenticated and has a valid email
    if not current_user.is_authenticated or not current_user.email:
        flash('You need to be authenticated with a valid email to send a message.', category='error')
        return redirect(url_for('views.home'))

    # Check if there is an existing chat room for the request and the current user is a member
    existing_chat = Chat.query.filter_by(request_id=request_id, user_id=current_user.id ).first()

    # If the chat room doesn't exist or the current user is not a member, create a new chat room
    if not existing_chat:
        # Create a new chat room associated with the request, the requester, and the current user
        new_chat = Chat(request_id=request.id, requester_id=request.user.id, responder_id=current_user.id)
        db.session.add(new_chat)
        db.session.commit()

        # Flash message for chat room creation
        flash('Chat room created successfully!', category='success')

    # Redirect the user to the chat room for the request
    return redirect(url_for('views.chat', room_id=request_id))


@views.route('/view-request/<int:request_id>', methods=['GET'])
@login_required
def view_request(request_id):
    # Fetch the request data from the database
    request_data = Request.query.get_or_404(request_id)
    
    # Pass the request data to the viewrequest.html template
    return render_template('view_request.html', request=request_data, user=current_user)

@views.route('/delete-account', methods=['POST'])
@login_required
def delete_account():
    user = User.query.get(current_user.id)

    if user:
        logout_user()
        db.session.delete(user)
        db.session.commit()

        flash('Your account has been deleted successfully!', category='success')
        return redirect(url_for('auth.login'))
    else:
        flash('User not found', category='error')
        return redirect(url_for('views.home'))
    
@views.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    requests = Request.query.get_or_404(id)
    
    if requests.user != current_user:
        flash('You cannot delete this request.', category='error')

    else:
        
        db.session.delete(requests)
        db.session.commit()
        
        flash('Requests Deleted!', category='success')
    return redirect(url_for('views.home'))


    