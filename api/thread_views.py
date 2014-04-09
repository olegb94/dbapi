from views import *

def thread_create(request):
	data = json.loads(request.body)

	slug = data.get('slug')
	isClosed = data.get('isClosed')
	forum_slug = data.get('forum')
	date = data.get('date')
	message = data.get('message')
	title = data.get('title')
	user_email = data.get('user')
	isDeleted = data.get('isDeleted') if data.has_key('isDeleted') else False


	data['id'] = db.update_get_id(
		"INSERT INTO thread (title, slug, message, date, user_id, forum_id, isClosed, isDeleted) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);",
		[title, slug, message, date, get_user_id_by_email(user_email), get_forum_id_by_slug(forum_slug), isClosed, isDeleted]
	)
	return info_message(data)

def thread_subscribe(request):
	data = json.loads(request.body)

	user_id = get_user_id_by_email(data['user'])
	thread_id = data.get('thread')
	result = db.query_one(
		"SELECT * FROM subscribe WHERE user_id = %s and thread_id = %s;",
		[user_id, thread_id]
	)
	if (result == None):
		db.update(
			"INSERT INTO subscribe (user_id, thread_id) VALUES (%s, %s)",
			[user_id, thread_id]
		)
	return info_message(data)

def thread_unsubscribe(request):
	# data = { 'user': '4e', 'thread': 6}
	data = json.loads(request.body)
	user_id = get_user_id_by_email(data['user'])
	thread_id = data.get('thread')

	db.update(
		"DELETE FROM subscribe WHERE user_id = %s and thread_id = %s;",
		[user_id, thread_id]
	)
	return info_message(data)

def thread_details(request):
	data = request.GET

	info = get_thread_info(data.get('thread'))
	return info_message(info)

def thread_close(request):
	data = json.loads(request.body)

	db.update(
		"UPDATE thread SET isClosed = True WHERE id = %s",
		[data['thread']]
	)
	return info_message(data)

def thread_open(request):
	data = json.loads(request.body)

	db.update(
		"UPDATE thread SET isClosed = False WHERE id = %s",
		[data['thread']]
	)
	return info_message(data)

def thread_remove(request):
	data = json.loads(request.body)

	db.update(
		"UPDATE thread SET isDeleted = True WHERE id = %s",
		[data['thread']]
	)
	return info_message(data)

def thread_restore(request):
	data = json.loads(request.body)

	db.update(
		"UPDATE thread SET isDeleted = False WHERE id = %s",
		[data['thread']]
	)
	return info_message(data)

def thread_update(request):

	data = json.loads(request.body)
	db.update(
		"UPDATE thread SET message = %s, slug = %s WHERE id = %s",
		[data['message'], data['slug'], data['thread']]
	)
	return info_message(get_thread_info(data['thread']))

def thread_vote(request):

	data = json.loads(request.body)
	if data['vote'] == 1:
		db.update(
			"UPDATE thread SET likes = likes+1 WHERE id = %s",
			[data['thread']]
		)
	elif data['vote'] == -1:
		db.update(
			"UPDATE thread SET dislikes = dislikes+1 WHERE id = %s",
			[data['thread']]
		)

	return info_message(get_thread_info(data['thread']))

def thread_listPosts(request):
	data = request.GET

	sort = {}
	sort['since'] = data.get('since')
	sort['limit'] = data.get('limit')
	sort['order'] = data.get('order') if data.has_key('order') else 'desc'
	related = data.get('related')
	
	plist = post_list(data.get('thread'), 'thread', sort, related)
	
	return info_message(plist)

def thread_List(request):
	data = request.GET
	
	sort = {}
	sort['since'] = data.get('since')
	sort['limit'] = data.get('limit')
	sort['order'] = data.get('order') if data.has_key('order') else 'desc'
	
	if data.has_key('forum'):
		forum_id = get_forum_id_by_slug(data['forum'])
		tlist = thread_list(forum_id, 'forum', sort)
	else:
		user_id = get_user_id_by_email(data['user'])
		tlist = thread_list(user_id, 'user', sort)
	
	return info_message(tlist)