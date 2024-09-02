import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

!pip install mailbox

import mailbox
mboxfile = "All mail Including Spam and Trash-002 (1).mbox"

mbox = mailbox.mbox(mboxfile)
mbox

for key in mbox[0].keys():
  print(key)

import csv

with open('mailbox.csv', 'w') as outputfile:
  writer = csv.writer(outputfile)
  writer.writerow(['subject','from','date','to','label','thread'])
    
  for message in mbox:
    writer.writerow([message['subject'], message['from'],  message['date'], message['to'],  message['X-Gmail-Labels'], message['X-GM-THRID']])

dfs = pd.read_csv('mailbox.csv', names=['subject', 'from', 'date', 'to', 'label', 'thread'])

dfs.dtypes

dfs['date'] = dfs['date'].apply(lambda x: pd.to_datetime(x, errors='coerce', utc=True))

dfs = dfs[dfs['date'].notna()]

dfs.to_csv('gmail.csv')

dfs.info()

dfs.head(10)

dfs.columns

from collections import Counter
import re

dfs['date'] = pd.to_datetime(dfs['date'])
dfs['hour'] = dfs['date'].dt.hour
dfs['day'] = dfs['date'].dt.day_name()
dfs['day_of_week'] = dfs['date'].dt.dayofweek

gmail_filter = dfs['from'].str.contains('gmail.com') | dfs['to'].str.contains('gmail.com')
gmail_emails = dfs[gmail_filter]
times_of_day = gmail_emails['hour'].value_counts().sort_index()

print("Times of the day you send and receive emails with Gmail account:")
print(times_of_day)

emails_per_day = dfs.groupby('day').size()
avg_emails_per_day = emails_per_day.mean()

print("\nAverage number of emails per day:")
print(avg_emails_per_day)

emails_per_hour = dfs.groupby('hour').size()
avg_emails_per_hour = emails_per_hour.mean()

print("\nAverage number of emails per hour:")
print(avg_emails_per_hour)

from_counts = dfs['from'].value_counts()
to_counts = dfs['to'].value_counts()
most_frequent_communicators = (from_counts.add(to_counts, fill_value=0)).sort_values(ascending=False)

print("\nWhom you communicate with most frequently:")
print(most_frequent_communicators.head(10))

active_days = dfs['day_of_week'].value_counts()

print("\nMost active emailing days:")
print(active_days)

subject_words = ' '.join(dfs['subject'].dropna()).lower()
subject_words = re.findall(r'\b\w+\b', subject_words)
subject_word_freq = Counter(subject_words).most_common()

print("\nWhat you are mostly emailing about:")
print(subject_word_freq[:10])

start_date = '2024-07-20'
end_date = '2024-07-30'
emails_in_given_time = dfs[(dfs['date'] >= start_date) & (dfs['date'] <= end_date)].shape[0]

print("\nNumber of emails sent during a given time:")
print(emails_in_given_time)