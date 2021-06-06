from django.shortcuts import render,redirect

def auth_middleware(get_response):
    def middleware(request):
        # print(request.session.get('customer'))
        if not request.session.get('customer'):
            # return redirect("login")
            return render(request, 'store/login.html')
        response = get_response(request)
        return response

    return middleware