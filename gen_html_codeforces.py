#!/usr/bin/python2.7 -S

#import sys #was for debugging
#sys.setdefaultencoding("utf-8")
import site

from os import listdir
from os.path import isfile, join
from random import randint
from unidecode import unidecode

from BeautifulSoup import BeautifulSoup
import datetime
import urllib2
    
def get_problem_html(prob_code):
    # currently only grabs from codeforces
    judge_site = 'http://codeforces.com/'
    request_param = 'problemset/problem/{}/{}'.format(prob_code[0], prob_code[1])

    # get HTML for problem
    req = urllib2.Request(judge_site + request_param)
    response = urllib2.urlopen(req)
    html_code = response.read()

    # extract and find problem statement with BeautifulSoup (beautiful!)
    soup = BeautifulSoup(html_code) 
    problem_html = soup.find('div', {'class': 'problem-statement'})

    # really bad. prints to html of page
    print '<div>Problem taken from <a href="{0}">here</a></div>'.format(judge_site + request_param)
    print '<hr>'

    print unidecode(str(problem_html).decode('utf-8', 'ignore'))

# preliminary stuff to make site look ok
print '<!DOCTYPE html>'
print '<html>'

print '<head>'

print '<title>500pauls.com</title>'
print '<meta http-equiv="Content-type" content="text/html;charset=UTF-8">'
print '<link rel="stylesheet" href="http://netdna.bootstrapcdn.com/bootstrap/3.0.3/css/bootstrap.min.css">'
print '<link rel="stylesheet" href="http://netdna.bootstrapcdn.com/bootstrap/3.0.3/css/bootstrap-theme.min.css">'
print '<link charset="utf-8" href="http://worker.codeforces.ru/static/combine/532a51f3e21ab4661013f28aa2665e53_429c63982abfce9ee19b92499fdeb13f.css" rel="stylesheet" type="text/css">'
print '</head>'

print '<body class="container">'
print '<h1 class="page-header">Daily Codeforces</h1>'

# open saved problems
with open('used_problems.txt', 'a+') as ufile:
    used_probs = set(eval(line) for line in ufile.readlines())

    # choose a random problem 
    max_set, max_prob = 427, 4
    while True:
        try:
            prob_code = (randint(1, max_set), chr(randint(0, max_prob) + 65))

            if prob_code in used_probs:
                raise Exception('This code is terrible.')

            get_problem_html(prob_code)
            ufile.write(str(prob_code) + '\n')
            break
        except:
            pass


    print '<hr>'

print '<script type="text/javascript" src="https://code.jquery.com/jquery.js"></script>'
print '<script type="text/javascript" src="js/bootstrap.min.js"></script>'
print '</body>'
print '</html>'

