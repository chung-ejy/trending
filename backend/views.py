from django.shortcuts import render
from django.http.response import JsonResponse
import pickle
import pandas as pd
import json
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
import requests
from pymongo import MongoClient
from textblob import TextBlob
@csrf_exempt
def backendView(request):
    info = json.loads(request.body.decode("utf-8"))
    factors = ['tbtitlepol',
                'tbtitlesub',
                'tbdescriptionpol',
                'tbdescriptionsub',
                'tbtagpol',
                'tbtagsub',
                'like_pct',
                'view_count']
    try:
        client = MongoClient("localhost",27017)
        db = client["youtube_trends"]
        table = db["model"]
        data = table.find(show_record_id=False)
        model =  pd.DataFrame(list(data))
        m = pickle.loads(model["model"].item())
        complete = info
        info["tag"] = info["tag"].split("|")[0]
        info["view_count"] = int(info["view_count"])
        info["like_pct"] = float(info["like_pct"])
        info["tbtitlepol"] = TextBlob(str(info["title"])).sentiment.polarity
        info["tbtitlesub"] = TextBlob(str(info["title"])).sentiment.subjectivity
        info["tbtagpol"] = TextBlob(str(info["tag"])).sentiment.polarity
        info["tbtagsub"] = TextBlob(str(info["tag"])).sentiment.subjectivity
        info["tbdescriptionpol"] = TextBlob(str(info["description"])).sentiment.polarity
        info["tbdescriptionsub"] = TextBlob(str(info["description"])).sentiment.subjectivity
        complete["prediction"] = int(m.predict(pd.DataFrame([info])[factors]))
    except Exception as e:
        complete = info
        complete["prediction"] = "not found"
        print(str(e))
    complete = {k: v for k,v in complete.items() if "tb" not in k}
    return JsonResponse(complete,safe=False)