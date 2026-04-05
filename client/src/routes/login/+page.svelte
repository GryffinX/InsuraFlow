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

<div class="min-h-[calc(100vh-80px)] flex items-center justify-center p-4 relative overflow-hidden">
    <!-- Abstract background shapes -->
    <div class="absolute top-0 left-0 w-96 h-96 bg-indigo-100 rounded-full blur-3xl -translate-x-1/2 -translate-y-1/2 opacity-50"></div>
    <div class="absolute bottom-0 right-0 w-96 h-96 bg-blue-50 rounded-full blur-3xl translate-x-1/2 translate-y-1/2 opacity-50"></div>

	<div class="max-w-md w-full space-y-8 bg-white p-10 rounded-3xl border border-slate-200 shadow-2xl relative z-10 animate-fade-in">
		<div class="text-center">
			<div class="bg-indigo-50 w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-inner">
				<ShieldCheck class="w-8 h-8 text-indigo-600" />
			</div>
			<h2 class="text-3xl font-black text-slate-900 tracking-tight mb-2">Welcome Back</h2>
			<p class="text-slate-500 font-medium">Continue your journey with InsuraFlow</p>
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

				<div class="flex items-center justify-between px-1">
					<label class="flex items-center group cursor-pointer">
						<input type="checkbox" class="w-4 h-4 text-indigo-600 border-slate-300 rounded focus:ring-indigo-500 transition-all cursor-pointer" />
						<span class="ml-2 text-sm text-slate-500 font-bold group-hover:text-slate-700 transition-colors">Remember me</span>
					</label>
				</div>
			</div>

			<Button type="submit" class="w-full h-14 text-lg" loading={isLoading}>
				Sign In
			</Button>

			<div class="text-center pt-4 border-t border-slate-100">
                <p class="text-sm text-slate-500 font-medium">
                    New to InsuraFlow? 
                    <a href="/register" class="text-indigo-600 font-black hover:text-indigo-700 transition-colors ml-1">
                        Create an account
                    </a>
                </p>
			</div>
		</form>
	</div>
</div>
