from database import DB

db_dns = "postgresql://postgres:password@localhost:5432/tochkarosta"

db = DB(db_dns)

template_images = "{% for image in images %}" \
                  "<div class='col-12 col-sm-6 col-md-4 p-2'>" \
                  "<div class='card d-flex flex-column height100'>" \
                  "<img src='/static/images/news/{{image}}' class='card-img img-fluid zoom-img'>" \
                  "</div>" \
                  "</div>" \
                  "{% endfor %}"