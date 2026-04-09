import datetime

from django.db import transaction

from db.models import Ticket, Order, User


@transaction.atomic
def create_order(tickets: list[dict], username: str, date: str = None):
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M')
        order.save()
    return [
        Ticket.objects.create(
            movie_session_id=ticket["movie_session"],
            order=order,
            row=ticket["row"],
            seat=ticket["seat"]
        ) for ticket in tickets]


def get_orders(
        username: str = None
):
    query_set = Order.objects.all()
    if username:
        query_set = query_set.select_related("user").filter(user__username=username)
    return query_set