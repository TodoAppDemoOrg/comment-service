from uuid import UUID
from uuid import uuid4
from typing import List
from typing import Dict
from typing import Optional
from datetime import datetime
from collections import Counter
import dataclasses
import winter


@dataclasses.dataclass
class Comment:
    id: UUID
    topic: str
    author: str
    text: str
    timestamp: datetime


@dataclasses.dataclass
class TopicStatistics:
    topic: str
    comment_count: int


comments: List[Comment] = [
    Comment(uuid4(), '11e7f524-8729-4286-81c4-991a10f408c1', 'Alexander E', 'Just a test comment', datetime(2022, 8, 31, 10, 11, 00)),
    Comment(uuid4(), '11e7f524-8729-4286-81c4-991a10f408c1', 'Alexander E', 'One more test comment', datetime(2022, 8, 31, 10, 12, 00)),
    Comment(uuid4(), '11e7f524-8729-4286-81c4-991a10f408c1', 'Alexander E', 'The third comment from my side', datetime(2022, 8, 31, 10, 13, 00)),
    Comment(uuid4(), '2b892f00-2b44-4351-9d18-f6b19c1d6d42', 'Alexander E', 'Is it finished?', datetime(2022, 8, 31, 10, 14, 00)),
    Comment(uuid4(), '2b892f00-2b44-4351-9d18-f6b19c1d6d42', 'Ivan Ivanov', 'Nope', datetime(2022, 8, 31, 10, 15, 00)),
    Comment(uuid4(), '333a2af4-4d24-446b-9024-95c477a25e93', 'Alexander E', 'How are you?', datetime(2022, 8, 31, 10, 16, 00)),
    Comment(uuid4(), '333a2af4-4d24-446b-9024-95c477a25e93', 'Ivan Ivanov', 'Fine, how are you?', datetime(2022, 8, 31, 10, 17, 00)),
    Comment(uuid4(), '333a2af4-4d24-446b-9024-95c477a25e93', 'Alexander E', "Thanks, I'm good", datetime(2022, 8, 31, 10, 18, 00)),
]


@winter.web.no_authentication
class CommentAPI:
    @winter.route_post('comments/')
    @winter.request_body('comment')
    def create_comment(self, comment: Comment):
        comments.append(comment)

    @winter.route_delete('comments/{comment_id}/')
    def delete_comment(self, comment_id: UUID):
        global comments
        comments = [comment for comment in comments if comment.id != comment_id]

    @winter.route_get('comments/{?topic}')
    def get_comments(self, topic: Optional[str] = None) -> List[Comment]:
        result = comments.copy()
        if topic is not None:
            result = [comment for comment in result if comment.topic == topic]
        return result

    @winter.route_get('topic-statistics/{?topics*}')
    def get_topic_statistics(self, topics: List[str]) -> List[TopicStatistics]:
        counter = Counter([comment.topic for comment in comments if comment.topic in topics])
        return [TopicStatistics(topic, count) for topic, count in counter.items()]
