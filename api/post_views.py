from views import *

def post_create(request):
	data = json.loads(request.body)

	date = data.get('date')
	forum = data.get('forum')
	message = data.get('message')
	thread_id = data.get('thread')
	user_email = data.get('user')
	forum_id = get_forum_id_by_slug(forum)
	isApproved = data.get('isApproved') if data.has_key('isApproved') else False
	isDeleted = data.get('isDeleted') if data.has_key('isDeleted') else False
	isEdited = data.get('isEdited') if data.has_key('isEdited') else False
	isHighlighted = data.get('isHighlighted') if data.has_key('isHighlighted') else False
	isSpam = data.get('isSpam') if data.has_key('isSpam') else False
	
	parents = None
	if (data.has_key('parent')):
		parents = db.query_one("SELECT parents FROM post WHERE id = %s;", [data.get('parent')])['parents']
		if (parents == None):
			parents = str(data.get('parent'))
		else:
			parents += '.' + str(data.get('parent'))

	data['id'] = db.update_get_id(
		"INSERT INTO post (date, message, thread_id, forum_id, user_id, isApproved, isDeleted, isEdited, isHighlighted, isSpam, parents) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
		[date, message, thread_id, forum_id, get_user_id_by_email(user_email), isApproved, isDeleted, isEdited, isHighlighted, isSpam, parents]
	)

	return info_message(data)

def post_details(request):
	data = request.GET

	info = get_post_info(data['post'], data.get('related'))
	return info_message(info)

def post_List(request):
	data = request.GET
	
	sort = {}
	sort['since'] = data.get('since')
	sort['limit'] = data.get('limit')
	sort['order'] = data.get('order') if data.has_key('order') else 'desc'
	related = data.get('related')
	if data.has_key('forum'):
		forum_id = get_forum_id_by_slug(data['forum'])
		plist = post_list(forum_id, 'forum', sort, related)
	else:
		plist = post_list(data.get('thread'), 'thread', sort, related)
	
	return info_message(plist)

def post_remove(request):
	data = json.loads(request.body)

	db.update(
		"UPDATE post SET isDeleted = True WHERE id = %s",
		[data['post']]
	)
	return info_message(data)

def post_restore(request):
	data = json.loads(request.body)

	db.update(
		"UPDATE post SET isDeleted = False WHERE id = %s",
		[data['post']]
	)
	return info_message(data)

def post_update(request):
	data = json.loads(request.body)

	db.update(
		"UPDATE post SET message = %s WHERE id = %s",
		[data['message'], data['post']]
	)
	return info_message(get_post_info(data['post']))

def post_vote(request):
	data = json.loads(request.body)
	
	if data['vote'] == 1:
		db.update(
			"UPDATE post SET likes = likes+1 WHERE id = %s",
			[data['post']]
		)
	elif data['vote'] == -1:
		db.update(
			"UPDATE post SET dislikes = dislikes+1 WHERE id = %s",
			[data['post']]
		)

	return info_message(get_post_info(data['post']))
