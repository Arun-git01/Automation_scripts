import requests
import configparser
import json
from code_file.testing.utils import connection_to_sql
from code_file.testing.test_jpeg_encode import test_jpeg_encode_img
from code_file.testing.test_png_encode import test_png_encode_img
from code_file.testing.test_jpg_encode import test_jpg_encode_img

config = configparser.ConfigParser()
config.read(r"C:\Users\Arunachalam\PycharmProjects\Pytest\.venv\config.ini")
url = config['config']['api_endpoint']
file_path = config['config']['file_path']
file_name = config['config']['file_name']
image_url = config['config']['image_url']
pdf_url = config['config']['pdf_url']
invalid_image_url = config['config']['invalid_image_url']
invalid_pdf_url = config['config']['invalid_pdf_url']
multi_page_pdf = config['config']['mulitple_page_pdf']
multi_page_file_path = config['config']['multi_page_file_path']
multi_page_file_name = config['config']['multi_page_file_name']
non_remittance_img = config['config']['non_remittance_img']
non_remi_file_path = config['config']['non_remi_file_path']
non_remi_file_name = config['config']['non_remi_file_name']
pwd_pdf = config['config']['pwd_pdf']
img_mb = config['config']['img_mb']
non_remi_pdf = config['config']['non_remi_pdf']
jpeg_url = config['config']['jpeg_url']
png_url = config['config']['png_url']
bmp_url = config['config']['bmp_url']
invalid_file = config['config']['invalid_file']
s3_url = config['config']['s3_url']
s3_url_pdf = config['config']['s3_url_pdf']
time_out_url = config['config']['timed_out_url']


# Sanity success flow response with pdf url
# TC-01
def test_sanity_success_flow_pdf_url_DS1_T3115():
    payload = {
        "clientRefId": "test@1",
        "pdf": pdf_url
    }
    response_json = requests.request(
        "POST",
        url,
        data=json.dumps(payload),
        headers={'accept': 'application/json',
                 'Content-Type': 'application/json',
                 'Authorization': 'Basic NzQwNTEzNjI1NjI1OjlDMG5VWDNoTlQwRDBKSEhPV0dtdU54aWhrSVJDR3lH'
                 })
    api_response_1 = response_json.json()
    req_id = api_response_1['ocrReqId']
    print("Test case: Sanity success flow response with pdf url")
    print("Input request payload:", payload)
    print("Output response: ", api_response_1)
    print("Client req id:", api_response_1['ocrReqId'])
    conn = connection_to_sql()
    cursor = conn.cursor()
    query = "SELECT * FROM ocr.ocr_remittance where ocr_id=%s order by id desc"
    cursor.execute(query, (req_id,))
    result = cursor.fetchall()
    print("DB output:", result)
    cursor.close()
    assert api_response_1['statusCode'] == 200
    assert api_response_1['status'] == 'success'
    assert api_response_1['clientRefId'] == 'test@1'
    assert api_response_1['ocrReqId'] == req_id
    assert api_response_1['result'][0]['payment_reference'] == '1852481'
    assert api_response_1['result'][0]['amount'] == '2,664.25'
    assert api_response_1['result'][0]['transfer_date'] == '29/01/2024'
    assert api_response_1['result'][0]['transfer_bank_name'] == 'kinabank'
    assert api_response_1['result'][0]['additional_reference'] == 'LRD ELECTRICAL PAY019964'
    assert api_response_1['result'][0]['to_account'] == '1000880939'
    assert api_response_1['result'][0]['recipient_name'] == 'NCSL CONTRIBUTION ACCOUNT'
    return


# Sanity for file upload success response
# TC-02
def test_sanity_img_file_upload_DS1_T3117():
    payload = {'clientRefId': 'test@2'}
    # file_path = file_path
    files = {
        'inputImage': (file_name, open(file_path, 'rb'), 'image/jpeg')
    }
    response_json = requests.request(
        "POST",
        url,
        data=payload,
        files=files,
        headers={
            'accept': 'application/json',
            'Authorization': 'Basic NzQwNTEzNjI1NjI1OjlDMG5VWDNoTlQwRDBKSEhPV0dtdU54aWhrSVJDR3lH'
        })
    api_response_2 = response_json.json()
    req_id = api_response_2['ocrReqId']
    print("Test case: Sanity for file upload success response")
    print("Input request payload:", payload, files)
    print("Output response: ", api_response_2)
    print("Client req id:", api_response_2['ocrReqId'])
    conn = connection_to_sql()
    cursor = conn.cursor()
    query = "SELECT * FROM ocr.ocr_remittance where ocr_id=%s order by id desc"
    cursor.execute(query, (req_id,))
    result = cursor.fetchall()
    print("Expected output:", result)
    cursor.close()
    assert api_response_2['statusCode'] == 200
    assert api_response_2['status'] == 'success'
    assert api_response_2['clientRefId'] == 'test@2'
    assert api_response_2['ocrReqId'] == req_id
    assert api_response_2['result'][0]['payment_reference'] == '2403101072688001'
    assert api_response_2['result'][0]['amount'] == '4,346.29'
    assert api_response_2['result'][0]['transfer_date'] == '31/01/2024'
    assert api_response_2['result'][0]['transfer_bank_name'] == 'BSP Financial Group Limited'
    assert api_response_2['result'][0]['additional_reference'] == 'NCSL NES CONTRIBUTIONS JANUARY 2024'
    assert api_response_2['result'][0]['to_account'] == '13391771'
    assert api_response_2['result'][0]['recipient_name'] == 'NCSL CONTRIBUTION ACCOUNT'
    return


# Unauthorised error response
# TC-03
def test_unauth_error_DS1_T3110():
    payload = {
        "clientRefId": "test@3",
        "pdf": pdf_url
    }
    response_json = requests.request(
        "POST",
        url, data=json.dumps(payload),
        headers={'accept': 'application/json', 'Content-Type': 'application/json'})
    api_response_3 = response_json.json()
    clientRefId = api_response_3['clientRefId']
    print("Test case: Unauthorised error response")
    print("Input request payload:", payload)
    print("Output response: ", api_response_3)
    conn = connection_to_sql()
    cursor = conn.cursor()
    query = "SELECT * FROM ocr.ocr_remittance where client_ref_id=%s order by id desc"
    cursor.execute(query, (clientRefId,))
    result = cursor.fetchall()
    print("DB output:", result)
    cursor.close()
    assert api_response_3['statusCode'] == 401
    assert api_response_3['status'] == 'failure'
    assert api_response_3['error'] == 'Unauthorized'
    return


