#!/usr/bin/python2.7

from collections import Counter
from os import listdir
from os.path import isfile, join
import datetime
import random
import urllib2
import re

import sys #was for debugging

def get_problem_html(prob_code):
    # currently only grabs from uva
    judge_site = 'http://uva.onlinejudge.org/'
    request_param = 'index.php?option=onlinejudge&page=show_problem&problem={}'.format(prob_code)
    
    # get HTML files from index.php
    req = urllib2.Request(judge_site + request_param)
    response = urllib2.urlopen(req)
    html_code = response.read()

    # do crappy REGEX parsing to get actual problem location (inside an iframe)
    results = re.search(r'<iframe src="external/(\d+)/(\d+)\.html"', html_code)
    #print >> sys.stderr, "found... " + results.group(1) + " " + results.group(2)
    outer_folder, inner_folder = results.group(1), results.group(2)
    external_id = outer_folder + '/' + inner_folder
    
    # request actual problem
    req = urllib2.Request(judge_site + 'external/' + external_id + '.html')
    response = urllib2.urlopen(req)
    html_code = response.read()

    # dont want any of their meta stuff
    if "<body" in html_code.lower():
        results = re.search('<body.*?>(.+)</body>', html_code, flags=re.IGNORECASE|re.DOTALL)
        html_code = results.group(1)
        #print >> sys.stderr, results.group(1)

    # woo! two terrible replace statements to take care their css and fix internal links
    html_code = re.sub('src=["]*(\w+\.\w+)["]*',
                       r'src={}\1'.format(judge_site+'external/{}/'.format(outer_folder)),
                       html_code, flags=re.IGNORECASE)
    html_code = re.sub('<style.*>(.*)</style>', '', html_code, flags=re.IGNORECASE)

    # really bad. prints to html of page
    print 'Problem taken from <a href="{0}.html">here</a>'.format(judge_site + request_param)
    print '<hr>'
    
    return html_code
    
# preliminary stuff to make site look ok
print '<html>'
print '<head>'
print '<title>500pauls.com</title>'
print '<link rel="stylesheet" href="http://netdna.bootstrapcdn.com/bootstrap/3.0.3/css/bootstrap.min.css">'
print '<link rel="stylesheet" href="http://netdna.bootstrapcdn.com/bootstrap/3.0.3/css/bootstrap-theme.min.css">'
print '</head>'

print '<h1 class="page-header">Daily UVA</h1>'
print '<body class="container">'

min_prob, max_prob = 100, 4500


while True:
    try:
        prob_code = random.randint(min_prob, max_prob)
        print get_problem_html(prob_code)
        break
    except:
        pass



print '<small style="color:gray; font-variant: small-caps;"> Last updated: [' + str(datetime.date.today()) + '] </small>'
print '<hr>'

print '<script src="https://code.jquery.com/jquery.js"></script>'
print '<script src="js/bootstrap.min.js"></script>'
print '</body>'
print '</html>'

