from views import *

def user_create(request):
	data = json.loads(request.body)
	username = data.get('username')
	about = data.get('about')
	name = data.get('name')
	email = data.get('email')
	isAnonymous = data.get('isAnonymous') if data.has_key('isAnonymous') else False
	
	if (get_user_id_by_email(email) == None):
		data['id'] = db.update_get_id(
			"INSERT INTO user (username, name, about, email, isAnonymous) VALUES (%s, %s, %s, %s, %s)", 
			[username, name, about, email, isAnonymous]
		)
		return info_message(data)

	return info_message(get_user_info(email))
	

def user_details(request):
	data = request.GET

	email = data.get('user')
	info = get_user_info(email)
	if info == None:
		return notexist_message('User', 'email', data.get('user'))
	return info_message(info)

def user_follow(request):
	data = json.loads(request.body)

	follower_email = data.get('follower')
	followee_email = data.get('followee')

	follower_id = get_user_id_by_email(follower_email)
	if follower_id == None:
		return notexist_message('User', 'email', data.get('follower'))
	followee_id = get_user_id_by_email(followee_email)
	if followee_id == None:
		return notexist_message('User', 'email', data.get('followee'))

	result = db.query_one(
		"SELECT * FROM follow WHERE follower_id = %s and followee_id = %s;",
		[follower_id, followee_id]
	)
	
	if (result == None):
		db.update(
			"INSERT INTO follow (follower_id, followee_id) VALUES (%s, %s)",
			[follower_id, followee_id]
		)

	return info_message(get_user_info(follower_email))


def user_unfollow(request):
	data = json.loads(request.body)

	follower_email = data.get('follower')
	followee_email = data.get('followee')

	follower_id = get_user_id_by_email(follower_email)
	if follower_id == None:
		return notexist_message('User', 'email', data.get('follower'))
	followee_id = get_user_id_by_email(followee_email)
	if followee_id == None:
		return notexist_message('User', 'email', data.get('followee'))

	db.update(
		"DELETE FROM follow WHERE follower_id = %s and followee_id = %s;",
		[follower_id, followee_id]
	)

	return info_message(get_user_info(follower_email))

def user_update(request):
	data = json.loads(request.body)

	name = data.get('name')
	about = data.get('about')
	email =  data.get('user')
	db.update("UPDATE user SET name =  %s, about = %s WHERE email = %s", [name, about, email])
	
	return info_message(get_user_info(email))

def user_listFollowing(request):
	data = request.GET

	user_id = get_user_id_by_email(data.get('user'))
	sort = {}
	sort['since_id'] = data.get('since_id')
	sort['limit'] = data.get('limit')
	sort['order'] = data.get('order') if data.has_key('order') else 'desc'
	sort['type'] = 'big'

	ulist = user_list(user_id, 'followee', sort)

	return info_message(ulist)

def user_listFollowers(request):
	data = request.GET

	user_id = get_user_id_by_email(data.get('user'))
	if followee_id == None:
		return notexist_message('User', 'email', data.get('user'))

	sort = {}
	sort['since_id'] = data.get('since_id')
	sort['limit'] = data.get('limit')
	sort['order'] = data.get('order') if data.has_key('order') else 'desc'
	sort['type'] = 'big'

	ulist = user_list(user_id, 'follower', sort)
	
	return info_message(ulist)

def user_listPosts(request):
	data = request.GET

	user_id = get_user_id_by_email(data.get('user'))
	if followee_id == None:
		return notexist_message('User', 'email', data.get('user'))
	
	sort = {}
	sort['since'] = data.get('since')
	sort['limit'] = data.get('limit')
	sort['order'] = data.get('order') if data.has_key('order') else 'desc'
	
	plist = post_list(user_id, 'user', sort)
	
	return info_message(plist)