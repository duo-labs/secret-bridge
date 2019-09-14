from github import Github, Event
from flask import Flask, request, abort
from urllib.parse import urlparse

import hmac
import hashlib
import logging
import json

from processor import Processor
from constants import (GITHUB_SIGNATURE_HEADER, GITHUB_EVENT_TYPE_HEADER,
                       WEBHOOK_PUSH_EVENT_TYPE)


def verify_signature(secret, request):
    """Verifies the provided HMAC SHA1 signature.

    This verifies that not only is an X-Hub-Signature header provided, but also
    that the provided signature matches the request body and the configured
    HMAC secret.

    Arguments:
        secret {str} -- The HMAC secret
        request {flask.request} -- The HTTP request received
    """
    if not secret:
        logging.error('No HMAC secret configured.')
        return False
    secret = secret.encode()

    # Verify that the X-Hub-Signature header is provided
    signature_header = request.headers.get(GITHUB_SIGNATURE_HEADER)
    if not signature_header:
        logging.error('No {} header provided'.format(GITHUB_SIGNATURE_HEADER))
        return False

    signature_parts = signature_header.split('=')
    if len(signature_parts) < 2 or signature_parts[0] != "sha1":
        return False
    signature = signature_parts[1]

    # Verify that the received signature is valid
    digest = hmac.new(secret, request.data, hashlib.sha1).hexdigest()
    return hmac.compare_digest(signature, digest)


def generate_event(payload, type=WEBHOOK_PUSH_EVENT_TYPE):
    """Generates a PyGithub.Event object from a webhook event payload.

    This translation is needed since the data provided in the webhook is
    different than the format given in the Events API.

    Arguments:
        payload {dict} -- The webhook event payload
    """
    payload['repo'] = payload['repository']
    payload.pop('repository')

    payload['actor'] = payload['sender']
    payload.pop('sender')

    payload['type'] = type
    payload['repo']['url'] = 'https://api.github.com/repos/{}'.format(
        payload['repo']['full_name'])

    for commit in payload['commits']:
        commit['sha'] = commit['id']

    payload['payload'] = {'commits': payload['commits']}
    payload.pop('commits')

    return Github().create_from_raw_data(Event.Event, payload)


app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    event_type = request.headers.get(GITHUB_EVENT_TYPE_HEADER)
    if not event_type:
        abort(400, 'No event type specified')
        return

    if event_type != WEBHOOK_PUSH_EVENT_TYPE:
        logging.info('Ignoring event type: {}'.format(event_type))
        return ('', 204)

    secret = app.config.get('GITHUB_WEBHOOK_SECRET')
    if not verify_signature(secret, request):
        abort(400, 'Bad signature')
        return

    event = generate_event(request.json)
    Processor.process_event(event)
    return ('', 204)
