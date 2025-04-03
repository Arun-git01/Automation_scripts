import pytest
import allure
import unittest
from code_file.testing.test import *
# from code_file.testing.testing_tests import Ocr_Remittance_api
# from code_file.testing.test import test_base64_jpeg_file
# from code_file.testing.test import test_base64_jpg_file
# from code_file.testing.test import test_base64_png_file


# def test_ocr_remittance():
#     # response = Ocr_Remittance_api()
#     api_response_1 = test_sanity_success_flow_pdf_url_DS1_T3115()
#     # print("Final response: ", api_response_1)
#     api_response_2 = test_sanity_img_file_upload_DS1_T3117()
#     # print("Final response: ", api_response_2)
#     api_response_3 = test_unauth_error_DS1_T3110()
#     # print("Final response: ", api_response_3)
#     api_response_4 = test_invalid_creds_DS1_T3113()
#     # print("Final response: ", api_response_4)
#     api_response_5 = test_sanity_success_flow_img_url_DS1_T3114()
#     # print("Final response: ", api_response_5)
#     api_response_6 = test_empty_value_clientRefId_DS1_T3119()
#     # print("Final response: ", api_response_6)
#     api_response_7 = test_empty_space_clientRefId_DS1_T3120()
#     # print("Final response: ", api_response_7)
#     api_response_8 = test_length_check_clientRefId_DS1_T3121()
#     # print("Final response: ", api_response_8)
#     api_response_9 = test_empty_value_img_key_DS1_T3123()
#     # print("Final response: ", api_response_9)
#     api_response_10 = test_empty_space_img_key_DS1_T3124()
#     # print("Final response: ", api_response_10)
#     api_response_11 = test_empty_value_pdf_key_DS1_T3125()
#     # print("Final response: ", api_response_11)
#     api_response_12 = test_empty_space_pdf_key_DS1_T3126()
#     # print("Final response: ", api_response_12)
#     api_response_13 = test_invalid_image_url_DS1_T3163()
#     # print("Final response: ", api_response_13)
#     api_response_14 = test_invalid_pdf_url_DS1_T3163()
#     # print("Final response: ", api_response_14)
#     api_response_15 = test_missing_client_ref_id_key_DS1_T3130()
#     # print("Final response: ", api_response_15)
#     api_response_16 = test_missing_inputImage_key_DS1_T3130()
#     # print("Final response: ", api_response_16)
#     api_response_17 = test_missing_pdf_key_DS1_T3130()
#     # print("Final response: ", api_response_17)
#     api_response_18 = test_multi_page_pdf_url_DS1_T3132()
#     # print("Final response: ", api_response_18)
#     api_response_19 = test_multi_page_pdf_upload_DS1_T3131()
#     # print("Final response: ", api_response_19)
#     api_response_20 = test_non_remi_img_upload_DS1_T3133()
#     # print("Final response: ", api_response_20)
#     api_response_21 = test_passing_both_inputImage_pdf_key_parameter_DS1_T3135()
#     # print("Final response: ", api_response_21)
#     api_response_22 = test_passing_both_inputImage_pdf_key_empty_DS1_T3136()
#     # print("Final response: ", api_response_22)
#     api_response_23 = test_pdf_key_value_inputImage_key_empty_DS1_T3137()
#     # print("Final response: ", api_response_23)
#     api_response_24 = test_inputImage_key_value_pdf_key_empty_DS1_T3138()
#     # print("Final response: ", api_response_24)
#     api_response_25 = test_with_pwd_pdf_url_DS1_T3139()
#     # print("Final response: ", api_response_25)
#     api_response_26 = test_pwd_pdf_upload_DS1_T3140()
#     # print("Final response: ", api_response_26)
#     api_response_27 = test_img_big_size_inputImage_DS1_T3142()
#     # print("Final response: ", api_response_27)
#     api_response_28 = test_non_remi_pdf_url_key_DS1_T3144()
#     # print("Final response: ", api_response_28)
#     api_response_29 = test_jpeg_file_inputImage_key_DS1_T3149()
#     # print("Final response: ", api_response_29)
#     api_response_30 = test_png_file_inputImage_key_DS1_T3147()
#     # print("Final response: ", api_response_30)
#     api_response_31 = test_bmp_file_inputImage_key_DS1_T3152()
#     # print("Final response: ", api_response_31)
#     api_response_32 = test_invalid_file_inputImage_key_DS1_T3163()
#     # print("Final response: ", api_response_32)
#     api_response_33 = test_s3_url_inputImage_key_DS1_T3159()
#     # print("Final response: ", api_response_33)
#     api_response_34 = test_s3_url_pdf_key_DS1_T3160()
#     # print("Final response: ", api_response_34)
#     api_response_35 = test_passing_timeout_url_DS1_T3162()
#     # print("Final response: ", api_response_35)


# def test_base64_jpeg_file():
#     response = test_jpeg_encode_img()
#     # api_response_36 = response.test_jpeg_encode_img()
#
#
# def test_base64_jpg_file():
#     response = test_jpg_encode_img()
#     # api_response_37 = response.test_jpg_encode_img()
#
#
# def test_base64_png_file():
#     response = test_png_encode_img()
#     # api_response_38 = response.test_png_encode_img()
