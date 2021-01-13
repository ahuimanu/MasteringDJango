from django.core.paginator import Paginator
from django.http import FileResponse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.response import TemplateResponse

import calendar
from calendar import HTMLCalendar
import csv
from datetime import date
import io
import logging

from reportlab.lib import pagesizes
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

from .models import Event, MyClubUser, Venue
from .forms import VenueForm

# get a logger
logger = logging.getLogger(__name__)

# Create your views here.
def index(request, year=date.today().year, month=date.today().month):

    # usr = request.user
    # ses = request.session
    # path = request.path
    # path_info = request.path_info
    # headers = request.headers

    year = int(year)
    month = int(month)
    logger.info(f"year: {year}")
    logger.info(f"month: {month}")
    month_name = calendar.month_name[month]

    if year < 2000 or year > 2099:
        year = date.today().year
        month_name = calendar.month_name[month]

    title = f"My Club Event Calendar - {month_name} {year}"
    cal = HTMLCalendar().formatmonth(year, month)
    announcements = [
        {
            "date": "12-21-2020",
            "announcement": "Christmas is here",
        },
        {
            "date": "12-22-2020",
            "announcement": "Be of good cheer",
        },
    ]
    # return HttpResponse(f"<h1>{title}</h1><p>{cal}</p>")
    # return render(
    #     request,
    #     "events/calendar_base.html",
    #     {"title": title, "cal": cal, "announcements": announcements},
    # )
    return TemplateResponse(
        request,
        "events/calendar_base.html",
        {"title": title, "cal": cal, "announcements": announcements},
    )


def all_events(request):
    event_list = Event.objects.all()
    return render(request, "events/event_list.html", {"event_list": event_list})


def add_venue(request):
    submitted = False
    if request.method == "POST":
        form = VenueForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/add_venue/?submitted=True")
    else:
        form = VenueForm()
        if "submitted" in request.GET:
            submitted = True

    return render(
        request, "events/add_venue.html", {"form": form, "submitted": submitted}
    )


def gen_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="venues.csv"'
    writer = csv.writer(response)
    venues = Venue.venues.all()
    writer.writerow(["Venue Name", "Address", "Phone", "Email"])
    for venue in venues:
        writer.writerow([venue.name, venue.address, venue.phone, venue.email_address])

    return response


def gen_pdf(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica-Oblique", 14)
    lines = [
        "green eggs and ham\n",
        "green eggs and spam\n",
        "green eggs and flan\n",
    ]
    for line in lines:
        textob.textLine(line)
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename="bart.pdf")


def get_text(request):
    response = HttpResponse(content_type="text/plain")
    response["Content-Disposition"] = 'attachment; filename="bart.txt"'
    lines = [
        "green eggs and ham\n",
        "green eggs and spam\n",
        "green eggs and flan\n",
    ]
    response.writelines(lines)
    return response


def list_subscribers(request):
    p = Paginator(MyClubUser.objects.all(), 3)
    page = request.GET.get('page')
    subscribers = p.get_page(page)
    return render(request,
        'events/subscribers.html',
        {'subscribers': subscribers}
    )

