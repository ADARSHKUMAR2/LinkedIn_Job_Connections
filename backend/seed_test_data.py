from sqlalchemy.exc import IntegrityError
from app.core.database import SessionLocal
from app.models.connection import LinkedInConnection

def seed_dummy_records():
    print("==================================================================")
    print("🌱 Initiating database data write test on Supabase cluster...")
    print("==================================================================")
    
    # Open an isolated session context block
    db = SessionLocal()
    
    # 1. Define distinct dummy data objects using your actual SQLAlchemy model structure
    dummy_records = [
        LinkedInConnection(
            first_name="Prakhar",
            last_name="Gupta",
            company="HighLevel",
            position="Recruiting Team Leader",
            connected_on="2026-06-22"
        ),
        LinkedInConnection(
            first_name="Adarsh",
            last_name="Kumar",
            company="Freelance AI Solutions",
            position="Full Stack AI Engineer",
            connected_on="2026-06-22"
        )
    ]
    
    try:
        print("🚀 Staging mock records into transaction workspace...")
        db.add_all(dummy_records)
        
        print("💾 Pushing write payload and committing to cloud storage...")
        db.commit()
        print("✅ SUCCESS: Dummy records saved cleanly to Supabase!")
        
    except IntegrityError:
        # Roll back the transaction state to clear the session block cleanly
        db.rollback()
        print("\n⚠️  CONSTRAINT NOTICE: Records already verified inside database storage.")
        print("   The 'UniqueConstraint' we built into app/models/connection.py successfully")
        print("   prevented duplicate records from being added!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ DATA WRITE CRASHED: {e}")
        return
        
    # 2. Extract entries from the database to prove read-write functionality
    try:
        print("\n🔍 Querying active database state to read current entries:")
        saved_connections = db.query(LinkedInConnection).all()
        
        print(f"📊 Found {len(saved_connections)} dynamic records inside table context:\n")
        for index, record in enumerate(saved_connections, start=1):
            print(f"   [{index}] {record.first_name} {record.last_name}")
            print(f"       💼 Role:    {record.position}")
            print(f"       🏢 Company: {record.company}")
            print(f"       📅 Date:    {record.connected_on}")
            print("       -----------------------------------------------------")
            
    except Exception as e:
        print(f"❌ DATA EXTRACTION FAILED: {e}")
    finally:
        # Close connection session pool handle
        db.close()
        print("==================================================================")

if __name__ == "__main__":
    seed_dummy_records()