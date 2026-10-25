# District Clone

A going-out and lifestyle web app built with Django. Users add money to a wallet and book slots at venues. Organizations list events and slots.

This is Phase 1 of the DVM Backend Round 2 task (Basic track).

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

1. Sign up at `/accounts/signup/`. New users join the **Customers** group and get a wallet with balance 0.
2. Add money at `/accounts/add-money/`. The form is fake, so no real payment happens.
3. Browse events at `/events/`, open one, and click **Book** on a slot. One click books one place.
4. See your tickets at `/events/my-tickets/` and your history at `/accounts/transactions/`.

### Creating events (through the admin, for now)

1. Log in to `/admin/` as the superuser.
2. Create a user for the organization and add it to the **Organizations** group.
3. Under Events, create an **Organization** linked to that user.
4. Create an **Event**, then add **Slots** to it with a start time, end time, and capacity.

The organization dashboard is part of Phase 2.

## Pages

| URL | Purpose |
|---|---|
| `/accounts/signup/` | create an account |
| `/accounts/login/` | log in |
| `/accounts/dashboard/` | balance and links |
| `/accounts/add-money/` | top up the wallet |
| `/accounts/transactions/` | timestamped history |
| `/events/` | active events |
| `/events/<id>/` | one event with its slots |
| `/events/my-tickets/` | active tickets |

## Models and relationships

```
Group -- User -- Profile
          |  \
          |   Transaction
          |
          +-- Ticket -- Slot -- Event -- Organization -- User
```

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
- **`select_for_update()` locks the slot and the wallet**, so two requests can't take the last place or spend the same money. SQLite ignores this lock, and it takes effect once PostgreSQL is in place.
- **Ticket IDs are UUIDs**, so they can't be guessed.
- **`Ticket.slot` uses `PROTECT`**, so a slot with paid tickets can't be deleted by accident.
- **A signal creates a wallet** for every new user.
- **Pages require login**, and each user only sees their own tickets and transactions.
- **Events can be switched off** with `is_active`, without deleting their bookings.

## Not done yet

- Organization dashboard, marking tickets as consumed, and analytics (Phase 2)
- PostgreSQL, uv, Docker, Gunicorn, Nginx, and hosting (Phase 3)
- Booking does not yet refuse slots that have already started
- Group checks: the Customers and Organizations groups exist, but pages don't restrict by group yet