# Unauthorised error response providing invalid creds
# TC-04
def test_invalid_creds_DS1_T3113():
    payload = {
        "clientRefId": "test@4",
        "pdf": pdf_url
    }
    response_json = requests.request(
        "POST",
        url, data=json.dumps(payload),
        headers={'accept': 'application/json',
                 'Content-Type': 'application/json',
                 'Authorization': 'Basic NzQwNTEzNjI1NjIsrdtfyvgubhinjomkcfyvgubhijnomk1OjlDMG5VWDNoTlQwRDBKSEhPV0dtdU54aWhrSVJDR3lH123'
                 })
    api_response_4 = response_json.json()
    clientRefId = api_response_4['clientRefId']
    print("Test case: Unauthorised error response providing invalid creds")
    print("Input request payload:", payload)
    print("Output response: ", api_response_4)
    conn = connection_to_sql()
    cursor = conn.cursor()
    query = "SELECT * FROM ocr.ocr_remittance where client_ref_id=%s order by id desc"
    cursor.execute(query, (clientRefId,))
    result = cursor.fetchall()
    print("DB Output:", result)
    cursor.close()
    assert api_response_4['statusCode'] == 401
    assert api_response_4['status'] == 'failure'
    assert api_response_4['clientRefId'] == 'test@4'
    assert api_response_4['error'] == 'Unauthorized'
    return


# Sanity for image url success response
# TC-05
def test_sanity_success_flow_img_url_DS1_T3114():
    payload = {
        "clientRefId": "test@5",
        "inputImage": image_url
    }
    response_json = requests.request(
        "POST",
        url, data=json.dumps(payload),
        headers={'accept': 'application/json',
                 'Content-Type': 'application/json',
                 'Authorization': 'Basic NzQwNTEzNjI1NjI1OjlDMG5VWDNoTlQwRDBKSEhPV0dtdU54aWhrSVJDR3lH'
                 })
    api_response_5 = response_json.json()
    req_id = api_response_5['ocrReqId']
    print("Test case: Sanity for image url success response")
    print("Input request payload:", payload)
    print("Output response: ", api_response_5)
    print("Client req id:", api_response_5['ocrReqId'])
    conn = connection_to_sql()
    cursor = conn.cursor()
    query = "SELECT * FROM ocr.ocr_remittance where ocr_id=%s order by id desc"
    cursor.execute(query, (req_id,))
    result = cursor.fetchall()
    print("Expected output:", result)
    cursor.close()
    assert api_response_5['statusCode'] == 200
    assert api_response_5['status'] == 'success'
    assert api_response_5['clientRefId'] == 'test@5'
    assert api_response_5['ocrReqId'] == req_id
    assert api_response_5['result'][0]['payment_reference'] == '126897385'
    assert api_response_5['result'][0]['amount'] == '11,713.15'
    assert api_response_5['result'][0]['transfer_date'] == '29/02/2024'
    assert api_response_5['result'][0]['transfer_bank_name'] == 'Westpac Banking Corporation'
    assert api_response_5['result'][0]['additional_reference'] == 'PPE05StaffContr'
    assert api_response_5['result'][0]['to_account'] is None
    assert api_response_5['result'][0]['recipient_name'] is None
    return


# Empty value in client ref id key
# TC-06
def test_empty_value_clientRefId_DS1_T3119():
    payload = {
        "clientRefId": "",
        "inputImage": image_url
    }
    response_json = requests.request(
        "POST",
        url, data=json.dumps(payload),
        headers={'accept': 'application/json',
                 'Content-Type': 'application/json',
                 'Authorization': 'Basic NzQwNTEzNjI1NjI1OjlDMG5VWDNoTlQwRDBKSEhPV0dtdU54aWhrSVJDR3lH'
                 })
    api_response_6 = response_json.json()
    print("Test case: Empty value in client ref id key")
    print("Input request payload:", payload)
    print("Output response: ", api_response_6)
    # conn = connection_to_sql()
    # cursor = conn.cursor()
    # query = "SELECT * FROM ocr.ocr_remittance order by id desc limit 1"
    # cursor.execute(query)
    # result = cursor.fetchall()
    # print("DB Output:", result)
    # cursor.close()
    assert api_response_6['statusCode'] == 400
    assert api_response_6['status'] == 'failure'
    assert api_response_6['error'] == 'Bad Request'
    return


# Empty space in client ref id key
# TC-07
def test_empty_space_clientRefId_DS1_T3120():
    payload = {
        "clientRefId": " ",
        "inputImage": image_url
    }
    response_json = requests.request(
        "POST",
        url,
        data=json.dumps(payload),
        headers={'accept': 'application/json',
                 'Content-Type': 'application/json',
                 'Authorization': 'Basic NzQwNTEzNjI1NjI1OjlDMG5VWDNoTlQwRDBKSEhPV0dtdU54aWhrSVJDR3lH'
                 })
    api_response_7 = response_json.json()
    print("Test case: Empty space in client ref id key")
    print("Input request payload:", payload)
    print("Output response: ", api_response_7)
    # conn = connection_to_sql()
    # cursor = conn.cursor()
    # query = "SELECT * FROM ocr.ocr_remittance order by id desc limit 1"
    # cursor.execute(query)
    # result = cursor.fetchall()
    # print("DB Output:", result)
    # cursor.close()
    assert api_response_7['statusCode'] == 400
    assert api_response_7['status'] == 'failure'
    assert api_response_7['error'] == 'Bad Request'
    return


