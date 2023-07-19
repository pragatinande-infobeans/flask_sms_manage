from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import current_user, login_required
from smsmanagement import db
from smsmanagement.models import Group
from smsmanagement.groups.forms import GroupForm

groups = Blueprint('groups', __name__)


@groups.route('/groupManage')
@login_required
def groupManage():
    list_groups = Group.query.order_by(Group.date.desc()).all()
    print(list_groups)
    return render_template('groupManage.html', list_groups=list_groups)


# Group creation route
@groups.route('/create_group', methods=['GET', 'POST'])
@login_required
def create_group():
    form = GroupForm()
    if form.validate_on_submit():
        group_post = Group(group_name=form.group_name.data,
                           group_description=form.group_description.data,
                           user_id=current_user.id
                           )
        db.session.add(group_post)
        db.session.commit()
        flash("Group created successfully!")
        return redirect(url_for('groups.groupManage'))

    # Render the group creation form
    return render_template('create_group.html', form=form)


@groups.route("/<int:group_id>/delete", methods=['POST'])
@login_required
def delete_group(group_id):
    blog_post = Group.query.get_or_404(group_id)

    db.session.delete(blog_post)
    db.session.commit()
    flash('Group has been deleted')
    return redirect(url_for('contacts.userContactManage'))


@groups.route("/<int:group_id>/update", methods=['GET', 'POST'])
@login_required
def update(group_id):
    group_post = Group.query.get_or_404(group_id)

    form = GroupForm()
    if form.validate_on_submit():
        group_post.group_name = form.group_name.data
        group_post.group_description = form.group_description.data
        db.session.commit()
        flash('Group Updated')
        return redirect(url_for('groups.groupManage'))

    # the old text and title.
    elif request.method == 'GET':
        form.group_name.data = group_post.group_name
        form.group_description.data = group_post.group_description
    return render_template('create_group.html', title='Update',
                           form=form)
