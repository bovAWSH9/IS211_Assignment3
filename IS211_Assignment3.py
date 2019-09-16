#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""IS211_Assignment3_Tomasz_Lodowski"""

import urllib.request
import csv
import re
import sys

def download_web_log_file(url):
    """Download the csv file"""
    with urllib.request.urlopen(url) as response:
        with open("weblog.csv", 'wb') as web_log_file:
            data = response.read()
            web_log_file.write(data)

def process_file(file_name):
    """Process the data in list"""
    data = []
    with open(file_name) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            data.append(row)

    return data

def get_images_hits(data):
    """Get count of image hits"""
    number_of_image_hits = 0
    for row_data in data:

        if len(re.findall(r".*\.(gif|png|jpg|jpeg|GIF|PNG|JPG|JPEG)", row_data[0])) == 1:
            number_of_image_hits += 1

    percent = (1.0 * number_of_image_hits / len(data)) * 100.0
    print("Image requests account for {:.1f}% of all requests".format(percent))

def find_most_popular_browser(data):
    """Find most popular browser by counting his hits and choose highest one"""
    chrome_hits = 0
    firefox_hits = 0
    safari_hits = 0
    internet_explorer_hits = 0
    for row_data in data:
        """Find if string contains once of browsers"""
        if len(re.findall(r".*(Chrome).*", row_data[2])) == 1:
            chrome_hits += 1
        elif len(re.findall(r".*(Firefox).*", row_data[2])) == 1:
            firefox_hits += 1
        elif len(re.findall(r".*(Safari).*", row_data[2])) == 1:
            safari_hits += 1
        elif len(re.findall(r".*(InternetExplorer).*", row_data[2])) == 1:
            internet_explorer_hits += 1

    browsers_hits = [(chrome_hits, "Chrome"), (firefox_hits, "Firefox"),
                     (safari_hits, "Safari"), (internet_explorer_hits, "Internet Explorer")]

    browsers_hits = sorted(browsers_hits, reverse=True)
    print("Most Popular Browser is", browsers_hits[0][1])

def total_number_of_hits_for_each_hour(data):
    """Count the hits for the 24 hour"""
    hours_hits = []
    for i in range(0, 24):
        hours_hits.append(0)

    for row_data in data:
        date_time = row_data[1]
        time = date_time.split(' ')[1]
        hour = time.split(':')[0]
        hours_hits[int(hour)] += 1

    """Print the hits for each hour"""
    for hour in range(0, 24):
        print("Hour %02d" % hour + " has " + str(hours_hits[hour]) + " hits")

def main():
    """Testign URL"""
    """https://filebin.net/js5vfdwy202rwkll/weblog.csv?t=m61680p5"""
    if len(sys.argv) == 2:
        url = sys.argv[1]
        download_web_log_file(url)
        data = process_file('weblog.csv')
        get_images_hits(data)
        find_most_popular_browser(data)
        total_number_of_hits_for_each_hour(data)

main()