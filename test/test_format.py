from cocreate.utils import format


def test_format_user_data():
    user_data = (
        1,
        "test_user",
        "Content type",
        "Target audience",
        "Additional context",
        "[1, 2, 3]",
        "[4, 5]",
    )
    formatted_data = format.user_data(user_data)
    assert formatted_data == {
        "id": 1,
        "username": "test_user",
        "content_type": "Content type",
        "target_audience": "Target audience",
        "additional_context": "Additional context",
        "generations": [1, 2, 3],
        "favorite_generations": [4, 5],
    }


def test_format_generation_data():
    generation_data = [
        (1, "newsletter", "This is a test generation."),
        (2, "thread", "This is another test generation."),
    ]
    formatted_data = format.generation_data(generation_data)
    assert formatted_data == [
        {"id": 1, "type": "newsletter", "content": "This is a test generation."},
        {"id": 2, "type": "thread", "content": "This is another test generation."},
    ]
