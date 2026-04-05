<script lang="ts">
	import { auth } from '$lib/stores/auth.svelte';
	import { Button, Input } from '$lib/components';
	import { toast } from 'svelte-sonner';
	import { goto } from '$app/navigation';
	import Lock from 'lucide-svelte/icons/lock';
	import Mail from 'lucide-svelte/icons/mail';
	import ShieldCheck from 'lucide-svelte/icons/shield-check';
	import Sparkles from 'lucide-svelte/icons/sparkles';
	import User from 'lucide-svelte/icons/user';

	let username = $state('');
	let email = $state('');
	let password = $state('');
	let role = $state('customer');
	let secretKey = $state('');
	let isLoading = $state(false);

	function getFirstErrorMessage(value: unknown): string | null {
		if (!value) return null;
		if (typeof value === 'string') return value;
		if (Array.isArray(value)) {
			const first = value.find(Boolean);
			return typeof first === 'string' ? first : null;
		}
		if (typeof value === 'object') {
			for (const nestedValue of Object.values(value as Record<string, unknown>)) {
				const message = getFirstErrorMessage(nestedValue);
				if (message) return message;
			}
		}
		return null;
	}

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
			toast.success('Account created! Sign in to continue.');
			goto('/login');
		} catch (error: any) {
			const errorData = error.response?.data;
			const details = errorData?.details;
			const msg =
				getFirstErrorMessage(errorData?.secret_key ?? details?.secret_key) ||
				getFirstErrorMessage(errorData?.password ?? details?.password) ||
				getFirstErrorMessage(errorData?.email ?? details?.email) ||
				getFirstErrorMessage(errorData?.username ?? details?.username) ||
				errorData?.detail ||
				getFirstErrorMessage(details?.detail) ||
				getFirstErrorMessage(details) ||
				errorData?.error ||
				'Registration failed';
			toast.error(msg);
		} finally {
			isLoading = false;
		}
	}
</script>

<div class="min-h-[calc(100vh-80px)] flex items-center justify-center p-4 relative overflow-hidden">
    <!-- Abstract background shapes -->
    <div class="absolute top-0 right-0 w-96 h-96 bg-indigo-100 rounded-full blur-3xl translate-x-1/2 -translate-y-1/2 opacity-50"></div>
    <div class="absolute bottom-0 left-0 w-96 h-96 bg-emerald-50 rounded-full blur-3xl -translate-x-1/2 translate-y-1/2 opacity-50"></div>

	<div class="max-w-md w-full space-y-8 bg-white p-10 rounded-3xl border border-slate-200 shadow-2xl relative z-10 animate-fade-in">
		<div class="text-center">
			<div class="bg-indigo-50 w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-inner">
				<Sparkles class="w-8 h-8 text-indigo-600" />
			</div>
			<h2 class="text-3xl font-black text-slate-900 tracking-tight mb-2">Create Account</h2>
			<p class="text-slate-500 font-medium">Join the next generation of insurance</p>
		</div>

		<form class="mt-10 space-y-6" onsubmit={handleSubmit}>
			<div class="space-y-5">
				<Input
					label="Username"
					placeholder="johndoe"
					required
					bind:value={username}
				/>
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

				<div class="space-y-2">
					<label for="register-role" class="block text-xs font-bold text-slate-500 uppercase tracking-widest ml-1">Account Type</label>
					<select
						id="register-role"
						bind:value={role}
						class="input-field py-[14px]"
					>
						<option value="customer">Customer</option>
						<option value="admin">Admin</option>
						<option value="agent">Agent</option>
						<option value="provider">Provider</option>
						<option value="surveyor">Surveyor</option>
					</select>
				</div>

				{#if role !== 'customer'}
					<Input
						label="Privileged Role Secret Key"
						type="password"
						placeholder="Provided by InsuraFlow"
						required
						bind:value={secretKey}
					/>
				{/if}
			</div>

			<Button type="submit" class="w-full h-14 text-lg" loading={isLoading}>
				Get Started
			</Button>

			<div class="text-center pt-4 border-t border-slate-100">
                <p class="text-sm text-slate-500 font-medium">
                    Already a member? 
                    <a href="/login" class="text-indigo-600 font-black hover:text-indigo-700 transition-colors ml-1">
                        Sign In
                    </a>
                </p>
			</div>
		</form>
	</div>
</div>
