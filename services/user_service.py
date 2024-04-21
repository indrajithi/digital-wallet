from app.models import User, db


class UserService:
    @staticmethod
    def create_user(phone):
        if User.query.filter_by(phone=phone).first():
            raise ValueError("User already exists")

        new_user = User(phone=phone)
        db.session.add(new_user)
        db.session.commit()
        return new_user
