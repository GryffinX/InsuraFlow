<script lang="ts">
	import { auth } from '$lib/stores/auth.svelte';
	import { Button } from '$lib/components';
	import { LogOut, User, Menu, X, ShieldCheck } from 'lucide-svelte';
	import { cn } from '$lib/utils';
    import { page } from '$app/state';

	let isOpen = $state(false);

	const navLinks = [
		{ href: '/dashboard', label: 'Dashboard' },
		{ href: '/policies', label: 'Policies' },
		{ href: '/claims', label: 'Claims' },
	];
</script>

<nav class="bg-white border-b border-slate-200 sticky top-0 z-50">
	<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
		<div class="flex justify-between h-16">
			<div class="flex items-center">
				<a href="/" class="flex items-center space-x-2 group">
					<div class="bg-indigo-600 p-1.5 rounded-lg group-hover:bg-indigo-700 transition-colors">
						<ShieldCheck class="w-6 h-6 text-white" />
					</div>
					<span class="text-xl font-bold text-slate-900 tracking-tight">InsuraFlow</span>
				</a>
				
				<div class="hidden md:ml-10 md:flex md:space-x-8">
					{#each navLinks as link}
						<a
							href={link.href}
							class={cn(
								'inline-flex items-center px-1 pt-1 text-sm font-medium transition-colors border-b-2',
								page.url.pathname.startsWith(link.href)
									? 'border-indigo-500 text-slate-900'
									: 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300'
							)}
						>
							{link.label}
						</a>
					{/each}
				</div>
			</div>

			<div class="hidden md:flex items-center space-x-4">
				{#if auth.user}
					<div class="flex items-center space-x-4">
						<div class="flex flex-col items-end">
							<span class="text-sm font-medium text-slate-900">{auth.user.username}</span>
							<span class="text-xs text-slate-500 capitalize">{auth.user.role}</span>
						</div>
						<Button variant="ghost" size="icon" onclick={() => auth.logout()}>
							<LogOut class="w-5 h-5 text-slate-500" />
						</Button>
					</div>
				{:else}
					<a href="/login">
						<Button variant="ghost">Log in</Button>
					</a>
					<a href="/register">
						<Button>Sign up</Button>
					</a>
				{/if}
			</div>

			<div class="flex items-center md:hidden">
				<button
					onclick={() => (isOpen = !isOpen)}
					class="inline-flex items-center justify-center p-2 rounded-md text-slate-400 hover:text-slate-500 hover:bg-slate-100 focus:outline-none"
				>
					{#if isOpen}
						<X class="block h-6 w-6" />
					{:else}
						<Menu class="block h-6 w-6" />
					{/if}
				</button>
			</div>
		</div>
	</div>

	<!-- Mobile menu -->
	{#if isOpen}
		<div class="md:hidden bg-white border-b border-slate-200">
			<div class="pt-2 pb-3 space-y-1">
				{#each navLinks as link}
					<a
						href={link.href}
						class={cn(
							'block pl-3 pr-4 py-2 border-l-4 text-base font-medium',
							page.url.pathname.startsWith(link.href)
								? 'bg-indigo-50 border-indigo-500 text-indigo-700'
								: 'border-transparent text-slate-500 hover:bg-slate-50 hover:border-slate-300 hover:text-slate-700'
						)}
						onclick={() => (isOpen = false)}
					>
						{link.label}
					</a>
				{/each}
			</div>
			<div class="pt-4 pb-3 border-t border-slate-200">
				{#if auth.user}
					<div class="flex items-center px-4 mb-3">
						<div class="flex-shrink-0">
							<div class="h-10 w-10 rounded-full bg-slate-200 flex items-center justify-center">
								<User class="w-6 h-6 text-slate-500" />
							</div>
						</div>
						<div class="ml-3">
							<div class="text-base font-medium text-slate-800">{auth.user.username}</div>
							<div class="text-sm font-medium text-slate-500">{auth.user.email}</div>
						</div>
					</div>
					<div class="mt-3 space-y-1 px-4">
						<Button class="w-full justify-start" variant="ghost" onclick={() => auth.logout()}>
							<LogOut class="mr-2 h-4 w-4" /> Log out
						</Button>
					</div>
				{:else}
					<div class="px-4 space-y-2">
						<a href="/login" class="block w-full">
							<Button class="w-full" variant="outline">Log in</Button>
						</a>
						<a href="/register" class="block w-full">
							<Button class="w-full">Sign up</Button>
						</a>
					</div>
				{/if}
			</div>
		</div>
	{/if}
</nav>
