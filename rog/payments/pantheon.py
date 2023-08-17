from django.conf import settings
from django.utils.text import slugify

import requests
import json


def create_ident(item):
    pantheon_ident_id = item.pantheon_ident_id
    name = item.name
    price = item.price
    vat = item.vat
    total_price = price + (price * vat / 100)
    data = {
        "ident": pantheon_ident_id,
        "name": name,
        "classif": "",
        "subClassif": 0,
        "classif2": "",
        "code": "",
        "setOfItem": "700", # vrsta materialnega sredstva npr. od storitve
        "supplier": "",
        "formula": "",
        "vat": vat,
        "currency": "EUR",
        "salePrice": price,
        "rtprice": total_price,
        "wsprice": 0,
        "wsprice2": 0,
        "prStPrice": 0,
        "prodPrice": 0,
        "buyPrice": 0,
        "um": "KOS",
        "umtoUm2": 0,
        "um2": "",
        "vatcode": "2S",
        "vatcodeLow": "2S",
        "discount": 0,
        "warrenty": 0,
        "serialNo": "",
        "active": "T",
        "httppath": "",
        "makeCalc": "",
        "price": price,
        "rebate": 0,
        "transport": 0,
        "duty": 0,
        "directCost": 0,
        "incTax": 0,
        "wsprice2P": 0,
        "wspriceP": 0,
        "rtpriceP": 0,
        "minStock": 0,
        "standardize": "",
        "docTypeProd": "",
        "docTypeOrdSupp": "",
        "dimHeight": 0,
        "dimWidth": 0,
        "dimDepth": 0,
        "dimWeight": 0,
        "dimWeightBrutto": 0,
        "custTariff": "",
        "priceSupp": 0,
        "prStPriceP": 0,
        "purchCurr": "",
        "orderTransInMf": "",
        "origin": "",
        "declarForOriginType": "",
        "acct": "",
        "fieldSa": "",
        "fieldSb": "",
        "fieldSc": "",
        "fieldNa": 0,
        "fieldNb": 0,
        "evidence": "",
        "excise": 0,
        "exciseP": 0,
        "maxStock": 0,
        "optStock": 0,
        "declarForOrigin": "",
        "dept": "",
        "qtyInCode": "",
        "umdim1": "",
        "umdim2": "",
        "wasteQty": 0,
        "umseries": "",
        "qtySeries": 0,
        "column": "",
        "umtoUm3": 0,
        "um3": "",
        "umtoDeclarReport": 0,
        "reportDeclar": "",
        "fieldNc": 0,
        "fieldNd": 0,
        "fieldNe": 0,
        "fieldSd": "",
        "fieldSe": "",
        "prstTime": 0,
        "prstUmtime": "",
        "prStInsertUserId": 0,
        "prStInsertTime": None,
        "prStUpdateUserId": 0,
        "prStUpdateTime": None,
        "prStCheckUserId": 0,
        "prStCheckTime": None,#"2023-08-11T04:54:32.661Z",
        "prStVariantValid": 0,
        "prStOptimalQty": 0,
        "prStDailyQty": 0,
        "unionDeadline": 0,
        "deliveryDeadline": 0,
        "posqty": 0,
        "showAtena": "",
        "acctIncome": "",
        "inFlowOutFlow": "",
        "fieldNf": 0,
        "fieldNg": 0,
        "fieldSf": "",
        "fieldSg": "",
        "fieldSh": "",
        "fieldSi": "",
        "fieldSj": "",
        "fieldNh": 0,
        "fieldNi": 0,
        "fieldNj": 0,
        "fixPriceDiff": 0,
        "qtyInCodeDecPlace": 0,
        "orderMinQty": 0,
        "orderOptQty": 0,
        "costDrv": "",
        "packing": "",
        "purExciseE": 0,
        "purExciseA": 0,
        "purExciseT": 0,
        "beatShare": 0,
        "timeIns": None, #"2023-08-11T04:54:32.661Z",
        "userIns": 1,
        "timeChg": None, #"2023-08-11T04:54:32.661Z",
        "userChg": 1,
        "isReturnPack": "",
        "envrmntCost": "",
        "wastePack": "",
        "wstEeequip": "",
        "usedTyre": "",
        "vehiclePart": "",
        "packSlopak": "",
        "packSlopaktype": "",
        "ummarkLabel": "",
        "qtyMarkLabel": 0,
        "prstPriceString": "",
        "plucode": 0,
        "dateDue": "",
        "monthDue": 0,
        "picture": "",
        "maxRebate": 0,
        "techProcedure": "",
        "descr": "",
        "touchPicture": "",
        "droe": "",
        "droesubject": "",
        "fieldDa": None, #"2023-08-11T04:54:32.661Z",
        "fieldDb": None, #"2023-08-11T04:54:32.661Z",
        "fieldDc": None, #"2023-08-11T04:54:32.661Z",
        "fieldDd": None, #"2023-08-11T04:54:32.661Z",
        "minMargin": 0,
        "discountBegin": None, #"2023-08-11T04:54:32.661Z",
        "discountEnd": None, #"2023-08-11T04:54:32.661Z",
        "docTypeIssue": "",
        "enableChgPrSt": "",
        "note": "",
        "plucode2": 0,
        "buyRebate2": 0,
        "buyRebate3": 0,
        "saleRebate2": 0,
        "saleRebate3": 0,
        "posQtyStep": 0,
        "qtyNotToKol": "",
        "qid": 0,
        "stretchPicture": "",
        "backPacking": "",
        "formulaRt": "",
        "acctNotTaxDeduct": "",
        "prtPicture": "",
        "classProdByAct": "",
        "bullId": "",
        "posprinterId": "",
        "bst": "",
        "vatcodeReceive": "",
        "vatreceive": 0,
        "weighableItem": "",
        "allowedWastage": 0,
        "serialnoDueType": "",
        "packagingType": "",
        "transferredWs": "",
        "colorCode": 0,
        "icon": "",
        "allowedInvShort": 0,
        "acctBuyVasale": "",
        "packWeight": 0,
        "packWasteWeight": 0,
        "discountPrice": 0,
        "discountPriceRt": 0,
        "useAsCostOnIntrastat": "",
        "printTechProc": "",
        "roundQtyToInt": True,
        "convertToUmForPos": True,
        "umForPos": "KOS",
        "webShopItem": "",
        "useAsCostOnVatba": "",
        "descrRtf": "",
        "techProcedureRtf": "",
        "vatcodeReduced": ""
        }
    response = requests.post(
        f'{settings.PANTHEON_URL}/api/Ident',
        json=data
    )
    return response


