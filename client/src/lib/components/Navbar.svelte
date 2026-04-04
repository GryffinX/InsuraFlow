<script lang="ts">
	import { auth } from '$lib/stores/auth.svelte';
	import { Button } from '$lib/components';
	import { LogOut, User, Menu, X, ShieldCheck } from 'lucide-svelte';
	import { cn } from '$lib/utils';
	import { page } from '$app/state';

	let isMenuOpen = $state(false);
	let isUserDropdownOpen = $state(false);

	const navLinks = $derived([
		{ href: '/dashboard', label: 'Dashboard' },
		{ href: '/policies', label: 'Explore' },
		{ href: '/claims', label: 'Claims' },
        ...(auth.user?.role === 'admin' ? [{ href: '/users', label: 'Team' }] : []),
	]);

	function toggleMenu() { isMenuOpen = !isMenuOpen; }
	function toggleUserDropdown() { isUserDropdownOpen = !isUserDropdownOpen; }
</script>

<nav class="sticky top-0 z-50 border-b border-white/8 bg-slate-950/45 backdrop-blur-2xl">
	<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
		<div class="flex justify-between h-20">
			<div class="flex items-center">
				<a href="/" class="flex items-center gap-3 transition-opacity hover:opacity-90">
					<div class="relative flex h-11 w-11 items-center justify-center overflow-hidden rounded-2xl border border-violet-300/20 bg-gradient-to-br from-violet-500 via-fuchsia-500 to-indigo-500 shadow-[0_12px_30px_rgba(91,33,182,0.35)]">
						<div class="absolute inset-[1px] rounded-[15px] bg-slate-950/20"></div>
						<ShieldCheck class="relative z-10 w-5 h-5 text-white" />
					</div>
					<div>
						<p class="text-[10px] font-black uppercase tracking-[0.28em] text-violet-300/80">Digital Coverage</p>
						<span class="text-xl font-black tracking-tight text-white">InsuraFlow</span>
					</div>
				</a>
				
				<div class="hidden md:ml-10 md:flex md:space-x-1">
					{#each navLinks as link}
						<a
							href={link.href}
							class={cn(
								'rounded-xl px-4 py-2 text-sm font-bold transition-all duration-200',
								page.url.pathname.startsWith(link.href)
									? 'border border-violet-300/14 bg-violet-400/12 text-violet-200 shadow-[0_10px_25px_rgba(76,29,149,0.18)]'
									: 'text-slate-300 hover:bg-white/6 hover:text-white'
							)}
						>
							{link.label}
						</a>
					{/each}
				</div>
			</div>

			<div class="hidden md:flex md:items-center md:gap-4">
				{#if auth.user}
					<div class="relative">
						<button
							onclick={toggleUserDropdown}
							class="flex items-center gap-3 rounded-2xl border border-white/6 bg-white/[0.03] py-1.5 pl-3 pr-2 transition-colors hover:border-white/10 hover:bg-white/[0.06]"
						>
							<div class="text-right">
								<p class="text-sm font-bold leading-none text-white">{auth.user.username}</p>
								<p class="mt-1 text-[10px] font-bold uppercase tracking-[0.18em] text-slate-400">{auth.user.role}</p>
							</div>
							<div class="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-violet-400/25 to-fuchsia-400/15 font-bold text-violet-100 ring-1 ring-inset ring-violet-200/15">
								{auth.user.username.charAt(0).toUpperCase()}
							</div>
						</button>

						{#if isUserDropdownOpen}
							<div class="glass-card absolute right-0 mt-2 w-56 overflow-hidden rounded-2xl py-2 animate-fade-in">
								<a href="/profile" class="flex items-center gap-3 px-4 py-3 text-sm font-bold text-slate-100 transition-colors hover:bg-white/6">
									<User class="w-4 h-4" /> Profile Settings
								</a>
								<button
									onclick={() => { auth.logout(); isUserDropdownOpen = false; }}
									class="flex w-full items-center gap-3 px-4 py-3 text-sm font-bold text-rose-300 transition-colors hover:bg-rose-400/10"
								>
									<LogOut class="w-4 h-4" /> Sign Out
								</button>
							</div>
						{/if}
					</div>
				{:else}
					<a href="/login">
						<Button variant="ghost">Sign in</Button>
					</a>
					<a href="/register">
						<Button>Get Started</Button>
					</a>
				{/if}
			</div>

			<div class="flex items-center md:hidden">
				<button onclick={toggleMenu} class="rounded-xl p-2 text-slate-300 transition-colors hover:bg-white/8 hover:text-white">
					{#if isMenuOpen} <X /> {:else} <Menu /> {/if}
				</button>
			</div>
		</div>
	</div>

	{#if isMenuOpen}
		<div class="space-y-4 border-t border-white/8 bg-slate-950/80 px-4 py-6 animate-fade-in md:hidden">
			{#each navLinks as link}
				<a href={link.href} class="block rounded-2xl px-4 py-3 text-base font-bold text-slate-200 hover:bg-white/6">
					{link.label}
				</a>
			{/each}
			<div class="grid grid-cols-2 gap-4 border-t border-white/8 pt-4">
				{#if auth.user}
					<Button variant="outline" class="w-full" onclick={auth.logout}>Sign Out</Button>
					<a href="/profile" class="w-full"><Button class="w-full">Profile</Button></a>
				{:else}
					<a href="/login" class="w-full"><Button variant="outline" class="w-full">Login</Button></a>
					<a href="/register" class="w-full"><Button class="w-full">Sign up</Button></a>
				{/if}
			</div>
		</div>
	{/if}
</nav>
