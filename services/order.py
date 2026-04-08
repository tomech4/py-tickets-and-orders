from django.db import transaction

from db.models import Ticket, Order, User


def create_order(tickets: list[dict], username: str, date: str = None):
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(
            user=user,
            created_at=date
        )
        generated_tickets = [
            Ticket(
                movie_session=ticket["movie_session"],
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            ) for ticket in tickets]
        return Ticket.objects.bulk_create(*generated_tickets)


def get_orders(
        username: str = None
):
    query_set = Order.objects.all()
    if username:
        query_set = query_set.select_related("user").filter(user__username=username)
    return query_set