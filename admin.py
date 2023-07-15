from flask_admin.contrib.sqla import ModelView
from flask import session, url_for, redirect, request, flash
from flask_login import current_user


class AdminView(ModelView):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.static_folder = 'static'
        
    def is_accessible(self):
        return current_user.is_authenticated and current_user.username == 'Chrisl2324'

    def inaccessible_callback(self, name, **kwargs):
        if not self.is_accessible:
            return redirect(url_for('index'))
        
class UserAdminView(AdminView):
    column_exclude_list = ['password_hash']
    def on_model_delete(self, model):
        try:
            # Perform the deletion operation on the model
            self.session.delete(model)
            self.session.commit()
        except Exception as e:
            flash('Error deleting record.', 'error')
            self.session.rollback()
            raise e
    
class ArticleAdminView(AdminView):
    def on_model_delete(self, model):
        try:
            self.session.delete(model)
            self.session.commit()
        except Exception as e:
            flash('Error deleting record.', 'error')
            self.session.rollback()
            raise e
        
    def on_model_change(self, form, model, is_created):
        try:
            model.user_id = current_user.id
            self.session.add(model)
            self.session.commit()
            flash('Record saved successfully.', 'success')
        except Exception as e:
            flash('Error saving record.', 'error')
            self.session.rollback()
            raise e

class CommentAdminView(AdminView):
    def on_model_delete(self, model):
        try:
            self.session.delete(model)
            self.session.commit()
        except Exception as e:
            flash('Error deleting record.', 'error')
            self.session.rollback()
            raise e

        