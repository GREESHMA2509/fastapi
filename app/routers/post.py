from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from .. import models,schemas,oauth2
from ..database import engine,get_db
from sqlalchemy.orm import Session
from typing import Optional,List
from sqlalchemy import func
router=APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user),limit:int=10,search:Optional[str]=""):
    #cursor.execute("""SELECT * FROM posts""")
    #posts=cursor.fetchall
    #print(posts)
    print(limit)
    print(search)
   
    #posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()
    print(results)
    #return {"data":posts}
    return posts

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post: schemas.PostCreate,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    """post_dict = post.dict()
    post_dict["id"] = randrange(0, 10000000)
    my_posts.append(post_dict)
    return {"data": post_dict}"""
    
    
    #cursor.execute(f"INSERT INTO posts (title,content,published) VALUES (title,content,published),({post.title},{post.content},{post.published})")
    #cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s)""",(post.title,post.content,post.published))
    #new_post=cursor.fetchone()
    #conn.commit()
    print(current_user.id)
    print(current_user.email)
    print(post.dict())
    print(user_id)
    new_post=models.Post(owner_id=current_user.id ,**post.dict())
    #return {"data":"created post"}
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    #return {"data":new_post}
    return new_post


@router.get("/latest")
def get_latest_post():
    latest_post = my_posts[-1]
    #return {"detail": latest_post}
    return latest_post

@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id: int,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):#/,response:Response):
    #cursor.execute("""SELECT * FROM posts where id=%s """,{str(id)})
    #post=cursor.fetchone()
    #print(post)
    #post = find_post(id)
    #post=db.query(models.Post).filter(models.Post.id==id).first()
    post=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} was not found")
        #response.status_code=status.HTTP_404_NOT_FOUND
        #return {'message':f"post with id:{id} was not found"}
    if post.owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform request action")
    #return {"post_detail": post}
    return post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    #cursor.execute("""DELETE FROM posts WHERE id=%s returning *""",{str(id),})
    #deleted_post=cursor.fetchone()
    #conn.commit()
    
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} does not exist")
    if post.owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform request action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    #if deleted_post==None:
    #    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} does not exist")
    """index=find_index_post(id)
    if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} does not exist")"""
    #my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int,post:schemas.PostCreate, db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    #cursor.execute("""UPDATE posts SET title=%s,content=%s,published=%s WHERE id=%s RETURNING *""",(post.title,post.content,post.published))
    #index=find_index_post(id)
    #updated_post=cursor.fetchone()
    post_query=db.query(models.Post).filter(models.Post.id==id)
    existing_post=post_query.first()
    if existing_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} does not exist")
    if post.owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform request action")
    post_query.update(post.dict(),synchronize_session=False)
    #post_query.update({'title':'hey this is my updated title','content':'this is my updated content'},synchronize_session=False)
    """if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} does not exist")"""
    """post_dict=post.dict()
    post_dict['id']=id
    my_posts[index]=post_dict"""
    #return {"data":updated_post}
    #return {"data":post_query.first()}
    db.commit()
    return post_query.first()
