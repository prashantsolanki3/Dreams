# from flask import Blueprint
from flask import *
from database import mongo, current_user
import math

account_api = Blueprint('account_api', __name__)
    
@account_api.route('/logout')
def logout():
    logout_user()
    current_user = None
    return redirect(url_for('index'))
   

@account_api.route('/registerfarmer', methods=['GET', 'POST'])
def registerfarmer():
    if request.method == 'GET':
        return render_template('registerfarmer.html')
    elif request.method == 'POST':
        username = request.form['txtUsername']
        name = request.form['txtName']
        password = request.form['txtPassword']
        age = request.form['txtAge']
        DOB = request.form['txtDOB']
        Location = request.form['txtLocation']
        collate = request.form['txtcollat']
        collatamt = request.form['txtcollamt']
        # TODO: Change this shit
        yield1 = float(request.form['txtyield1'])
        yield2 = float(request.form['txtyield2'])
        yield3 = float(request.form['txtyield3'])
        avg = 0.0
        
        creditscore = 0.0
        avg = float(((yield1+yield2+yield3)/3.0)/67.5)
        creditscore = float(avg+0.55)
        csflr = math.floor(creditscore)
        csciel = math.ceil(creditscore)
        if(csflr < 1):
        	flash('not eligible')
        	return redirect(url_for('account_api.registerfarmer'))
        csdec = creditscore%csflr
        if(csflr == 1):
            roi = 17.5 - (2.5 * csdec)
        if(csflr == 2):
            roi = 15 - (2.5 * csdec)
        if(csflr == 3):
            roi = 12.5 - (2.5 * csdec)
        if(csflr == 4):
            roi = 10 - (2.5 * csdec)
        if(csflr >= 5):
            roi = 7.5               
        
        db = mongo['db']
        test = db['testFarm']	
        login = mongo['db']['testLogin']
        for usr in test.find():
            if usr['_id'] == username:
                flash('The username {0} is already in use.  Please try a new username.'.format(username))
                return redirect(url_for('account_api.registerfarmer'))
        test.insert({'_id': username,'name':name,'age':age,'dob':DOB,'location':Location,'cred_cs':creditscore,'yield1':yield1,'yield2':yield2,'yield3':yield3,'pwd':password, 'roi':roi})
        login.insert({'_id': username,'pwd':password,'role':"farmer"}) 

        flash('You have registered the username {0}. Please login'.format(username))
        return redirect(url_for('account_api.login'))
    else:
        abort(405)

@account_api.route('/registerinvestor', methods=['GET', 'POST'])
def registerinvestor():
    if request.method == 'GET':
        return render_template('registerinvestor.html')
    elif request.method == 'POST':
        username = request.form['txtUsername']
        name = request.form['txtName']
        password = request.form['txtPassword']
        age = request.form['txtAge']
        DOB = request.form['txtDOB']
        Location = request.form['txtLocation']
        login = mongo['db']['testLogin']
        test = mongo['db']['testInv']
        for usr in test.find():
            if usr['_id'] == username:
                flash('The username {0} is already in use.  Please try a new username.'.format(username))
                return redirect(url_for('account_api.registerinvestor'))
        test.insert({'_id': username,'name':name,'age':age,'dob':DOB,'location':Location,'pwd':password})
        login.insert({'_id': username,'pwd':password,'role':"farmer"}) 
            
        flash('You have registered the username {0}. Please login'.format(username))
        return redirect(url_for('account_api.login'))
    else:
        abort(405)


@account_api.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', next=request.args.get('next'))
    elif request.method == 'POST':
        username = request.form['txtUsername']
        password = request.form['txtPassword']

        user = mongo['db']['testLogin']
        for usr in user.find():
            userName = usr['_id']
            pwd = usr['pwd']
            role = usr['role']
            ## add pages acordingly
            if(userName == username and pwd == password):
                if(role == 'farmer'):
                    usrname = usr['_id']

                    current_user = usr['_id']
                    flash('Welcome back farmer {0}'.format(username))
                    try:
                        #next = request.form['next']
                        return redirect(url_for('account_api.investor'))
                    except:
                        return redirect(url_for('index'))
                else:
                    flash('Welcome back investor {0}'.format(username))
                    try:
                        next = request.form['next']
                        return redirect(next)
                    except:
                        return redirect(url_for('index'))
        else:
            flash('Invalid login')
            return redirect(url_for('account_api.login'))
    else:
        return abort(405)