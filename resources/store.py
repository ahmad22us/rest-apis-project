import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from resources.db import *
from schemas import StoreSchema
from models import StoreModel
from resources.db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blb = Blueprint("stores", __name__, description="Operations on stores")


@blb.route("/store/<int:store_id>")
class Store(MethodView):
    @blb.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

        # try:
        #     return stores[store_id]
        # except KeyError:
        #     abort(404, message="Store not found.")

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store Deleted"}
        # raise NotImplemented("Deleting a Store is not implemented.")
        # try:
        #     del stores[store_id]
        #     return {"message": "Store Deleted."}
        # except KeyError:
        #     abort(404, message="Store not found.")


@blb.route("/store")
class StoreList(MethodView):

    @blb.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()
        # return stores.values()
        # return {"stores": list(stores.values())}

    @blb.arguments(StoreSchema)
    @blb.response(200, StoreSchema)
    def post(self, store_data):
        # store_data = request.get_json()
        # if "name" not in store_data:
        #     abort(
        #         400,
        #         message="Bad request. Ensure 'name' is included in the JSON payload.",
        #     )
        # for store in stores.values():
        #     if store_data["name"] == store["name"]:
        #         abort(400, message=f"Store already exists.")
        #
        # store_id = uuid.uuid4().hex
        # store = {**store_data, "id": store_id}
        # stores[store_id] = store
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A store with that name already exists.",
            )
        except SQLAlchemyError:
            abort(500, message=f"An error occurred creating the store.{SQLAlchemyError}")
        return store, 201
