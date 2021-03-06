# Copyright (c) 2014, Matt Makai
# All rights reserved.
# Full License can be read here: http://bit.ly/1qBgqzn

import cgi
from flask import render_template, abort, request
from jinja2 import TemplateNotFound
from twilio import twiml
from twilio.rest import TwilioRestClient

from .config import TWILIO_NUMBER

from . import app, redis_db, socketio

client = TwilioRestClient()


@app.route('/<presentation_name>/', methods=['GET'])
def landing(presentation_name):
    try:
        return render_template(presentation_name + '.html')
    except TemplateNotFound:
        abort(404)

@app.route('/nasa/twilio/webhook/', methods=['POST'])
def twilio_callback():
    to = request.form.get('To', '')
    from_ = request.form.get('From', '')
    message = request.form.get('Body', '').lower()
    if to == TWILIO_NUMBER:
        redis_db.incr(cgi.escape(message))
        socketio.emit('msg', {'div': cgi.escape(message),
                              'val': redis_db.get(message)},
                      namespace='/nasa')
    resp = twiml.Response()
    resp.message("Thanks for your vote! For contact info, links about Ansible or this presentation, please go here: http://bit.ly/1tAGcyo")
    return str(resp)
