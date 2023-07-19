from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_required
from smsmanagement import db
from smsmanagement.contacts import keys
from smsmanagement.models import Contact, Group
from smsmanagement.contacts.forms import ContactForm
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

contacts = Blueprint('contacts', __name__)


@contacts.route('/messageManage', methods=['GET', 'POST'])
def messageManage():
    list_contacts = Contact.query.order_by(Contact.date.desc()).all()
    list_groups = Group.query.order_by(Group.date.desc()).all()
    return render_template('messageManage.html', list_contacts=list_contacts,list_groups=list_groups)


@contacts.route('/userContactManage')
@login_required
def userContactManage():
    list_contacts = Contact.query.order_by(Contact.date.desc()).all()
    print(list_contacts)
    # return render_template('contacts.html', groups=groups)
    return render_template('userContactManage.html', list_contacts=list_contacts)


# Group creation route
@contacts.route('/create_contact_list', methods=['GET', 'POST'])
@login_required
def create_contact_list():
    form = ContactForm()
    form.set_group_choices([(group.id, group.group_name) for group in Group.query.all()])
    if form.validate_on_submit():
        contact_post = Contact(contact_name=form.contact_name.data,
                               contact_nos=form.contact_nos.data,
                               contact_email=form.contact_email.data,
                               group_id=form.group.data
                               )

        db.session.add(contact_post)
        db.session.commit()
        flash("Contact created successfully!")
        return redirect(url_for('contacts.userContactManage'))

    # Render the group creation form
    groups = Group.query.all()

    return render_template('create_contact_list.html', form=form, groups=groups)


@contacts.route("/<int:contact_id>/", methods=['POST'])
@login_required
def delete_contact(contact_id):
    contact_post = Contact.query.get_or_404(contact_id)
    print(contact_post)
    db.session.delete(contact_post)
    db.session.commit()
    flash('Contact has been deleted')
    return redirect(url_for('contacts.userContactManage'))


@contacts.route("/<int:contact_id>/update_contact", methods=['GET', 'POST'])
@login_required
def update_contact(contact_id):
    contact_post = Contact.query.get_or_404(contact_id)

    form = ContactForm()
    form.set_group_choices([(group.id, group.group_name) for group in Group.query.all()])
    if form.validate_on_submit():
        contact_post.contact_name = form.contact_name.data
        contact_post.contact_nos = form.contact_nos.data
        contact_post.contact_email = form.contact_email.data
        contact_post.group_id = form.group.data
        db.session.commit()
        flash('Contact Updated')
        return redirect(url_for('contacts.userContactManage'))

    # the old text and title.
    elif request.method == 'GET':
        groups = Group.query.all()
        form.contact_name.data = contact_post.contact_name
        form.contact_nos.data = contact_post.contact_nos
        form.contact_email.data = contact_post.contact_email
        form.group.data = contact_post.group.id

    return render_template('create_contact_list.html', title='Update',
                           form=form, groups=groups)


@contacts.route("/sendSMS", methods=['GET','POST'])
@login_required
def sendSMSContact():
    client = Client(keys.account_sid, keys.auth_token)
    print(client)
    group_id = request.form.get('group_id')
    contacts_list = Contact.query.filter_by(group_id=group_id).all()
    sms_text = request.form.get('sms_text')
    twilio_number = '+18148319047'
    for contact in contacts_list:
        contact_nos = '+91'+contact.contact_nos
        try:
            client.messages.create(body=sms_text, from_=twilio_number, to=contact_nos)
            print("SMS sent successfully!")
        except TwilioRestException as e:
            print(f"Error sending SMS: {e}")

    return render_template('index.html')


