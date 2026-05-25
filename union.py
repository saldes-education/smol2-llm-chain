from typing import Literal, Union
from dataclasses import dataclass

@dataclass
class EmailNotification:
    # The 'type' field is our DISCRIMINATOR (the tag)
    type: Literal["email"] = "email"
    email_address: str
    subject: str

@dataclass
class SMSNotification:
    type: Literal["sms"] = "sms"
    phone_number: str
    message: str


@dataclass
class WhatAppNotification:
    type: Literal["whatsapp"] = "whatsapp"
    user_name: str
    message: str

# Define the Union type
Notification = EmailNotification | SMSNotification | WhatAppNotification

# A function that handles the union cleanly using pattern matching
def send_notification(notification: Notification):
    # Python reads the 'type' tag and instantly jumps to the right case
    match notification.type:
        case "email":
            print(f"Sending email to {notification.email_address}: {notification.subject}")
        case "sms":
            print(f"Sending SMS to {notification.phone_number}: {notification.message}")