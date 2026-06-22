import csv
import os
import sys
from sqlalchemy.exc import IntegrityError
from app.core.database import SessionLocal
from app.models.connection import LinkedInConnection

def clean_row_data(row: dict) -> dict:
    """Standardizes string values and handles empty fields safely."""
    return {
        "first_name": row.get("First Name", "").strip(),
        "last_name": row.get("Last Name", "").strip(),
        "company": row.get("Company", "").strip() or None,
        "position": row.get("Position", "").strip() or None,
        "connected_on": row.get("Connected On", "").strip() or None,
    }

def ingest_linkedin_csv(file_path: str):
    print("==================================================================")
    print(f"📥 Starting raw ingestion pipeline for: {file_path}")
    print("==================================================================")

    if not os.path.exists(file_path):
        print(f"❌ INGESTION ERROR: Target file not found at '{file_path}'", file=sys.stderr)
        return

    db = SessionLocal()
    success_count = 0
    duplicate_count = 0
    error_count = 0

    try:
        with open(file_path, mode="r", encoding="utf-8") as f:
            # Skip any leading promotional text rows that LinkedIn sometimes injects
            lines = f.readlines()
            start_index = 0
            for i, line in enumerate(lines):
                if "First Name" in line and "Last Name" in line:
                    start_index = i
                    break
            
            # Reset pointer and pass data rows cleanly to the DictReader
            f.seek(0)
            for _ in range(start_index):
                next(f)
                
            reader = csv.DictReader(f)

            print("🚀 Processing records and streaming payloads to Supabase...")
            for row in reader:
                # Bypass empty rows
                if not row.get("First Name") or not row.get("Last Name"):
                    continue

                clean_data = clean_row_data(row)
                
                # Instantiate an isolated database record
                connection_record = LinkedInConnection(**clean_data)
                
                try:
                    db.add(connection_record)
                    db.commit()
                    success_count += 1
                except IntegrityError:
                    # Triggers if the user already exists in the table matching our UniqueConstraint
                    db.rollback()
                    duplicate_count += 1
                except Exception as e:
                    db.rollback()
                    error_count += 1

        print("\n🎉 INGESTION PIPELINE SUMMARY:")
        print(f"   📊 Newly Synced Records: {success_count}")
        print(f"   ⚠️  Skipped Duplicates:  {duplicate_count}")
        print(f"   ❌ Execution Failures:   {error_count}")

    except Exception as global_err:
        print(f"❌ CRITICAL PIPELINE CRASH: {global_err}", file=sys.stderr)
    finally:
        db.close()
        print("==================================================================")

if __name__ == "__main__":
    # Standard entry point mapping for verification runs
    sample_path = os.path.join(os.path.dirname(__file__), "../../Connections.csv")
    ingest_linkedin_csv(sample_path)