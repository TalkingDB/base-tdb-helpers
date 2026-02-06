from talkingdb.models.metadata.metadata import Metadata
from talkingdb.models.event.event import EventModel
from talkingdb.models.event.status import EventStatus


def create_event(metadata: Metadata, event_type: str, event_data: dict = {}, event_status: EventStatus = EventStatus.CREATED):
    event_group_id = EventModel.ensure_id(metadata.event_group_id)
    event_id = EventModel.ensure_id(None)
    id = EventModel.make_id(event_id)
    scope = metadata.scope
    user_email = "mayank@talkingdb.io"

    event = EventModel(
        id=id,
        event_id=event_id,
        event_type=event_type,
        event_data=event_data,
        event_status=event_status,
        event_group_id=event_group_id,
        trigger_event_id=metadata.trigger_event_id,
        scope=scope,
        user_email=user_email
    )

    return event


def update_event(event: EventModel, event_status: EventStatus, event_data: dict = {}):
    event.event_status = event_status
    event.event_data.update(event_data)

    return event
