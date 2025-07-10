import requests
from bs4 import BeautifulSoup
import urllib.parse


def login_and_get_subjects(stud_code, stud_nid, stud_name):
    login_url = "https://mis.bu.edu.eg/benha_new/Registration/ed_login.aspx"
    subjects_url = "https://mis.bu.edu.eg/benha_new/Registration/ED/OR_RecordStudentPrimarySubjectsCredit.aspx"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive'
    }

    session = requests.Session()
    session.cookies.clear()

    try:
        response = session.get(login_url, headers=headers, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        return {"error": f"Failed to access login page: {str(e)}"}

    soup = BeautifulSoup(response.text, 'html.parser')
    form_data = {
        '__VIEWSTATE': soup.find('input', {'name': '__VIEWSTATE'})['value'] if soup.find('input', {'name': '__VIEWSTATE'}) else '',
        '__VIEWSTATEGENERATOR': soup.find('input', {'name': '__VIEWSTATEGENERATOR'})['value'] if soup.find('input', {'name': '__VIEWSTATEGENERATOR'}) else '',
        '__EVENTVALIDATION': soup.find('input', {'name': '__EVENTVALIDATION'})['value'] if soup.find('input', {'name': '__EVENTVALIDATION'}) else '',
        '__PREVIOUSPAGE': soup.find('input', {'name': '__PREVIOUSPAGE'})['value'] if soup.find('input', {'name': '__PREVIOUSPAGE'}) else '',
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__LASTFOCUS': '',
        'ctl00$cntphmaster$txt_StudCode': stud_code,
        'ctl00$cntphmaster$txt_Nationalnum': stud_nid,
        'ctl00$cntphmaster$btn_Login': 'تسجيل دخول',
        'ctl00$hidden_ed_scholastic': '0',
        'ctl00$stud_id': ''
    }

    headers['Referer'] = login_url
    try:
        response = session.post(login_url, headers=headers, data=form_data, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        print('Login failed, invalid NID!')
        return None

    if 'OR_MAIN_PAGE.aspx?name=' in response.url:
        secret = urllib.parse.urlparse(response.url).query.split('name=')[1]
    else:
        print('Login failed, maybe the website is closed for login now!')
        return -1
    

    subjects_page_url = f"{subjects_url}?name={secret}"
    headers['Referer'] = response.url
    try:
        response = session.get(subjects_page_url, headers=headers, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        return {"error": f"Failed to access subjects page: {str(e)}"}


    soup = BeautifulSoup(response.text, 'html.parser')
    
    image_src = soup.find('img', id="ctl00_imgedstud").get('src')

    form_data = {
        'ctl00$ScriptManager1': 'ctl00$cntphmaster$panal1|ctl00$cntphmaster$GridDataCount_DropDownList',
        'ctl00$hidden_ed_scholastic': '0',
        'ctl00$cntphmaster$txtEdAcadYearYearIdHidden': soup.find('input', {'name': 'ctl00$cntphmaster$txtEdAcadYearYearIdHidden'})['value'] if soup.find('input', {'name': 'ctl00$cntphmaster$txtEdAcadYearYearIdHidden'}) else '58',
        'ctl00$cntphmaster$txtEdPhaseNodeIdHidden': soup.find('input', {'name': 'ctl00$cntphmaster$txtEdPhaseNodeIdHidden'})['value'] if soup.find('input', {'name': 'ctl00$cntphmaster$txtEdPhaseNodeIdHidden'}) else '2669',
        'ctl00$cntphmaster$txtAsNodeHidden': soup.find('input', {'name': 'ctl00$cntphmaster$txtAsNodeHidden'})['value'] if soup.find('input', {'name': 'ctl00$cntphmaster$txtAsNodeHidden'}) else '3687',
        'ctl00$cntphmaster$Txtstudid': soup.find('input', {'name': 'ctl00$cntphmaster$Txtstudid'})['value'] if soup.find('input', {'name': 'ctl00$cntphmaster$Txtstudid'}) else '402504',
        'ctl00$cntphmaster$txtSubjectCode': '',
        'ctl00$cntphmaster$txtSubjectDescrEn': '',
        'ctl00$cntphmaster$txtSubjectDescrAr': '',
        'ctl00$cntphmaster$drpPhaseNode': '',
        'ctl00$cntphmaster$TextBox2': '',
        'ctl00$cntphmaster$ddledPhaseNodeSemeter': '',
        'ctl00$cntphmaster$dropAsNodeId': '',
        'ctl00$cntphmaster$txtStudentSemester': '',
        'ctl00$cntphmaster$txtFirstPhaseNodeHidden': '',
        'ctl00$cntphmaster$TextBox1': '',
        'ctl00$cntphmaster$GridDataCount_DropDownList': '300',
        'ctl00$cntphmaster$txtEdStudScholasticHidden': '',
        'ctl00$cntphmaster$txtAsNodeIDHidden': soup.find('input', {'name': 'ctl00$cntphmaster$txtAsNodeIDHidden'})['value'] if soup.find('input', {'name': 'ctl00$cntphmaster$txtAsNodeIDHidden'}) else '3687',
        'ctl00$cntphmaster$txtEDSUBJECTID': '',
        'ctl00$cntphmaster$txtFacultyTransfereFrom': '',
        'ctl00$cntphmaster$txtCurrentFacultyTransfereTo': '',
        'ctl00$cntphmaster$txtEdPhaseNodeID': '',
        'ctl00$cntphmaster$txtAsNodeID': '',
        'ctl00$cntphmaster$txtedStudDiversionToAppId': '',
        'ctl00$cntphmaster$txtEdAcadYearID': '',
        'ctl00$cntphmaster$txtEdSubjectIDs': '',
        'ctl00$cntphmaster$HidEdStudScholasticId': soup.find('input', {'name': 'ctl00$cntphmaster$HidEdStudScholasticId'})['value'] if soup.find('input', {'name': 'ctl00$cntphmaster$HidEdStudScholasticId'}) else '3102066',
        'ctl00$stud_id': '',
        '__EVENTTARGET': 'ctl00$cntphmaster$GridDataCount_DropDownList',
        '__EVENTARGUMENT': '',
        '__LASTFOCUS': '',
        '__VIEWSTATE': soup.find('input', {'name': '__VIEWSTATE'})['value'] if soup.find('input', {'name': '__VIEWSTATE'}) else '',
        '__VIEWSTATEGENERATOR': soup.find('input', {'name': '__VIEWSTATEGENERATOR'})['value'] if soup.find('input', {'name': '__VIEWSTATEGENERATOR'}) else 'F587968A',
        '__SCROLLPOSITIONX': '0',
        '__SCROLLPOSITIONY': '0',
        '__PREVIOUSPAGE': soup.find('input', {'name': '__PREVIOUSPAGE'})['value'] if soup.find('input', {'name': '__PREVIOUSPAGE'}) else '',
        '__EVENTVALIDATION': soup.find('input', {'name': '__EVENTVALIDATION'})['value'] if soup.find('input', {'name': '__EVENTVALIDATION'}) else '',
        '__VIEWSTATEENCRYPTED': '',
        '__ASYNCPOST': 'true'
    }

    for input_tag in soup.find_all('input', {'type': 'hidden'}):
        name = input_tag.get('name')
        value = input_tag.get('value', '')
        if name and name not in form_data:
            form_data[name] = value

    table = soup.find('table', id='ctl00_cntphmaster_grdEdStudSubjectPhase')
    if table:
        for row in table.find_all('tr'):
            checkbox = row.find('input', {'type': 'checkbox'})
            if checkbox and checkbox.get('name'):
                form_data[checkbox['name']] = 'on'


    headers['Referer'] = subjects_page_url
    try:
        response = session.post(subjects_page_url, headers=headers, data=form_data, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        with open('error_response.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        return {"error": f"Failed to set GridDataCount to 300: {str(e)}"}


    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', id='ctl00_cntphmaster_grdEdSubject')
    if not table:
        return {"error": "Table with id 'ctl00_cntphmaster_grdEdSubject' not found"}

    file_path = f'html/{stud_name}.html'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(str(table))

    return file_path, image_src