# More length of character(45+) in client ref id key
# TC-08
def test_length_check_clientRefId_DS1_T3121():
    payload = {
        "clientRefId": "qwertyuiopasdfghjklzxcvbnmqwertyuiopqwertyuiop",
        "inputImage": image_url
    }
    response_json = requests.request(
        "POST",
        url,
        data=json.dumps(payload),
        headers={'accept': 'application/json',
                 'Content-Type': 'application/json',
                 'Authorization': 'Basic NzQwNTEzNjI1NjI1OjlDMG5VWDNoTlQwRDBKSEhPV0dtdU54aWhrSVJDR3lH'
                 })
    api_response_8 = response_json.json()
    print("Test case: More length of character(45+) in client ref id key")
    print("Input request payload:", payload)
    print("Output response: ", api_response_8)
    # conn = connection_to_sql()
    # cursor = conn.cursor()
    # query = "SELECT * FROM ocr.ocr_remittance where client_ref_id=%s"
    # cursor.execute(query, (clientRefId,))
    # result = cursor.fetchall()
    # print("DB Output:", result)
    # cursor.close()
    assert api_response_8['statusCode'] == 400
    assert api_response_8['status'] == 'failure'
    assert api_response_8['error'] == 'Bad Request'
    return


# Empty value in inputImage key
# TC-09
def test_empty_value_img_key_DS1_T3123():
    payload = {
        "clientRefId": "test@9",
        "inputImage": ""
    }
    response_json = requests.request(
        "POST",
        url,
        data=json.dumps(payload),
        headers={'accept': 'application/json',
                 'Content-Type': 'application/json',
                 'Authorization': 'Basic NzQwNTEzNjI1NjI1OjlDMG5VWDNoTlQwRDBKSEhPV0dtdU54aWhrSVJDR3lH'
                 })
    api_response_9 = response_json.json()
    clientRefId = api_response_9['clientRefId']
    print("Test case: Empty value in inputImage key")
    print("Input request payload:", payload)
    print("Output response: ", api_response_9)
    conn = connection_to_sql()
    cursor = conn.cursor()
    query = "SELECT * FROM ocr.ocr_remittance where client_ref_id=%s order by id desc"
    cursor.execute(query, (clientRefId,))
    result = cursor.fetchall()
    print("DB Output:", result)
    cursor.close()
    assert api_response_9['statusCode'] == 400
    assert api_response_9['status'] == 'failure'
    assert api_response_9['error'] == 'API call requires one input image'
    return


# Empty space in inputImage key
# TC-10
def test_empty_space_img_key_DS1_T3124():
    payload = {
        "clientRefId": "test@10",
        "inputImage": " "
    }
    response_json = requests.request(
        "POST",
        url,
        data=json.dumps(payload),
        headers={'accept': 'application/json',
                 'Content-Type': 'application/json',
                 'Authorization': 'Basic NzQwNTEzNjI1NjI1OjlDMG5VWDNoTlQwRDBKSEhPV0dtdU54aWhrSVJDR3lH'
                 })
    api_response_10 = response_json.json()
    req_id = api_response_10['ocrReqId']
    print("Test case: Empty space in inputImage key")
    print("Input request payload:", payload)
    print("Output response: ", api_response_10)
    conn = connection_to_sql()
    cursor = conn.cursor()
    query = "SELECT * FROM ocr.ocr_remittance where client_ref_id=%s order by id desc"
    cursor.execute(query, (req_id,))
    result = cursor.fetchall()
    print("DB Output:", result)
    cursor.close()
    assert api_response_10['statusCode'] == 400
    assert api_response_10['status'] == 'failure'
    assert api_response_10['ocrReqId'] == req_id
    assert api_response_10['error'] == 'Not a valid Image/PDF'
    return


# Empty value in pdf key
# TC-11
def test_empty_value_pdf_key_DS1_T3125():
    payload = {
        "clientRefId": "test@11",
        "pdf": ""
    }
    response_json = requests.request(
        "POST",
        url,
        data=json.dumps(payload),
        headers={'accept': 'application/json',
                 'Content-Type': 'application/json',
                 'Authorization': 'Basic NzQwNTEzNjI1NjI1OjlDMG5VWDNoTlQwRDBKSEhPV0dtdU54aWhrSVJDR3lH'
                 })
    api_response_11 = response_json.json()
    clientRefId = api_response_11['clientRefId']
    print("Test case: Empty value in pdf key")
    print("Input request payload:", payload)
    print("Output response: ", api_response_11)
    conn = connection_to_sql()
    cursor = conn.cursor()
    query = "SELECT * FROM ocr.ocr_remittance where client_ref_id=%s order by id desc"
    cursor.execute(query, (clientRefId,))
    result = cursor.fetchall()
    print("DB Output:", result)
    cursor.close()
    assert api_response_11['statusCode'] == 400
    assert api_response_11['status'] == 'failure'
    assert api_response_11['error'] == 'API call requires one input image'
    return


# Empty space in pdf key
# TC-12
def test_empty_space_pdf_key_DS1_T3126():
    payload = {
        "clientRefId": "test@12",
        "pdf": " "
    }
    response_json = requests.request(
        "POST",
        url,
        data=json.dumps(payload),
        headers={'accept': 'application/json',
                 'Content-Type': 'application/json',
                 'Authorization': 'Basic NzQwNTEzNjI1NjI1OjlDMG5VWDNoTlQwRDBKSEhPV0dtdU54aWhrSVJDR3lH'
                 })
    api_response_12 = response_json.json()
    req_id = api_response_12['ocrReqId']
    print("Test case: Empty space in pdf key")
    print("Input request payload:", payload)
    print("Output response: ", api_response_12)
    conn = connection_to_sql()
    cursor = conn.cursor()
    query = "SELECT * FROM ocr.ocr_remittance where client_ref_id=%s order by id desc"
    cursor.execute(query, (req_id,))
    result = cursor.fetchall()
    print("DB Output:", result)
    cursor.close()
    assert api_response_12['statusCode'] == 400
    assert api_response_12['status'] == 'failure'
    assert api_response_12['ocrReqId'] == req_id
    assert api_response_12['error'] == 'Not a valid Image/PDF'
    return


