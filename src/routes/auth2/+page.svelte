<script >
    import { onMount,getContext } from 'svelte';
    import { goto } from '$app/navigation';
    import { WEBUI_NAME, config, user, socket } from '$lib/stores';
    import { getSessionUser, userSignIn2 } from '$lib/apis/auths';
    import { getBackendConfig } from '$lib/apis';
    import { toast } from 'svelte-sonner';
    const i18n = getContext('i18n');
    // 定义存储 email 和 name 的变量
    let email = '';
    let name = '';
    let from = '';
    let loading = true;  // 控制加载动画的显示状态

    const setSessionUser = async (sessionUser) => {
		if (sessionUser) {
			console.log(sessionUser);
			toast.success($i18n.t(`You're now logged in.`));
			if (sessionUser.token) {
				localStorage.token = sessionUser.token;
			}

			$socket.emit('user-join', { auth: { token: sessionUser.token } });
			await user.set(sessionUser);
			await config.set(await getBackendConfig());
			goto('/');
		}
	};
    // onMount 确保在组件挂载后获取 URL 的查询参数
    onMount(async () => {
        if ($user !== undefined) {
			await goto('/');
		}
        const params = new URLSearchParams(window.location.search);
        email = params.get('email') || '';
        name = params.get('name') || '';
        from = params.get('from') || '';
        if (from !== '') {
            localStorage.from = from
        } else {
            if (localStorage.from!==undefined) {
                window.location = localStorage.from
                localStorage.removeItem('from')
                return;
            }
            loading = false;
            return;
        }
        if (email==='') {
            loading = false;

            window.location = localStorage.from
            localStorage.removeItem('from')
            return;
        }
        // 延迟 1 秒后发送 POST 请求
        await new Promise(resolve => setTimeout(resolve, 1000));
        await signin();
        // 请求完成后隐藏加载动画
        loading = false;
    });
    // 发起 POST 请求
    async function signin() {
        const sessionUser = await userSignIn2(email, name).catch((error) => {
			toast.error(error);
			return null;
		});

		await setSessionUser(sessionUser);
    }
</script>

<main>
    <h1>欢迎，{name}!</h1>
    <p>正在进入: {email}</p>
    {#if loading}
    <div class="spinner"></div>  <!-- 加载动画 -->
    {/if}
</main>

<style>
    main {
        text-align: center;
        margin-top: 20vh;
        font-family: Arial, sans-serif;
    }

    h1 {
        font-size: 2rem;
        color: #4caf50;
    }

    p {
        font-size: 1.2rem;
        color: #555;
    }
    /* 加载动画样式 */
    .spinner {
        width: 50px;
        height: 50px;
        border: 6px solid #f3f3f3;
        border-top: 6px solid #3498db;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 0 auto;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
</style>
