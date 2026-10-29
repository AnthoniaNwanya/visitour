# Booking Service

## Run

Install dependencies and configure `.env`:

```bash
pip install -r requirements.txt
cd src
uvicorn main:app --reload --port 8003
```

Set `DATABASE_HOST`, `DATABASE_PORT`, `DATABASE_NAME`, `DATABASE_USER`,
`DATABASE_PASSWORD`, and `AUTH_SECRET_KEY`. The auth secret must match
traveler_service. The shared PostgreSQL database must contain the `travelers`, `agencies`,
`tours`, `visa_applications`, and `visa_types` tables. Create the cart and
booking tables from `../CreateQueries/7_CreateBooking.sql` before starting the
service, followed by `../CreateQueries/8_CreatePayment.sql`. These are fresh
schema definitions; `IF NOT EXISTS` does not upgrade legacy booking tables.
The payment script adds `cart_id` and changes the amount column for an older
payments table, but existing payment rows are not associated with carts and
remain outside the new cart payment API. Migrate existing booking/payment data
before deploying against an existing database.

The API runs on port 8003. Open `/docs` for the interactive API reference.

## Cart and booking API

Authenticated booking and cart endpoints require a traveler bearer token; the
agency booking endpoints require an agency bearer token. IDs are read from the
verified token, never from the request body.

- All `/bookings` and `/carts` routes require a traveler token. The root
  health-check route is intentionally public.
- `POST /carts/items` adds a selected tour or visa application to the
  authenticated traveler's active cart. Send `booking_type` (`tour` or
  `visa`), the selected catalog `item_id`, and optionally `quantity`. The
  service reads the name and current unit price from the catalog; repeated
  selections of the same item increase its quantity.
- `GET /carts/` returns the active cart, its items, and its calculated
  `total_order_summary`.
- `PUT /carts/items/{item_id}` accepts only `quantity`. A quantity of zero
  removes the item; removing the final item deletes the cart.
- `DELETE /carts/items/{item_id}` removes an item and deletes the cart when it
  becomes empty.
- `POST /payments/` starts a payment for an active cart. Send `cart_id` and
  optionally `payment_method`; the server validates current item availability
  and prices and calculates the amount itself. It does not accept a client
  amount.
- `GET /payments/` lists the traveler's payments, and
  `GET /payments/{payment_id}` retrieves one payment.
- `PUT /payments/{payment_id}` updates a pending payment's
  `payment_method`, and/or sets its status to `paid`, `failed`, or `cancelled`.
  This is a manual/demo status update, not proof of money received. Marking it
  `paid` atomically creates the cart's bookings and checks out the cart.
- `DELETE /payments/{payment_id}` removes an unpaid payment. Deleting a pending
  payment reopens its cart. Paid payments cannot be deleted.
- `GET /bookings/` returns only the authenticated traveler's generated
  bookings.
- `GET /agency/bookings/tours` returns tour bookings belonging to the
  authenticated agency, including the traveler identity, booking reference,
  tour, quantity, price, and status.
- `GET /agency/bookings/visas` returns visa bookings belonging to the
  authenticated agency, including the traveler identity, booking reference,
  visa, quantity, processing fee, and status.

Agency booking endpoints require an agency bearer token. The agency ID is read
from that token; clients cannot select another agency by passing an ID.
Booking references and traveler IDs are read through the related `bookings`
record, so those values have one source of truth instead of being duplicated
on each service-booking row. A visa booking's `visa_id` identifies the
selected `visa_applications` row. `visa_type_id` belongs to the visa
application catalog only; it is not a column or reference in
`visa_bookings`.

This service does not receive or verify real money. For local/demo use, the
frontend can create a pending payment, display the returned server-calculated
amount, then update its status to `paid` to simulate success. That update
creates one booking header per cart item, inserts the corresponding
`tour_bookings` or `visa_bookings` detail row, deducts tour slots, and marks
the cart checked out in one database transaction. Do not expose the manual
`paid` update as real payment confirmation in production; replace it with a
verified payment-provider callback before accepting real payments.

The `abandoned` cart status currently has no automatic behavior: carts are
created as `active`, and there is no inactivity timeout, background job, or
traveler endpoint that changes a cart to `abandoned`. It is reserved for a
future expiration/cleanup policy.