# Invalid url in inputImage key
# TC-13
def test_invalid_image_url_DS1_T3163():
    payload = {
        "clientRefId": "test@13",
        "inputImage": invalid_image_url
    }
    response_json = requests.request(
        "POST",
        url,
        data=json.dumps(payload),
        headers={'accept': 'application/json',
                 'Content-Type': 'application/json',
                 'Authorization': 'Basic NzQwNTEzNjI1NjI1OjlDMG5VWDNoTlQwRDBKSEhPV0dtdU54aWhrSVJDR3lH'
                 })
    api_response_13 = response_json.json()
    clientRefId = api_response_13['clientRefId']
    print("Test case: Invalid url in inputImage key")
    print("Input request payload:", payload)
    print("Output response: ", api_response_13)
    conn = connection_to_sql()
    cursor = conn.cursor()
    query = "SELECT * FROM ocr.ocr_remittance where client_ref_id=%s order by id desc"
    cursor.execute(query, (clientRefId,))
    result = cursor.fetchall()
    print("DB Output:", result)
    cursor.close()
    assert api_response_13['statusCode'] == 400
    assert api_response_13['status'] == 'failure'
    assert api_response_13['error'] == 'Not a valid Image/PDF'
    return


# Invalid url in pdf key
# TC-14
def test_invalid_pdf_url_DS1_T3163():
    payload = {
        "clientRefId": "test@14",
        "pdf": invalid_pdf_url
    }
    response_json = requests.request(
        "POST",
        url,
        data=json.dumps(payload),
        headers={'accept': 'application/json',
                 'Content-Type': 'application/json',
                 'Authorization': 'Basic NzQwNTEzNjI1NjI1OjlDMG5VWDNoTlQwRDBKSEhPV0dtdU54aWhrSVJDR3lH'
                 })
    api_response_14 = response_json.json()
    clientRefId = api_response_14['clientRefId']
    print("Test case: Invalid url in pdf key")
    print("Input request payload:", payload)
    print("Output response: ", api_response_14)
    conn = connection_to_sql()
    cursor = conn.cursor()
    query = "SELECT * FROM ocr.ocr_remittance where client_ref_id=%s order by id desc"
    cursor.execute(query, (clientRefId,))
    result = cursor.fetchall()
    print("DB Output:", result)
    cursor.close()
    assert api_response_14['statusCode'] == 400
    assert api_response_14['status'] == 'failure'
    assert api_response_14['error'] == 'Not a valid Image/PDF'
    return


# missing client ref id key
# TC-15
def test_missing_client_ref_id_key_DS1_T3130():
    payload = {
        "pdf": image_url
    }
    response_json = requests.request(
        "POST",
        url,
        data=json.dumps(payload),
        headers={'accept': 'application/json',
                 'Content-Type': 'application/json',
                 'Authorization': 'Basic NzQwNTEzNjI1NjI1OjlDMG5VWDNoTlQwRDBKSEhPV0dtdU54aWhrSVJDR3lH'
                 })
    api_response_15 = response_json.json()
    # clientRefId = api_response_15['clientRefId']
    print("Test case: missing client ref id key")
    print("Input request payload:", payload)
    print("Output response: ", api_response_15)
    # conn = connection_to_sql()
    # cursor = conn.cursor()
    # query = "SELECT * FROM ocr.ocr_remittance where client_ref_id=%s order by id desc"
    # cursor.execute(query, (clientRefId,))
    # result = cursor.fetchall()
    # print("DB Output:", result)
    # cursor.close()
    assert api_response_15['statusCode'] == 400
    assert api_response_15['status'] == 'failure'
    assert api_response_15['error'] == 'Bad Request'
    return


# missing inputImage key
# TC-16
def test_missing_inputImage_key_DS1_T3130():
    payload = {
        "clientRefId": "test@16"
    }
    response_json = requests.request(
        "POST",
        url,
        data=json.dumps(payload),
        headers={'accept': 'application/json',
                 'Content-Type': 'application/json',
                 'Authorization': 'Basic NzQwNTEzNjI1NjI1OjlDMG5VWDNoTlQwRDBKSEhPV0dtdU54aWhrSVJDR3lH'
                 })
    api_response_16 = response_json.json()
    clientRefId = api_response_16['clientRefId']
    print("Test case: missing inputImage key")
    print("Input request payload:", payload)
    print("Output response: ", api_response_16)
    conn = connection_to_sql()
    cursor = conn.cursor()
    query = "SELECT * FROM ocr.ocr_remittance where client_ref_id=%s order by id desc"
    cursor.execute(query, (clientRefId,))
    result = cursor.fetchall()
    print("DB Output:", result)
    cursor.close()
    assert api_response_16['statusCode'] == 400
    assert api_response_16['status'] == 'failure'
    assert api_response_16['error'] == 'API call requires one input image'
    return


# missing PDF key
# TC-17
def test_missing_pdf_key_DS1_T3130():
    payload = {
        "clientRefId": "test@17"
    }
    response_json = requests.request(
        "POST",
        url,
        data=json.dumps(payload),
        headers={'accept': 'application/json',
                 'Content-Type': 'application/json',
                 'Authorization': 'Basic NzQwNTEzNjI1NjI1OjlDMG5VWDNoTlQwRDBKSEhPV0dtdU54aWhrSVJDR3lH'
                 })
    api_response_17 = response_json.json()
    clientRefId = api_response_17['clientRefId']
    print("Test case: missing PDF key")
    print("Input request payload:", payload)
    print("Output response: ", api_response_17)
    conn = connection_to_sql()
    cursor = conn.cursor()
    query = "SELECT * FROM ocr.ocr_remittance where client_ref_id=%s order by id desc"
    cursor.execute(query, (clientRefId,))
    result = cursor.fetchall()
    print("DB Output:", result)
    cursor.close()
    assert api_response_17['statusCode'] == 400
    assert api_response_17['status'] == 'failure'
    assert api_response_17['error'] == 'API call requires one input image'
    return


# multiple page pdf url
# TC-18
def test_multi_page_pdf_url_DS1_T3132():
    payload = {
        "clientRefId": "test@18",
        "pdf": multi_page_pdf
    }
    response_json = requests.request(
        "POST",
        url,
        data=json.dumps(payload),
        headers={'accept': 'application/json',
                 'Content-Type': 'application/json',
                 'Authorization': 'Basic NzQwNTEzNjI1NjI1OjlDMG5VWDNoTlQwRDBKSEhPV0dtdU54aWhrSVJDR3lH'
                 })
    api_response_18 = response_json.json()
    clientRefId = api_response_18['clientRefId']
    print("Test case: multiple page pdf url")
    print("Input request payload:", payload)
    print("Output response: ", api_response_18)
    conn = connection_to_sql()
    cursor = conn.cursor()
    query = "SELECT * FROM ocr.ocr_remittance where client_ref_id=%s order by id desc"
    cursor.execute(query, (clientRefId,))
    result = cursor.fetchall()
    print("DB Output:", result)
    cursor.close()
    assert api_response_18['statusCode'] == 400
    assert api_response_18['status'] == 'failure'
    assert api_response_18['error'] == 'Multiple pages in PDF not supported'
    return


