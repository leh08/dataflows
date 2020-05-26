from flask import redirect
from flask_restful import Resource

from models.confirmation import ConfirmationModel
from services.locales import gettext


class Confirmation(Resource):
    @classmethod
    def get(cls, confirmation_id: str):
        confirmation = ConfirmationModel.find_by_id(confirmation_id)
        
        if not confirmation:
            return {"message": gettext("confirmation_not_found")}, 404
        
        if confirmation.expired:
            return {"message": gettext("confirmation_link_expired")}, 400
        
        if confirmation.confirmed:
            return {"message": gettext("confirmation_already_confirmed")}, 400
        
        confirmation.confirmed = True
        confirmation.save_to_db()
        
        return {"message": gettext("confirmation_confirmed")}