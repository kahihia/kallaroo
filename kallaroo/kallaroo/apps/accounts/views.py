from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View, TemplateView, ListView, DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .forms import UserCreationForm, UserChangeForm, LoginForm, FullUserAddressForm, UserAddressForm, StripePaymentForm
from .models import User, UserAddress
from ..categories.models import Subcategory
from ..tasks.models import Task
from ..tasks.forms import CreateTaskForm
from ..reviews.forms import CreateReviewForm
from ..reviews.models import Review
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse

from formtools.wizard.views import NamedUrlSessionWizardView
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import braintree
import stripe
import time
import os

braintree.Configuration.configure(braintree.Environment.Sandbox,
    merchant_id=settings.BRAINTREE_MERCHANT_ID,
    public_key=settings.BRAINTREE_PUBLIC,
    private_key=settings.BRAINTREE_PRIVATE,
)



class RegisterProfileView(View):
	model = User
	form_class = UserCreationForm
	template_name = 'accounts/register_user/step1.html'

	def get(self, request, *args, **kwargs):
		
		form = self.form_class()

		context = {
			'form': form,
		}

		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):

		
		if request.method == "POST":
			form = self.form_class(request.POST, request.FILES)
			if form.is_valid():

				username = form.cleaned_data.get('username')
				email = form.cleaned_data.get('email')
				first_name = form.cleaned_data.get('first_name')
				last_name = form.cleaned_data.get('last_name')
				password = form.cleaned_data.get('password1')

				user = User.objects.create_user(email, username, first_name, last_name, password)
				user.profile_pic = request.FILES['profile_pic']

				try:
					user.is_contractor = request.POST['is_contractor']
					subcategory = Subcategory.objects.get(id=request.POST['subcategory'])
					user.subcategory = subcategory
				except:
					pass

				# user.braintree_id = user.get_braintree_id()

				# user.braintree_client_token = user.get_client_token()

				user.save()

				user = authenticate(username=email, password=password)
				print(user)
				login(request, user)
				print("=============")
				print("user logged in")
				print("=============")
				request.session['user_id'] = user.id
				user.is_online = True
				user.save()
				return HttpResponseRedirect('%s'%(reverse('accounts:register_address')))
			# else:
		context = {

			'form': form,

		}	

		print("uh oh, something went wrong")
		return render(request, self.template_name, context)

class RegisterAddressView(View):
	model = UserAddress
	# form = UserAddressForm
	form = FullUserAddressForm
	template_name = 'accounts/register_user/step2.html'

	def get(self, request, *args, **kwargs):
		
		form = self.form()
		# form2 = self.form2()

		context = {
			'form': form,
			# 'form2': form2, 
		}

		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):

		# form = UserAddressForm(request.POST)
		
		if request.method == "POST":

			form = FullUserAddressForm(request.POST)
			
			if form.is_valid():
				
				street_number = form.cleaned_data.get('street_number')
				street_address = form.cleaned_data.get('street_address')
				city = form.cleaned_data.get('city')
				state = form.cleaned_data.get('state')
				postal_code = form.cleaned_data.get('postal_code')
				print form.cleaned_data
				
				new_address = UserAddress.objects.create_address(street_number, street_address, city, state, postal_code)
				new_address.user = request.user
				
				new_address.save()

				return HttpResponseRedirect('%s'%(reverse('accounts:register_payment')))

		context = {
			'form': form,
		}

		print("error, something went wrong")
		return render(request, self.template_name, context)

