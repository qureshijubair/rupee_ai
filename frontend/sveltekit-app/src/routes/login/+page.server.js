import { redirect, fail } from '@sveltejs/kit';
import { LOGIN_EMAIL, LOGIN_PASSWORD } from '$env/static/private';


export function load({ cookies, url }) {
	if (cookies.get('logged_in')) {
		throw redirect(307, url.searchParams.get('redirectTo') ?? '/chat');
	}
}

export const actions = {
	default: async ({ request, cookies, url }) => {
		const data = await request.formData();

		if ((data.get('email') === LOGIN_EMAIL) && (data.get('password') === LOGIN_PASSWORD) && (data.get('captcha-status') === "CORRECT")) {
			cookies.set('logged_in', 'true', {
				path: '/'
			});

			throw redirect(303, url.searchParams.get('redirectTo') ?? '/chat');
		}

		return fail(403, {
			incorrect: true
		});
	}
};