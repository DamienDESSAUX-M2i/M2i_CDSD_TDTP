orders_db: dict[str, dict] = {}

users_db: dict[int, dict] = {
    1: {
        "id": 1,
        "username": "john",
        "email": "john@example.com",
        "is_active": True
    }
}
next_user_id = 2

events_db: dict[int, dict] = {}
next_event_id = 1