class RegisterPaymentView(View):
	model = User
	template_name = 'accounts/register_user/step3_stripe.html'

	def get(self, request, *args, **kwargs):
		
		user = request.user
		# braintree_client_token = user.braintree_client_token
		context = {
			# 'braintree_client_token': braintree_client_token,
			'user': user,
			'form': StripePaymentForm,
		}

		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		# print(request.POST.get('payment_method_nonce'))
		user = request.user
		# user.payment_method_nonce = request.POST.get('payment_method_nonce')
		# user.save()

		# result = braintree.PaymentMethod.create({
		# 	"customer_id": user.braintree_id,
		# 	"payment_method_nonce": user.payment_method_nonce,
		# })

		# if result.is_success:
		# 	print("=============")
		# 	print("success")
		# 	print("=============")
		# 	# print(result.payment_method)
		# 	# print(result.payment_method.unique_number_identifier)
		# 	# print(result.payment_method.token)
		# 	user.payment_method_token = result.payment_method.token
		# 	user.save()
		# 	messages.success(request, "You have successfully registered your account.")

		# 	return HttpResponseRedirect('%s'%(reverse('accounts:dashboard',args=[user.id])))
		# else:
		# 	print("=============")
		# 	print("failed")
		# 	print("=============")
		# 	return HttpResponseRedirect('%s'%(reverse('accounts:register_payment')))


		""" Stripe Integration """
		
		# grab user date of birth
		dob = request.POST['date_of_birth']
		print("==========")
		print(dob)	# 1980-01-29
		print("==========")

		# dob = user.date_of_birth

		# dob = dob.split('-')

		# year = dob[0]
		# month = dob[1]
		# day = dob[2]
		print user.get_full_name()

		day, month, year = user.format_date_of_birth(dob)

		print day, month, year

		stripe.api_key = 'sk_test_BvXnJuHaPBDFDR0nou3Qq4Qn'
		# stripe.api_key = os.environ['STRIPE_API_KEY']

		# create the account
		result = stripe.Account.create(
			country='US',
			managed=True,
			email=user.email,
		)

		# store the acct_xxxxxxxx
		user.stripe_account_id = result.id
		print("===========")
		print("user stripe account id: " + result.id)
		print("===========")

		# secret and publishable key
		print("===========")
		print(result)
		# print(result.keys.publishable)
		# print(result.keys.secret)
		print("===========")


		# retrieve the account and sign the ToS
		account = stripe.Account.retrieve(result.id)
		account.tos_acceptance.date = int(time.time())
		account.tos_acceptance.ip = '67.160.206.40' # Depends on what web framework you're using

		# update account to include legal_entity data
		account.legal_entity.first_name = user.first_name
		account.legal_entity.last_name = user.last_name
		account.legal_entity.dob.day = day
		account.legal_entity.dob.month = month
		account.legal_entity.dob.year = year
		account.legal_entity.type = "individual"
		account.save()
		

		# grab the stripeToken
		stripe_cc_token = request.POST['stripeToken']

		print("==========")
		print("the credit card stripe token is: " + stripe_cc_token)
		print("==========")

		# use the stripeToken to create a Customer w/ credit card
		customer = stripe.Customer.create(
		  description="Stripe account for: " + user.get_full_name(),
		  source=stripe_cc_token,
		)

		print("=============")
		print("this is the customer: ")
		print(customer)
		print("=============")

		# save the cus_xxxxxxxx to the user (this will be used to create the charges)
		user.stripe_customer_id = customer.id
		# save the card_xxxxxxx to the user (credit card)
		user.stripe_card_id = customer.sources.data[0].id
		

		# grab the bank account data from form submission
		"""
		"id": "ba_17UnXx2eZvKYlo2CxDVhPoUp",
		"object": "bank_account",
		"account": "acct_1032D82eZvKYlo2C",
		"account_holder_type": "individual",
		"bank_name": "STRIPE TEST BANK",
		"country": "US",
		"currency": "usd",
		"default_for_currency": false,
		"fingerprint": "1JWtPxqbdX5Gamtc",
		"last4": "6789",
		"metadata": {
		},
		"name": "Jane Austen",
		"routing_number": "110000000",
		"status": "new",
		"customer": "cus_7kHbMq1VpX8gJN"
		"""

		bank_account_number = request.POST['bank_account']
		bank_name = request.POST['bank_name']
		routing_number = request.POST['routing_number']

		# attach a bank account to the 'managed account'
		# how to do verification/authentication???
		"""
		"legal_entity": {
	    	"additional_owners": null,
		    "address": {
		      "city": null,
		      "country": "US",
		      "line1": null,
		      "line2": null,
		      "postal_code": null,
		      "state": null
		    },
	    	"business_name": null,
		    "dob": {
		      "day": null,
		      "month": null,
		      "year": null
		    },
		    "first_name": null,
		    "last_name": null,
		    "personal_address": {
		      "city": null,
		      "country": null,
		      "line1": null,
		      "line2": null,
		      "postal_code": null,
		      "state": null
		    },
		    "personal_id_number_provided": false,
		    "ssn_last_4_provided": false,
		    "type": null,
		    "verification": {
		      "details": null,
		      "details_code": "failed_other",
		      "document": null,
		      "status": "unverified"
		    }
	    """
		bank_account = account.external_accounts.create(
			external_account={
				'object': 'bank_account',
				'account_number': bank_account_number,
				'account_holder_type': 'individual',
				'bank_name': bank_name,
				'country': 'US',
				'currency': 'usd',
				'routing_number': routing_number,

			}
		)


		print bank_account
		account.save()
		user.stripe_bank_account_id = bank_account.id
		
		user.save()
		# store the bank_id
		# ba_17Umvt2eZvKYlo2CdPjUT86K
		# account = stripe.Account.retrieve("acct_1032D82eZvKYlo2C")
		# bank_account = account.external_accounts.retrieve("ba_17Umvt2eZvKYlo2CdPjUT86K")

		return HttpResponseRedirect('%s'%(reverse('accounts:dashboard',args=[user.id])))

