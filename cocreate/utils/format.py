import ast


def user_data(data):
    """Format user data for display."""
    return {
        "id": data[0],
        "username": data[1],
        "content_type": data[2],
        "target_audience": data[3],
        "additional_context": data[4],
        "generations": ast.literal_eval(data[5]),
    }


def generation_data(data):
    """Format generation data for display."""
    return [{"id": row[0], "type": row[1], "content": row[2]} for row in data]
