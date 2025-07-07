import re
import random

class Dataset_Creation:

    def extract_content(self, email):
        match = re.search("Subject:(.*)", email, flags=re.IGNORECASE)
        if match:
            return match.group(1)
        return None

    def spam_normal_extraction(self, emails_dataset2):
        spam_emails = []
        normal_emails = []

        for mail in emails_dataset2:
            mail = mail.strip('\n').split('",')  # Split string on ", to separate mail and its label
            mail_obj = re.search('Subject:(.*)', mail[0], flags=re.IGNORECASE)
            unique_spam = len(set(spam_emails))
            unique_normal = len(set(normal_emails))

            if mail_obj is not None:
                mail_string = mail_obj.group(1).replace('"', "'")  # Replace double quotes

                if len(mail_string) > 13000:
                    continue  # Skip long emails

                if mail[-1] == '1' and unique_spam < 1000:
                    spam_emails.append(('SPAM', mail_string))
                elif mail[-1] == '0' and unique_normal < 1000:
                    normal_emails.append(('NORMAL', mail_string))

            if unique_spam == 1000 and unique_normal == 1000:
                break

        print('--', len(set(spam_emails)), 'Spam Emails Found --')
        print('--', len(set(normal_emails)), 'Normal Emails Found --')
        return spam_emails, normal_emails

    def generate_csv_file(self, email_list):
        with open('Datasets/final_dataset.csv', 'w', encoding='utf-8') as file:
            file.write('"CATEGORY","CONTENT"\n')
            for email in email_list:
                category = email[0]
                content = email[1].replace(',', ' ').replace('\n', ' ')
                file.write(f'"{category}","{content}"\n')
        print("\n✅ Final dataset created at: Datasets/final_dataset.csv")


# ------------------------ MAIN PROGRAM ------------------------

valid_emails = []
print('DATASET = FRAUD EMAILS')
print('----------------------')

create_dataset = Dataset_Creation()

# Read fraud emails
with open('Datasets/fradulent_emails.txt', 'r', encoding='utf-8', errors='ignore') as f:
    emails_dataset = f.read()

email_list = emails_dataset.split('From r')

for email in email_list:
    email_content = create_dataset.extract_content(email)
    if email_content is not None:
        single_line_email = email_content.replace('\n', ' ')
        if 100 < len(single_line_email) < 13000:
            valid_emails.append(('FRAUD', single_line_email.replace('"', '')))
            if len(set(valid_emails)) == 1000:
                break

fraud_emails = set(valid_emails)
print('--', len(fraud_emails), 'Fraud Emails Found --')

print('\nDATASET = SPAM AND NORMAL EMAILS')
print('-------------------------')

with open('Datasets/emails.csv', 'r', encoding='utf-8', errors='ignore') as f:
    emails_dataset2 = f.readlines()

spam_emails, normal_emails = create_dataset.spam_normal_extraction(emails_dataset2)

all_emails = list(fraud_emails) + list(set(spam_emails)) + list(set(normal_emails))
random.shuffle(all_emails)

create_dataset.generate_csv_file(all_emails)