from flask_mail import Message


class FMSG():
    def __init__(self):
        self.msg = Message(sender=' ')

    def set_sender(self, sender):
        self.msg.sender = sender

    def set_recipient(self, recipients):
        self.msg.recipients = recipients

    def welcome(self):
        self.msg.subject = "welcome"
        self.msg.body = "Hello from OTP-Semaphore"
        self.msg.html = '<h1>HTML body</h1>'
        return self.msg

    def send_code(self, code):
        self.msg.subject = "OTP-Semaphore: Identification Code"
        self.msg.body = "Hello, please enter the code: "+ code
        return self.msg