def create_subject(subject):
    print(subject.email)
    data = {
        "subject": subject.email,
        "buyer": "T",
        "supplier": "F",
        "bank": "F",
        "municipality": "F",
        "locComm": "F",
        "warehouse": "F",
        "worker": "F",
        "user": "F",
        "dept": "F",
        "school": "F",
        "institution": "F",
        "name2": subject.legal_person_name,
        "address": subject.legal_person_address_1,
        "name3": subject.legal_person_name,
        "post": f'SI-{subject.legal_person_address_2}' if subject.legal_person_address_2 else 'SI-1000',
        "country": "Slovenija",
        "km": 0,
        "vatcodePrefix": "SI",
        "code": subject.legal_person_vat,
        "region": "",
        "suprCommune": "",
        "phone": "",
        "fax": "",
        "subUnit": "",
        "priceRate": "1",
        "daysForPayment": 0,
        "yearStatement": "",
        "dateState": None, #"2023-08-11T05:05:12.971Z",
        "statement": "",
        "limit": 0,
        "dateLimit": None, #"2023-08-11T05:05:12.971Z",
        "maxDaysPayDelay": 0,
        "subjTypeSupp": "",
        "subjTypeBuyer": "",
        "stockManage": "",
        "stockValue": "",
        "stockInMinus": "",
        "dateInvent": None,#"2023-08-11T05:05:12.971Z",
        "clerk": 0,
        "rebate": 0,
        "wayOfSale": "Z",
        "currency": "EUR",
        "priceCalcMethod": "0",
        "payMethod": "1",
        "delivery": "5",
        "regNo": "6436005000 ",
        "acPayer": "",
        "activityCode": "",
        "separSaleCalc": "",
        "suppPriceCalcMet": "",
        "suppDiscount": 0,
        "suppSaleMet": "",
        "suppYearStatement": "",
        "suppDateSta": None,#"2023-08-11T05:05:12.971Z",
        "suppPayDays": 0,
        "suppPayMet": "",
        "suppStatement": "",
        "suppLimit": 0,
        "suppDateLim": None,#"2023-08-11T05:05:12.971Z",
        "suppDelivery": "",
        "suppCurr": "",
        "suppClerk": 0,
        "payOrdPriorty": "",
        "swiftcode": "",
        "atwarehouse": "",
        "municipCode": "",
        "dispDoc": "",
        "setOfInterestRates": "",
        "stockRetailValue": "",
        "parity": "",
        "parityPost": "",
        "suppParity": "",
        "suppParityPost": "",
        "fieldSa": "",
        "fieldSb": "",
        "fieldSc": "",
        "fieldSd": "",
        "fieldSe": "",
        "fieldSf": "",
        "fieldSg": "",
        "fieldSh": "",
        "fieldSi": "",
        "fieldSj": "",
        "fieldNa": 0,
        "fieldNb": 0,
        "fieldNc": 0,
        "fieldNd": 0,
        "fieldNe": 0,
        "fieldNf": 0,
        "fieldNg": 0,
        "fieldNh": 0,
        "fieldNi": 0,
        "fieldNj": 0,
        "fieldDa": None, #"2023-08-11T05:05:12.971Z",
        "fieldDb": None, #"2023-08-11T05:05:12.971Z",
        "fieldDc": None, #"2023-08-11T05:05:12.971Z",
        "fieldDd": None, #"2023-08-11T05:05:12.971Z",
        "skis": "",
        "xmldocType": "",
        "xmldocCript": "",
        "xmldocSign": "",
        "createPayOrd": "",
        "xmlglnno": "",
        "intrstsBuyer": "",
        "intrstsSupplier": "",
        "rsbainDistrikt": "",
        "httppath": "",
        "ibanprefix": "",
        "suprDept": "",
        "subjVar1": 0,
        "subjVar2": 0,
        "subjVar3": 0,
        "subjVar4": 0,
        "subjVar5": 0,
        "subjVar6": 0,
        "subjVar7": 0,
        "subjVar8": 0,
        "subjVar9": 0,
        "subjVar10": 0,
        "latitude": 0,
        "longitude": 0,
        "maxRebate": 0,
        "perInv": "",
        "suppPerInv": "",
        "active": "T",
        "activeContacts": "",
        "deptRegNo": "",
        "payLoc": "",
        "buyerLimitCtrl": "",
        "timeIns": "2023-08-11T05:05:12.971Z",
        "userIns": 1,
        "timeChg": "2023-08-11T05:05:12.971Z",
        "userChg": 1,
        "subUnitCode": "",
        "jibcode": "",
        "note": "",
        "pin": "",
        "deptMuni": "",
        "contactPrsnB": 0,
        "contactPrsnS": 0,
        "subUnitRegNo": "",
        "subUnitTaxCode": "",
        "workingHours": 0,
        "workingDaysInWeek": 0,
        "budgetUser": "",
        "exciseNumber": "",
        "instalmentNo": 0,
        "suppInstalmentNo": 0,
        "branch": "",
        "branchForm": "",
        "orgColor": 0,
        "loyaltyPrefix": "",
        "dontSendReminders": "",
        "gln": "",
        "municipCreditor": "",
        "bankCode": "",
        "retail": "",
        "fiscalNo": "",
        "payerS": "",
        "acctClaim": "",
        "acctOblig": "",
        "eSlogVer": "",
        "pincodePrefix": "",
        "acctGlopen": "",
        "noExciseCalc": "",
        "rsbainDistriktBuyer": "",
        "vatpayRealSupp": "",
        "warehouseCapacity": 0,
        "warehouseCapacityUm": "",
        "acctExpense": "",
        "acctIncome": "",
        "permitLumpCompen": "",
        "remindersSendType": "",
        "pac": "",
        "eslogContractCt": "",
        "skis2": "",
        "allowedInvShort": 0,
        "acctRebateExtra": "",
        "veterinarian": "",
        "anafcheckDate": None, #"2023-08-11T05:05:12.971Z",
        "parityType": "",
        "suppParityType": "",
        "naturalPerson": "",
        "minMargin": 0,
        "ncc": "",
        "buyerCalcInvoOutFallDue": "",
        "assortment": "",
        "orgUnit": "",
        "accountingPeriod": "",
        "orderValidBuyer": 0,
        "orderValidSupplier": 0,
        "lei": "",
        "freeStockReport": "",
        "webShopSubject": "",
        "deliveryPriority": 1,
        "deliveryDays": 0,
        "priceRatePos": True
    }
    response = requests.post(
        f'{settings.PANTHEON_URL}/api/Subject',
        json=data
    )
    return response



