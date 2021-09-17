from django.shortcuts import render
from .forms import UserForm

# Create your views here.
def home(request):
    form = UserForm()
    context = {'form':form, 'data':False, 'insurance_price':10000}
    
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            context['form'] = form
            context['data'] = True
            context['insurance_price'] = form['age']
            print(form)
        
    return render(request, 'home.html', context)