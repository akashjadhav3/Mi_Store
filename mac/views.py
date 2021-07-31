from django.shortcuts import render

from django.http import HttpResponse
from shop.models import Contact

def home(request):
    return render(request, 'home.html')


from django.contrib.auth.decorators import login_required
@login_required
def contactus_admin(request):
    is_admin_group = request.user.groups.filter(name__in=['admin']).exists()
    if is_admin_group:
        context ={}
        contacts_info = Contact.objects.all()
        context['info']=contacts_info
        context['isAdmin']=is_admin_group
        return render(request, 'contacts_us_admin.html',context)
    return redirect('ShopHome')

@login_required
def contactus_admin_details(request,id=None):    
    is_admin_group = request.user.groups.filter(name__in=['admin']).exists()
    if is_admin_group:
        if id:
            context = {}
            obj = Contact.objects.filter(pk=id)
            context['info']=obj
            context['isAdmin']=is_admin_group
            return render(request, 'contactus_admin_details.html',context)
        return HttpResponse("Id invalid")
    return redirect('ShopHome')

from shop.models import Orders
@login_required
def admin_order_approval(request):
    is_admin_group = request.user.groups.filter(name__in=['admin']).exists()
    if is_admin_group:
        context = {}
        obj = Orders.objects.all().order_by('-created')
        context['info']=obj
        context['isAdmin']=is_admin_group
        return render(request, 'admin_order_approval.html',context)
    return redirect('ShopHome')


from django.contrib import messages
from django.shortcuts import render, redirect
@login_required
def set_order_approval(request,id):
    is_admin_group = request.user.groups.filter(name__in=['admin']).exists()
    if is_admin_group:
        obj = Orders.objects.get(pk=id)
        obj.status = True
        obj.save()
        messages.success(request,"Order Approved {} ".format(obj.name))
        return redirect('admin_order_approval')
    return redirect('ShopHome')


@login_required
def order_cancel(request,id):
    is_admin_group = request.user.groups.filter(name__in=['admin']).exists()
    if is_admin_group:
        obj = Orders.objects.get(pk=id)
        obj.delete()
        messages.success(request,"Order Deleted {} ".format(obj.name))
        return redirect('admin_order_approval')
    return redirect('ShopHome')


from shop.models import Product
from shop.forms import NewProductForm
from django.views.generic.edit import FormView,UpdateView,DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy,reverse

class product_creation(LoginRequiredMixin,FormView):
    form_class = NewProductForm
    success_url = reverse_lazy("product_list")
    template_name = "product_create.html"
    def form_valid(self, form):
        form.save()
        messages.success(self.request,"Product add successfully")
        return redirect(self.success_url )


class ProductUpdate(LoginRequiredMixin,UpdateView):
    template_name = 'product_create.html'
    form_class = NewProductForm
    model = Product
    success_url = reverse_lazy("product_list")
    def form_valid(self, form):
        messages.success(self.request,"Product Updated successfully")
        return super().form_valid(form)

class ProductDelete(LoginRequiredMixin,DeleteView):
    model = Product
    template_name = "product_create.html"
    context_object_name = 'product'
    success_url = reverse_lazy('product_list') 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@login_required
def products_list(request):
    is_admin_group = request.user.groups.filter(name__in=['admin']).exists()
    if is_admin_group:
        context = {}
        obj = Product.objects.all()
        context['products']=obj
        context['isAdmin']=is_admin_group
        return render(request, 'products_list.html',context)
    return redirect('ShopHome')

@login_required
def admin_site(request):
    is_admin_group = request.user.groups.filter(name__in=['admin']).exists()
    if is_admin_group:
        context = {'isAdmin': is_admin_group}
        return render(request, 'admin_sites.html',context)
    return redirect('ShopHome')

