from revscoring.extractors import api
from revscoring import Feature, features
from revscoring.features import wikibase
import mwapi

api_session = mwapi.Session("https://www.wikidata.org", user_agent="Hoo working on T158430")
extractor = api.Extractor(api_session)

#print(list(extractor.extract(738916611, [wikibase.revision.sitelinks])))

def proc_item_completeness(properties_present):
    properties_present = set(properties_present.keys())
    # TODO: Don't hardcode item id...
    all_res = api_session.get(action='wbsgetsuggestions', entity='Q15430523', include='all')['search']

    all_prob = 0.0
    present_prob = 0.0
    for statement in all_res:
        all_prob += float(statement['rating'])
        if statement['id'] in properties_present:
            present_prob += float(statement['rating'])

    return present_prob/all_prob

item_completeness = Feature(
    'item_completeness',
    proc_item_completeness,
    depends_on=[wikibase.revision.datasources.properties],
    returns=float
)

print("Old rev, very incomplete")
print(list(extractor.extract(197236276, [item_completeness])))
print("New rev, fairly incomplete")
print(list(extractor.extract(417558088, [item_completeness])))
