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

<div class="relative flex min-h-[calc(100vh-80px)] items-center justify-center overflow-hidden p-4">
    <!-- Abstract background shapes -->
    <div class="absolute right-0 top-0 h-96 w-96 translate-x-1/2 -translate-y-1/2 rounded-full bg-violet-500/18 blur-3xl"></div>
    <div class="absolute bottom-0 left-0 h-96 w-96 -translate-x-1/2 translate-y-1/2 rounded-full bg-emerald-400/10 blur-3xl"></div>
	<div class="absolute inset-0 bg-[radial-gradient(circle_at_top,rgba(168,85,247,0.08),transparent_30%),linear-gradient(180deg,rgba(18,18,44,0.92),rgba(8,11,26,0.96))]"></div>

	<div class="glass-card relative z-10 w-full max-w-md space-y-8 rounded-3xl border border-white/10 p-10 shadow-[0_30px_90px_rgba(2,6,23,0.45)] animate-fade-in">
		<div class="text-center">
			<div class="mx-auto mb-6 flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-violet-500/22 to-fuchsia-500/16 shadow-inner shadow-violet-900/40 ring-1 ring-inset ring-violet-200/10">
				<Sparkles class="w-8 h-8 text-violet-200" />
			</div>
			<h2 class="mb-2 text-3xl font-black tracking-tight text-white">Create Account</h2>
			<p class="font-medium text-slate-300">Join the next generation of insurance</p>
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
					<label for="register-role" class="ml-1 block text-xs font-bold uppercase tracking-widest text-slate-400">Account Type</label>
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

			<div class="border-t border-white/8 pt-4 text-center">
                <p class="text-sm font-medium text-slate-400">
                    Already a member? 
                    <a href="/login" class="ml-1 font-black text-violet-300 transition-colors hover:text-white">
                        Sign In
                    </a>
                </p>
			</div>
		</form>
	</div>
</div>
