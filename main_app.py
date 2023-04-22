from flask import Flask,render_template,request
from datetime import datetime
import pandas as pd
import csv

weak = {'Monday':[],'Tuesday':[],'Wednesday':[],'Thursday':[],'Friday':[],'Saturday':[]}
Subjects={}

app = Flask(__name__,template_folder='template',static_folder='static')

def table(file):
    with open(file) as f:
        csv_data = list(csv.reader(f))
    return render_template("Status.html", csv=csv_data)

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/TimeTable',methods=['POST','GET'])
def timetable():
    if request.method=='POST':
        if 'submitHours' in request.form:
            global hours
            hours = int(request.form['hours'])
            print(hours)
            return render_template('Home1.html',hours=hours,weak=weak)
        
        if "submitlist" in request.form:
            for i in weak:
                for j in range(1,hours+1):
                    k = i+str(j)
                    sub = (request.form[k]).upper()
                    weak[i].append(sub)
                    Subjects[sub]=[0,0]
            Table = pd.DataFrame(weak,index=None)
            Table.to_csv("Test_Time_Table.csv")
            atnd = pd.DataFrame(Subjects,index=None)
            atnd.to_csv('Test_Total_Atnd.csv',index=False)
            hrs = {}
            hrs['Date']=['00-00-0000']
            hrs['Day']=['dddddd']
            for i in range(1,hours+1):
                hrs[i]=[0]
            sheet = pd.DataFrame(hrs,index=None)
            sheet.to_csv("Test_Sheet.csv",index=False)
            return table('Test_Time_Table.csv')
    return render_template('Home1.html')

@app.route('/Post',methods=['POST','GET'])
def post():
    global sublist
    global day
    global date
    if request.method=='POST':
        data = pd.read_csv("Test_Total_Atnd.csv",index_col=False)
        sheet = pd.read_csv("Test_Sheet.csv",index_col='Date')
        daily = []
        daily.append(day)
        for i in sublist:
            j=0
            if i in request.form:
                j=1
                data[i]+=1
            else:
                d=data[i]
                d[1]+=1
            daily.append(i+'-'+str(j))
        data.to_csv("Test_Total_Atnd.csv",index=None)
        sheet.loc[date]= daily
        sheet.to_csv("Test_Sheet.csv")
        sub = pd.read_csv("Test_Total_Atnd.csv",index_col=None)
        total = 0
        status = []
        for i in sub:
            d = sub[i]
            percent = (d[0]/d[1])*100
            status.append(i+'-'+str("%.2f"%percent)+'%')
            if str(percent).isnumeric:
                total += percent
        status.append('Total percentage - '+str("%.2f"%(total/16)))
        status = pd.DataFrame(status,index=None,columns=['Percentage'])
        status.to_csv("Test_status.csv")
        return render_template('Post.html',status='Attendance successfully posted for'+str(date))
    else:
        weak = pd.read_csv("Test_Time_Table.csv",index_col=False)
        sheet = pd.read_csv("Test_Sheet.csv",index_col='Date')
        d=str(datetime.date(datetime.now())).split('-')
        date = d[2]+'-'+d[1]+'-'+d[0]
        if date in sheet.index:
            return render_template('Post.html',status='Attendance already posted for'+str(date))
        else:
            days = list(weak.keys())
            day = days[(datetime.weekday(datetime.now())+1)]
            print(day)
            sublist = list(weak[day])
            print(sublist)
            return render_template('Post.html',weakday=day,sublist=sublist)
    return render_template('Post.html')


@app.route('/Status',methods=['POST','GET'])
def status():
    return render_template('Status.html')

@app.route('/tt',methods=['POST','GET'])
def TT():
    return table('Test_Time_Table.csv')

@app.route('/ta',methods=['POST','GET'])
def TA():
    return table('Test_Total_Atnd.csv')

@app.route('/h',methods=['POST','GET'])
def H():
    return table('Test_Sheet.csv')

@app.route('/s',methods=['POST','GET'])
def S():
    return table('Test_status.csv')


if __name__== '__main__' :
    app.run(debug=True,port=34)
