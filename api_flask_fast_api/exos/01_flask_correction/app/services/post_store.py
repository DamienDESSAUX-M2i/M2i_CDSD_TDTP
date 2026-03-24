from datetime import datetime


posts_db = {
    1: {
        'id': 1,
        'title': 'Welcome to the Blog',
        'content': 'This is the first post!',
        'author': 'Admin',
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }
}
next_post_id = 2


def list_posts():
    return list(posts_db.values())


def get_post_by_id(post_id: int):
    return posts_db.get(post_id)


def create_post(data: dict):
    global next_post_id

    title = data.get('title', '').strip()
    content = data.get('content', '').strip()
    author = data.get('author', 'Anonymous').strip()

    if not title or len(title) < 1:
        return {'error': 'Title is required and cannot be empty'}, 422

    if not content or len(content) < 1:
        return {'error': 'Content is required and cannot be empty'}, 422

    now = datetime.now().isoformat()
    post = {
        'id': next_post_id,
        'title': title,
        'content': content,
        'author': author,
        'created_at': now,
        'updated_at': now
    }

    posts_db[next_post_id] = post
    next_post_id += 1
    return post, 201


def update_post(post_id: int, data: dict):
    post = posts_db.get(post_id)
    if not post:
        return {'error': f'Post with ID {post_id} not found'}, 404

    if 'title' in data and data['title'].strip():
        post['title'] = data['title'].strip()

    if 'content' in data and data['content'].strip():
        post['content'] = data['content'].strip()

    if 'author' in data and data['author'].strip():
        post['author'] = data['author'].strip()

    post['updated_at'] = datetime.now().isoformat()
    return post, 200


def delete_post(post_id: int):
    if post_id not in posts_db:
        return {'error': f'Post with ID {post_id} not found'}, 404

    deleted_post = posts_db.pop(post_id)
    return {
        'message': 'Post deleted successfully',
        'post': deleted_post
    }, 200
