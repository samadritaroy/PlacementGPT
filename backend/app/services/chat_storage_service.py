from app.services.supabase_service import supabase


def create_chat_session(
    user_id: str = "user_id",
    session_type: str = "session_type",
    company: str = "company"
):
    result = (
        supabase.table("chat_sessions")
        .insert({
            "user_id": user_id,
            "session_type": session_type,
            "company": company
        })
        .execute()
    )

    return result.data[0]


def add_chat_message(
    session_id: str,
    role: str,
    content: str
):
    result = (
        supabase.table("chat_messages")
        .insert({
            "session_id": session_id,
            "role": role,
            "content": content
        })
        .execute()
    )

    return result.data[0]


def get_chat_history(
    session_id: str
):
    result = (
        supabase.table("chat_messages")
        .select("role,content")
        .eq("session_id", session_id)
        .order("created_at")
        .execute()
    )

    return result.data
def clear_session(session_id: str):
    supabase.table("chat_messages") \
        .delete() \
        .eq("session_id", session_id) \
        .execute()

    supabase.table("chat_sessions") \
        .delete() \
        .eq("id", session_id) \
        .execute()