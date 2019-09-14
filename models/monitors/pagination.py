import logging

PAGE_SIZE = 30


def paginate(poll_func, event_offset=0):
    """Paginates through the available events returned from calls to poll_func,
    returning the gathered events.

    If no existing event_offset is provided, this will only fetch the latest
    page.

    Events are returned newest to oldest.

    Arguments:
        poll_func {func} -- A function which fetches a list of `github.Event`

    Keyword Arguments:
        event_offset {int} -- The latest event ID retrieved (default: {0})

    Returns:
        list(github.Event) -- A list of new events
    """
    events = []
    for idx, event in enumerate(poll_func()):
        # If we've reached our offset, break out of the loop
        if int(event.id) <= event_offset:
            break
        events.append(event)
        # If we don't have a current offset, we only want to grab one page
        # so we can short-circuit at the fixed page size of 30 items
        if not event_offset and idx == PAGE_SIZE:
            break
    return events
