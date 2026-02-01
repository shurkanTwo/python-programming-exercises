from datetime import datetime, date


class Event:
    title: str
    start: datetime
    end: datetime

    def __init__(self, title: str, start: datetime, end: datetime) -> None:
        self.title = title

        if end <= start:
            raise ValueError("end must be after start")

        self.start = start
        self.end = end

    def __repr__(self) -> str:
        return f"title: {self.title!r}, start: {self.start!r}, end: {self.end!r}"

    def __str__(self) -> str:
        return f"title: {self.title}, start: {self.start}, end: {self.end}"


class Scheduler:
    events: list[Event]

    def __init__(self, events: list[Event] | None = None):
        self.events = events or []

    def add_event(self, event: Event) -> None:
        for current_event in self.events:
            if self.do_events_overlap(current_event, event):
                raise ValueError("Event overlaps with an existing event")
        self.events.append(event)

    def do_events_overlap(self, event_one: Event, event_two: Event) -> bool:
        return event_one.start < event_two.end and event_two.start < event_one.end

    def next_events(self, n: int = 5) -> list[Event]:
        return sorted(self.events, key=lambda event: event.start)[:n]

    def events_on(self, date: datetime) -> list[Event]:
        todays_events: list[Event] = []
        target: date = date.date()
        for current_event in self.events:
            if current_event.start.date() <= target <= current_event.end.date():
                todays_events.append(current_event)
        return todays_events

    def __repr__(self):
        return f"events: {self.events}"


scheduler: Scheduler = Scheduler()

event_one: Event = Event(
    title="event01", start=datetime(2025, 11, 29, 12), end=datetime(2025, 11, 29, 13)
)
event_two: Event = Event(
    title="event01", start=datetime(2025, 11, 30, 12), end=datetime(2025, 11, 30, 13)
)
event_three: Event = Event(
    title="event01", start=datetime(2025, 11, 27, 12), end=datetime(2025, 11, 27, 13)
)

print(scheduler.add_event(event_one))
print(scheduler.add_event(event_two))
print(scheduler.add_event(event_three))

print(scheduler.next_events())
