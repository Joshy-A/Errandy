from .__init__ import create_app, db
from .models import User, Request, Chat, Message

app = create_app()

def seed_database():
    with app.app_context():
        db.drop_all()

        db.create_all()

        user1 = User(username='user1', password='password1', email='user1@example.com')
        user2 = User(username='user2', password='password2', email='user2@example.com')
        db.session.add_all([user1, user2])
        db.session.commit()

        user1 = User(
            email='pelumi@example.com',
            password='Password@1',
            first_name='Pelumi',
            last_name='Awonuga',
        )

        user2 = User(
            email='oluwafemi@example.com',
            password='Password@2',
            first_name='Favour',
            last_name='Oluwafemi',
        )

        db.session.add_all([user1, user2])
        db.session.commit()

        request1 = Request(title='Who is at the magistrate hall of Kansas?', description='I need to get something', user=user1)
        request2 = Request(title='Who is at the school hostel?', description='Pick something from my room', user=user2)
        db.session.add_all([request1, request2])
        db.session.commit()

        chat1 = Chat(request=request1, responder=user2, requester=user1)
        db.session.add(chat1)
        db.session.commit()

        message1 = Message(content='Hello!', chat=chat1, sender=user1)
        message2 = Message(content='Hi there!', chat=chat1, sender=user2)
        db.session.add_all([message1, message2])
        db.session.commit()

        print("Database seeded successfully.")

if __name__ == '__main__':
    seed_database()
