from django.conf import settings

import requests
import json


def create_ident(name, price, vat, ident_id):
    if not settings.PANTHEON_URL:
        return None
    price = float(price)
    vat = int(vat)
    total_price = price + (price * vat / 100)
    data = {
        "ident": ident_id,
        "name": name,
        "classif": "",
        "subClassif": 0,
        "classif2": "",
        "code": "",
        "setOfItem": "700", # vrsta materialnega sredstva npr. od storitve
        "supplier": "",
        "formula": "",
        "vat": 0,
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
        "vatcode": "NN",
        "vatcodeLow": "NN",
        "discount": 0,
        "warrenty": 0,
        "serialNo": "",
        "active": "T",
        "httppath": "",
        "makeCalc": "",
        "price": price,
        "rabate": 0,
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
        "dept": "LASTNA SREDSTVA/TRG/03",
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
        "acctIncome": "760103",
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
        "costDrv": "PMS",
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
    print(response)
    return response


def create_subject(subject):
    print(subject.email)
    if not settings.PANTHEON_URL:
        return None

    taxer = False

    tax_number = subject.legal_person_tax_number
    tax_number = tax_number.replace('SI', '').strip()
    if subject.legal_person_vat:
        taxer = True

    data = {
        "subject": subject.get_pantheon_subject_id(),
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
        "name2": f'{subject.first_name} {subject.last_name}',
        "address": subject.address_1,
        "name3": subject.legal_person_name,
        "post": f'SI-{subject.get_post()}',
        "country": "Slovenija",
        "km": 0,
        "vatcodePrefix": "SI" if taxer else "",
        "code": tax_number,
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
        "rabate": 0,
        "wayOfSale": "Z" if taxer else "K",
        "currency": "EUR",
        "priceCalcMethod": "0",
        "payMethod": "",
        "delivery": "",
        "regNo": "",
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
        "timeIns": subject.created_at.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "userIns": 1,
        "timeChg": subject.created_at.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
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
    print(response)
    return response



def create_move(
        payment,
        vat=22):
    if not settings.PANTHEON_URL:
        return None
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
        "receiver": "",
        "receiverId": payment.user.get_pantheon_subject_id(),
        "receiverAddress": payment.user.address_1,
        "issuer": "Veleprodajno skladišče",
        "issuerId": "Veleprodajno skladišče",
        "thirdParty": payment.user.legal_person_name,
        "thirdPartyId": payment.user.legal_person_name,
        "docType": "3690", # poslovni dogodek
        "date": payment.successed_at.strftime("%Y-%m-%dT00:00:00.000Z"),
        "dateDue": payment.successed_at.strftime("%Y-%m-%dT00:00:00.000Z"),
        "invoiceDate": payment.successed_at.strftime("%Y-%m-%dT00:00:00.000Z"),
        "taxDate": payment.successed_at.strftime("%Y-%m-%dT00:00:00.000Z"),
        "expectedDeliveryDate": payment.successed_at.strftime("%Y-%m-%dT00:00:00.000Z"),
        "wayOfSale": "Z" if payment.user.legal_person_vat else "K",
        "paymentMethod": "1",
        "paymentMethodId": "1",
        "paymentMethods": [
            {
                "acPayMethod": "1",
                "name": "",
                "amount": float(payment.amount),
                "code": "",
                "isRefund": True,
                "fiscalGroup": ""
            }
        ],
        "clerkId": 1,
        "clerk": "Administrator",
        "price": float(payment.amount),
        "vat": 0.0,
        "discount": 0,
        "department": "",
        "status": "N",
        "order": str(payment.id),        # dokument 1
        "orderDate": payment.created_at.strftime("%Y-%m-%dT00:00:00.000Z"),
        "orderForm": str(payment.invoice_number),
        "orderFormDate":  payment.successed_at.strftime("%Y-%m-%dT00:00:00.000Z"), # no date SQL offset
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
                "ident": item.get_pantheon_ident_id(),
                "name": item.plan_name,
                "anNo": 1,
                "quantity": 1,
                "price": float(item.original_price),
                "priceCurrency": 0,
                "rabate": item.promo_code.percent_discount if item.promo_code else 0,
                "vat": 0,
                "vatCode": "NN",
                "vatCodeTR": "NN",
                "note": "", # opomba na poziciji
                "measurementUnit": "KOS",
                "taxPrice": 0,
                "basisForTax": 0,
                "priceForValue": 0,
                "stock": 0,
                "costDrv": "PMS",
                "department": "LASTNA SREDSTVA/TRG/03",
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
            } for item in payment.payment_plans.all()
        ]
    }
    response = requests.post(
        f'{settings.PANTHEON_URL}/api/Move/insert',
        json=data
    )
    print(response)
    return response
