from flask import Flask,jsonify,request,make_response,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from functools import wraps
import redis
from flask_caching import Cache
from my_celery import make_celery
from datetime import datetime, timedelta
from flask_mail import Mail, Message
from celery.schedules import crontab
app=Flask(__name__)
# Configure Flask-Mail


app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)
celery = make_celery(app)


cache = Cache(config={'CACHE_TYPE': 'redis','CACHE_REDIS_HOST':'127.0.0.1','CACHE_REDIS_PORT':6379})
cache.init_app(app)

CORS(app)
cors=CORS(app, resources={
    r"/*":{
        "origins":"*"
    }
})

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'ticketshowteam@gmail.com'  
app.config['MAIL_PASSWORD'] = 'syyswytfnocajcmf' 
app.config['MAIL_DEFAULT_SENDER'] = 'ticketshowteam@gmail.com'  

mail = Mail(app)
app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Ticketshow.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# ma=Marshmallow(app)

# ------------------------MODELS---------------------------------

class Venue(db.Model):
    id = db.Column('venue_id', db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    place = db.Column(db.String(100))
    location = db.Column(db.String(100))
    capacity = db.Column(db.Integer)
    shows=db.relationship('Shows', backref='venue', lazy=True,cascade='all,delete-orphan')

    def __init__(self, name,place,location,capacity):
        self.name = name
        self.place=place
        self.location = location
        self.capacity=capacity

class Shows(db.Model):
    id=db.Column('show_id',db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    rating = db.Column(db.Float(100))
    tag = db.Column(db.String(100))
    timing= db.Column(db.String(100))
    price = db.Column(db.Integer)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.venue_id'), nullable=False)
    booking=db.relationship('Booking', backref='shows', lazy=True,cascade='all,delete-orphan')
   
    def __init__(self,name,rating,tag,timing,price,venue_id):
        self.name = name
        self.rating=rating
        self.tag =tag
        self.timing = timing
        self.price=price
        self.venue_id=venue_id

class User_reg(db.Model):
    id = db.Column('user_id', db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    email = db.Column(db.String(50))  
    booking=db.relationship('Booking', backref='user_reg', lazy=True,cascade='all,delete-orphan')
    def __init__(self, name,password,email):
        self.name = name
        self.password=password
        self.email = email    

class Admin(db.Model):
    id=db.Column('admin_id',db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    email=db.Column(db.String(100))
    password=db.Column(db.String(100))

    # def __init__(self,name,email,password):
    #     self.name = name
    #     self.email=email
    #     self.password=password 

class Booking(db.Model):
    id=db.Column('booking_id',db.Integer,primary_key=True)
    number=db.Column(db.Integer)
    show_id = db.Column(db.Integer, db.ForeignKey('shows.show_id'), nullable=True)
    u_id= db.Column(db.Integer, db.ForeignKey('user_reg.user_id'), nullable=True)
    booking_date=db.Column(db.Date)
    def __init__(self,number,show_id,u_id,booking_date):
        self.number = number
        self.show_id=show_id
        self.u_id=u_id  
        self.booking_date=booking_date  



class logininfo(db.Model):
    id=db.Column('login_id',db.Integer,primary_key=True)
    userid=db.Column(db.Integer)
    date=db.Column(db.Date)

    def __init__(self, userid,date):
        self.userid = userid
        self.date=date

class emailinfo(db.Model):
    id=db.Column('email_id',db.Integer,primary_key=True)
    email=db.Column(db.String(100))
    date=db.Column(db.Date)

    def __init__(self, email,date):
        self.email = email
        self.date=date

class profileemailinfo(db.Model):
    id=db.Column('profileemail_id',db.Integer,primary_key=True)
    email=db.Column(db.String(100))
    date=db.Column(db.Date)

    def __init__(self, email,date):
        self.email = email
        self.date=date
# ------------------------Token------------------------------------

def token_required(t):
    @wraps(t)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User_reg.query.filter_by(id=data['user_id']).first()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return t(current_user, *args, **kwargs)

    return decorated

def adtoken_required(t):
    @wraps(t)
    # It is necessary when you create custom decorators to preserve the original function metadata.(wraps)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try: 
            # print(token)
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            # print(data)
            current_admin = Admin.query.filter_by(id=data['admin_id']).first()
            # print(current_admin)
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return t(current_admin, *args, **kwargs)

    return decorated
# -------------------------ROUTES--------------------------------------------
celery.conf.beat_schedule = {
    'send-monthly-email': {
        'task': 'app.getprofilemail',
        'schedule': crontab(day_of_month='1', hour=12, minute=0),  # Schedule to run on the 1st day of each month at 12:00 PM (noon).
    },
}
celery.conf.beat_schedule = {
    'send-evening-email': {
        'task': 'app.checklogin',
        'schedule': crontab(hour=20, minute=0),  # Schedule to run at 8:00 PM (20:00).
    },
}



# ---------------------------LOGIN-----------------------------------------

@app.route('/userreg', methods=['POST'] )

def userreg():  
        hashed_password = generate_password_hash(request.json['password'], method='sha256')
        user_reg=User_reg(request.json['name'],hashed_password,request.json['email'])
        db.session.add(user_reg)
        db.session.commit()
        content={"message":"Registered"}
        return content


@app.route('/login/<string:emails>/<string:passwords>', methods =['GET'])

def login(emails,passwords):
   
    admin = Admin.query.filter_by(email=emails).first()
    user = User_reg.query.filter_by(email=emails).first()


    if user:
        if check_password_hash(user.password, passwords):
            token = jwt.encode({'user_id': user.id,'username':user.name,'expiration' : str(datetime.utcnow() + timedelta(minutes=120))}, app.config['SECRET_KEY'])
            uk=int(user.id)
            logindata=logininfo(userid=user.id,date=datetime.now())
            db.session.add(logindata)
            db.session.commit()
            return make_response(jsonify({'token' : token,'username':user.name,'email':user.email,'password':user.password,'login':"user"}), 201)
        else:
            return make_response ({'error':"Passwords doesnt match!"})
    
    elif admin:   
        if(passwords==admin.password):
            token = jwt.encode({'admin_id': admin.id,'expiration' : str(datetime.utcnow() + timedelta(minutes=120))}, app.config['SECRET_KEY'])
            return make_response(jsonify({'token' : token,'username':admin.name,'login':"admin"}), 201)
        else:
            return make_response ({'error':"Passwords doesnt match!"})
    else:   
        return make_response ({'error':"Invalid LogIn!Register"})
    
# ---------------------------------Create for Admin-----------------------------------

@app.route('/createven', methods=['POST','GET'] )
@adtoken_required
def createven(current_admin): 
        content={"mesage":"Success"}
        if request.method=="POST":
            venue=Venue(request.json['name'],request.json['place'],request.json['location'],request.json['capacity'])
            db.session.add(venue)
            db.session.commit()
            return content

@app.route('/createshow', methods=['POST','GET'] )
@adtoken_required
def createshow(current_admin): 
    content={"message":"Show Added"} 
    if request.method=="POST":
        venuedata=Venue.query.get(request.json['venueid'])
        show=Shows(request.json['name'],request.json['rating'],request.json['tag'],request.json['timing'],request.json['price'],venuedata.id)
        db.session.add(show)
        db.session.commit()
        return content

    
# -----------------------------Delete for Admin---------------------------------------
    
@app.route("/delven/<int:id>", methods=['DELETE'])  
@adtoken_required            
def delete(current_admin,id): 
    content={"mesage":"Success"}
    delven=Venue.query.get(id)
    db.session.delete(delven)
    db.session.commit()
    return content

@app.route('/delshow/<int:id>', methods=['DELETE'])   
@adtoken_required     
def delshow(current_admin,id):
    content={"mesage":"Success"}
    dshow=Shows.query.get(id)
    db.session.delete(dshow)
    db.session.commit()
    return content

# -----------------------------Get for Admin---------------------------------------

@app.route('/getdvenue',methods=['GET'])
@cache.memoize(5)
@adtoken_required
def getdvenue(current_admin):
    venue=Venue.query.all()
    output = []
    for i in venue:
        list_data = {}
        list_data['id'] = i.id
        list_data['name'] = i.name 
        list_data['place']=i.place
        list_data['location']=i.location
        list_data['capacity']=i.capacity
        output.append(list_data)
    return jsonify({'data' : output})   

@app.route('/getdshows',methods=['GET'])
@cache.memoize(5)
@adtoken_required
def getdshows(current_admin):
        varray=[]
        shows=Shows.query.all()
        showoutput = []
        for i in shows:
            show_data = {}
            show_data['id'] = i.id
            show_data['name'] = i.name 
            show_data['rating']=i.rating
            show_data['tag']=i.tag
            show_data['timing']=i.timing
            show_data['price']=i.price
            show_data['venu']=i.venue_id
            showoutput.append(show_data)
        for i in shows:
             vdict={}
             vdict['venue']=i.venue_id
             varray.append(vdict)
        return jsonify({'data' : showoutput,'vd':varray}) 

# ----------------------------Get with Id for Admin---------------------------------------

@app.route('/getdven/<int:id>',methods=['GET'])
@adtoken_required
def getdven(current_admin,id):
    getvenudata=Venue.query.get(id)
    venuoutput = []
    ven_data = {}
    ven_data['name']=getvenudata.name
    ven_data['place']=getvenudata.place
    ven_data['location']=getvenudata.location
    ven_data['capacity']=getvenudata.capacity
    venuoutput.append(ven_data)
    return jsonify({'data':venuoutput})

@app.route('/getdshow/<int:id>',methods=['GET'])
@adtoken_required
def getdshow(current_admin,id):
    getshowdata=Shows.query.get(id)
    showid=getshowdata.id
    venid=getshowdata.venue_id
    vndata=Venue.query.get(venid)
    getbook=Booking.query.all()
    vcp=vndata.capacity
    total=0
    for i in getbook:
        if i.show_id==showid:
            total=total+i.number
    maxcapacity=vcp-total

    # print(num)
    showoutput=[]
    show_data={}
    show_data['name']=getshowdata.name
    show_data['rating']=getshowdata.rating
    show_data['tag']=getshowdata.tag
    show_data['timing']=getshowdata.timing
    show_data['price']=getshowdata.price
    show_data['venue_id']=getshowdata.venue_id
    show_data["ven_name"]=vndata.name
    show_data["ven_capacity"]=maxcapacity
    showoutput.append(show_data)
  
    return jsonify({'data':showoutput})

# --------------------------Update for Admin------------------------------------------


@app.route('/updatevenu', methods=['POST'] )
def updateven(): 
        content={"mesage":"Success"}
        vend=Venue.query.get(request.json['id'])
        vend.name=request.json['name']
        vend.place=request.json['place']
        vend.location=request.json['location']
        vend.capacity=request.json['capacity']   
        db.session.commit()
        return content

@app.route('/updateshow', methods=['POST'] )
def updateshow(): 
        content={"mesage":"Success"}
        showd=Shows.query.get(request.json['id'])
        showd.name=request.json['name']
        showd.rating=request.json['rating']
        showd.tag=request.json['tag']
        showd.timing=request.json['timing']
        showd.price=request.json['price']    
        showd.venue_id=request.json['venid']  
        db.session.commit()
        return content

# ----------------------Get for User----------------------------------------------

@app.route('/getvenue',methods=['GET'])
#@cache.memoize(5)
@token_required
def getvenue(current_user):
    venue=Venue.query.all()
    output = []
    for i in venue:
        list_data = {}
        list_data['id'] = i.id
        list_data['name'] = i.name 
        list_data['place']=i.place
        list_data['location']=i.location
        list_data['capacity']=i.capacity
        output.append(list_data)
    return jsonify({'data' : output})   

@app.route('/getshows',methods=['GET'])
#@cache.memoize(5)
@token_required
def getshows(current_user):
        varray=[]
        shows=Shows.query.all()
        showoutput = []
        for i in shows:
            show_data = {}
            show_data['id'] = i.id
            show_data['name'] = i.name 
            show_data['rating']=i.rating
            show_data['tag']=i.tag
            show_data['timing']=i.timing
            show_data['price']=i.price
            show_data['venu']=i.venue_id
            showoutput.append(show_data)
        for i in shows:
             vdict={}
             vdict['venue']=i.venue_id
             varray.append(vdict)
        return jsonify({'data' : showoutput,'vd':varray}) 

@app.route('/getuser',methods=['GET'])
#@cache.memoize(5)
@token_required
def getuser(current_user):
    
    user=User_reg.query.get(current_user.id)
    useroutput = []
    user_data = {}
    user_data['id'] = user.id
    user_data['name'] = user.name 
    useroutput.append(user_data)
    return jsonify({'data' :useroutput})  

@app.route('/getbooking',methods=['GET'])
#@cache.memoize(5)
@token_required
def getbookings(current_user):
    bookingoutput = []
    varray=[]
    bookdata=Booking.query.all()
    for i in bookdata:
        if i.u_id==current_user.id:
            books={}
            
            showdata=Shows.query.get(i.show_id)
            books["id"]=showdata.id
            books["venue_id"]=showdata.venue_id
            books["showname"]=showdata.name
            books["timing"]=showdata.timing
            books["tag"]=showdata.tag
            if books in bookingoutput:
                print("Hello")
                continue
            else:
                print("delna")
                bookingoutput.append(books)

    content={'message':"Sucess"}
    return jsonify({'data' :bookingoutput}) 




@celery.task
def getprofilemail(current_user):
   userdata=User_reg.query.get(current_user.id)
   today = datetime.today()
   first_day_of_month = today.replace(day=1)
   next_month = today.replace(month=today.month + 1, day=1)
   last_day_of_month = next_month - timedelta(days=1)
   books = Booking.query.filter(Booking.booking_date.between(first_day_of_month, last_day_of_month)).all()
   emailmessage=render_template('monthlyreport.html',data=books)
   recipient = userdata.email
   subject = 'Subject of the email'
   message = Message(subject=subject, recipients=[recipient], html=emailmessage)

   try:
        mail.send(message)
        return jsonify({'message': 'Email sent successfully!'}), 200
   except Exception as e:
        return jsonify({'error': f'Error sending the email: {str(e)}'}), 500
    
# --------------------------Search for user--------------------------------------------
@app.route('/showtag/<string:tg>',methods=['GET'])
@token_required
def tagsearch(current_user,tg):
    #print(type(loc))
    varray=[]
    shows=Shows.query.all()
    showoutput = []
    for i in shows:
        if i.tag==tg:
            show_data = {}
            show_data['id'] = i.id
            show_data['name'] = i.name 
            show_data['rating']=i.rating
            show_data['tag']=i.tag
            show_data['timing']=i.timing
            show_data['price']=i.price
            show_data['venu']=i.venue_id
            showoutput.append(show_data)
    for i in shows:
             if i.tag==tg:
                vdict={}
                vdict['venue']=i.venue_id
                varray.append(vdict)
    return jsonify({'data' :showoutput,'vd':varray})   
     
@app.route('/showrating/<string:rate>',methods=['GET'])
@token_required
def ratingsearch(current_user,rate):
    #print(type(loc))
    varray=[]
    shows=Shows.query.all()
    showoutput = []
    for i in shows:
        if i.rating==rate:
            show_data = {}
            show_data['id'] = i.id
            show_data['name'] = i.name 
            show_data['rating']=i.rating
            show_data['tag']=i.tag
            show_data['timing']=i.timing
            show_data['price']=i.price
            show_data['venu']=i.venue_id
            showoutput.append(show_data)
    for i in shows:
             if i.rating==rate:
                vdict={}
                vdict['venue']=i.venue_id
                varray.append(vdict)
    return jsonify({'data' :showoutput,'vd':varray})  

@app.route('/showname/<string:nm>',methods=['GET'])
@token_required
def showname(current_user,nm):
    shows=Shows.query.all()
    varray=[]
    output=[]
    for i in shows:
        if i.name==nm:
            show_data={}
            show_data['id'] = i.id
            show_data['name'] = i.name 
            show_data['rating']=i.rating
            show_data['tag']=i.tag
            show_data['timing']=i.timing
            show_data['price']=i.price
            show_data['venu']=i.venue_id
            output.append(show_data)
    for i in shows:
            if i.name==nm:
                vdict={}
                vdict['venue']=i.venue_id
                varray.append(vdict)
    return jsonify({'data' :output,'vd':varray}) 

@app.route('/showtime/<string:tm>',methods=['GET'])
@token_required
def showtime(current_user,tm):
    varray=[]
    shows=Shows.query.all()
    output=[]
    for i in shows:
        if i.timing==tm:
            show_data={}
            show_data['id'] = i.id
            show_data['name'] = i.name 
            show_data['rating']=i.rating
            show_data['tag']=i.tag
            show_data['timing']=i.timing
            show_data['price']=i.price
            show_data['venu']=i.venue_id
            output.append(show_data)
    for i in shows:
            if i.timing==tm:
                vdict={}
                vdict['venue']=i.venue_id
                varray.append(vdict)
    return jsonify({'data' :output,'vd':varray}) 

@app.route('/venulocation/<string:loc>',methods=['GET'])
@token_required
def venuloc(current_user,loc):
    #print(type(loc))
    venue=Venue.query.all()
    output = []
    for i in venue:
        # print(type(i.location))
        if i.location==loc or i.place==loc:
         
            list_data = {}
            list_data['id'] = i.id
            list_data['name'] = i.name 
            list_data['place']=i.place
            list_data['location']=i.location
            list_data['capacity']=i.capacity
            output.append(list_data)
    return jsonify({'data' :output})  


    
            

# --------------------------Get with id for user------------------------------------------

@app.route('/getven/<int:id>',methods=['GET'])
@token_required
def getven(current_user,id):
    getvenudata=Venue.query.get(id)
    venuoutput = []
    ven_data = {}
    ven_data['name']=getvenudata.name
    ven_data['place']=getvenudata.place
    ven_data['location']=getvenudata.location
    ven_data['capacity']=getvenudata.capacity
    venuoutput.append(ven_data)
    return jsonify({'data':venuoutput})

@app.route('/getshow/<int:id>',methods=['GET'])
@token_required
def getshow(current_user,id):
    getshowdata=Shows.query.get(id)
    showid=getshowdata.id
    venid=getshowdata.venue_id
    vndata=Venue.query.get(venid)
    getbook=Booking.query.all()
    vcp=vndata.capacity
    total=0
    for i in getbook:
        if i.show_id==showid:
            total=total+i.number
    maxcapacity=vcp-total

    # print(num)
    showoutput=[]
    show_data={}
    show_data['name']=getshowdata.name
    show_data['rating']=getshowdata.rating
    show_data['tag']=getshowdata.tag
    show_data['timing']=getshowdata.timing
    show_data['price']=getshowdata.price
    show_data['venue_id']=getshowdata.venue_id
    show_data["ven_name"]=vndata.name
    show_data["ven_capacity"]=maxcapacity
    showoutput.append(show_data)
  
    return jsonify({'data':showoutput})


# -----------------------------Booking---------------------------------------
   
@app.route('/booking', methods=['POST'] )
@token_required
def booking(current_user):  
    date=datetime.now()
    booking=Booking(request.json['number'],request.json['show_id'],current_user.id,date)
    db.session.add(booking)
    db.session.commit()
    content={"message":"Booked"}
    return content

# ---------------------Summary--------------------------------
@app.route('/showlist/<int:id>',methods=['GET'])
# #@cache.memoize(5)
def getbooking(id):
    # print(id)
    varray=[]
    bookoutput=[]
    venue=Venue.query.get(id)
    vid=venue.id
    # print(vid)
    shows=Shows.query.all()
    booking=Booking.query.all()
    for i in shows:
        if i.venue_id==vid:
            count=0
            
            show_data = {}
            for j in booking:
                if i.id==j.show_id:
                    count=count+j.number
            show_data['show_name']=i.name
            show_data['tickets_sold']=count

            bookoutput.append(show_data)
    return jsonify({'data' :bookoutput,'vd':varray})  







@celery.task
def checklogin():
    #print("Hello Sir")
    #outputdata=[]
    datem=datetime.now()
    parray=[]
    emailarray=[]
    recipient=[]
    #userdata=User_reg.query.all()
    # logindata=logininfo.query.all()
    datas = logininfo.query.all()
    for i in datas:
        if i.date==datem:
            print("Hai")
        else:
            parray.append(i.userid)
    users = User_reg.query.filter(~User_reg.id.in_(parray)).all()
    emaildata=emailinfo.query.all()
    for l in emaildata:
        datem=datetime.now()
        if l.date==datem:
            continue
        else:
            emailarray.append(l.email)
    for k in users:
        if k.email in emailarray:
            continue
        else:
            recipient.append(k.email)
    subject = 'Do Check Out Our App'
    body = 'Plz Use Our Website'

    message = Message(subject=subject, recipients=recipient, body=body)
    for i in recipient:
        email=emailinfo(i,datem)
        db.session.add(email)
        db.session.commit()
    try:
        mail.send(message)
        
        return jsonify({"message": "Email sent successfully!"}), 200
    except Exception as e:
        return jsonify({"message": f"Error sending email: {str(e)}"}), 500
    #return jsonify({'data':outputdata})

with app.app_context():
    db.create_all()


if "__name__"=="__main__":
    app.run(debug=True)