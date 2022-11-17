import ssl, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app import session, app_logger, error_logger
from app.config import SENDER, SERVER, PORT, PASSWORD, BUCKET_DOWNLOAD_PUBLIC_URL
from app.models import Inquiry, InquiryDetails
from app.schemas import InquiryDetailsSchema

def send_email(inquiry_id):
    inquiry = session.query(Inquiry).filter_by(id=inquiry_id).first()

    recipient = inquiry.requester
    filename = f'file{ inquiry.id }.csv'
    download_link = BUCKET_DOWNLOAD_PUBLIC_URL + filename

    context = ssl.create_default_context()
    em = MIMEMultipart()
    em['From'] = SENDER
    em['To'] = recipient
    em['Subject'] = 'Data Peminjam'
    content = f'''
        <p>Your data has arrived!</p>
        <p>File name: <b>{ inquiry.name }</b></p>
        <br>
        <div style="margin-bottom:10px;">
            <a href={ download_link } style="text-decoration:none;color:white;background-color:rgb(28,140,68);border:1px solid rgb(28,140,68);border-radius:5px;padding:8px;">
                DOWNLOAD
            </a>
        </div>
        '''
    body = MIMEText(content, 'html')
    em.attach(body)

    try:
        with smtplib.SMTP_SSL(SERVER, PORT, context=context) as smtp:
            smtp.login(SENDER, PASSWORD)
            smtp.sendmail(SENDER, recipient, em.as_string())
            app_logger.info(f'Email sent to { recipient }')
        del em
    except Exception as e:
        error_logger.exception(e)

    inquiry.status = 'sent'
    inquiry.update()
    inquiry_details_schema = InquiryDetailsSchema(many=True)
    all_inquiry_details = session.query(InquiryDetails).filter_by(inquiry_id=inquiry.id).all()
    inquiry_details = inquiry_details_schema.dump(all_inquiry_details)
    for details in inquiry_details:
        current_inquiry_details = session.query(InquiryDetails).filter_by(id=details['id']).first()
        current_inquiry_details.status = 'sent'
        current_inquiry_details.update()