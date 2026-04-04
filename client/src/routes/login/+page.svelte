<script lang="ts">
	import { auth } from '$lib/stores/auth.svelte';
	import { Button, Input } from '$lib/components';
	import { toast } from 'svelte-sonner';
	import { goto } from '$app/navigation';
	import { ShieldCheck, Mail, Lock } from 'lucide-svelte';

	let email = $state('');
	let password = $state('');
	let isLoading = $state(false);

	async function handleSubmit(e: Event) {
		e.preventDefault();
		isLoading = true;

		try {
			await auth.login({ email, password });
			toast.success('Welcome back!');
			goto('/dashboard');
		} catch (error: any) {
            console.error('Login error details:', error.response?.data);
            const message = error.response?.data?.details || error.response?.data?.error || 'Login failed';
			toast.error(message);
		} finally {
			isLoading = false;
		}
	}
</script>

<div class="min-h-screen flex items-center justify-center bg-slate-50 px-4 py-12">
	<div class="max-w-md w-full space-y-8 bg-white p-10 rounded-3xl border border-slate-200 shadow-xl">
		<div class="text-center">
			<div class="bg-indigo-50 w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-4">
				<ShieldCheck class="w-8 h-8 text-indigo-600" />
			</div>
			<h2 class="text-3xl font-extrabold text-slate-900 tracking-tight">Sign in to your account</h2>
			<p class="mt-2 text-slate-500">Welcome back to InsuraFlow.</p>
		</div>

		<form class="mt-8 space-y-6" onsubmit={handleSubmit}>
			<div class="space-y-4">
				<Input
					label="Email address"
					type="email"
					placeholder="name@example.com"
					required
					bind:value={email}
				/>
				<div class="space-y-1">
					<Input
						label="Password"
						type="password"
						placeholder="••••••••"
						required
						bind:value={password}
					/>
				</div>

				<div class="flex items-center justify-between">
					<label class="flex items-center">
						<input type="checkbox" class="w-4 h-4 text-indigo-600 border-slate-300 rounded focus:ring-indigo-500" />
						<span class="ml-2 text-sm text-slate-600 font-medium">Remember me</span>
					</label>
				</div>
			</div>

			<Button type="submit" class="w-full h-12 text-lg font-bold" loading={isLoading}>
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
