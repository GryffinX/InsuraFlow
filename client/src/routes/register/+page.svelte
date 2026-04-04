<script lang="ts">
	import { auth } from '$lib/stores/auth.svelte';
	import { Button, Input } from '$lib/components';
	import { toast } from 'svelte-sonner';
	import { goto } from '$app/navigation';
	import { ShieldCheck, User, Mail, Lock } from 'lucide-svelte';

	let username = $state('');
	let email = $state('');
	let password = $state('');
	let role = $state('customer');
	let secretKey = $state('');
	let isLoading = $state(false);

	async function handleSubmit(e: Event) {
		e.preventDefault();
		isLoading = true;

		try {
			await auth.register({
				username,
				email,
				password,
				role,
				secret_key: secretKey
			});
			toast.success('Registration successful! Please log in.');
			goto('/login');
		} catch (error: any) {
			toast.error(error.response?.data?.secret_key || error.response?.data?.error || 'Registration failed');
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
			<h2 class="text-3xl font-extrabold text-slate-900 tracking-tight">Create an account</h2>
			<p class="mt-2 text-slate-500">Join InsuraFlow today.</p>
		</div>

		<form class="mt-8 space-y-6" onsubmit={handleSubmit}>
			<div class="space-y-4">
				<Input
					label="Username"
					placeholder="johndoe"
					required
					bind:value={username}
				/>
				<Input
					label="Email address"
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

				<div class="space-y-1">
					<label class="block text-sm font-medium text-slate-700">I am a...</label>
					<select
						bind:value={role}
						class="block w-full rounded-md border-slate-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm transition-colors border p-2 outline-none"
					>
						<option value="customer">Customer</option>
						<option value="agent">Agent</option>
						<option value="provider">Provider</option>
						<option value="surveyor">Surveyor</option>
						<option value="admin">Admin</option>
					</select>
				</div>

				{#if role !== 'customer'}
					<Input
						label="Secret Key"
						type="password"
						placeholder="Enter role-specific secret key"
						required
						bind:value={secretKey}
					/>
				{/if}
			</div>

			<Button type="submit" class="w-full h-12 text-lg font-bold" loading={isLoading}>
				Sign up
			</Button>

			<div class="relative">
				<div class="absolute inset-0 flex items-center">
					<div class="w-full border-t border-slate-200"></div>
				</div>
				<div class="relative flex justify-center text-sm">
					<span class="px-2 bg-white text-slate-500">Already have an account?</span>
				</div>
			</div>

			<a href="/login" class="block w-full text-center text-sm font-bold text-indigo-600 hover:text-indigo-500">
				Log in instead
			</a>
		</form>
	</div>
</div>