class UserProfileDetailView(DetailView):
	model = User
	template_name = 'accounts/partials/users/profile.html'
	form = UserChangeForm

	def get_context_data(self, **kwargs):
		context = super(UserProfileDetailView, self).get_context_data(**kwargs)
		user = self.object
		context['form'] = self.form(instance=user)
		return context

	def post(self, request, *args, **kwargs):
		pass

class UserTaskView(View):
	# model = User
	template_name = 'accounts/partials/users/tasks.html'
	form = CreateTaskForm

	def get(self, request, *args, **kwargs):
		# context = super(UserTaskView ,self).get_context_data(**kwargs)
		user = self.request.user
		# context['form'] = self.form()
		# context['tasks'] = Task.objects.filter(user=user)
		tasks = Task.objects.filter(user=user)
		form = self.form()
		context = {

			'user': user,
			'tasks': tasks,
			'form': form,
		}
		return render(request, self.template_name, context)

@method_decorator(login_required, name='dispatch')
# @csrf_protect
class DashboardTemplateView(TemplateView):
	template_name = 'accounts/dashboard.html'

	def get_context_data(self, **kwargs):
		context = super(DashboardTemplateView, self).get_context_data(**kwargs)
		context['user'] = User.objects.get(id=self.request.session['user_id'])
		return context

@csrf_exempt
def assign_socket_id(request):
	if request.method == "POST":
		if 'socket_id' not in request.session:
			request.session['socket_id'] = request.POST.get('socket_id')
			user = User.objects.get(id=request.POST.get('user_id'))
			# user = request.user
			user.socket_id = request.POST.get('socket_id')
			user.save()
			print("your session socket id is: " + request.session['socket_id'])
			print("your socket id is: " + user.socket_id)
			print("current user is: " + user.username)
			return user
		else:
			user = User.objects.get(id=request.POST.get('user_id'))
			# user = request.user
			request.session['socket_id'] = user.socket_id
			return user

class UsersListView(ListView):
	model = User
	template_name = 'accounts/user_list.html'

class AccountView(TemplateView):
	template_name = 'accounts/index.html'

	def get_context_data(self, **kwargs):
		context = super(AccountView, self).get_context_data(**kwargs)

		context['login_form'] = LoginForm
		return context


"""
Need to update the LoginUserView
"""

def login_user(request):
	context = {
		'register_form': UserCreationForm,
		'login_form': LoginForm,
	}

	form = LoginForm(request.POST)
	if request.method == "POST":
		"""
		AuthenticationForm uses id_username;
		username is dependent on USERNAME_FIELD in models;

		If you use custom LoginForm with id_email, set authenticate(username=email)
		"""
		email = request.POST['email']
		password = request.POST['password']

		user = authenticate(username=email, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				print("=============")
				print("user logged in successfully")
				print(user)
				print("=============")
				request.session['user_id'] = user.id
				print("sessionid is: ")
				print(request.session.session_key)
				# return HttpResponseRedirect('/accounts/success')
				user.is_online = True
				user.save()
				return HttpResponseRedirect('%s'%(reverse('accounts:dashboard',args=[request.session['user_id']])))
			else:
				return HttpResponseRedirect('%s'%(reverse('accounts:main')))
		else:
			return HttpResponseRedirect('%s'%(reverse('accounts:main')))
	else:
		return HttpResponseRedirect('%s'%(reverse('accounts:main')))

def logout_view(request):
	user = User.objects.get(id=request.session['user_id'])
	user.is_online = False
	if 'socket_id' in request.session:
		del request.session['socket_id']

	if 'user_id' in request.session:
		del request.session['user_id']

	user.socket_id = None

	logout(request)
	print("=============")
	print("user logged out successfully")
	print("=============")
	return HttpResponseRedirect('%s'%(reverse('accounts:main')))

class SuccessView(TemplateView):
	template_name = 'accounts/success.html'



"""
=================
Contractor
=================
"""

class AllContractorsView(View):
	model = User
	template_name = 'accounts/contractors/all.html'

	def get(self, request, *args, **kwargs):
		contractors = User.objects.all().filter(is_contractor=True)
		context = {
			'contractors': contractors,
		}

		return render(request, self.template_name, context)

class ContractorProfileView(DetailView):
	model = User
	template_name = 'accounts/contractors/detail.html'
	form = CreateReviewForm

	def get_context_data(self, **kwargs):
		context = super(ContractorProfileView, self).get_context_data(**kwargs)
		# context['reviews'] = Review.objects.all().filter(reviewee=self.object)
		context['reviews'] = self.object.reviewee.all()
		# print(context['reviews'])
		context['review_form'] = self.form()
		return context

	