# multiple page pdf upload
# TC-19
def test_multi_page_pdf_upload_DS1_T3131():
    payload = {'clientRefId': 'test@19'}
    # file_path = multi_page_file_path
    files = {
        'pdf': (multi_page_file_name, open(file_path, 'rb'), 'application/pdf')
    }
    response_json = requests.request(
        "POST",
        url,
        data=payload,
        files=files,
        headers={'accept': 'application/json',
                 'Authorization': 'Basic NzQwNTEzNjI1NjI1OjlDMG5VWDNoTlQwRDBKSEhPV0dtdU54aWhrSVJDR3lH'
                 })
    api_response_19 = response_json.json()
    clientRefId = api_response_19['clientRefId']
    print("Test case: multiple page pdf upload")
    print("Input request payload:", payload, files)
    print("Output response: ", api_response_19)
    conn = connection_to_sql()
    cursor = conn.cursor()
    query = "SELECT * FROM ocr.ocr_remittance where client_ref_id=%s order by id desc"
    cursor.execute(query, (clientRefId,))
    result = cursor.fetchall()
    print("DB Output:", result)
    cursor.close()
    assert api_response_19['statusCode'] == 400
    assert api_response_19['status'] == 'failure'
    assert api_response_19['error'] == 'Multiple pages in PDF not supported'
    return


# Non remittance image upload
# TC-20
def test_non_remi_img_upload_DS1_T3133():
    payload = {'clientRefId': 'test@20'}
    # file_path = non_remi_file_path
    files = {
        'inputImage': (non_remi_file_name, open(file_path, 'rb'), 'image/jpeg')
    }
    response_json = requests.request(
        "POST",
        url,
        data=payload,
        files=files,
        headers={'accept': 'application/json',
                 'Authorization': 'Basic NzQwNTEzNjI1NjI1OjlDMG5VWDNoTlQwRDBKSEhPV0dtdU54aWhrSVJDR3lH'
                 })
    api_response_20 = response_json.json()
    clientRefId = api_response_20['clientRefId']
    print("Test case: Non remittance image upload")
    print("Input request payload:", payload, files)
    print("Output response: ", api_response_20)
    conn = connection_to_sql()
    cursor = conn.cursor()
    query = "SELECT * FROM ocr.ocr_remittance where client_ref_id=%s order by id desc"
    cursor.execute(query, (clientRefId,))
    result = cursor.fetchall()
    print("DB Output:", result)
    cursor.close()
    assert api_response_20['statusCode'] == 422
    assert api_response_20['status'] == 'failure'
    assert api_response_20['error'] == 'Error in Remittance OCR engine'
    return


# Two input key in payload
# TC-21
def test_passing_both_inputImage_pdf_key_parameter_DS1_T3135():
    payload = {
        "clientRefId": "test@21",
        "pdf": pdf_url,
        "inputImage": image_url
    }
    response_json = requests.request(
        "POST",
        url,
        data=json.dumps(payload),
        headers={'accept': 'application/json',
                 'Content-Type': 'application/json',
                 'Authorization': 'Basic NzQwNTEzNjI1NjI1OjlDMG5VWDNoTlQwRDBKSEhPV0dtdU54aWhrSVJDR3lH'
                 })
    api_response_21 = response_json.json()
    clientRefId = api_response_21['clientRefId']
    print("Test case: Two input key in payload")
    print("Input request payload:", payload)
    print("Output response: ", api_response_21)
    conn = connection_to_sql()
    cursor = conn.cursor()
    query = "SELECT * FROM ocr.ocr_remittance where client_ref_id=%s order by id desc"
    cursor.execute(query, (clientRefId,))
    result = cursor.fetchall()
    print("DB Output:", result)
    cursor.close()
    assert api_response_21['statusCode'] == 400
    assert api_response_21['status'] == 'failure'
    assert api_response_21['error'] == 'API call handles only one input image'
    return


# Two input key payload with both key empty value
# TC-22
def test_passing_both_inputImage_pdf_key_empty_DS1_T3136():
    payload = {
        "clientRefId": "test@22",
        "pdf": " ",
        "inputImage": " "
    }
    response_json = requests.request(
        "POST",
        url,
        data=payload,
        headers={'accept': 'application/json',
                 'Content-Type': 'application/json',
                 'Authorization': 'Basic NzQwNTEzNjI1NjI1OjlDMG5VWDNoTlQwRDBKSEhPV0dtdU54aWhrSVJDR3lH'
                 })
    api_response_22 = response_json.json()
    clientRefId = api_response_22['clientRefId']
    print("Test case: Two input key payload with both key empty value")
    print("Input request payload:", payload)
    print("Output response: ", api_response_22)
    conn = connection_to_sql()
    cursor = conn.cursor()
    query = "SELECT * FROM ocr.ocr_remittance where client_ref_id=%s order by id desc"
    cursor.execute(query, (clientRefId,))
    result = cursor.fetchall()
    print("DB Output:", result)
    cursor.close()
    assert api_response_22['statusCode'] == 400
    assert api_response_22['status'] == 'failure'
    assert api_response_22['error'] == 'API call handles only one input image'
    return


# Two input key payload with inputImage key empty value
# TC-23
def test_pdf_key_value_inputImage_key_empty_DS1_T3137():
    payload = {
        "clientRefId": "test@23",
        "pdf": pdf_url,
        "inputImage": " "
    }
    response_json = requests.request(
        "POST",
        url,
        data=payload,
        headers={'accept': 'application/json',
                 'Content-Type': 'application/json',
                 'Authorization': 'Basic NzQwNTEzNjI1NjI1OjlDMG5VWDNoTlQwRDBKSEhPV0dtdU54aWhrSVJDR3lH'
                 })
    api_response_23 = response_json.json()
    clientRefId = api_response_23['clientRefId']
    print("Test case: Two input key payload with inputImage key empty value")
    print("Input request payload:", payload)
    print("Output response: ", api_response_23)
    conn = connection_to_sql()
    cursor = conn.cursor()
    query = "SELECT * FROM ocr.ocr_remittance where client_ref_id=%s order by id desc"
    cursor.execute(query, (clientRefId,))
    result = cursor.fetchall()
    print("DB Output:", result)
    cursor.close()
    assert api_response_23['statusCode'] == 400
    assert api_response_23['status'] == 'failure'
    assert api_response_23['error'] == 'API call handles only one input image'
    return


