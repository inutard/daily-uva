#!/usr/bin/python2.7 -S

#import sys #was for debugging
#sys.setdefaultencoding("utf-8")
import site

from pynliner import Pynliner
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


    output_html = unidecode(str(problem_html).decode('utf-8', 'ignore'))
    if output_html == 'None':
        return False
    
    # really bad. prints to html of page
    out.append('<div style="font-size: 14px">Problem taken from <a href="{0}" style="color: blue">here</a>.</div>'.format(judge_site + request_param))
    out.append('<hr>')
    out.append(output_html)
    
    return True

out = []
# preliminary stuff to make site look ok
out.append('<html>')

out.append('<head>')

out.append('<title>500pauls.com</title>')

css = []
ufile = open('codeforces.css')
for line in ufile.readlines():
    css.append(line)
css_string = '\n'.join(css)
	
out.append('</head>')

out.append('<body>')
out.append('<h1 style="font-size: 32px; font-weight:bold; margin-bottom: 0.3cm">Daily Codeforces</h1>')

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

            if not get_problem_html(prob_code):
                raise Exception('This code is terrible.')
                
            ufile.write(str(prob_code) + '\n')
            break
        except:
            pass


    out.append('<hr>')
    
out.append('</body>')
out.append('</html>')

preinline_html = '\n'.join(out)

final_p = Pynliner().from_string(preinline_html).with_cssString(css_string)
final_html = final_p.run()

print final_html
