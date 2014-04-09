# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
import json
from database import *
from parameters import *

db = Database(5)

# db.update("delete from user;")
# db.update("delete from forum;")
# db.update("delete from thread;")
# db.update("delete from post;")
# db.update("delete from follow;")
# db.update("delete from subscribe;")



# def check_params(request):
# 	url = request.path.split('/')
# 	entity = url[3]
# 	method = url[4]
	

def error_message(message):
	return HttpResponse(content=json.dumps({'code': 1, 'message': message}), content_type='application/json')

def info_message(message):
	return HttpResponse(content=json.dumps({'code': 0, 'message': 'OK', 'response': message}), content_type='application/json')

def notexist_message(who, parameter, value):
	return error_message("%s with '%s'='%s' doesn't exitst" % (who, parameter, value))

def other_pages(request):
	return error_message("Incorrect URL")

def get_user_id_by_email(email):
	result = db.query_one("SELECT id FROM user WHERE email = %s;", [email])
	if result == None:
		return None
	return int(result['id'])

def get_user_email_by_id(user_id):
	result = db.query_one("SELECT email FROM user WHERE id = %s;", [user_id])
	if result == None:
		return None
	return result['email']

def get_forum_id_by_slug(slug):
	result = db.query_one("SELECT id FROM forum WHERE slug = %s;", [slug])
	if result == None:
		return None
	return int(result['id'])

def get_forum_slug_by_id(id):
	result = db.query_one("SELECT slug FROM forum WHERE id = %s;", [id])
	if result == None:
		return None
	return result['slug']

def get_user_info(email):
	result = db.query_one("SELECT * FROM user WHERE email = %s;", [email])
	if result == None:
		return None
	return decorate_user_info(result)

def get_user_info_by_id(id):
	result = db.query_one("SELECT * FROM user WHERE id = %s;", [id])
	if result == None:
		return None
	return decorate_user_info(result)

def decorate_user_info(result):
	info = {
		'id': result['id'],
		'username': result['username'],
		'name': result['name'],
		'about': result['about'],
		'email': result['email'],
		'isAnonymous': result['isAnonymous'],
		'followers': user_list(result['id'], "follower"),
		'following': user_list(result['id'], "followee"),
		'subscriptions': []
	}

	subscriptions = db.query(
		"SELECT thread_id FROM subscribe WHERE user_id = %s;",
		[result['id']]
	)
	for s in subscriptions:
		info['subscriptions'].append(s['thread_id'])
	return info

def get_forum_info(slug):
	result = db.query_one("SELECT * FROM forum WHERE slug = %s;", [slug])
	if result == None:
		return None

	return decorate_forum_info(result)

def get_forum_info_by_id(id):
	result = db.query_one("SELECT * FROM forum WHERE id = %s;", [id])
	if result == None:
		return None
	return decorate_forum_info(result)

def decorate_forum_info(result):
	info = {
		'id': result['id'],
		'name': result['name'],
		'short_name': result['slug'],
		'user': get_user_email_by_id(result['user_id'])
	}
	return info

def get_post_info(id, related=None):
	result = db.query_one("SELECT * FROM post WHERE id = %s;", [id])
	if result == None:
		return None
	return decorate_post_info(result, related)

def decorate_post_info(result, related):
	info = {
		'date': str(result['date']),
		'id': result['id'],
		'isApproved': result['isApproved'],
		'isDeleted': result['isDeleted'],
		'isEdited': result['isEdited'],
		'isHighlighted': result['isHighlighted'],
		'isSpam': result['isSpam'],
		'message': result['message'],
		'dislikes': result['dislikes'],
		'likes': result['likes'],
		'points': result['likes'] - result['dislikes']
	}
	if result['parents'] != None:
		info['parent'] = int(result['parents'].split('.')[-1])	
	else:
		info['parent'] = None

	if related == None:
		related = ""

	if "'user'" in related:
		info['user'] = get_user_info_by_id(result['user_id'])
	else:
		info['user'] = get_user_email_by_id(result['user_id'])

	if "'thread'" in related:
		info['thread'] = get_thread_info(result['thread_id'])
	else:
		info['thread'] = result['thread_id']

	if "'forum'" in related:
		info['forum'] = get_forum_info_by_id(result['forum_id'])
	else:
		info['forum'] = get_forum_slug_by_id(result['forum_id'])
	return info