# Two input key payload with PDF key empty value
# TC-24
def test_inputImage_key_value_pdf_key_empty_DS1_T3138():
    payload = {
        "clientRefId": "test@24",
        "pdf": "",
        "inputImage": image_url
    }
    response_json = requests.request(
        "POST",
        url,
        data=json.dumps(payload),
        headers={'accept': 'application/json',
                 'Content-Type': 'application/json',
                 'Authorization': 'Basic NzQwNTEzNjI1NjI1OjlDMG5VWDNoTlQwRDBKSEhPV0dtdU54aWhrSVJDR3lH'
                 })
    api_response_24 = response_json.json()
    clientRefId = api_response_24['clientRefId']
    print("Test case: Two input key payload with PDF key empty value")
    print("Input request payload:", payload)
    print("Output response: ", api_response_24)
    conn = connection_to_sql()
    cursor = conn.cursor()
    query = "SELECT * FROM ocr.ocr_remittance where client_ref_id=%s order by id desc"
    cursor.execute(query, (clientRefId,))
    result = cursor.fetchall()
    print("DB Output:", result)
    cursor.close()
    assert api_response_24['statusCode'] == 400
    assert api_response_24['status'] == 'failure'
    assert api_response_24['error'] == 'API call handles only one input image'
    return


# Pdf with password protected passed as url
# TC-25
def test_with_pwd_pdf_url_DS1_T3139():
    payload = {
        "clientRefId": "test@25",
        "pdf": pwd_pdf
    }
    response_json = requests.request(
        "POST",
        url,
        data=json.dumps(payload),
        headers={'accept': 'application/json',
                 'Content-Type': 'application/json',
                 'Authorization': 'Basic NzQwNTEzNjI1NjI1OjlDMG5VWDNoTlQwRDBKSEhPV0dtdU54aWhrSVJDR3lH'
                 })
    api_response_25 = response_json.json()
    clientRefId = api_response_25['clientRefId']
    print("Test case: Pdf with password protected passed as url")
    print("Input request payload:", payload)
    print("Output response: ", api_response_25)
    conn = connection_to_sql()
    cursor = conn.cursor()
    query = "SELECT * FROM ocr.ocr_remittance where client_ref_id=%s order by id desc"
    cursor.execute(query, (clientRefId,))
    result = cursor.fetchall()
    print("DB Output:", result)
    cursor.close()
    assert api_response_25['statusCode'] == 400
    assert api_response_25['status'] == 'failure'
    assert api_response_25['error'] == 'Not a valid Image/PDF'
    return


# Password-protected pdf upload
# TC-26
def test_pwd_pdf_upload_DS1_T3140():
    payload = {'clientRefId': 'test@26'}
    # file_path = multi_page_file_path
    files = {
        'inputImage': (multi_page_file_name, open(file_path, 'rb'), 'application/pdf')
    }
    response_json = requests.request("POST", url, data=payload, files=files, headers={'accept': 'application/json',
                                                                                      'Authorization': 'Basic NzQwNTEzNjI1NjI1OjlDMG5VWDNoTlQwRDBKSEhPV0dtdU54aWhrSVJDR3lH'
                                                                                      })
    api_response_26 = response_json.json()
    clientRefId = api_response_26['clientRefId']
    print("Test case: Password-protected pdf upload")
    print("Input request payload:", payload, files)
    print("Output response: ", api_response_26)
    conn = connection_to_sql()
    cursor = conn.cursor()
    query = "SELECT * FROM ocr.ocr_remittance where client_ref_id=%s order by id desc"
    cursor.execute(query, (clientRefId,))
    result = cursor.fetchall()
    print("DB Output:", result)
    cursor.close()
    assert api_response_26['statusCode'] == 400
    assert api_response_26['status'] == 'failure'
    assert api_response_26['error'] == 'Not a valid Image/PDF'
    return


# Image url more than 9mb
# TC-27
def test_img_big_size_inputImage_DS1_T3142():
    payload = {
        "clientRefId": "test@27",
        "inputImage": img_mb
    }
    response_json = requests.request(
        "POST",
        url,
        data=json.dumps(payload),
        headers={'accept': 'application/json',
                 'Content-Type': 'application/json',
                 'Authorization': 'Basic NzQwNTEzNjI1NjI1OjlDMG5VWDNoTlQwRDBKSEhPV0dtdU54aWhrSVJDR3lH'
                 })
    api_response_27 = response_json.json()
    clientRefId = api_response_27['clientRefId']
    print("Test case: Image url more than 9mb")
    print("Input request payload:", payload)
    print("Output response: ", api_response_27)
    conn = connection_to_sql()
    cursor = conn.cursor()
    query = "SELECT * FROM ocr.ocr_remittance where client_ref_id=%s order by id desc"
    cursor.execute(query, (clientRefId,))
    result = cursor.fetchall()
    print("DB Output:", result)
    cursor.close()
    assert api_response_27['statusCode'] == 413
    assert api_response_27['status'] == 'failure'
    assert api_response_27['error'] == 'Size exceeds limit'
    return


# Non remittance pdf
# TC-28
def test_non_remi_pdf_url_key_DS1_T3144():
    payload = {
        "clientRefId": "test@28",
        "pdf": non_remi_pdf
    }
    response_json = requests.request(
        "POST",
        url,
        data=payload,
        headers={'accept': 'application/json',
                 'Content-Type': 'application/json',
                 'Authorization': 'Basic NzQwNTEzNjI1NjI1OjlDMG5VWDNoTlQwRDBKSEhPV0dtdU54aWhrSVJDR3lH'
                 })
    api_response_28 = response_json.json()
    req_id = api_response_28['ocrReqId']
    print("Test case: Non remittance pdf")
    print("Input request payload:", payload)
    print("Output response: ", api_response_28)
    conn = connection_to_sql()
    cursor = conn.cursor()
    query = "SELECT * FROM ocr.ocr_remittance where ocr_id=%s"
    cursor.execute(query, (req_id,))
    result = cursor.fetchall()
    print("Expected output:", result)
    cursor.close()
    assert api_response_28['statusCode'] == 400
    assert api_response_28['status'] == 'failure'
    assert api_response_28['error'] == 'Not a valid Image/PDF'
    return


