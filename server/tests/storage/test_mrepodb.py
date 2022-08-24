from src.domain.mrepo import (
    _find_resolved_comments,
    _find_new_comments,
)  # Temporarily move to the domain layer

# fmt: off
def test_find_resolved_comments():

    dummy_parsed_comments = [
        {
            "id": "85136c79cbf9fe36bb9d05d0639c70c265c18d37",
            "title": "Refactor the methods",
        },
        {
            "id": "535e775e273d93844920103bad8e8d709639f7f9", 
            "title": "Add test"
        },
        {
            "id": "bd073433caebf2f73f9440ab4815f665d84fd1b8",
            "title": "Improve performance",
        },
    ]

    dummy_comments_from_db = [
        {
            "id": "85136c79cbf9fe36bb9d05d0639c70c265c18d37",
            "title": "Refactor the methods",
        },
        {
            "id": "535e775e273d93844920103bad8e8d709639f7f9", 
            "title": "Add test"
        },
        {
            "id": "bd073433caebf2f73f9440ab4815f665d84fd1b8",
            "title": "Improve performance",
        },
        {
            "id": "b56e396f011f1159207e1a33453db14fdc741f0c", 
            "title": "Resolved comment"
        },
        {
            "id": "df211ccdd94a63e0bcb9e6ae427a249484a49d60",
            "title": "Resolved comment - 2",
        },
    ]
    resolved = _find_resolved_comments(dummy_comments_from_db, dummy_parsed_comments)

    assert len(resolved) == 2


def test_find_new_comments():

    dummy_parsed_comments = [
        {
            "id": "85136c79cbf9fe36bb9d05d0639c70c265c18d37",
            "title": "Refactor the methods",
        },
        {
            "id": "535e775e273d93844920103bad8e8d709639f7f9", 
            "title": "Add test"
        },
        {
            "id": "bd073433caebf2f73f9440ab4815f665d84fd1b8",
            "title": "Improve performance",
        },
                {
            "id": "b56e396f011f1159207e1a33453db14fdc741f0c", 
            "title": "New comment"
        },
        {
            "id": "df211ccdd94a63e0bcb9e6ae427a249484a49d60",
            "title": "New comment - 2",
        },
    ]

    dummy_comments_from_db = [
        {
            "id": "85136c79cbf9fe36bb9d05d0639c70c265c18d37",
            "title": "Refactor the methods",
        },
        {
            "id": "535e775e273d93844920103bad8e8d709639f7f9", 
            "title": "Add test"
        },
        {
            "id": "bd073433caebf2f73f9440ab4815f665d84fd1b8",
            "title": "Improve performance",
        },
    ]
    new = _find_new_comments(dummy_comments_from_db, dummy_parsed_comments)

    assert len(new) == 2
# fmt: on