def get_thread_info(id):
	result = db.query_one("SELECT * FROM thread WHERE id = %s", [id])
	if result == None:
		return None
	return decorate_thread_info(result)

def decorate_thread_info(result, related=None):
	info = {
		'date': str(result['date']),
		'id': result['id'],
		'isClosed': result['isClosed'],
		'isDeleted': result['isDeleted'],
		'message': result['message'],
		'dislikes': result['dislikes'],
		'likes': result['likes'],
		'points': result['likes'] - result['dislikes'],
		'slug': result['slug'],
		'title': result['title'],
	}
	info['posts'] = db.query_one("SELECT COUNT(*) FROM post WHERE thread_id = %s", [result['id']])['COUNT(*)']

	if related == None: related = ""
	if "'user'" in related:
		info['user'] = get_user_info_by_id(result['user_id'])
	else:
		info['user'] = get_user_email_by_id(result['user_id'])

	if "'forum'" in related:
		info['forum'] = get_forum_info_by_id(result['forum_id'])
	else:
		info['forum'] = get_forum_slug_by_id(result['forum_id'])
	return info

def user_list(need_id, what, sort = {'type': 'little'}):
	user_list = []
	if what == "follower":
		query = "SELECT * FROM (SELECT follower_id FROM follow WHERE followee_id = %s) AS f JOIN user ON user.id = f.follower_id "
	elif what == "followee":
		query = "SELECT * FROM (SELECT followee_id FROM follow WHERE follower_id = %s) AS f JOIN user ON user.id = f.followee_id "
	elif what == 'forum':
		query = "SELECT DISTINCT * FROM (SELECT user_id FROM post WHERE forum_id = %s) AS posts JOIN user ON user.id = posts.user_id "
	else:
		return None;

	if sort.get('since_id') != None:
		query += "WHERE user.id >= %s " % sort.get('since_id')

	if sort.get('order') != None:
		if what != 'forum':
			query += "ORDER BY name %s " % sort.get('order');
		else:
			query += "ORDER BY user_id %s " % sort.get('order');

	if sort.get('limit') != None:
		query += "LIMIT %s " % sort.get('limit')

	list = db.query(query, [need_id])

	if sort['type'] == 'little':
		for user in list:
			user_list.append(user['email'])
	else:
		for user in list:
			user_list.append(decorate_user_info(user))
	return user_list

def post_list(need_id, what, sort={}, related=None):
	post_list = []
	if what == 'forum':
		query = "SELECT * FROM post WHERE forum_id = %s "
	elif what == 'thread':
		query = "SELECT * FROM post WHERE thread_id = %s "
	elif what == 'user':
		query = "SELECT * FROM post WHERE user_id = %s "
	else:
		return None

	if sort.get('since') != None:
		query += "and date >= '%s' " % sort.get('since')

	if sort.get('order') != None:
		query += "ORDER BY date %s " % sort.get('order');

	if sort.get('limit') != None:
		query += "LIMIT %s " % sort.get('limit')

	list = db.query(query, [need_id])

	for post in list:
		post_list.append(decorate_post_info(post, related))
	return post_list

def thread_list(need_id, what, sort={}, related=None):
	thread_list = []
	if what == 'user':
		query = "SELECT * FROM thread WHERE user_id = %s "
	elif what == 'forum':
		query = "SELECT * FROM thread WHERE forum_id = %s "
	else:
		return None
	
	if sort.get('since') != None:
		query += "and date >= '%s' " % sort.get('since')

	if sort.get('order') != None:
		query += "ORDER BY date %s " % sort.get('order');

	if sort.get('limit') != None:
		query += "LIMIT %s " % sort.get('limit')

	list = db.query(query, [need_id])

	for thread in list:
		thread_list.append(decorate_thread_info(thread, related))
	return thread_list

