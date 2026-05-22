from app import app, db, User

def init_test_accounts():
    with app.app_context():
        db.create_all()
        test_users = [
            {"username": "admin", "password": "sonam101", "role": "admin"},
            {"username": "operator_01", "password": "password123", "role": "operator"},
            {"username": "viewer_guest", "password": "guest_password", "role": "viewer"}
        ]
        print("--- 正在初始化三级权限测试账号 ---")
        for user_data in test_users:
            if not User.query.filter_by(username=user_data["username"]).first():
                new_user = User(username=user_data["username"], role=user_data["role"])
                new_user.set_password(user_data["password"])
                db.session.add(new_user)
                print(f"成功创建用户: {user_data['username']} (角色: {user_data['role']})")
        db.session.commit()
        print("--- 账号初始化完成 ---")

if __name__ == "__main__":
    init_test_accounts()
