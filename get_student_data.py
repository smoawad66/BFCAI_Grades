import requests
from bs4 import BeautifulSoup

def extract_viewstate_fields(soup):
    def val(name):
        el = soup.find('input', {'name': name})
        return el['value'] if el else ''
    return {
        '__VIEWSTATE': val('__VIEWSTATE'),
        '__EVENTVALIDATION': val('__EVENTVALIDATION'),
        '__VIEWSTATEGENERATOR': val('__VIEWSTATEGENERATOR'),
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__LASTFOCUS': ''
    }

def get_student_data(national_id, faculty_id=729):
    url = "https://mis.bu.edu.eg/benha_new/Registration/ED/help2.aspx"
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    session = requests.Session()
    
    get_resp = session.get(url, headers=headers)
    soup = BeautifulSoup(get_resp.text, 'html.parser')
    fields = extract_viewstate_fields(soup)

    fields.update({
        '__EVENTTARGET': 'ctl00$cntphmaster$drpAsFacultyInfoId',
        'ctl00$cntphmaster$drpAsFacultyInfoId': faculty_id,
    })

    faculty_change_resp = session.post(url, data=fields, headers=headers)
    soup = BeautifulSoup(faculty_change_resp.text, 'html.parser')

    fields = extract_viewstate_fields(soup)
    fields.update({
        'ctl00$cntphmaster$drpAsFacultyInfoId': faculty_id,
        'ctl00$cntphmaster$TextBox3': national_id,
        'ctl00$cntphmaster$Button2': 'بحث',
        'ctl00$cntphmaster$fac_desc': '',
        'ctl00$hidden_ed_scholastic': '0',
        'ctl00$stud_id': ''
    })

    final_post = session.post(url, data=fields, headers=headers)
    soup = BeautifulSoup(final_post.text, 'html.parser')

    error_span = soup.find('span', id='ctl00_lblmeetinferror')
    if error_span and error_span.text.strip():
        return {"error": error_span.text.strip()}

    table_div = soup.find('div', id='ctl00_cntphmaster_stud_data')
    if not table_div:
        print('Invalid NID!')
        return None

    table = table_div.find('table')
    if not table:
        return {"error": "No table inside the div"}

    result = {}

    for row in table.find_all('tr'):
        tds = row.find_all('td')
        if len(tds) < 2:
            continue

        value_td = tds[0]
        label_td = tds[1]

        label = label_td.get_text(strip=True)

        inputs = value_td.find_all('input')
        value = None
        for inp in inputs:
            if inp.get('type') != 'hidden' and inp.has_attr('value'):
                value = inp['value'].strip()
                break

        if not value:
            value = value_td.get_text(strip=True)

        if label and value:
            result[label] = value

    return result