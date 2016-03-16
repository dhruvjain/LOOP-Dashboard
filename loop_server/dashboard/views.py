from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render
import datetime

# Create your views here.

def index(request):
	start_date = FT.objects.order_by('day').first().day.strftime("%d/%m/%Y")
	end_date = FT.objects.order_by('day').last().day.strftime("%d/%m/%Y")
	context = RequestContext(request, {
		'start_date' : start_date,
		'end_date' : end_date,
	})
	return render(request, "index.html", context)

def home(request):
	return render(request, "home.html")

