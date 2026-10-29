# District Clone

A going-out and lifestyle web app built with Django. Users add money to a wallet and book slots at venues. Organizations create events and slots, see who bought tickets, mark tickets as used, and see sales.

This is Phase 2 of the DVM Backend Round 2 task (Basic track).

## Tech

- Python 3 and Django 4.2
- SQLite for now. PostgreSQL is planned for Phase 3.

## How to run

```
git clone https://github.com/pagan-min2/district-clone.git
cd district-clone
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver
```

Open http://127.0.0.1:8000/

## How to use

### As a customer

1. Sign up at `/accounts/signup/`. New users join the **Customers** group and get a wallet with balance 0.
2. Add money at `/accounts/add-money/`. The form is fake, so no real payment happens.
3. Browse events at `/events/`, open one, and click **Book** on a slot. One click books one place.
4. See your tickets at `/events/my-tickets/` and your history at `/accounts/transactions/`.

### As an organization

1. Log in to `/admin/` as the superuser.
2. Create a user for the organization and add it to the **Organizations** group.
3. Under Events, create an **Organization** linked to that user.
4. Log in on the site as that user. The dashboard shows an **Organization dashboard** link.
5. From the organization dashboard you can create events, add slots, see the tickets for each event, mark tickets as consumed, and open analytics.

## Pages

| URL | Purpose | Who |
|---|---|---|
| `/accounts/signup/` | create an account | anyone |
| `/accounts/login/` | log in | anyone |
| `/accounts/dashboard/` | balance and links | logged in |
| `/accounts/add-money/` | top up the wallet | logged in |
| `/accounts/transactions/` | timestamped history | logged in |
| `/events/` | active events | logged in |
| `/events/<id>/` | one event with its slots | logged in |
| `/events/my-tickets/` | active tickets | logged in |
| `/events/org/` | the organization's events | organizations |
| `/events/org/events/new/` | create an event | organizations |
| `/events/org/events/<id>/slots/new/` | add a slot to an event | the event's organization |
| `/events/org/events/<id>/tickets/` | tickets sold for an event | the event's organization |
| `/events/org/tickets/<id>/consume/` | mark a ticket as used (POST) | the ticket's organization |
| `/events/org/analytics/` | tickets sold and revenue per event | organizations |

## Models and relationships

| Model | Holds | Relationship | Why |
|---|---|---|---|
| Profile | wallet balance | one-to-one with User | each user has exactly one wallet |
| Transaction | one money movement, credit or debit | many per User | a timestamped history, kept separate from the balance |
| Organization | a business | one-to-one with User | each organization has exactly one login |
| Event | what is on offer | many per Organization | an organization runs many events |
| Slot | a time window with a capacity | many per Event | a turf has many hourly slots, and a concert has one |
| Ticket | one purchase | many per User and many per Slot | records who bought which slot, with a unique ID |

Slot-based events (a turf) and ticket-based events (a concert) share one Event table, and the `kind` field tells them apart. A concert is an event with a single slot.

## Design decisions

- **Money uses `DecimalField`**, not floats, so amounts are exact.
- **Booking runs inside `transaction.atomic()`.** The slot count, the wallet, the receipt, and the ticket all save together, or none of them do.
- **`select_for_update()` locks the slot and the wallet** when booking, and the ticket when marking it consumed, so two requests can't take the last place, spend the same money, or consume a ticket twice. SQLite ignores this lock, and it takes effect once PostgreSQL is in place.
- **Ticket IDs are UUIDs**, so they can't be guessed.
- **`Ticket.slot` uses `CASCADE`**, so deleting a slot also deletes its tickets.
- **A signal creates a wallet** for every new user.
- **Organization pages need two things**: membership of the **Organizations** group and an Organization row. Anyone else gets a 403.
- **Ownership checks**: an organization can only see and change its own events, slots and tickets. Anything else returns a 404.
- **Changing data needs a POST**: booking and marking a ticket consumed can't happen through a plain link.
- **Analytics** counts tickets and adds up revenue per event in one query with `annotate`, `Count` and `Sum`.
- **Events can be switched off** with `is_active`, without deleting their bookings.

## Not done yet

- PostgreSQL, uv, Docker, Gunicorn, Nginx, and hosting (Phase 3)
