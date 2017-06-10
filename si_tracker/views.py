from django.shortcuts import render
from django.http import HttpResponse

def general(req):
    return HttpResponse("Hello")
