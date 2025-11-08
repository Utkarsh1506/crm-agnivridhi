from django.contrib.auth import get_user_model

USERNAME = 'owner'
PASSWORD = 'test123'

User = get_user_model()
u, created = User.objects.get_or_create(username=USERNAME, defaults={'email': 'owner@example.com'})
u.first_name = 'Owner'
u.role = 'ADMIN'
u.is_owner = True
u.is_active = True
u.set_password(PASSWORD)
u.save()
print({'username': u.username, 'id': u.id, 'created': created, 'role': u.role, 'is_owner': u.is_owner})
