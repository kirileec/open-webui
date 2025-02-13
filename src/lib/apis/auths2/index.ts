import { WEBUI_API_BASE_URL } from '$lib/constants';

export const userSignIn2 = async (email: string, name: string) => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/auths2/signin2`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		credentials: 'include',
		body: JSON.stringify({
			email: email,
			name: name
		})
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			console.log(err);

			error = err.detail;
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};