# JPEG file url in inputImage key
# TC-29
def test_jpeg_file_inputImage_key_DS1_T3149():
    payload = {
        "clientRefId": "test@29",
        "inputImage": jpeg_url
    }
    response_json = requests.request(
        "POST",
        url,
        data=json.dumps(payload),
        headers={'accept': 'application/json',
                 'Content-Type': 'application/json',
                 'Authorization': 'Basic NzQwNTEzNjI1NjI1OjlDMG5VWDNoTlQwRDBKSEhPV0dtdU54aWhrSVJDR3lH'
                 })
    api_response_29 = response_json.json()
    req_id = api_response_29['ocrReqId']
    print("Test case: JPEG file url in inputImage key")
    print("Input request payload:", payload)
    print("Client req id:", api_response_29['ocrReqId'])
    print("Output response: ", api_response_29)
    conn = connection_to_sql()
    cursor = conn.cursor()
    query = "SELECT * FROM ocr.ocr_remittance where ocr_id=%s"
    cursor.execute(query, (req_id,))
    result = cursor.fetchall()
    print("Expected output:", result)
    cursor.close()
    assert api_response_29['statusCode'] == 200
    assert api_response_29['status'] == 'success'
    assert api_response_29['clientRefId'] == 'test@29'
    assert api_response_29['ocrReqId'] == req_id
    assert api_response_29['result'][0]['payment_reference'] == '1868378'
    assert api_response_29['result'][0]['amount'] == '6,684.00'
    assert api_response_29['result'][0]['transfer_date'] == '06/02/2024'
    assert api_response_29['result'][0]['transfer_bank_name'] == 'kinabank'
    assert api_response_29['result'][0]['additional_reference'].replace("'",
                                                                        " ") == 'AFP -NCSL -Jan 24 -Employer No:018941'
    assert api_response_29['result'][0]['to_account'] == '20882217'
    assert api_response_29['result'][0]['recipient_name'] == 'NASFUND CONTRIBUTORS SAVINGS &'
    return


# PNG file url in inputImage key
# TC-30
def test_png_file_inputImage_key_DS1_T3147():
    payload = {
        "clientRefId": "test@30",
        "inputImage": png_url
    }
    response_json = requests.request(
        "POST",
        url,
        data=json.dumps(payload),
        headers={'accept': 'application/json',
                 'Content-Type': 'application/json',
                 'Authorization': 'Basic NzQwNTEzNjI1NjI1OjlDMG5VWDNoTlQwRDBKSEhPV0dtdU54aWhrSVJDR3lH'
                 })
    api_response_30 = response_json.json()
    req_id = api_response_30['ocrReqId']
    print("Test case: PNG file url in inputImage key")
    print("Input request payload:", payload)
    print("Client req id:", api_response_30['ocrReqId'])
    print("Output response: ", api_response_30)
    conn = connection_to_sql()
    cursor = conn.cursor()
    query = "SELECT * FROM ocr.ocr_remittance where ocr_id=%s"
    cursor.execute(query, (req_id,))
    result = cursor.fetchall()
    print("Expected output:", result)
    cursor.close()
    assert api_response_30['statusCode'] == 200
    assert api_response_30['status'] == 'success'
    assert api_response_30['clientRefId'] == 'test@30'
    assert api_response_30['ocrReqId'] == req_id
    assert api_response_30['result'][0]['payment_reference'] == '1868378'
    assert api_response_30['result'][0]['amount'] == '6,684.00'
    assert api_response_30['result'][0]['transfer_date'] == '06/02/2024'
    assert api_response_30['result'][0]['transfer_bank_name'] == 'kinabank'
    assert api_response_30['result'][0]['additional_reference'].replace("'",
                                                                        " ") == 'AFP -NCSL -Jan 24 -Employer No:018941'
    assert api_response_30['result'][0]['to_account'] == '20882217'
    assert api_response_30['result'][0]['recipient_name'] == 'NASFUND CONTRIBUTORS SAVINGS &'
    return


# BMP file url in inputImage key
# TC-31
def test_bmp_file_inputImage_key_DS1_T3152():
    payload = {
        "clientRefId": "test@123",
        "inputImage": bmp_url
    }
    response_json = requests.request(
        "POST",
        url,
        data=json.dumps(payload),
        headers={'accept': 'application/json',
                 'Content-Type': 'application/json',
                 'Authorization': 'Basic NzQwNTEzNjI1NjI1OjlDMG5VWDNoTlQwRDBKSEhPV0dtdU54aWhrSVJDR3lH'
                 })
    api_response_31 = response_json.json()
    print("The output 31 is: ", api_response_31)
    assert api_response_31['statusCode'] == 200
    assert api_response_31['status'] == 'success'
    assert api_response_31['clientRefId'] == 'test@123'
    assert api_response_31['result'][0]['payment_reference'] == '1868378'
    assert api_response_31['result'][0]['amount'] == '6,684.00'
    assert api_response_31['result'][0]['transfer_date'] == '06/02/2024'
    assert api_response_31['result'][0]['transfer_bank_name'] == 'kinabank'
    assert api_response_31['result'][0]['additional_reference'].replace("'",
                                                                        " ") == 'AFP -NCSL -Jan 24 -Employer No:018941'
    assert api_response_31['result'][0]['to_account'] == '20882217'
    assert api_response_31['result'][0]['recipient_name'] == 'NASFUND CONTRIBUTORS SAVINGS &'
    return


