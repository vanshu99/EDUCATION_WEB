
from django.shortcuts import render ,redirect
from django.conf import settings
from django.http import HttpResponse

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from random import randint

    


def home(request):
	return render(request,'home.html')

def about(request):
    return render(request,'about.html')	

def contact(request):
    return render(request,'contact.html') 

def saveContact(request):
    name = request.GET.get("name")
    mail = request.GET.get("email")
    msg = request.GET.get("message")
    print(name,mail,msg)
    return HttpResponse("Yes !")          

def login(request):
    msg = ""
    err = request.GET.get("error")
    if err is not None:
        msg = "Invalid User !"

    return render(request,"login.html",{"msg":msg})  

def register(request):
    name = request.POST.get('name')
    email = request.POST.get('mail')
    password = request.POST.get('password')
    type = request.POST.get('type')
    branch = request.POST.get('branch')

    otp = sendMail(name,email)

    query = "insert into user(name,mail,password,type,branch,otp) value('{0}','{1}','{2}',{3},{4},{5})".format(name,email,password,type,branch,otp)

    cnn = settings.CONNECTION()

    cr = cnn.cursor()
    cr.execute(query)
    cnn.commit()
    cnn.close()
    
    return HttpResponse("Register User Success !")

def loginuser(request):
    email = request.POST.get('mail')
    password = request.POST.get('password')

    query = "select * from user where mail='{0}' and password='{1}'".format(email,password)

    cnn = settings.CONNECTION()
    cr = cnn.cursor()
    cr.execute(query)        
    
    record = cr.fetchone()
    print(">>>>>>  ",record)

    if record is None:
        msg = "Login Failed !"
        return redirect('/call/login?error=1')
    else:
        id = record[0]
        name = record[1]
        email = record[2]
        phone = record[3]
        branch = record[6]
        type = record[5] 
        
        isVerify = record[8] # 0
        if isVerify==0:
            return redirect('/call/verify') 
        else:  
             user = {"id":id,"name":name,"email":email,"phone":phone,"branch":branch,"type":type}
             request.session['userdata'] = user

             if type==1: # faculty
                 return redirect('/faculty/home')  
             else: # student
                 return redirect('/student/home')            


def verify(request):
    if request.method=="GET":
        return render(request,'verify.html')
    else:
        otp = request.POST.get('otp')       
        mail = request.POST.get('email')
        query = "update user set isVerify=1 where mail='{0}' and otp={1}".format(mail,otp)
        cnn = settings.CONNECTION()
        cr = cnn.cursor()
        cr.execute(query) 
        cnn.commit()       
        return redirect('/call/login')
            
    
def logout(request):
    del request.session['userdata']
    return redirect('/call/home')   



def sendMail(name,mail):
    otp = randomdigit(6)
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "OTP Verification "
    msg['From'] = 'justsample4mail@gmail.com'
    msg['To'] = "vanshidhankani99@gmail.com"
    
    html = """
        <html>        
          <body>
            <h1 style='color:red'>Email Confirmation</h1>
            <hr>
            <b>Welcome {0} , </b>
            <br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            Your Registeration is successfully done, please verify your email with this otp <b>{1}</b>.
            <br><br>
            Thanks
          </body>
        </html>
        """.format(name,otp)
    part2 = MIMEText(html, 'html')
    msg.attach(part2)


    fromaddr = 'justsample4mail@gmail.com'
    toaddrs  =  "vanshidhankani99@gmail.com"
    username = 'justsample4mail@gmail.com'
    password = 'sample@123'
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg.as_string())
    server.quit()
    return otp

def randomdigit(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)    
