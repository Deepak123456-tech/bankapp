from flask import Flask,request,render_template,redirect,session,url_for

app=Flask(__name__)
app.secret_key='srinubabu@123'


#home route
@app.route('/')
def home():
    return render_template('home.html')

#username:password
accounts={
    1234:1234,
    1235:1235,
    1236:1236
}

amounts={
    1234:1000,
    1235:2000,
    1236:4000
}

#login route
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST': #check weather the request is post or not
        username=int(request.form['username'])#get from data in app
        password=int(request.form['password'])#get from data in app
        session['username']=username #storing username in seesion 
        #data validation
        if username in accounts:
            if accounts[username]==password:
                return redirect(url_for('dashboard'))
            else:
                return render_template("login.html",msg="flash msg:incorrect credentials")
        else:
            return render_template("login.html",msg="flash msg: account not found")
    
    return render_template("login.html")

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")
  
    

@app.route('/balance')
def balance():
    if 'username' not in session:
        return redirect(url_for('login'))
    account=session['username']
    return render_template("balance.html",amount=amounts[account])
   
    

@app.route('/deposite',methods=['GET','POST'])
def deposite():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method=='POST':
        account=session['username']
        deposite_amount=int(request.form['amount'])
        amounts[account]+=deposite_amount
        return render_template("deposite.html",msg=f"flash msg:{deposite_amount} deposited successfully and current balance is {amounts[account]}")
    return render_template("deposite.html")





@app.route('/withdraw',methods = ['GET','POST'])
def withdraw():
    if 'username' not  in session:
        return redirect(url_for('login'))
    if request.method=='POST':
        account=session['username']
        withdraw_amount=int(request.form['amount'])
        curr_amount=amounts[account]
        if curr_amount>=withdraw_amount:
            amounts[account]-=withdraw_amount
            return render_template("withdraw.html", msg=f"flash msg:{withdraw_amount} withdraws successfully andcurrent balance is {curr_amount-withdraw_amount}"              )
        else:
            return render_template("withdraw.html",msg="flash MSG:insufficient balance")

    return render_template("withdraw.html")



@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        sender = session['username']
        receiver = int(request.form['recieiveraccount'])
        transfer_amount = int(request.form['amount'])

        # check receiver exists
        if receiver not in accounts:
            return render_template("transfer.html", msg="Flash msg: Receiver account not found")

        # check sufficient balance
        if amounts[sender] < transfer_amount:
            return render_template("transfer.html", msg="Flash msg: Insufficient balance")

        # perform transfer
        amounts[sender] -= transfer_amount
        amounts[receiver] += transfer_amount

        return render_template(
            "transfer.html",
            msg=f"Flash msg: {transfer_amount} transferred successfully to account {receiver}"
        )

    return render_template("transfer.html")

    
@app.route("/ministatement")
def ministatement():
    return "ministatement page underdevelopment process....."

@app.route("/logout")
def logout():
    session.pop('username')
    if 'username' not in session:
        return redirect(url_for('login'))    
   

#main
if __name__=='__main__':
    app.run(debug=True,port=5001)
    


