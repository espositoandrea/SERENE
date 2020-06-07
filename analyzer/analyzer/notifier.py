import logging
import json
import os

import requests

logger = logging.getLogger(__name__)


def notify(out_dir: str, to_email: str):
    url = "https://api.sendinblue.com/v3/smtp/email"

    with open('{}/report.log'.format(out_dir), "r") as f:
        log = f.read()
    content = f'''
    <html>
    <body>
        <p>Analisi e trasformazione dei dati completata. Di seguito, il file di log.</p>
        <pre><code>{log}</code></pre>
    </body>
    </html>
    '''
    payload = {
        'sender': {
            "email": "espositothesis@notifier.com",
            "name": "Esposito's Thesis"
        },
        "to": [
            {
                "email": to_email
            }
        ],
        "htmlContent": content,
        "subject": "Completamento analisi e trasformazione"
    }
    headers = {
        'accept': "application/json",
        'content-type': "application/json",
        'api-key': os.getenv('SENDINBLUE_API_KEY')
    }

    response = requests.post(url, data=json.dumps(payload), headers=headers)
    logger.info("Sent email notification. Response: %s", response.text)
