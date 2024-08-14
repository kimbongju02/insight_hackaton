from django.http import HttpResponse
from django.shortcuts import render



#import openai_api, speech_to_file

def index(request):
    return render(request, 'html/button.html')

