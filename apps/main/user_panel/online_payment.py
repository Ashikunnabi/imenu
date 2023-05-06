import codecs
import decimal
import json
import logging
import os
import sys
import time
import requests
from decimal import *
from django.conf import settings as django_settings
from authorizenet import apicontractsv1
from authorizenet.apicontrollers import *

success_logger = logging.getLogger('success_logger')
warning_logger = logging.getLogger('warning_logger')


class Auth:

    def __init__(self):
        self._username = django_settings.AUTHORIZE_USERNAME
        self._token = django_settings.AUTHORIZE_TOKEN

    def authorize(self):
        """ Check given credentials is valid or not """
        data = """
            {
                "authenticateTestRequest": {
                    "merchantAuthentication": {
                        "name": "",
                        "transactionKey": ""
                    }
                }
            }
        """
        data = json.loads(data)
        data['authenticateTestRequest']['merchantAuthentication']['name'] = self._username
        data['authenticateTestRequest']['merchantAuthentication']['transactionKey'] = self._token
        res = requests.post(
            django_settings.AUTHORIZE_URL,
            data=json.dumps(data)
        )
        decoded_data = codecs.decode(res.text.encode(), 'utf-8-sig')
        response = json.loads(decoded_data)
        success_logger.info(response)

        if response['messages']['resultCode'] == "Error":
            return None
        else:
            # Create a merchantAuthenticationType object with authentication details
            merchantAuth = apicontractsv1.merchantAuthenticationType()
            merchantAuth.name = self._username
            merchantAuth.transactionKey = self._token
            return merchantAuth


