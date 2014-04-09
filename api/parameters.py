
parameters = {
	'user': {
		'create': {
			'method': 'POST',
			'pars': ['username', 'about', 'name', 'email'],
		},
		'details': {
			'method': 'POST',
			'pars': ['username', 'about', 'name', 'email'],
		},
		'follow': {
			'method': 'POST',
			'pars': ['follower', 'followee'],
		},
		'listFollowers': {
			'method': 'POST',
			'pars': ['user'],
		},
		'listFollowing': {
			'method': 'POST',
			'pars': ['user'],
		},
		'listPosts': {
			'method': 'POST',
			'pars': ['user'],
		},
		'unfollow': {
			'method': 'POST',
			'pars': ['follower', 'followee'],
		},
		'updateProfile': {
			'method': 'POST',
			'pars': ['user', 'name', 'about'],
		},
	},
	'forum': {
		'create': {
			'method': 'POST',
			'pars': ['name', 'short_name', 'user'],
		},
		'details': {
			'method': 'POST',
			'pars': ['forum'],
		},
		'listPosts': {
			'method': 'POST',
			'pars': ['forum'],
		},
		'listTreads': {
			'method': 'POST',
			'pars': ['forum'],
		},
		'listUsers': {
			'method': 'POST',
			'pars': ['forum'],
		},
	},
	'post': {
		'create': {
			'method': 'POST',
			'pars': ['date', 'thread', 'message', 'user', 'forum'],
		},
		'details': {
			'method': 'POST',
			'pars': ['post'],
		},
		'list': {
			'method': 'POST',
			'pars': [],
		},
		'remove': {
			'method': 'POST',
			'pars': ['post'],
		},
		'restore': {
			'method': 'POST',
			'pars': ['post'],
		},
		'update': {
			'method': 'POST',
			'pars': ['post', 'message'],
		},
		'vote': {
			'method': 'POST',
			'pars': ['post', 'vote'],
		},
	},
	'thread': {
		'close': {
			'method': 'POST',
			'pars': ['thread'],
		},
		'create': {
			'method': 'POST',
			'pars': ['username', 'about', 'name', 'email'],
		},
		'details': {
			'method': 'POST',
			'pars': ['thread'],
		},
		'list': {
			'method': 'POST',
			'pars': [],
		},
		'listPosts': {
			'method': 'POST',
			'pars': ['thread'],
		},
		'open': {
			'method': 'POST',
			'pars': ['thread'],
		},
		'remove': {
			'method': 'POST',
			'pars': ['thread'],
		},
		'restore': {
			'method': 'POST',
			'pars': ['thread'],
		},
		'subscribe': {
			'method': 'POST',
			'pars': ['thread', 'user'],
		},
		'unsubscribe': {
			'method': 'POST',
			'pars': ['thread', 'user'],
		},
		'update': {
			'method': 'POST',
			'pars': ['thread', 'slug', 'message'],
		},
		'vote': {
			'method': 'POST',
			'pars': ['thread', 'vote'],
		},
	}
}