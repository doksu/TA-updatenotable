import splunk.Intersplunk, splunk.rest

# The following is derived from Luke Murphey's post: https://www.splunk.com/en_us/blog/tips-and-tricks/how-to-edit-notable-events-in-es-programatically.html

keywords, options = splunk.Intersplunk.getKeywordsAndOptions()
results, dummyresults, settings = splunk.Intersplunk.getOrganizedResults()

sessionKey = settings.get("sessionKey")

for result in results:

    args = {'ruleUIDs': result['event_id']}

    if 'comment' in result:
        args['comment'] = result['comment']
    if 'status' in result:
        args['status'] = result['status']
    if 'urgency' in result:
        args['urgency'] = result['urgency']
    if 'owner' in result:
        args['newOwner'] = result['owner']

    serverResponse, serverContent = splunk.rest.simpleRequest('/services/notable_update', sessionKey=sessionKey, method='POST', postargs=args)

    if serverResponse['status'] != '200':
        splunk.Intersplunk.generateErrorResults(serverContent)
    else:
        result['updatenotable_result'] = serverContent

splunk.Intersplunk.outputResults(results)
