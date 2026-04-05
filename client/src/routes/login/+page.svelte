<script lang="ts">
	import { auth } from '$lib/stores/auth.svelte';
	import { Button, Input } from '$lib/components';
	import { toast } from 'svelte-sonner';
	import { goto } from '$app/navigation';
	import ArrowRight from 'lucide-svelte/icons/arrow-right';
	import Lock from 'lucide-svelte/icons/lock';
	import Mail from 'lucide-svelte/icons/mail';
	import ShieldCheck from 'lucide-svelte/icons/shield-check';

	let email = $state('');
	let password = $state('');
	let isLoading = $state(false);

	async function handleSubmit(e: Event) {
		e.preventDefault();
		isLoading = true;

		try {
			await auth.login({ email, password });
			toast.success('Welcome back to InsuraFlow');
			goto('/dashboard');
		} catch (error: any) {
			const errorData = error.response?.data;
			const details = errorData?.details;
			const message =
				errorData?.detail ||
				details?.detail ||
				(typeof details === 'string' ? details : null) ||
				errorData?.error ||
				'Unable to sign in';
			toast.error(message);
		} finally {
			isLoading = false;
		}
	}
</script>

<div class="relative flex min-h-[calc(100vh-80px)] items-center justify-center overflow-hidden p-4">
    <!-- Abstract background shapes -->
    <div class="absolute left-0 top-0 h-96 w-96 -translate-x-1/2 -translate-y-1/2 rounded-full bg-violet-500/18 blur-3xl"></div>
    <div class="absolute bottom-0 right-0 h-96 w-96 translate-x-1/2 translate-y-1/2 rounded-full bg-cyan-400/8 blur-3xl"></div>
	<div class="absolute inset-0 bg-[radial-gradient(circle_at_top,rgba(168,85,247,0.08),transparent_30%),linear-gradient(180deg,rgba(18,18,44,0.92),rgba(8,11,26,0.96))]"></div>

	<div class="glass-card relative z-10 w-full max-w-md space-y-8 rounded-3xl border border-white/10 p-10 shadow-[0_30px_90px_rgba(2,6,23,0.45)] animate-fade-in">
		<div class="text-center">
			<div class="mx-auto mb-6 flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-violet-500/22 to-fuchsia-500/16 shadow-inner shadow-violet-900/40 ring-1 ring-inset ring-violet-200/10">
				<ShieldCheck class="w-8 h-8 text-violet-200" />
			</div>
			<h2 class="mb-2 text-3xl font-black tracking-tight text-white">Welcome Back</h2>
			<p class="font-medium text-slate-300">Continue your journey with InsuraFlow</p>
		</div>

		<form class="mt-10 space-y-6" onsubmit={handleSubmit}>
			<div class="space-y-5">
				<Input
					label="Email Address"
					type="email"
					placeholder="name@example.com"
					required
					bind:value={email}
				/>
				<Input
					label="Password"
					type="password"
					placeholder="••••••••"
					required
					bind:value={password}
				/>

			</div>

			<Button type="submit" class="w-full h-14 text-lg" loading={isLoading}>
				Sign In
			</Button>

			<div class="border-t border-white/8 pt-4 text-center">
                <p class="text-sm font-medium text-slate-400">
                    New to InsuraFlow? 
                    <a href="/register" class="ml-1 font-black text-violet-300 transition-colors hover:text-white">
                        Create an account
                    </a>
                </p>
			</div>
		</form>
	</div>
</div>
