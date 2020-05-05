# Create your views here.

from .models import *


def index(request):
    data = Country.objects.Last()

    stu = {
        "Country": data
    }
    return render_to_response("database/mainpage.html", stu)
