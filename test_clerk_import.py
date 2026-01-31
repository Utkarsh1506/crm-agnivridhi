import sys
import json

# Check clerk imports
try:
    from clerk_sdk_python import Clerk
    print("✓ clerk_sdk_python.Clerk available")
except ImportError as e:
    print(f"✗ clerk_sdk_python.Clerk: {e}")

try:
    from clerk_sdk_python.clerk import Clerk
    print("✓ clerk_sdk_python.clerk.Clerk available")
except ImportError as e:
    print(f"✗ clerk_sdk_python.clerk.Clerk: {e}")

try:
    from clerk_backend_api import Clerk
    print("✓ clerk_backend_api.Clerk available")
except ImportError as e:
    print(f"✗ clerk_backend_api.Clerk: {e}")

try:
    import clerk_sdk_python
    print(f"\nAvailable modules in clerk_sdk_python: {dir(clerk_sdk_python)}")
except Exception as e:
    print(f"Error: {e}")