# Invalid file url in inputImage key
# TC-32
def test_invalid_file_inputImage_key_DS1_T3163():
    payload = {
        "clientRefId": "test@32",
        "inputImage": invalid_file
    }
    response_json = requests.request(
        "POST",
        url,
        data=json.dumps(payload),
        headers={'accept': 'application/json',
                 'Content-Type': 'application/json',
                 'Authorization': 'Basic NzQwNTEzNjI1NjI1OjlDMG5VWDNoTlQwRDBKSEhPV0dtdU54aWhrSVJDR3lH'
                 })
    api_response_32 = response_json.json()
    req_id = api_response_32['ocrReqId']
    print("Test case: Invalid file url in inputImage key")
    print("Input request payload:", payload)
    print("Output response: ", api_response_32)
    print("Client req id:", api_response_32['ocrReqId'])
    conn = connection_to_sql()
    cursor = conn.cursor()
    query = "SELECT * FROM ocr.ocr_remittance where ocr_id=%s"
    cursor.execute(query, (req_id,))
    result = cursor.fetchall()
    print("Expected output:", result)
    cursor.close()
    assert api_response_32['statusCode'] == 400
    assert api_response_32['status'] == 'failure'
    assert api_response_32['error'] == 'Not a valid Image/PDF'
    return


# S3 file url in inputImage key
# TC-33
def test_s3_url_inputImage_key_DS1_T3159():
    payload = {
        "clientRefId": "test@33",
        "inputImage": s3_url
    }
    response_json = requests.request(
        "POST",
        url,
        data=payload,
        headers={'accept': 'application/json',
                 'Content-Type': 'application/json',
                 'Authorization': 'Basic NzQwNTEzNjI1NjI1OjlDMG5VWDNoTlQwRDBKSEhPV0dtdU54aWhrSVJDR3lH'
                 })
    api_response_33 = response_json.json()
    clientRefId = api_response_33['clientRefId']
    print("Test case: S3 file url in inputImage key")
    print("Input request payload:", payload)
    print("Output response: ", api_response_33)
    conn = connection_to_sql()
    cursor = conn.cursor()
    query = "SELECT * FROM ocr.ocr_remittance where client_ref_id=%s order by id desc"
    cursor.execute(query, (clientRefId,))
    result = cursor.fetchall()
    print("DB Output:", result)
    cursor.close()
    assert api_response_33['statusCode'] == 400
    assert api_response_33['status'] == 'failure'
    assert api_response_33['error'] == 'Not a valid Image/PDF'
    return


# S3 file url in pdf key
# TC-34
def test_s3_url_pdf_key_DS1_T3160():
    payload = {
        "clientRefId": "test@34",
        "pdf": s3_url_pdf
    }
    response_json = requests.request(
        "POST",
        url,
        data=json.dumps(payload),
        headers={'accept': 'application/json',
                 'Content-Type': 'application/json',
                 'Authorization': 'Basic NzQwNTEzNjI1NjI1OjlDMG5VWDNoTlQwRDBKSEhPV0dtdU54aWhrSVJDR3lH'
                 })
    api_response_34 = response_json.json()
    clientRefId = api_response_34['clientRefId']
    print("Test case: S3 file url in pdf key")
    print("Input request payload:", payload)
    print("Output response: ", api_response_34)
    conn = connection_to_sql()
    cursor = conn.cursor()
    query = "SELECT * FROM ocr.ocr_remittance where client_ref_id=%s order by id desc"
    cursor.execute(query, (clientRefId,))
    result = cursor.fetchall()
    print("DB Output:", result)
    cursor.close()
    assert api_response_34['statusCode'] == 400
    assert api_response_34['status'] == 'failure'
    assert api_response_34['error'] == 'Not a valid Image/PDF'
    return


# Passing timeout url
# TC-35
def test_passing_timeout_url_DS1_T3162():
    payload = {
        "clientRefId": "test@35",
        "pdf": time_out_url
    }
    response_json = requests.request(
        "POST",
        url,
        data=json.dumps(payload),
        headers={'accept': 'application/json',
                 'Content-Type': 'application/json',
                 'Authorization': 'Basic NzQwNTEzNjI1NjI1OjlDMG5VWDNoTlQwRDBKSEhPV0dtdU54aWhrSVJDR3lH'
                 })
    api_response_35 = response_json.json()
    clientRefId = api_response_35['clientRefId']
    print("Test case: Passing timeout url")
    print("Input request payload:", payload)
    print("Output response: ", api_response_35)
    conn = connection_to_sql()
    cursor = conn.cursor()
    query = "SELECT * FROM ocr.ocr_remittance where client_ref_id=%s order by id desc"
    cursor.execute(query, (clientRefId,))
    result = cursor.fetchall()
    print("DB Output:", result)
    cursor.close()
    assert api_response_35['statusCode'] == 400
    assert api_response_35['status'] == 'failure'
    assert api_response_35['error'] == 'Not a valid Image/PDF'
    return


# def test_base64_jpeg_file():
#     response = test_jpeg_encode_img()
#     # api_response_36 = response.test_jpeg_encode_img()
#
#
# def test_base64_jpg_file():
#     response = test_jpg_encode_img()
#     # api_response_37 = response
#
#
# def test_base64_png_file():
#     response = test_png_encode_img()
#     # api_response_38 = response.test_png_encode_img()

# test.test_remittance_api()
# test.test_file_img()
# test.test_unauth_error()
# test.test_invalid_creds()
# test.test_success_flow()
# test.test_empty_value()
# test.test_empty_space()
# test.test_length_check()
# test.test_empty_value_img_key()
# test.test_empty_space_img_value()
# test.test_empty_value_pdf_key()
# test.test_empty_space_pdf_value()
# test.test_invalid_image_url()
# test.test_invalid_pdf_url()
# test.test_missing_client_ref_id()
# test.test_missing_client_image_key()
# test.test_missing_client_pdf_key()
# test.test_multi_page_pdf()
# test.test_multi_page_pdf_upload()
# test.test_non_remi_img_upload()
# test.test_both_parameter()
# test.test_both_parameter_empty()
# test.test_with_one_value_1()
# test.test_with_one_value()
# test.test_with_pwd_pdf()
# test.test_pwd_pdf_upload()
# test.test_img_big_size()
# test.test_non_remi_pdf()
# test.test_jpeg_file()
# test.test_png_file()
# test.test_bmp_file()
# test.test_invalid_file()
# test.test_s3_url()
# test.test_s3_url_pdf()
# test.test_timeout_url()
