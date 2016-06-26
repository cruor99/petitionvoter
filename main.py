#!/usr/bin/env python

#https://github.com/saippuakauppias/temp-mail/blob/master/tempmail.py
import tempmail

import mechanize, time, re
import random, string


def genname():
    length = random.randint(3, 12)
    s = ''
    while len(s) < length:
        s += random.choice(string.lowercase)
    return s


def doit():
    print 'Generating TempMail...'
    tm = tempmail.TempMail()
    email = tm.get_email_address()

    url = 'https://petition.parliament.uk/petitions/131215/signatures/new'

    name = genname() + ' ' + genname()
    postcode = 'SW1A 0AA'

    print 'Signing as %s / %s (%s)' % (name, email, postcode)

    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open(url)
    br.form = list(br.forms())[0]

    c = br.form.find_control(type="checkbox")
    c.value = ['1']
    br.form['signature[name]'] = name
    br.form['signature[email]'] = email
    br.form['signature[location_code]'] = ['GB']
    br.form['signature[postcode]'] = postcode

    response = br.submit()
    html = response.read()
    #with open('temp.html', 'w') as f: f.write(html)

    badness = ["Postcode not recognised", "disposable email address"]

    for x in badness:
        if x in html:
            print x
            print 'Fuck.'
            exit()

    br.form = list(br.forms())[0]
    print 'Confirming...'
    response = br.submit()
    html = response.read()

    while True:
        print 'Checking mail...'
        mb = tm.get_mailbox(email)
        if not 'error' in mb:
            html = mb[0]['mail_html']
            url = re.search('<p><a href="(.*?)">', html).group(1)
            break
        time.sleep(1)

    print 'Validating %s' % url
    response = mechanize.urlopen(url)
    html = response.read()
    #with open('temp2.html', 'w') as f: f.write(html)
    sigs = re.search('<h1 class="visuallyhidden">(.*?) signatures</h1>',
                     html).group(1)
    print '%s total signatures' % sigs


while True:
    doit()
