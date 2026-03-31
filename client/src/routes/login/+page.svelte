<script lang="ts">
	import { auth } from '$lib/stores/auth.svelte';
	import { Button, Input } from '$lib/components';
	import { toast } from 'svelte-sonner';
	import { goto } from '$app/navigation';
    import { ShieldCheck } from 'lucide-svelte';

	let email = $state('');
	let password = $state('');
	let isLoading = $state(false);

	async function handleSubmit(e: Event) {
		e.preventDefault();
		isLoading = true;
		try {
			await auth.login({ email, password });
			toast.success('Logged in successfully');
			goto('/dashboard');
		} catch (error: any) {
			const errorData = error.response?.data;
			const message = errorData?.error || errorData?.details?.detail || 'Login failed';
			toast.error(message);
		} finally {
			isLoading = false;
		}
	}
</script>

<div class="min-h-[calc(100vh-64px)] flex items-center justify-center p-4">
	<div class="max-w-md w-full bg-white rounded-2xl shadow-xl border border-slate-200 p-8 space-y-8">
		<div class="text-center space-y-2">
			<div class="inline-flex items-center justify-center p-3 bg-indigo-50 rounded-2xl mb-2">
				<ShieldCheck class="w-8 h-8 text-indigo-600" />
			</div>
			<h1 class="text-3xl font-bold text-slate-900 tracking-tight">Welcome back</h1>
			<p class="text-slate-500">Log in to manage your insurance and claims</p>
		</div>

		<form onsubmit={handleSubmit} class="space-y-6">
			<Input
				label="Email Address"
				type="email"
				id="email"
				placeholder="name@example.com"
				required
				bind:value={email}
			/>
			<div class="space-y-1">
				<Input
					label="Password"
					type="password"
					id="password"
					placeholder="••••••••"
					required
					bind:value={password}
				/>
				<div class="flex justify-end">
					<a href="/forgot-password" class="text-sm font-medium text-indigo-600 hover:text-indigo-500">
						Forgot password?
					</a>
				</div>
			</div>

			<Button type="submit" class="w-full h-11" loading={isLoading}>
				Sign in
			</Button>

			<div class="relative">
				<div class="absolute inset-0 flex items-center">
					<div class="w-full border-t border-slate-200"></div>
				</div>
				<div class="relative flex justify-center text-sm">
					<span class="px-2 bg-white text-slate-500">New to InsuraFlow?</span>
				</div>
			</div>

			<a href="/register" class="block w-full">
				<Button variant="outline" class="w-full h-11">
					Create an account
				</Button>
			</a>
		</form>
	</div>
</div>
