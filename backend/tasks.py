from flask import render_template,jsonify
from jinja2 import Template
import smtplib
from weasyprint import HTML
from celery import Celery
from application import application
from celery.schedules import crontab
from application import db,user,logtable,tracker

application.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/1'

celery = Celery(application.name , broker=application.config['CELERY_BROKER_URL'])
celery.conf.update(application.config)

celery.conf.beat_schedule = {
    'report_gen' : {
        'tasks' : 'application.tasks.report',
        'schedule': crontab(0,0,day_of_month=1)
    },
    'daily_reminder' : {
        'tasks' :'application.tasks.daily_reminder',
        'schedule' : crontab(minute=0, hour=0)
    }
}

@celery.task()
def report(id):
    with application.app_context():
        udata = user.query.filter_by(uid=id).first()
        tdata = tracker.query.filter_by(u_id=id).all()
        l1 =[]
        for i in tdata:
            tracker_id = i.tracker_id
            
            if(i.tracker_type == 'Numerical'):
                avgvalue = 0
                ldata = logtable.query.filter_by(user_id=id,t_id=tracker_id).all()
                for j in ldata:
                    avgvalue += int(j.value)
                avgvalue = avgvalue/len(ldata)
                l1.append([i.tracker_name,i.tracker_type,avgvalue])
            else:
                cnt = 0
                highest = ''
                d ={}
                ldata = logtable.query.filter_by(user_id=id,t_id=tracker_id).all()
                for j in ldata:
                    if j.value not in d.keys():
                        d[j.value] = 1
                    else:
                        d[j.value]+=1
                for j in d.items():
                    if(j[1]>cnt):
                        highest = j[0]
                        cnt = j[1]
                l1.append([i.tracker_name,i.tracker_type,highest])
        with 'report.html' as file_:
            template = Template(file_.read())
        message = render_template(template,udata=udata)
        html = HTML(string=message)
        file_name = udata.name + ".pdf"
        print(file_name)
        html.write_pdf(target=file_name)

#Configuring SMTP


@celery.task()
def daily_reminder():
    message = """From: From Team <quantified.self.v2@gmail.com>

    Subject: Daily reminder

    This is a daily reminder for you to log into your trackers
    """
    sender = 'quantified.self.v2@gmail.com'
    receivers =[]
    udata = user.query.all()
    for i in udata:
        receivers.append(i.mail)
    try:
        smtpObj = smtplib.SMTP('smtp.gmail.com')
        smtpObj.sendmail(sender, receivers, message)         
        return ("Successfully sent email")
    except:
        return ("Error: unable to send email")


