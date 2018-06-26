#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Enviar correo Gmail con Python
import configparser
import getopt
import smtplib
import sys

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

messageHtml = '<h1> Correo enviado utilizando Python  sendMailZip.py</h1>'

# Datos
config = configparser.ConfigParser()  # type: ConfigParser
config.read('sendMail.conf')

username = config['Mail_Auth']['LOGIN_USERNAME']
password = config['Mail_Auth']['LOGIN_PASSWORD']


def main(argv):
    inputfile = ''

    try:
        opts, args = getopt.getopt(argv, "hi:o", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print ('sendMail.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('Comando de ayuda')
        elif opt in ("-i", "--ifile"):
            print('sendMail...')
            inputfile = arg
            sendMail(inputfile)

    print ('Input file is "', inputfile)


def sendMail(file):
    # Modificación del nombre para que no envie la ruta completa del archivo
    filename = file.split('/')[-1]

    subject = 'Informes: %s' % filename

    # Creating email
    header = MIMEMultipart()

    header['Subject'] = subject
    header['To'] = toaddrs
    header['From'] = fromaddr
    header.attach(MIMEText(messageHtml, 'html'))

    zip = getZipFile(file, filename)
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


def getZipFile(file, filename):
    fp = open(file, 'rb')
    zip2 = MIMEBase('application', 'zip')
    zip2.set_payload(fp.read())
    zip2.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    fp.close()
    encoders.encode_base64(zip2)
    return zip2

if __name__ == "__main__":
    main(sys.argv[1:])
