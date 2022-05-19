import csv
from email.policy import default
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import FileForm
import random
import string
import pandas as pd
import numpy as np
from cryptography.fernet import Fernet
import rsa
from sklearn.preprocessing import OrdinalEncoder
import os
from django.core.files.storage import default_storage
from django.conf import settings
# Create your views here.


def ranString():
    S = 40
    ran = ''.join(random.choices(string.ascii_letters + string.digits, k=S))
    return str(ran)


def ordinal(df, categ):
    encoder = OrdinalEncoder()
    df[categ] = encoder.fit_transform(df[categ])
    return df


def RSA(df, col, publickey, rows):
    for i in range(0, rows):
        message = df.iat[i, col]
        message_encrypted = rsa.encrypt(message.encode(), publickey)
        df.iat[i, col] = message_encrypted
    return df


def encrypt(obj):
    dataset = obj.doc
    # temp_id = obj.temp_id
    df = pd.read_csv(dataset)
    df = isCategorical(df)
    cols = df.columns
    rows = len(df.index)
    # key = Fernet.generate_key()
    publickey, privatekey = rsa.newkeys(256)

    categ = []
    for col in cols:
        if df.dtypes[col] == 'category':
            categ.append(col)
    for col in range(0, len(cols)):
        # if df.iloc[:, col].dtypes == 'category':
        #     a = Fernet(key)
        #     df = fernet(df, col, a, rows)

        if df.iloc[:, col].dtypes == 'O':
            df = RSA(df, col, publickey, rows)

    df = ordinal(df, categ)
    print(df.head())
    return df
    # return df.to_csv('{temp_id}.csv' .format(temp_id=temp_id))
    # print(file)
    # return file


def isCategorical(df):
    words = df.columns
    rows = len(df.index)
    for i in words:
        if (df.dtypes[i] == 'O'):
            diff = len(df[i]) - len(df[i].unique())
            percent = diff / len(df[i]) * 100
            if rows <= 50 and percent >= 70:
                df[i] = df[i].astype('category')
            elif percent >= 90:
                df[i] = df[i].astype('category')
    return df


def home(request):
    return render(request, 'Home.html')


x = ""


def upload(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            obj = form.save()
            temp_id = obj.temp_id
            df = encrypt(obj)
            # obj.doc = df.to_csv()
            save_path = os.path.join(
                settings.MEDIA_ROOT, '{temp_id}.csv' .format(temp_id=temp_id))
            df.to_csv(save_path)
            file = default_storage.open(save_path)
            print(file)
            file_url = default_storage.url(save_path)
            # fs = FileSystemStorage()
            # fs.save(df.to_csv())
            # csv_data = df.to_csv(encoding='utf-8')
            # file_name = default_storage.save(df.to_csv('{temp_id'.csv))
            # path = os.path.join(
            #     settings.BASE_DIR, '/media/{temp_id}.csv' .format(temp_id=temp_id))
            # response = HttpResponse(content_type='text/csv')
            # response['Content-Disposition'] = 'attachment; filename=filename.csv'
            # df.to_csv(path_or_buf=response, sep=';',
            #   float_format='%.2f', index=False, decimal=",")
            file = '{temp_id}.csv' .format(temp_id=temp_id)
            return render(request, 'Download.html', {'file': file})
    else:
        form = FileForm(initial={'temp_id': str(ranString())})
    return render(request, 'Home.html', {'form': form})


def test(request):
    return render(request, 'Download.html')


def about(request):
    return render(request, 'About.html')


def contact(request):
    return render(request, 'Contact.html')
