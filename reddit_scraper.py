from typing import Dict, List, Optional, Generator
import praw
import json
from services.database import RedditSubmission
from services.database.util import transaction

secrets_dict = json.loads(
    open('/home/markn/Documents/RedditBot/reddit_api/client_secrets.json', 'r').read())
reddit = praw.Reddit(
    client_id=secrets_dict['client_id'],
    client_secret=secrets_dict['client_secret'],
    user_agent=secrets_dict['user_agent'],
    refresh_token=secrets_dict['refresh_token']
)

def get_hot_from_sub (subreddit: str, limit: int) -> List[str]:
    return list(
            map(
                lambda x: x.selftext,
                reddit.subreddit(subreddit).hot(limit=limit)
            )
    )

def _list_mods(subreddit):
    return [str(moderator) for moderator in reddit.subreddit(subreddit).moderator()]

def _is_repeat (id: int) -> bool:
    with transaction() as session:
        return (session.query(RedditSubmission.id) \
            .filter (RedditSubmission.id == id) \
            .first()) is not None
    
def _insert_submission (id: str, subreddit: str, content_type: str):
    with transaction() as session:
        submission = RedditSubmission(
            id=id,
            subreddit=subreddit,
            content_type=content_type
        )
        session.add(submission)

def filter (subreddit: str, max_posts: int, min_upvotes: int, sort_by: str, period: Optional[str] = None) -> Generator[str, None, None]:
    posts = []
    mods = _list_mods(subreddit)
    if sort_by == 'hot':
        submissions = reddit.subreddit(subreddit).hot(limit=100)
    elif sort_by == 'new':
        submissions = reddit.subreddit(subreddit).new(limit=100)
    elif sort_by == 'top':
        submissions = reddit.subreddit(subreddit).top(time_filter=period, limit=100)
    elif sort_by == 'rising':
        submissions = reddit.subreddit(subreddit).rising(limit=100)
    else:
        submissions = reddit.subreddit(subreddit).hot(limit=100)
    for i in submissions:
        # print (i.selftext)
        if len(posts) >= max_posts:
            break
        print (i.id)
        print (_is_repeat(i.id))
        if not i.stickied and i.author not in mods and \
            not hasattr(i, "crosspost_parent") and \
            not _is_repeat (i.id) and i.score >= min_upvotes:

            posts.append(i.selftext)
            _insert_submission(i.id, subreddit, 'text')
            yield i.selftext