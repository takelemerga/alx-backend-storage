#!/usr/bin/env python3
""" sort students
"""


def top_students(mongo_collection):
    """order top students
    """
    return mongo_collection.aggregate([
        {
            "$project": {
                "name": "$name",
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {"$sort": {"averageScore": -1}}
    ])
