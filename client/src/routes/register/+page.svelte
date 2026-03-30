<script lang="ts">
	import { auth } from '$lib/stores/auth.svelte';
	import { Button, Input } from '$lib/components';
	import { toast } from 'svelte-sonner';
	import { goto } from '$app/navigation';
    import { ShieldCheck } from 'lucide-svelte';

	let username = $state('');
	let email = $state('');
	let password = $state('');
	let role = $state('customer');
	let isLoading = $state(false);

	async function handleSubmit(e: Event) {
		e.preventDefault();
		isLoading = true;
		try {
			await auth.register({ username, email, password, role });
			toast.success('Account created! Please log in.');
			goto('/login');
		} catch (error: any) {
			const detail = error.response?.data;
			if (typeof detail === 'object') {
				const firstError = Object.values(detail)[0];
				toast.error(Array.isArray(firstError) ? firstError[0] : 'Registration failed');
			} else {
				toast.error('Registration failed');
			}
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
			<h1 class="text-3xl font-bold text-slate-900 tracking-tight">Create Account</h1>
			<p class="text-slate-500">Join InsuraFlow to start your journey</p>
		</div>

		<form onsubmit={handleSubmit} class="space-y-6">
			<Input
				label="Username"
				id="username"
				placeholder="johndoe"
				required
				bind:value={username}
			/>
			<Input
				label="Email Address"
				type="email"
				id="email"
				placeholder="name@example.com"
				required
				bind:value={email}
			/>
			<Input
				label="Password"
				type="password"
				id="password"
				placeholder="••••••••"
				required
				bind:value={password}
			/>

			<div class="space-y-1">
				<label class="block text-sm font-medium text-slate-700" for="role">
					I am a...
				</label>
				<select
					id="role"
					class="block w-full rounded-md border-slate-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm transition-colors border p-2 outline-none"
					bind:value={role}
				>
					<option value="customer">Customer</option>
					<option value="agent">Insurance Agent</option>
					<option value="surveyor">Claims Surveyor</option>
				</select>
			</div>

			<Button type="submit" class="w-full h-11" loading={isLoading}>
				Create Account
			</Button>

			<div class="relative">
				<div class="absolute inset-0 flex items-center">
					<div class="w-full border-t border-slate-200"></div>
				</div>
				<div class="relative flex justify-center text-sm">
					<span class="px-2 bg-white text-slate-500">Already have an account?</span>
				</div>
			</div>

			<a href="/login" class="block w-full">
				<Button variant="outline" class="w-full h-11">
					Log in instead
				</Button>
			</a>
		</form>
	</div>
</div>
