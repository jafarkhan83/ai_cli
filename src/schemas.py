json_schema = {
    "type": "object",
    "properties" : {
        "title": {"type": "string"},
        "description": {"type": "string"},
        "content": {"type": "string"},
        "metadata": {
            "type": "object",
            "properties": {
                "input_user_tokens": {"type": "integer"},
                "input_system_tokens": {"type": "integer"},
                "output_tokens": {"type": "integer"},
                "total_tokens": {"type": "integer"}
            },
            "required": ["input_user_tokens", "input_system_tokens", "output_tokens", "total_tokens"]
        }
    },
    "required": ["title", "description", "content", "metadata"]
}