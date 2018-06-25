#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Enviar correo Gmail con Python

import smtplib
import sys
import getopt

from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64

fromaddr = 'xxxxxxxxxxxxx@gmail.com'
toaddrs = 'xxxxxxxxxxxxxx@xxxx.com'
messageHtml = '<h1> Correo enviado utilizano Python </h1>'

# Datos
username = 'xxxxxxxxxxxxxxx@gmail.com'
password = 'xxxxxxxxxx'

def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print ('sendMail.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            sendMail()
            print ('Comando de ayuda')

        elif opt in ("-i", "--ifile"):
            print('sendMail...')
            inputfile = arg
            sendMail(inputfile)
       
    print ('Input file is "', inputfile) 


def sendMail(file):
    subject = 'Asunto con nombre fichero: %s' % file

    print(file)

    # Creating email
    header = MIMEMultipart()

    header['Subject'] = subject
    header['To'] = toaddrs
    header['From'] = fromaddr
    header.attach(MIMEText(messageHtml, 'html'))

    fp = open(file, 'rb')
    zip = MIMEBase('application', 'zip')
    zip.set_payload(fp.read())
    zip.add_header('Content-Disposition', "attachment; filename= %s" % file)
    fp.close()
    encoders.encode_base64(zip)
    header.attach(zip)

    # Sending email
    print ('Cargando fichero...')
    print ('sending...')
    server = smtplib.SMTP('smtp.gmail.com:587')

    server.starttls()

    server.login(username, password)
    server.sendmail(fromaddr, toaddrs, header.as_string())
    print ('Succesfully sent email...')
    server.quit()

if __name__ == "__main__":
    main(sys.argv[1:])
