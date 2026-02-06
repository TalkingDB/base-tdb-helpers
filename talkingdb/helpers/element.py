from typing import List, Optional
from talkingdb.models.document.layouts.layout import LayoutModel
from talkingdb.helpers.container import get_container
from talkingdb.models.container import doc_source_node_model
from talkingdb.models.metadata.metadata import Metadata

from talkingdb.helpers.index import get_child_ids


def link_elem(layout: LayoutModel, idx):
    p_elem = layout.elements[idx - 1].id if idx > 0 else None
    n_elem = layout.elements[idx +
                             1].id if idx < len(layout.elements) - 1 else None
    return p_elem, n_elem

def get_contents(metadata: Metadata, elem_uids: List[str]) -> List[str]:
    """Query source nodes for multiple elem_uids and return their content in order."""
    if not elem_uids:
        return []

    container = get_container(doc_source_node_model, metadata.scope)

    in_clause = ", ".join(f"@uid{i}" for i in range(len(elem_uids)))

    query = f"""
        SELECT c.elem_uid, c.content
        FROM c
        WHERE c.event_group_id = @event_group_id
          AND c.elem_uid IN ({in_clause})
          AND c.metadata.index = "section@para"
    """

    params = [{"name": "@event_group_id", "value": metadata.event_group_id}]
    params.extend(
        {"name": f"@uid{i}", "value": uid}
        for i, uid in enumerate(elem_uids)
    )

    items = container.query_items(
        query=query,
        parameters=params,
        partition_key=metadata.event_group_id,
    )

    content_map = {
        item["elem_uid"]: item["content"].strip()
        for item in items
        if item.get("content", "").strip()
    }

    # Preserve original order
    return [content_map[uid] for uid in elem_uids if uid in content_map]



def get_content(metadata: Metadata, element_id: str) -> Optional[str]:
    """Get content for a heading by fetching its child paragraphs."""
    child_ids = get_child_ids(metadata, element_id)

    if not child_ids:
        return None

    contents = get_contents(metadata, child_ids)
    return "\n\n".join(contents) if contents else None
