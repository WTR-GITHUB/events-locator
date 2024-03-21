import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URI"
    ) or "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# <ul>
#         {% for item in distance_with_names %}
#         <li>{{ item.city_name }}: {{ item.distance }} {% endblock %}</li>
#         {% endfor %}
#     </ul>
