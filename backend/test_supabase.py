import sys
from sqlalchemy import text
from app.core.database import engine, Base
# Import the model to register its metadata structure
from app.models.connection import LinkedInConnection

def verify_supabase_integration():
    print("==================================================================")
    print("🔄 Initiating connection verification with Supabase cloud cluster...")
    print("==================================================================")
    
    # Test 1: Validate network handshake and user authentication
    try:
        with engine.connect() as connection:
            # Run a lightweight query that does not touch any tables
            connection.execute(text("SELECT 1"))
        print("📡 Test 1/2: Network handshake successful! Cloud authentication verified.")
    except Exception as e:
        print(f"\n❌ Test 1/2 FAILED: Unable to authenticate or reach the cloud node.", file=sys.stderr)
        print(f"Error Details: {e}\n", file=sys.stderr)
        print("💡 Debug Checklist:")
        print("   1. Verify your password inside DATABASE_URL is exact.")
        print("   2. If your password has special characters (@, #, !, ?), they must be URL-encoded.")
        print("   3. Check that you are using the 'Connection Pooler' string (port 6543) if on a restricted network.")
        print("   4. Ensure '?sslmode=require' is appended to the end of the string.")
        return

    # Test 2: Validate metadata registration and table engine execution
    try:
        print("\n🏗️  Test 2/2: Syncing schema blueprints and pushing tables...")
        Base.metadata.create_all(bind=engine)
        print("🎉 SUCCESS: Connection is flawless! Database tables successfully provisioned.")
        print("\n👉 Next Steps:")
        print("   Log into your Supabase dashboard, click the 'Table Editor' tab,")
        print("   and verify that the 'linkedin_connections' schema is present.")
    except Exception as e:
        print(f"\n❌ Test 2/2 FAILED: Authenticated successfully, but table generation failed.", file=sys.stderr)
        print(f"Error Details: {e}", file=sys.stderr)
    print("==================================================================")

if __name__ == "__main__":
    verify_supabase_integration()