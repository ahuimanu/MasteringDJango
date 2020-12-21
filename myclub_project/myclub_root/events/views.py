from django.shortcuts import render
from django.http import HttpResponse
from datetime import date
import calendar
from calendar import HTMLCalendar
import logging

from .models import Event

# get a logger
logger = logging.getLogger(__name__)

# Create your views here.
def index(request, year=date.today().year, month=date.today().month):
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
    return render(
        request,
        "events/calendar_base.html",
        {"title": title, "cal": cal, "announcements": announcements},
    )


def all_events(request):
    event_list = Event.objects.all()
    return render(request, "events/event_list.html", {"event_list": event_list})
