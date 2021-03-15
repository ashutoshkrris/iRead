from django.shortcuts import render
from datetime import datetime, date
from .paytm import generate_checksum, verify_checksum
from .models import Transaction
from decouple import config
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse

PAYTM_MERCHANT_ID = config("PAYTM_MERCHANT_ID")
PAYTM_MERCHANT_KEY = config("PAYTM_MERCHANT_KEY")


# Create your views here.
def dashboard(request):
    if request.method == 'POST':
        global name
        global email
        name = request.POST.get("name")
        email = request.POST.get("email")
        amount = request.POST.get("amount")
        gateway = request.POST.get("gateway")
        if gateway == 'paytm':
            order_id = f"IREAD{date.today().year}{datetime.now().strftime('%d%m%f')}"
            param_dict = {
                'MID': PAYTM_MERCHANT_ID,
                'ORDER_ID': order_id,
                'TXN_AMOUNT': str(amount),
                'CUST_ID': email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL': f'http://{get_current_site(request)}/payment/paytm/handler/',
            }
        param_dict['CHECKSUMHASH'] = generate_checksum(
            param_dict, PAYTM_MERCHANT_KEY)
        return render(request, "payment/paytm/paytm.html", {'param_dict': param_dict})
    return render(request, "payment/dashboard.html")


def paytm_handler(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = verify_checksum(response_dict, PAYTM_MERCHANT_KEY, checksum)
    new_txn = Transaction(
        name=name,
        email=email,
        order_id=response_dict['ORDERID'],
        currency=response_dict['CURRENCY'],
        gateway_name=response_dict['GATEWAYNAME'],
        response_msg=response_dict['RESPMSG'],
        bank_name=response_dict['BANKNAME'],
        payment_mode=response_dict['PAYMENTMODE'],
        mid=response_dict['MID'],
        response_code=response_dict['RESPCODE'],
        txn_id=response_dict['TXNID'],
        txn_amount=response_dict['TXNAMOUNT'],
        status=response_dict['STATUS'],
        bank_txn_id=response_dict['BANKTXNID'],
        txn_date=response_dict['TXNDATE'],
    )
    new_txn.save()
    if verify:
        if response_dict['RESPCODE'] == '01':
            order_id = response_dict['ORDERID']
            txn_amount = response_dict['TXNAMOUNT']
            context = {
                'orderid': order_id,
                'name': name,
                'email': email,
                'amount': txn_amount,
                'date': date.today(),
                'invoice_num': order_id[5:]
            }
            return render(request, 'payment/invoice.html', context)
        return render(request, 'payment/paytm/payment_status.html', {'response': response_dict})
    return HttpResponse("Invalid")


def invoice(request):
    return render(request, 'payment/invoice.html')
