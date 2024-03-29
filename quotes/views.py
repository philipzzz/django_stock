# Copyright 2019-2020 All Right By Philip Tan
from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages

def home(request):

	import requests
	import json

	if request.method == 'POST':
		ticker2 = request.POST['ticker']
		api_request = requests.get("https://cloud.iexapis.com/stable/stock/" +ticker2+ "/quote?token=pk_cc31f9187cfb4494bbafcf46f292dde7")

		try:
			api = json.loads(api_request.content)
		except Exception as e:
			api = "Error..."
		return render(request, 'home.html', {'api': api})

	else :
		return render(request,'home.html',{'ticker2' : "Please input a ticker .."})

	#pk_cc31f9187cfb4494bbafcf46f292dde7
	#api_request = requests.get("https://cloud.iexapis.com/stable/stock/aapl/quote?token=pk_cc31f9187cfb4494bbafcf46f292dde7")



	#return render(request,'home.html',{'api2' : api1})

def about(request):
	return render(request,'about.html',{})

def add_stock(request):
	import requests
	import json

	if request.method == 'POST':
		form = StockForm(request.POST or None)

		if form.is_valid():
			form.save()
			messages.success(request, ("Stock Has Been Added"))
			return redirect('add_stock')

	else:
		ticker = Stock.objects.all()
		output = []
		for ticker_item in ticker:
			api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_cc31f9187cfb4494bbafcf46f292dde7")

			try:
				api = json.loads(api_request.content)
				output.append(api)

			except Exception as e:
				api = "Error..."

	return render(request,'add_stock.html',{'ticker':ticker, 'output':output})

def delete(request, stock_id):
	item = Stock.objects.get(pk=stock_id)
	item.delete()
	messages.success(request,("Stock Has Been Deleted!"))
	return redirect(add_stock)

def delete_stock(request):
	return render(request,'delete_stock.html',{})