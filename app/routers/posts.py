from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Post, User
from app.schemas import PostCreate, PostResponse
from app.auth import get_current_user

router = APIRouter(prefix="/posts", tags=["posts"])

# GET all posts — anyone can view
@router.get("/", response_model=list[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).order_by(Post.created_at.desc()).all()
    return posts

# GET single post — anyone can view
@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

# POST create — must be logged in
@router.post("/", response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_post = Post(title=post.title, body=post.body, author_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# DELETE — only the author can delete their own post
@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only delete your own posts")
    db.delete(post)
    db.commit()
    return {"message": "Post deleted"}

# POST Update - update the post, only admin allowed
@router.put("/{post_id}", response_model=PostResponse)
def update_post(post_id: int, post: PostCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    existing = db.query(Post).filter(Post.id == post_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Post not found")
    if existing.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only edit your own posts")
    existing.title = post.title
    existing.body = post.body
    db.commit()
    db.refresh(existing)
    return existing
