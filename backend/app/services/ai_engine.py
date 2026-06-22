from app.core.ai_client import get_chat_inference_client, GitHubModelConfig
from app.core.schemas import SemanticMatchResult, MatchInputSchema, OutreachDraftResult

class MatchmakerPrompts:
    """Isolated prompting blueprints for the AI matchmaking engine."""
    SYSTEM_INSTRUCTIONS = (
        "You are the core intelligence matching engine for LinkHunter-AI. Your job is to match open job listings "
        "with a user's LinkedIn connections based on company alignment. You must handle semantic variations "
        "(e.g., 'Google' matches 'Google Cloud', 'Meta' matches 'Facebook', 'LTI' matches 'LTIMindtree').\n\n"
        "CRITICAL RESPONSE INSTRUCTIONS:\n"
        "1. You must return your output EXCLUSIVELY as a raw JSON object matching the exact schema below.\n"
        "2. Do NOT change the keys. Do NOT include fields like 'job_title', 'name', or 'company' inside the matches array.\n"
        "3. Every object inside the 'matches' list MUST contain exactly three keys: 'job_id' (int), 'connection_id' (int), and 'reason' (string).\n"
        "4. Do NOT wrap your response in markdown code blocks (like ```json).\n\n"
        "Strict JSON Template Target:\n"
        "{\n"
        "  \"matches\": [\n"
        "    {\n"
        "      \"job_id\": 1,\n"
        "      \"connection_id\": 3,\n"
        "      \"reason\": \"Connection works at target company entity.\"\n"
        "    }\n"
        "  ]\n"
        "}"
    )

def execute_llm_matchmaking(validated_data: MatchInputSchema) -> SemanticMatchResult:
    """
    Handles raw API execution to GitHub Models.
    Completely isolated from database connections or data formatting layers.
    """
    client = get_chat_inference_client()
    if not client:
        raise RuntimeError("GitHub Models client failed to initialize. Missing GITHUB_TOKEN.")

    response = client.complete(
        messages=[
            {"role": "system", "content": MatchmakerPrompts.SYSTEM_INSTRUCTIONS},
            {"role": "user", "content": f"Inputs Matrix:\n{validated_data.model_dump_json(indent=2)}"}
        ],
        model=GitHubModelConfig.DEFAULT_MODEL,
        temperature=0.1
    )
    
    raw_content = response.choices[0].message.content.strip()
    
    # Clean up any markdown code-block ticks if the model accidentally includes them anyway
    if raw_content.startswith("```"):
        raw_content = raw_content.split("\n", 1)[1].rsplit("\n", 1)[0].strip()
        if raw_content.startswith("json"):
            raw_content = raw_content[4:].strip()
    
    # Local Pydantic structural validation happens here safely
    return SemanticMatchResult.model_validate_json(raw_content)


class OutreachPrompts:
    """Isolated prompting blueprints for drafting high-conversion outreach text."""
    SYSTEM_INSTRUCTIONS = (
        "You are an expert executive networking coach for top tech talent. Your job is to draft a short, "
        "compelling, and highly authentic LinkedIn networking message or email from the user to an internal connection.\n\n"
        "CRITICAL RULES:\n"
        "1. Be brief and respectful of their time (under 150 words).\n"
        "2. Do NOT sound transactional, robotic, or overly desperate.\n"
        "3. Reference their specific role and the target job title to establish context naturally.\n\n"
        "CRITICAL RESPONSE FORMAT INSTRUCTIONS:\n"
        "1. Return your output EXCLUSIVELY as a raw JSON object matching the exact schema below.\n"
        "2. Do NOT use the key 'message'. You must use 'message_body'.\n"
        "3. Do NOT use the key 'subject'. You must use 'subject_line'.\n"
        "4. Do NOT wrap your response in markdown code blocks (like ```json).\n\n"
        "Strict JSON Template Target:\n"
        "{\n"
        "  \"subject_line\": \"An inside look at engineering teams\",\n"
        "  \"message_body\": \"Hi [Name], I noticed your incredible track record at...\"\n"
        "}"
    )

def execute_llm_outreach_draft(match_context: dict) -> OutreachDraftResult:
    """Handles raw message generation requests via GitHub Models."""
    client = get_chat_inference_client()
    if not client:
        raise RuntimeError("GitHub Models client failed to initialize.")

    user_payload = (
        f"Draft a personalized message based on this validated match data:\n"
        f"- Connection Name: {match_context.get('Inside Contact')}\n"
        f"- Connection Role: {match_context.get('Contact Position')}\n"
        f"- Target Company: {match_context.get('Company')}\n"
        f"- My Target Role: {match_context.get('Target Role')}\n"
        f"- Job Location: {match_context.get('Location')}\n"
    )

    response = client.complete(
        messages=[
            {"role": "system", "content": OutreachPrompts.SYSTEM_INSTRUCTIONS},
            {"role": "user", "content": user_payload}
        ],
        model=GitHubModelConfig.DEFAULT_MODEL,
        temperature=0.7 # Bumped slightly up for natural, creative phrasing
    )

    raw_content = response.choices[0].message.content.strip()
    
    if raw_content.startswith("```"):
        raw_content = raw_content.split("\n", 1)[1].rsplit("\n", 1)[0].strip()
        if raw_content.startswith("json"):
            raw_content = raw_content[4:].strip()

    return OutreachDraftResult.model_validate_json(raw_content)