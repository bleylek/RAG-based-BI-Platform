from app import create_app
from app.auth.models import db, User

app = create_app()

with app.app_context():
    # Normal kullanıcı oluştur
    user = User(email='user@example.com', is_verified=True)
    user.set_password('user123')
    db.session.add(user)
    db.session.commit()
    print('Normal kullanıcı oluşturuldu.')
    
    # Tüm kullanıcıları listele
    users = User.query.all()
    
    print("\nKullanıcı Listesi:")
    print("="*60)
    print(f"{'ID':<5} {'Email':<30} {'Doğrulanmış':<12} {'Admin':<5}")
    print("-"*60)
    
    for user in users:
        print(f"{user.id:<5} {user.email:<30} {user.is_verified:<12} {getattr(user, 'is_admin', False):<5}")
