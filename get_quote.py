#!/usr/local/bin/python3.6

##################################################################
#								 #
# Filename:  get_quote.py					 #
#								 #
# Purpose:  Get the current price of a stock			 #
#								 #
# Author:  Nolan R. H. Gagnon					 #
#								 #
# Date: Dec. 03, 2017                                            #
#								 #
##################################################################

## IMPORTS -----------------------------------------------------##
from termcolor import colored
import sys
import  requests
from bs4 import BeautifulSoup
import re
from json import loads
from pprint import pprint

# Functions

def str_to_int(string):
	t = string.replace(',', '')
	return int(t)

def get_stock_price(ticker):
	webpage = "https://finance.yahoo.com/quote/" + ticker + "?p=" + ticker	
	soup = BeautifulSoup(requests.get(webpage).content, "html5lib")
	script = soup.find("script", text = re.compile("root.App.main")).text
	data = loads(re.search("root.App.main\s+=\s+(\{.*\})", script).group(1))
	price = data["context"]["dispatcher"]["stores"]["QuoteSummaryStore"]["financialData"]["currentPrice"]["raw"]
	
	## Return stock price to caller
	return price	

def get_current_ratio(ticker):
	webpage = "https://finance.yahoo.com/quote/" + ticker + "/balance-sheet?p=" + ticker	
	soup = BeautifulSoup(requests.get(webpage).content, "html5lib")	
	script = soup.find("script", text = re.compile("root.App.main")).text
	data = loads(re.search("root.App.main\s+=\s+(\{.*\})", script).group(1))		
	
	## Balance sheet data
	bs = data["context"]["dispatcher"]["stores"]["QuoteSummaryStore"]["balanceSheetHistoryQuarterly"]["balanceSheetStatements"]
	
	## Get total current assets and total current liabilities
	tot_curr_assets = bs[0]['totalCurrentAssets']['raw']	
	tot_curr_liabs = bs[0]['totalCurrentLiabilities']['raw']
	
	## Calculate the current ratio	
	current_ratio = (tot_curr_assets * 1.0) / tot_curr_liabs
	
	## Return current ratio to caller	
	return current_ratio

def get_de_ratio(ticker):
	webpage = "https://finance.yahoo.com/quote/" + ticker + "/balance-sheet?p=" + ticker	
	soup = BeautifulSoup(requests.get(webpage).content, "html5lib")	
	script = soup.find("script", text = re.compile("root.App.main")).text
	data = loads(re.search("root.App.main\s+=\s+(\{.*\})", script).group(1))		
	
	## Balance sheet data
	bs = data["context"]["dispatcher"]["stores"]["QuoteSummaryStore"]["balanceSheetHistoryQuarterly"]["balanceSheetStatements"]
	
	## Calculate total liabilites and total stockholder's equity
	tot_liab = bs[0]['totalLiab']['raw']
	sh_equity = bs[0]['totalStockholderEquity']['raw']
	
	## Calculate debt-to-equity ratio
	de_ratio = (tot_liab * 1.0) / sh_equity
	
	## Return debt-to-equity ratio to caller
	return de_ratio

def print_summary(ticker):
	
	## Fetch stock price, current ratio, and debt-to-equity ratio	
	price = get_stock_price(ticker)	
	curr = get_current_ratio(ticker)
	de = get_de_ratio(ticker)	
	
	print("\n\n")
	print(40*"-" + " |" + colored(ticker, attrs = ['bold']) + "| " + 40*"-" + "\n")
	print("Current Price: " + colored(price, 'green', attrs=['bold']))
	print("\n")

	print(colored("Debt Metrics", attrs = ['bold']))
	
	if (de < 1.00):
		print("Debt-to-equity Ratio: " + colored("%.2f" % de, 'green', attrs = ['bold']))
	else:
		print("Debt-to-equity Ratio: " + colored("%.2f" % de, 'red', attrs = ['bold']))	

	if (curr > 1.00):
		print("Current Ratio: " + colored("%.2f" % curr, 'green', attrs = ['bold']))
	else:
		print("Current Ratio: " + colored("%.2f" % curr, 'red', attrs = ['bold']))

	print("\n\n")		


## Check for proper usage of script
if len(sys.argv) > 2:
	print("Please supply only the ticker symbol.  Example usage: ./get_quote NVDA")
	exit()
elif len(sys.argv) < 2:
	print("Please supply a ticker symbol.")
	exit()
else:
	print_summary(sys.argv[1])
