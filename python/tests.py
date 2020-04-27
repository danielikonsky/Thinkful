from datetime import date
from app import app

def formatdate(rawdate):

    dateformat = ''
    dateformatlist = list (rawdate)

    for i in range(len(dateformatlist)):
        if i == 0 or i == 3:
            if dateformatlist[i] == '0':
                pass
            else:
                dateformat = dateformat + dateformatlist[i]
        else:
            dateformat = dateformat + dateformatlist[i]

    return (dateformat)

def test_today():
    with app.test_client() as cli:
        resp = cli.get('/today')
        assert resp.status_code == 200
        assert resp.json == {"today": "{}".format(formatdate(date.today().strftime("%m/%d/%Y")))}
