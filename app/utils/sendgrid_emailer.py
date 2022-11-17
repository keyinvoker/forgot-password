from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from app import session, app_logger, error_logger
from app.config import SENDER, BUCKET_DOWNLOAD_PUBLIC_URL, SENDGRID_API_KEY
from app.models import Inquiry, InquiryDetails
from app.schemas import InquiryDetailsSchema

def send_email_with_sendgrid(inquiry_id):
    inquiry = session.query(Inquiry).filter_by(id=inquiry_id).first()

    subject = 'Data Peminjam'
    recipient = inquiry.requester
    filename = f'file{ inquiry.id }.csv'
    download_link = BUCKET_DOWNLOAD_PUBLIC_URL + filename

    message = Mail(
        from_email=SENDER,
        to_emails=recipient,
        subject=subject,
        html_content=f'''
            <p>Your data has arrived!</p>
            <p>File name: <b>{ inquiry.name }</b></p>
            <br>
            <div style="margin-bottom:10px;">
                <a href={ download_link } style="text-decoration:none;color:white;background-color:green;border:1px solid green;border-radius:5px;padding:8px;">
                    DOWNLOAD
                </a>
            </div>
            '''
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        app_logger.info('Email sent with SendGrid:', response.status_code, response.body, response.headers)
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