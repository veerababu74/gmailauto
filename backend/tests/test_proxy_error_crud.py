"""
Complete test of proxy error CRUD operations
This script creates, reads, updates, and deletes proxy error records to verify functionality.
"""

from sqlalchemy.orm import Session
from app.core.database import db_manager
from app.models.proxy_error import ProxyError
from app.schemas.proxy_error import ProxyErrorCreate, ProxyErrorUpdate
from app.crud.crud_proxy_error import proxy_error
from datetime import datetime


def test_proxy_error_crud():
    """Test all CRUD operations for proxy errors"""

    print("Starting Proxy Error CRUD Test")
    print("=" * 40)

    # Get database session
    db = next(db_manager.get_db())

    try:
        # 1. CREATE - Add a new proxy error
        print("\n1. Testing CREATE operation...")
        proxy_error_data = ProxyErrorCreate(
            agent_name="test_agent_001",
            proxy="192.168.1.100:8080",
            error_details="Connection timeout after 30 seconds during authentication",
            profile_name="test_profile_001",
        )

        created_error = proxy_error.create(db=db, obj_in=proxy_error_data)
        print(f"✓ Created proxy error with ID: {created_error.id}")
        print(f"  Agent: {created_error.agent_name}")
        print(f"  Proxy: {created_error.proxy}")
        print(f"  Profile: {created_error.profile_name}")
        print(f"  Created at: {created_error.created_at}")

        # 2. READ - Get the created error
        print("\n2. Testing READ operation...")
        retrieved_error = proxy_error.get(db=db, id=created_error.id)
        if retrieved_error:
            print(f"✓ Retrieved proxy error ID: {retrieved_error.id}")
            print(f"  Error details: {retrieved_error.error_details}")
        else:
            print("✗ Failed to retrieve proxy error")
            return

        # 3. GET MULTIPLE - Test pagination and filtering
        print("\n3. Testing GET MULTIPLE operation...")
        errors, total = proxy_error.get_multi(
            db=db, skip=0, limit=10, agent_name="test_agent_001"
        )
        print(f"✓ Found {total} total errors for agent 'test_agent_001'")
        print(f"  Retrieved {len(errors)} errors in this page")

        # 4. UPDATE - Modify the error
        print("\n4. Testing UPDATE operation...")
        update_data = ProxyErrorUpdate(
            error_details="Updated: Connection timeout - proxy server unreachable after multiple attempts"
        )
        updated_error = proxy_error.update(
            db=db, db_obj=retrieved_error, obj_in=update_data
        )
        print(f"✓ Updated proxy error ID: {updated_error.id}")
        print(f"  New error details: {updated_error.error_details}")
        print(f"  Updated at: {updated_error.updated_at}")

        # 5. SEARCH - Test search functionality
        print("\n5. Testing SEARCH operation...")
        search_errors, search_total = proxy_error.get_multi(
            db=db, skip=0, limit=10, search="timeout"
        )
        print(f"✓ Found {search_total} errors containing 'timeout'")

        # 6. ANALYTICS - Test statistics methods
        print("\n6. Testing ANALYTICS operations...")

        # Test get_unique_agents
        unique_agents = proxy_error.get_unique_agents(db=db)
        print(f"✓ Unique agents: {unique_agents}")

        # Test get_unique_proxies
        unique_proxies = proxy_error.get_unique_proxies(db=db)
        print(f"✓ Unique proxies: {unique_proxies}")

        # Test get_unique_profiles
        unique_profiles = proxy_error.get_unique_profiles(db=db)
        print(f"✓ Unique profiles: {unique_profiles}")

        # Test count_by_proxy
        count = proxy_error.count_by_proxy(db=db, proxy="192.168.1.100:8080")
        print(f"✓ Error count for proxy '192.168.1.100:8080': {count}")

        # Test get_recent_by_agent
        recent_errors = proxy_error.get_recent_by_agent(
            db=db, agent_name="test_agent_001", limit=5
        )
        print(f"✓ Recent errors for agent 'test_agent_001': {len(recent_errors)}")

        # 7. DELETE - Remove the error
        print("\n7. Testing DELETE operation...")
        deleted_error = proxy_error.remove(db=db, id=created_error.id)
        if deleted_error:
            print(f"✓ Deleted proxy error ID: {deleted_error.id}")
        else:
            print("✗ Failed to delete proxy error")

        # 8. VERIFY DELETE - Confirm it's gone
        print("\n8. Verifying DELETE operation...")
        verify_error = proxy_error.get(db=db, id=created_error.id)
        if verify_error is None:
            print("✓ Proxy error successfully deleted")
        else:
            print("✗ Proxy error still exists after deletion")

    except Exception as e:
        print(f"✗ Error during test: {str(e)}")
        import traceback

        traceback.print_exc()
    finally:
        db.close()

    print("\n" + "=" * 40)
    print("Proxy Error CRUD Test Completed")


if __name__ == "__main__":
    test_proxy_error_crud()
