from views import *

def forum_create(request):
	data = json.loads(request.body)

	name = data.get('name')
	slug = data.get('short_name')
	user_email = data.get('user')
	user_id = get_user_id_by_email(user_email)

	result = get_forum_id_by_slug(slug)
	if result == None:
		data['id'] = db.update_get_id(
			"INSERT INTO forum (name, slug, user_id) VALUES (%s, %s, %s)", 
			[name, slug, user_id]
		)
		return info_message(data)

	return info_message(get_forum_info(slug))

def forum_details(request):
	data = request.GET
	
	info = get_forum_info(data.get('forum'))
	if info == None:
		return notexist_message('Forum', 'short_name', data.get('forum'))

	related = []
	if data.has_key('related'):
		related = data.get('related')
	if "'user'" in related:
		info['user'] = get_user_info(info['user'])

	return info_message(info)

def forum_listUsers(request):
	data = request.GET

	forum_id = get_forum_id_by_slug(data['forum'])
	if forum_id == None:
		return notexist_message('Forum', 'short_name', data.get('forum'))
	
	sort = {}
	sort['since_id'] = data.get('since_id')
	sort['limit'] = data.get('limit')
	sort['order'] = data.get('order') if data.has_key('order') else 'desc'
	sort['type'] = 'big'

	ulist = user_list(forum_id, 'forum', sort)
	return info_message(ulist)

def forum_listPosts(request):
	data = request.GET

	forum_id = get_forum_id_by_slug(data.get('forum'))
	if forum_id == None:
		return notexist_message('Forum', 'short_name', data.get('forum'))

	sort = {}
	sort['since'] = data.get('since')
	sort['limit'] = data.get('limit')
	sort['order'] = data.get('order') if data.has_key('order') else 'desc'
	related = data.get('related')

	plist = post_list(forum_id, 'forum', sort, related)
	
	return info_message(plist)

def forum_listThreads(request):
	data = request.GET

	forum_id = get_forum_id_by_slug(data['forum'])
	if forum_id == None:
		return notexist_message('Forum', 'short_name', data.get('forum'))

	sort = {}
	sort['since'] = data.get('since')
	sort['limit'] = data.get('limit')
	sort['order'] = data.get('order') if data.has_key('order') else 'desc'
	related = data.get('related')
	
	tlist = thread_list(forum_id, 'forum', sort, related)

	return info_message(tlist)
