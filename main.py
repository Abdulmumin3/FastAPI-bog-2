from fastapi import FastAPI, Depends, HTTPException, status
import schemas, models, hashing
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from sqlalchemy.sql import func


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/posts', status_code=status.HTTP_200_OK, tags=['Blogs'])
async def get_posts(db: Session = Depends(get_db)):
    blogs = db.query(models.Post).all()
    return blogs

@app.post('/create-post', status_code=status.HTTP_201_CREATED, tags=['Blogs'], )
async def create_post(request: schemas.PostBase, db: Session = Depends(get_db)):
    new_blog = models.Post(title=request.title, body = request.body,  published = request.published, created_at = request.created_at, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/post/{id}', status_code=status.HTTP_200_OK, response_model=schemas.GetPost, tags=['Blogs'], )
async def get_post_by_id(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Post).filter(models.Post.id == id).first()
    if blog is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
    return blog

@app.put('/update/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.PostUpdate, tags=['Blogs'])
async def update_post_by_id(id: int, request: schemas.PostUpdate, db: Session = Depends(get_db)):
    blog = db.query(models.Post).filter(models.Post.id == id).first()
    if blog is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    # updated_blog = request.dict()
    # blog.update(updated_blog)
    # db.commit()
    blog.title = request.title
    blog.body = request.body
    blog.published = request.published
    blog.updated_at = func.now()
    
    db.commit()
    return blog

@app.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Blogs'])
async def delete_post_by_id(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Post).filter(models.Post.id == id)
    
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
    blog.delete(synchronize_session=False)
    db.commit()
    
    return "deleted"



@app.post('/create-user', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser, tags=['Users'])
async def create_user(request: schemas.User, db: Session = Depends(get_db)):
    
    new_user = models.User(name=request.name, email=request.email, password=hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/get-user/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowUser, tags=["Users"])
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    
    return user