class OnlinePayment:

    def __init__(self):
        self.auth = Auth().authorize()

    def create_an_accept_payment_transaction(self, data: dict):
        # check given credentials are valid or not
        if self.auth is None:
            # store request data in log
            success_logger.info(
                'ORDER_PAYMENT_AUTH - Authentication failed.'
                ' Invalid username or token'
            )

            return {
                'status': 400,
                'details': 'Authentication failed. Invalid username or token'
            }
        try:
            request_data = {
                'auth_status': 200,
                'refId': "ref-1120-{}".format(time.time())[:20],
                'dataDescriptor': data['dataDescriptor'],
                'dataValue': data['dataValue'],
                'invoiceNumber': "140" + data['id'],
                'description': '',
                'firstName': data['user_details']['name'],
                'lastName': '',
                'company': data['user_details']['company_name'],
                'address': data['billing_address'],
                'city': data['billing_city'],
                'state': data['billing_state'],
                'zip': data['billing_postal_code'],
                'country': '',
                'customer_type': 'individual',
                'customer_id': data['user_details']['uuid'],
                'customer_email': data['user_details']['email'],
                'transactionType': 'authCaptureTransaction',
                'amount': data['total_price'],
            }

            # Create a merchantAuthenticationType object with authentication details
            merchantAuth = self.auth

            # Set the transaction's refId
            refId = request_data['refId']

            # Create the payment object for a payment nonce
            opaqueData = apicontractsv1.opaqueDataType()
            opaqueData.dataDescriptor = request_data['dataDescriptor']
            opaqueData.dataValue = request_data['dataValue']

            # Add the payment data to a paymentType object
            paymentOne = apicontractsv1.paymentType()
            paymentOne.opaqueData = opaqueData

            # Create order information
            order = apicontractsv1.orderType()
            order.invoiceNumber = request_data['invoiceNumber']
            order.description = request_data['description']

            # Set the customer's Bill To address
            customerAddress = apicontractsv1.customerAddressType()
            customerAddress.firstName = request_data['firstName']
            customerAddress.lastName = request_data['lastName']
            customerAddress.company = request_data['company']
            customerAddress.address = request_data['address']
            customerAddress.city = request_data['city']
            customerAddress.state = request_data['state']
            customerAddress.zip = request_data['zip']
            customerAddress.country = request_data['country']

            # Set the customer's identifying information
            customerData = apicontractsv1.customerDataType()
            customerData.type = request_data['customer_type']
            customerData.id = request_data['customer_id']
            customerData.email = request_data['customer_email']

            # Add values for transaction settings
            duplicateWindowSetting = apicontractsv1.settingType()
            duplicateWindowSetting.settingName = "duplicateWindow"
            duplicateWindowSetting.settingValue = "600"
            settings = apicontractsv1.ArrayOfSetting()
            settings.setting.append(duplicateWindowSetting)

            # Create a transactionRequestType object and add the previous objects to it
            transactionrequest = apicontractsv1.transactionRequestType()
            transactionrequest.transactionType = request_data['transactionType']
            transactionrequest.amount = decimal.Decimal(str(request_data['amount']))
            transactionrequest.order = order
            transactionrequest.payment = paymentOne
            transactionrequest.billTo = customerAddress
            transactionrequest.customer = customerData
            transactionrequest.transactionSettings = settings

            # Assemble the complete transaction request
            createtransactionrequest = apicontractsv1.createTransactionRequest()
            createtransactionrequest.merchantAuthentication = merchantAuth
            createtransactionrequest.refId = refId
            createtransactionrequest.transactionRequest = transactionrequest

            # Create the controller and get response
            createtransactioncontroller = createTransactionController(
                createtransactionrequest
            )
            if django_settings.AUTHORIZE_PRODUCTION:
                createtransactioncontroller.setenvironment(django_settings.AUTHORIZE_URL)

            # store request data in log
            success_logger.info(
                {f'ORDER_PAYMENT_REQUEST_DATA - {request_data["invoiceNumber"]}': request_data}
            )

            # send payment request to Authorized.net
            createtransactioncontroller.execute()

            response = createtransactioncontroller.getresponse()

            if response is not None:
                # Check to see if the API request was successfully received and acted upon
                if response.messages.resultCode == "Ok":
                    # Since the API request was successful, look for a transaction response
                    # and parse it to display the results of authorizing the card
                    if hasattr(response.transactionResponse, 'messages') == True:
                        response_data = {
                            'refId': str(response.refId),
                            'messages': {
                                'resultCode': str(response.messages.resultCode),
                                'message': {
                                    'code': str(response.messages.message.code),
                                    'text': str(response.messages.message.text),
                                }
                            },
                            'transactionResponse': {
                                'responseCode': str(response.transactionResponse.responseCode),
                                'authCode': str(response.transactionResponse.authCode),
                                'avsResultCode': str(response.transactionResponse.avsResultCode),
                                'cvvResultCode': str(response.transactionResponse.cvvResultCode),
                                'cavvResultCode': str(response.transactionResponse.cavvResultCode),
                                'transId': str(response.transactionResponse.transId),
                                'refTransID': str(response.transactionResponse.refTransID),
                                'transHash': str(response.transactionResponse.transHash),
                                'accountNumber': str(response.transactionResponse.accountNumber),
                                'accountType': str(response.transactionResponse.accountType),
                                "messages": [
                                    {
                                        "code": str(response.transactionResponse.messages.message[0].code),
                                        "description": str(response.transactionResponse.messages.message[0].description)
                                    }
                                ],
                                "transHashSha2": str(response.transactionResponse.transHashSha2)
                            }
                        }
                        success_logger.info(
                            {f'ORDER_PAYMENT_RESPONSE_DATA - {request_data["invoiceNumber"]}': response_data}
                        )
                    else:
                        response_data = {
                            'custom_text': 'Failed Transaction'
                        }
                        if hasattr(response.transactionResponse, 'errors') == True:
                            response_data['errorCode'] = str(
                                response.transactionResponse.errors.error[0].errorCode
                            )
                            response_data['errorMessage'] = response.transactionResponse.errors.error[0].errorText

                        success_logger.error(
                            {f'ORDER_PAYMENT_RESPONSE_DATA - {request_data["invoiceNumber"]}': response_data}
                        )
                        return {'status': 400, 'details': response_data}
                # Or, print errors if the API request wasn't successful
                else:
                    response_data = {
                        'custom_text': 'Failed Transaction'
                    }
                    if hasattr(response, 'transactionResponse') == True \
                            and hasattr(response.transactionResponse, 'errors') == True:
                        response_data['errorCode'] = str(
                            response.transactionResponse.errors.error[0].errorCode
                        )
                        response_data['errorMessage'] = response.transactionResponse.errors.error[0].errorText
                    else:
                        response_data['errorCode'] = response.messages.message[0]['code'].text
                        response_data['errorMessage'] = response.messages.message[0]['text'].text

                    success_logger.error(
                        {f'ORDER_PAYMENT_RESPONSE_DATA - {request_data["invoiceNumber"]}': response_data}
                    )
                    return {'status': 400, 'details': response_data}
            else:
                response_data = {}
                success_logger.error(
                    {f'ORDER_PAYMENT_RESPONSE_DATA - {request_data["invoiceNumber"]}': 'Null Response.'}
                )
                return {'status': 400, 'data': response_data}
            return {'status': 200, 'data': response_data}
        except Exception as ex:
            success_logger.error(
                {f'ORDER_PAYMENT_RESPONSE_DATA - {"140" + data["id"]}': ex.__str__()}
            )
            return {'status': 400, 'details': ex.__str__()}

    def void_transaction(self, refTransId):
        # check given credentials are valid or not
        if self.auth is None:
            # store request data in log
            success_logger.info(
                'ORDER_PAYMENT_AUTH - Authentication failed.'
                ' Invalid username or token'
            )

            return {
                'status': 400,
                'details': 'Authentication failed. Invalid username or token'
            }
        try:
            transactionrequest = apicontractsv1.transactionRequestType()
            transactionrequest.transactionType = "voidTransaction"
            # set refTransId to transId of an unsettled transaction
            transactionrequest.refTransId = refTransId

            # Create a merchantAuthenticationType object with authentication
            # details
            merchantAuth = self.auth

            createtransactionrequest = apicontractsv1.createTransactionRequest()
            createtransactionrequest.merchantAuthentication = merchantAuth
            createtransactionrequest.refId = "ref-1120-{}".format(time.time())[:20]

            createtransactionrequest.transactionRequest = transactionrequest
            createtransactioncontroller = createTransactionController(createtransactionrequest)
            if django_settings.AUTHORIZE_PRODUCTION:
                createtransactioncontroller.setenvironment(django_settings.AUTHORIZE_URL)
            raise
            # store request data in log
            request_data = {
                'rfid': createtransactionrequest.refId,
                'transaction_id': refTransId
            }
            success_logger.info(
                {f'ORDER_PAYMENT_VOID_REQUEST_DATA - {request_data["transaction_id"]}': request_data}
            )
            createtransactioncontroller.execute()

            response = createtransactioncontroller.getresponse()

            if response is not None:
                if response.messages.resultCode == "Ok":
                    if hasattr(response.transactionResponse, 'messages') == True:
                        response_data = {
                            'transactionResponse': {
                                'responseCode': str(response.transactionResponse.responseCode),
                                'transId': str(response.transactionResponse.transId),
                                "messages": [
                                    {
                                        "code": str(response.transactionResponse.messages.message[0].code),
                                        "description": str(response.transactionResponse.messages.message[0].description)
                                    }
                                ]
                            }
                        }
                        success_logger.info(
                            {f'ORDER_PAYMENT_VOID_REQUEST_DATA - {request_data["transaction_id"]}': response_data}
                        )
                    else:
                        response_data = {
                            'custom_text': 'Failed Void Transaction'
                        }
                        if hasattr(response.transactionResponse, 'errors') == True:
                            response_data['errorCode'] = str(
                                response.transactionResponse.errors.error[0].errorCode
                            )
                            response_data['errorMessage'] = response.transactionResponse.errors.error[0].errorText

                        success_logger.error(
                            {f'ORDER_PAYMENT_VOID_REQUEST_DATA - {request_data["transaction_id"]}': response_data}
                        )
                        return {'status': 400, 'details': response_data}
                else:
                    response_data = {
                        'custom_text': 'Failed Void Transaction'
                    }
                    if hasattr(response, 'transactionResponse') == True and hasattr(response.transactionResponse, 'errors') == True:
                        response_data['errorCode'] = str(
                            response.transactionResponse.errors.error[0].errorCode
                        )
                        response_data['errorMessage'] = response.transactionResponse.errors.error[0].errorText
                    else:
                        response_data['errorCode'] = response.messages.message[0]['code'].text
                        response_data['errorMessage'] = response.messages.message[0]['text'].text

                    success_logger.error(
                        {f'ORDER_PAYMENT_VOID_REQUEST_DATA - {request_data["transaction_id"]}': response_data}
                    )
                    return {'status': 400, 'details': response_data}
            else:
                response_data = {}
                success_logger.error(
                    {f'ORDER_PAYMENT_VOID_REQUEST_DATA - {request_data["transaction_id"]}': 'Null Response.'}
                )
                return {'status': 400, 'data': response_data}
            return {'status': 200, 'data': response_data}

        except Exception as ex:
            success_logger.error(
                {f'ORDER_PAYMENT_VOID_REQUEST_DATA - {str(refTransId)}': ex.__str__()}
            )
            return {'status': 400, 'details': ex.__str__()}
