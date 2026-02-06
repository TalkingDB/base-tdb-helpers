from talkingdb.models.metadata.metadata import Metadata
from talkingdb.models.event.event import EventModel


def update_metadata(metadata: Metadata, event: EventModel):
    metadata.event_group_id = event.event_group_id
    metadata.trigger_event_id = event.event_id

    return metadata
