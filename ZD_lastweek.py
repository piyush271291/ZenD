import urllib2, json
import datetime, time
import re
from datetime import timedelta


def generate_date():
    today = datetime.datetime.utcnow()
    print (today)
    idx = (today.weekday() + 1) % 7
    # print idx
    this_sun=today - datetime.timedelta(7 + idx)
    this_sun_time=datetime.datetime.strftime(this_sun,'%Y-%m-%dT18:30:00Z')
    last_sun = today - datetime.timedelta(7 + idx - 7)
    last_sun_time = datetime.datetime.strftime(last_sun,'%Y-%m-%dT18:30:00Z')
    return (this_sun_time,last_sun_time)
# print(lastweek_date)



def alltickets_lastweek():
    count = 0
    lastSun, thisSun = generate_date()
    r = search_query(lastSun, thisSun)

    for i in r["results"]:
        #      for tag in i["tags"]:
        #            for tag in i["tags"] :
        #                if re.search("actionable_alert", tag) :
        ticket_id = i["id"]
        created_at = i["created_at"]
        print (str(ticket_id) + "  " + created_at)
        count += 1
    print count


def whistletickets():
    count = 0
    lastSun, thisSun = generate_date()
    r = search_query(lastSun, thisSun)

    for i in r["results"]:
        if re.search("api", i["via"]["channel"]):
            ticket_id = i["id"]
            created_at = i["created_at"]
            print (str(ticket_id) + "  " + created_at)
            count += 1
    print count


def customertickets():
    count = 0
    lastSun, thisSun = generate_date()
    r = search_query(lastSun, thisSun)

    for i in r["results"]:
        if not re.search("api", i["via"]["channel"]):
            ticket_id = i["id"]
            created_at = i["created_at"]
            print (str(ticket_id) + "  " + created_at)
            count += 1
    print count


def search_query(last_sun_time,this_sun_time):
    print last_sun_time
    print this_sun_time
    Q = "created>"+last_sun_time+"%20created<"+this_sun_time+"+type%3Aticket&sort_by=created_at"
   #Q1 = 'created>192hours'
    url = 'https://platform9.zendesk.com/api/v2/search.json?query=%s' % Q
    print url
    req = urllib2.Request(url)
    req.add_header("Authorization", "Basic cGl5dXNoQHBsYXRmb3JtOS5jb206c0cjMmY3cm0=")

    response = urllib2.urlopen(req)
    return (json.load(response))


def false_recovered_alerts():
    count = 0
    lastSun, thisSun = generate_date()
    r = search_query(lastSun, thisSun)

    for i in r["results"]:
        if re.search("api", i["via"]["channel"]):
            for tags in i["tags"]:
                # print tags
                if tags == "false_alarm" or tags == "recovered":
                    ticket_id = i["id"]
                    created_at = i["created_at"]
                    print (str(ticket_id) + "  " + created_at)
                    count += 1


def Incident_tickets():
    count = 0
    lastSun, thisSun = generate_date()
    r = search_query(lastSun,thisSun)
    for i in r["results"]:
        if not re.search("api", i["via"]["channel"]):
            for tags in i["tags"]:
                if tags == "incident_mgmt":
                    ticket_id = i["id"]
                    created_at = i["created_at"]
                    print (str(ticket_id) + "  " + created_at)
                    count += 1
    print count


def Solved_tickets():
    count = 0
    Q = "solved<24hours+type%3Aticket"
    print(Q)

    #url = 'https://platform9.zendesk.com/api/v2/search.json?query=%s' % Q
    url = 'https://platform9.zendesk.com/api/v1/stats/summation/account/0/ticket_stats_by_account/solve_count?start=1552847400&end=1553452200&interval=8640'
    req = urllib2.Request(url)
    req.add_header("Authorization", "Basic cGl5dXNoQHBsYXRmb3JtOS5jb206c0cjMmY3cm0=")

    response = urllib2.urlopen(req)
    r = json.load(response)
    for i in r["results"]:
        ticket_id = i["id"]
        created_at = i["created_at"]
        print (str(ticket_id) + "  " + created_at)
        count += 1
    print count


# tickets_hours()
#Incident_tickets()

alltickets_lastweek()
false_recovered_alerts()
customertickets()
whistletickets()

