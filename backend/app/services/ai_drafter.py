import sys
from app.core.database import SessionLocal
from app.services.ai_matcher import calculate_matches
from app.services.ai_engine import execute_llm_outreach_draft

def generate_outreach_for_matches():
    """Loops through discovered matches and drafts custom outreach messages."""
    db = SessionLocal()
    
    print("🔄 Pulling active match pairs...")
    # Reuses your dynamic match engine directly
    matches = calculate_matches(db, user_config=None)
    
    if not matches:
        print("⚠️ No matches found to generate drafts for.")
        db.close()
        return

    print(f"✍️ Found {len(matches)} pathways. Generating custom copies...")
    
    for idx, match in enumerate(matches, 1):
        print(f"\n🤖 [{idx}/{len(matches)}] Drafting for {match['Inside Contact']} at {match['Company']}...")
        try:
            draft = execute_llm_outreach_draft(match)
            print(f"   📧 Subject: {draft.subject_line or 'N/A (LinkedIn)'}")
            print(f"   📝 Body:\n{draft.message_body}\n")
            print("-" * 50)
        except Exception as e:
            print(f"   ❌ Generation failed for this row: {e}", file=sys.stderr)

    db.close()

if __name__ == "__main__":
    generate_outreach_for_matches()