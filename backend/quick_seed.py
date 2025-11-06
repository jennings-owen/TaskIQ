# To run  python seed_user_tasks.py --list-users 1

#!/usr/bin/env python3
"""
Simple script to quickly seed the database with library app tasks.
Usage: python quick_seed.py [user_id]
"""

import sys
from seed_user_tasks import execute_seed_for_user, verify_user_exists, list_users


def main():
    """Quick seed script entry point."""
    if len(sys.argv) != 2:
        print("Usage: python quick_seed.py <user_id>")
        print("\nAvailable users:")
        users = list_users()
        if users:
            for user in users:
                print(f"  ID: {user['id']} - {user['name']} ({user['email']})")
        else:
            print("  No users found in database.")
        sys.exit(1)
    
    try:
        user_id = int(sys.argv[1])
    except ValueError:
        print("Error: user_id must be a number")
        sys.exit(1)
    
    if not verify_user_exists(user_id):
        print(f"Error: User with ID {user_id} does not exist.")
        sys.exit(1)
    
    try:
        execute_seed_for_user(user_id)
        print(f"\n✅ Successfully seeded tasks for user {user_id}!")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()