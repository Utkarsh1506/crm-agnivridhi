# Update base.html to add notification badge
import re

base_html_path = r'c:\Users\Admin\Desktop\agni\CRM\templates\base.html'

with open(base_html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the navbar section
old_navbar = '''                <ul class="navbar-nav ms-auto">
                    {% if user.is_authenticated %}
                        <li class="nav-item me-3">'''

new_navbar = '''                <ul class="navbar-nav ms-auto">
                    {% if user.is_authenticated %}
                        {% if user.is_admin or user.is_manager %}
                        <li class="nav-item">
                            <a class="nav-link position-relative" href="{% url 'pending_applications' %}">
                                <i class="bi bi-bell"></i> Pending Approvals
                                {% if pending_count > 0 %}
                                <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
                                    {{ pending_count }}
                                    <span class="visually-hidden">pending applications</span>
                                </span>
                                {% endif %}
                            </a>
                        </li>
                        {% endif %}
                        <li class="nav-item me-3">'''

if 'pending_applications' not in content:
    content = content.replace(old_navbar, new_navbar)
    with open(base_html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Added notification badge to navbar")
else:
    print("⚠️  Badge already exists")
