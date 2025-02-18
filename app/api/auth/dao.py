from app.api.dao import BaseDAO
from app.models.models import Users


class UsersDAO(BaseDAO):
    model = Users