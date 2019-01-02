entity_id = data.get('entity_id')
state = data.get('state')

if isinstance(entity_id, str):
    entity = hass.states.get(entity_id)
    hass.states.set(entity_id, state, entity.attributes, True)
else:
    for ident in entity_id:
        entity = hass.states.get(ident)
        hass.states.set(ident, state, entity.attributes, True)
