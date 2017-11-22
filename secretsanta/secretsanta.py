import itertools
import json
import random
import smtplib

def smtp_init(smtp_info):
    smtp_obj = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_obj.starttls()
    smtp_obj.login(smtp_info['email_address'], smtp_info['app_specific_password'])
    return smtp_obj

def smtp_send(smtp_obj, smtp_info, email_recipient, email_recipient_name, secret_santa_recipient):
    smtp_obj.sendmail(smtp_info['email_address'],
                      email_recipient,
                      ('Subject: SECRET SANTA\n'
                       'Hi {},\n\n'
                       'You\'ll be purchasing a gift for {}.\n\n'
                       'Merry Christmas!'
                       .format(email_recipient_name, secret_santa_recipient)))

def smtp_quit(smtp_obj):
    smtp_obj.quit()

if __name__ == '__main__':
    print('Reading data...')
    with open('secretsanta.json', 'r') as f:
        config = json.load(f)
    email_dict = config['participants']
    smtp_info = config['smtp_info']
    participants = [x for x in email_dict]
    if len(participants) <= 1:
        raise IndexError('There must be at least two participants.')
    print('Generating permutations...')
    permutations = list(itertools.permutations(participants))
    random.shuffle(permutations)
    recipients = None
    print('Finding an acceptable permutation...')
    for permutation in permutations:
        for index, _ in enumerate(permutation):
            found = True
            if permutation[index] == participants[index]:
                found = False
                break
        if found:
            recipients = permutation
            break
    print('Emailing results...')
    smtp_obj = smtp_init(smtp_info)
    for index, participant in enumerate(participants):
        smtp_send(smtp_obj, smtp_info, email_dict[participant], participant, recipients[index])
    smtp_quit(smtp_obj)
    print('All done!')
