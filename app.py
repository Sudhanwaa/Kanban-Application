from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship,Session,sessionmaker
from flask_restful import Resource,Api
from sqlalchemy import create_engine
from sqlalchemy.orm.exc import UnmappedInstanceError

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///data.sqlite3" 
db=SQLAlchemy(app)

engine = create_engine("sqlite:///data.sqlite3")

class User(db.Model):
    __tablename__="data"

    srno=db.Column(db.Integer,autoincrement=True,primary_key=True)
    name=db.Column(db.String,nullable=False)
    group=db.Column(db.String,nullable=False)
    title=db.Column(db.String,nullable=False)
    desc=db.Column(db.String)
    deadline=db.Column(db.String)
    name=db.Column(db.String)

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/home", methods=["POST","GET"])
def home():
    # if method
    user_name=request.form["user_name"]
    user=User.query.filter(User.name==user_name).all()
    
    if(len(user)==0):
        return render_template("empty.html",user_name=user_name)
    
    srno=user[0].srno
    
    lst=[]
    
    for i in range(len(user)):
        lst.append(user[i].group)
    
    groups=set(lst)
    # print(groups)
    temp=[]
    outer=[]
    inner=[]  
    mapping={}
    
    for group_ in groups:
        for i in range(len(user)):
            if(user[i].group==group_):
                temp.append(user[i].title)
                temp.append(user[i].desc)
                temp.append(user[i].deadline)
                temp.append(user[i].srno)
                # print(group_,end='')
                # print(temp)
                inner=temp
                outer.append(inner)
                # print("Sudi")
                temp=[]
        mapping[group_]=outer
        outer=[]
  
    
    final_list=[]
    final_list.append(mapping)
    # print(final_list)
     
    return render_template("home.html",final_list=final_list,user_name=user_name,srno=srno,user=user)
    
@app.route("/test/<string:name>", methods=["POST","GET"])
def test(name):
    title=request.form["card_title"]
    desc=request.form["card_desc"]
    deadline=request.form["card_deadline"]
    
    return render_template("test.html",title=title,desc=desc,deadline=deadline,name=name)

@app.route("/card/<string:user_name>", methods=["POST","GET"])
def card(user_name):
    
    # return render_template("card.html",name=name)
    return render_template("card.html",user_name=user_name)

@app.route("/add/<string:user_name>",methods=["GET","POST"])
def add(user_name):
    card_title=request.form["card_title"]
    card_desc=request.form["card_desc"]
    card_deadline=request.form["card_deadline"]
    card_group=request.form["card_group"]
    Session = sessionmaker(bind = engine)
    session=Session()
    add_data=User(name=user_name,group=card_group,title=card_title,desc=card_desc,deadline=card_deadline)
    session.add(add_data)
    session.commit()

    
    return render_template("success.html")

@app.route("/delete/<int:srno>",methods=["POST","GET"])
def delete(srno):
    print(srno,"Sudhanwa")
    # session=Session()
    record=User.query.filter(User.srno==srno).all()
    Session = sessionmaker(bind = engine)
    session=Session()
    session.delete(record[0])
    session.commit()

    return render_template("login.html")

@app.route("/update/<int:srno>",methods=["POST","GET"])
def update(srno):
    if request.method=="POST":
        record=User.query.filter(User.srno==srno).all()
        card_title=request.form["card_title"]
        card_desc=request.form["card_desc"]
        card_deadline=request.form["card_deadline"]
        card_group=request.form["card_group"]
        name=request.form["user_name"]
        record[0].group=card_group
        record[0].title=card_title
        record[0].desc=card_desc
        record[0].deadline=card_deadline
        record[0].name=name
        Session = sessionmaker(bind = engine)
        session=Session()
        session.add(record)
        session.close()
        session.commit()     
        
        
    record=User.query.filter(User.srno==srno).first()   
    return render_template("update.html",record=record)
        
if __name__=='__main__':
    app.debug=True
    app.run(port=8000)
    
