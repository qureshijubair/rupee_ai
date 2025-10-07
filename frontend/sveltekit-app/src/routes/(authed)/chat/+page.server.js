import { redirect } from '@sveltejs/kit';
// import { fail } from '@sveltejs/kit';
// import { error } from '@sveltejs/kit';

export function load({ cookies, url }) {
	if (!cookies.get('logged_in')) {
		throw redirect(303, `/login?redirectTo=${url.pathname}`);
	}
}