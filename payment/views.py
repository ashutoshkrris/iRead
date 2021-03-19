from django.http.response import Http404, JsonResponse
from django.shortcuts import render
from datetime import datetime, date
from .paytm import generate_checksum, verify_checksum
from .models import Transaction
from decouple import config
from django.http import HttpResponse
import razorpay
import hmac
import hashlib


PAYTM_MERCHANT_ID = config("PAYTM_MERCHANT_ID")
PAYTM_MERCHANT_KEY = config("PAYTM_MERCHANT_KEY")
RAZORPAY_KEY_ID = config("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = config("RAZORPAY_KEY_SECRET")



# Create your views here.
def dashboard(request):
    if request.method == 'POST':
        global name
        global email
        global amount
        name = request.POST.get("name")
        email = request.POST.get("email")
        amount = request.POST.get("amount")
        gateway = request.POST.get("gateway")
        
        if gateway == 'paytm':
            order_id = f"IREAD{date.today().year}{datetime.now().strftime('%d%m%f')}"
            param_dict = {
                'MID': PAYTM_MERCHANT_ID,
                'ORDER_ID': order_id,
                'TXN_AMOUNT': str(int(float(amount))),
                'CUST_ID': email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL': f'{request.scheme}://{request.get_host()}/payment/paytm/handler/',
            }
            param_dict['CHECKSUMHASH'] = generate_checksum(
                param_dict, PAYTM_MERCHANT_KEY)
            return render(request, "payment/paytm/paytm.html", {'param_dict': param_dict})
        else:
            order_amount = int(float(amount))*100
            order_currency = 'INR'
            client = razorpay.Client(
                auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
            order = client.order.create(
                {'amount': order_amount, 'currency': order_currency, 'payment_capture': '1'})
            context = {
                'payment': order,
                'name': name,
                'email': email,
                'razorpay_id': RAZORPAY_KEY_ID,
                'currency': order_currency
            }
            return render(request, "payment/razorpay/razorpay.html", context)
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
            txn_status = response_dict['STATUS']
            context = {
                'orderid': order_id,
                'name': name,
                'email': email,
                'amount': txn_amount,
                'date': date.today(),
                'invoice_num': order_id[5:],
                'status': txn_status,

            }
            return render(request, 'payment/invoice.html', context)
        return render(request, 'payment/paytm/payment_status.html', {'response': response_dict})
    return HttpResponse("Invalid")


def razorpay_handler(request):
    if request.is_ajax():

        # from front end
        payment_id = request.POST.get('payment_id')
        order_id = request.POST.get('order_id')
        sign = request.POST.get('sign')
        server_order = request.POST.get('server_order')

        # genrate signature
        secret_key = bytes(RAZORPAY_KEY_SECRET, 'utf-8')
        generated_signature = hmac.new(secret_key, bytes(
            server_order + "|" + payment_id, 'utf-8'), hashlib.sha256).hexdigest()

        # checking authentic source
        if generated_signature == sign:
            new_txn = Transaction(name=name,email=email,order_id=order_id, mid=payment_id,
                                  txn_amount=amount, currency='INR', response_msg=sign, status="TXN_SUCCESS", txn_date=datetime.now())
            new_txn.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})


def failed_payment(request):
    if request.is_ajax():

        # from front end
        payment_id = request.POST.get('payment_id')
        order_id = request.POST.get('order_id')
        server_order = request.POST.get('server_order')
        reason = request.POST.get('reason')
        step = request.POST.get('step')
        source = request.POST.get('source')
        description = request.POST.get('description')
        code = request.POST.get('code')
        transaction = Transaction.objects.create(name=name,email=email,payment_mode=code, order_id=order_id, mid=payment_id, txn_amount=0, gateway_name=source,
                                                 currency='INR', response_msg="Step : " + step + ", Reason : " + reason + ", Desc: " + description, status='TXN_FAILURE', txn_date=datetime.now())
        return JsonResponse({'success': True})


def invoice(request, id):
    try:
        txn = Transaction.objects.get(order_id=id)
        context = {
            'orderid': id,
            'name': txn.name,
            'email': txn.email,
            'amount': txn.txn_amount,
            'txn_date': txn.txn_date,
            'invoice_num': id[5:],
            'status': txn.status,
            'mid': txn.mid
        }
        return render(request, 'payment/invoice.html', context)
    except Exception:
        raise Http404()

def show_invoice(request):
    return render(request, "payment/invoice.html")