def create_move(
        payment,
        vat=22):
    """
    {
        'acKey': '2330000000009',
        'docType': '3000',
        'reference': '2330000009001',
        'orderForm': None,
        'success': True,
        'error': '',
        'fiscalSalesBookExists': False,
        'itemsCreateResponse': [
            {
                'acKey': '2330000000009',
                'anNo': 1,
                'costDrv': None,
                'department': None,
                'status': 'T',
                'error': '',
                'success': True
            }
        ]
    }
    """
    data = {
        "acKey": "",
        "receiver": payment.user.email,
        "receiverId": payment.user.email,
        "receiverAddress": payment.user.address_1,
        "issuer": "Veleprodajno skladišče",
        "issuerId": "Veleprodajno skladišče",
        "thirdParty": payment.user.legal_person_name,
        "thirdPartyId": payment.user.legal_person_name,
        "docType": "3000", # poslovni dogodek
        "date": payment.successed_at.strftime("%Y-%m-%dT00:00:00.000Z"),
        "dateDue": payment.successed_at.strftime("%Y-%m-%dT00:00:00.000Z"),
        "invoiceDate": payment.successed_at.strftime("%Y-%m-%dT00:00:00.000Z"),
        "taxDate": payment.successed_at.strftime("%Y-%m-%dT00:00:00.000Z"),
        "expectedDeliveryDate": payment.successed_at.strftime("%Y-%m-%dT00:00:00.000Z"),
        "wayOfSale": "Z",
        "paymentMethod": "1",
        "paymentMethodId": "1",
        "paymentMethods": [
            {
                "acPayMethod": "1",
                "name": "",
                "amount": payment.amount,
                "code": "",
                "isRefund": True,
                "fiscalGroup": ""
            }
        ],
        "clerkId": 1,
        "clerk": "Administrator",
        "price": payment.amount,
        "vat": vat * 100 / payment.amount,
        "discount": 0,
        "department": "",
        "status": "N",
        "order": str(payment.id),        # dokument 1
        "orderDate": payment.successed_at.strftime("%Y-%m-%dT00:00:00.000Z"),
        "orderForm": "",
        "orderFormDate":  "1900-01-01T00:00:00.000Z", # no date SQL offset
        "credited": "",
        "note": "", # opomba v glavi dokumenta
        "title": "",
        "titleText": "",
        "days": 0,
        "isPos": True,
        "takeoverDate": "1900-01-01T00:00:00.000Z", # no date SQL offset
        "refNumber": "",
        "refCode": "",
        "fiscSalesBookDocNo": "",
        "fiscSalesBookSerNo": "",
        "fiscSalesBookSetNo": "",
        "author": "",
        "sale": "",
        "statement": "",
        "currency": "EUR",
        "deliveryType": "5",
        "deliveryPlace": "",
        "fxRate": 0,
        "corrType": "",
        "fillDeptFromCostDrv": True,
        "filterDeptForCostDrv": True,
        "invoiceItems": [
            {
                "acKey": "",
                "ident": payment.plan.pantheon_ident_id,
                "name": payment.plan.name,
                "anNo": 1,
                "quantity": 1,
                "price": payment.amount,
                "priceCurrency": 0,
                "rabate": 0,
                "vat": vat,
                "vatCode": "2S",
                "vatCodeTR": "2S",
                "note": "", # opomba na poziciji
                "measurementUnit": "KOS",
                "taxPrice": 0,
                "basisForTax": 0,
                "priceForValue": 0,
                "stock": 0,
                "costDrv": "",
                "department": "",
                "retailPrice": 0,
                "newRetailPrice": 0,
                "rabateRetail": 0,
                "marginRetail": 0,
                "percentRetail": 0,
                "salePrice": 0,
                "newSalePrice": 0,
                "rabateSale": 0,
                "marginSale": 0,
                "percentSale": 0,
                "directCost": 0,
                "duty": 0,
                "warehouseValue": 0,
                "allowedShortage": 0,
                "allowedShortagePercent": 0,
                "turnoverQuantity": 0,
                "isSerialNo": True,
                "author": ""
            }
        ]
    }
    print(json.dumps(data))
    response = requests.post(
        f'{settings.PANTHEON_URL}/api/Move/insert',
        json=data
    )
    return response
