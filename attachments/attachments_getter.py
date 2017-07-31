import os
import logging


def save_attachments(msg):
    """

    :param msg: a Python Message object
    :return: true if the file is closed
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    logger.info("Subject: %s, From: %s, To: %s",
                msg['subject'], msg['from'], msg['to'])

    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            # print part.as_string()
            continue
        if part.get('Content-Disposition') is None:
            # print part.as_string()
            continue
        fileName = part.get_filename()

        if bool(fileName):
            filePath = os.path.join('./attachments_files/', fileName)
            if not os.path.isfile(filePath):
                print fileName
                fp = open(filePath, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()

    return fp.closed
