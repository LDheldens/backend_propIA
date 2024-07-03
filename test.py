from backend.wsgi import *
from users.models import *

role = Role()
role.name = "admin"
role.save()

role = Role()
role.name = "user"
role.save()

user = User()
user.role_id = 1
user.username="admin user"
user.phone = "987654321"
user.email ="admin@gmail.com"
user.set_password('admin123')
user.save()