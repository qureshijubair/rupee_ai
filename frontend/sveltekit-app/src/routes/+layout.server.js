let loginStatus = false;

export function load({ cookies }) {
	if (cookies.get('logged_in')) {
		loginStatus = true;
	}
	else {
		loginStatus = false;
	}

	return {
		loginStatus
	};
}
