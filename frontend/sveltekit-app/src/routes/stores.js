import { writable } from 'svelte/store';

function createLoginStatus() {
	const { subscribe, set } = writable(0);

	return {
		subscribe,
		setLogIn: () => set(1),
		setLogOut: () => set(0)
	};
}

export const loginStatus = createLoginStatus();
export const captchaValue = writable('sld7sH2');