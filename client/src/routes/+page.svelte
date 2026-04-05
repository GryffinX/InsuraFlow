<script lang="ts">
	import { auth } from '$lib/stores/auth.svelte';
	import { api } from '$lib/api/axios';
	import { Button } from '$lib/components';
	import ArrowRight from 'lucide-svelte/icons/arrow-right';
	import BadgeCheck from 'lucide-svelte/icons/badge-check';
	import Globe from 'lucide-svelte/icons/globe';
	import Lock from 'lucide-svelte/icons/lock';
	import Shield from 'lucide-svelte/icons/shield';
	import ShieldCheck from 'lucide-svelte/icons/shield-check';
	import Sparkles from 'lucide-svelte/icons/sparkles';
	import Zap from 'lucide-svelte/icons/zap';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { toast } from 'svelte-sonner';

	let policies = $state<any[]>([]);
	let isLoading = $state(true);

	const capabilities = [
		{
			title: 'Instant onboarding',
			copy: 'Modern enrollment flows with less friction and clearer policy setup.',
			icon: Zap,
			tone: 'from-violet-500/25 to-fuchsia-500/10 text-violet-200'
		},
		{
			title: 'Transparent claims',
			copy: 'Every claim stays visible through review, assessment, and settlement.',
			icon: ShieldCheck,
			tone: 'from-cyan-400/20 to-sky-500/10 text-cyan-100'
		},
		{
			title: 'Trusted security',
			copy: 'Built for secure handling of customer policies, providers, and documentation.',
			icon: Lock,
			tone: 'from-emerald-400/20 to-teal-500/10 text-emerald-100'
		}
	];

	onMount(async () => {
		try {
			const res = await api.get('policies/');
			policies = res.data.results || res.data;
		} catch (error) {
			console.error('Failed to load policies');
		} finally {
			isLoading = false;
		}
	});

	async function handleBuy(policyId: number) {
		if (!auth.user) {
			toast.info('Please sign in to purchase coverage');
			goto('/login');
			return;
		}

		try {
			await api.post(`policies/${policyId}/buy/`);
			toast.success('Coverage activated successfully!');
			const res = await api.get('policies/');
			policies = res.data.results || res.data;
		} catch (error: any) {
			toast.error(error.response?.data?.error || 'Failed to activate coverage');
		}
	}
</script>

<svelte:head>
	<title>InsuraFlow | Modern Digital Insurance</title>
</svelte:head>

<div class="relative overflow-hidden bg-[linear-gradient(180deg,_#171433_0%,_#0f1731_45%,_#0b1225_100%)]">
	<div class="pointer-events-none absolute inset-0">
		<div class="animate-float-orb absolute left-[-8rem] top-20 h-72 w-72 rounded-full bg-violet-500/18 blur-3xl"></div>
		<div class="animate-float-orb absolute right-[-6rem] top-32 h-80 w-80 rounded-full bg-fuchsia-500/14 blur-3xl [animation-delay:1.5s]"></div>
		<div class="animate-float-orb absolute bottom-24 left-1/3 h-64 w-64 rounded-full bg-cyan-400/10 blur-3xl [animation-delay:3s]"></div>
	</div>

	<section class="relative px-4 pb-24 pt-12 sm:px-6 lg:px-8 lg:pb-32 lg:pt-20">
		<div class="mx-auto grid max-w-7xl items-center gap-14 lg:grid-cols-[1.1fr_0.9fr]">
			<div class="relative z-10">
				<div class="brand-chip animate-fade-in">
					<Sparkles class="h-4 w-4" />
					InsuraFlow platform
				</div>
				<h1 class="mt-8 max-w-4xl text-5xl font-black leading-[0.95] tracking-tight text-white sm:text-6xl lg:text-7xl animate-fade-in">
					Insurance that feels
					<span class="bg-gradient-to-r from-violet-300 via-fuchsia-300 to-cyan-200 bg-clip-text text-transparent">
						 effortless, visible, and premium.
					</span>
				</h1>
				<p class="mt-8 max-w-2xl text-lg leading-8 text-slate-300 animate-fade-in-delay sm:text-xl">
					InsuraFlow brings policies, claims, providers, and customer journeys into one elegant digital flow, built for speed without losing trust.
				</p>
				<div class="mt-10 flex flex-col gap-4 sm:flex-row animate-fade-in-delay">
					<a href="/policies">
						<Button size="lg" class="w-full sm:w-auto">
							Explore Coverage
							<ArrowRight class="ml-2 h-5 w-5" />
						</Button>
					</a>
					<a href={auth.user ? '/dashboard' : '/register'}>
						<Button variant="outline" size="lg" class="w-full sm:w-auto">
							{auth.user ? 'Open Dashboard' : 'Start With InsuraFlow'}
						</Button>
					</a>
				</div>
				<div class="mt-12 grid max-w-2xl grid-cols-1 gap-4 sm:grid-cols-3">
					<div class="panel-card p-5 animate-fade-in">
						<p class="text-xs font-black uppercase tracking-[0.22em] text-violet-200">24/7 visibility</p>
						<p class="mt-2 text-sm leading-6 text-slate-300">Follow policies and claims without hidden status changes.</p>
					</div>
					<div class="panel-card p-5 animate-fade-in-delay">
						<p class="text-xs font-black uppercase tracking-[0.22em] text-cyan-100">Provider ready</p>
						<p class="mt-2 text-sm leading-6 text-slate-300">Built for admins, providers, agents, surveyors, and customers.</p>
					</div>
					<div class="panel-card p-5 animate-fade-in-delay">
						<p class="text-xs font-black uppercase tracking-[0.22em] text-emerald-100">Fast actions</p>
						<p class="mt-2 text-sm leading-6 text-slate-300">Cleaner workflows for buying, reviewing, and managing coverage.</p>
					</div>
				</div>
			</div>

			<div class="relative z-10">
				<div class="glass-card animate-pulse-glow rounded-[34px] p-6 sm:p-8">
					<div class="flex items-center justify-between">
						<div>
							<p class="text-xs font-black uppercase tracking-[0.24em] text-violet-200">InsuraFlow live overview</p>
							<h2 class="mt-3 text-2xl font-black text-white sm:text-3xl">A cleaner operating surface for digital insurance.</h2>
						</div>
						<div class="hidden h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-violet-500 to-fuchsia-500 shadow-[0_12px_30px_rgba(109,40,217,0.35)] sm:flex">
							<Shield class="h-7 w-7 text-white" />
						</div>
					</div>

					<div class="mt-8 space-y-4">
						<div class="rounded-3xl border border-white/8 bg-white/[0.03] p-5">
							<div class="flex items-center justify-between">
								<div>
									<p class="text-sm font-bold text-white">Coverage design</p>
									<p class="mt-1 text-sm text-slate-400">Publish plans with pricing, coverage, and provider visibility.</p>
								</div>
								<span class="rounded-full bg-violet-400/16 px-3 py-1 text-[11px] font-black uppercase tracking-[0.18em] text-violet-200">
									Active
								</span>
							</div>
						</div>
						<div class="grid gap-4 sm:grid-cols-2">
							<div class="rounded-3xl border border-white/8 bg-white/[0.03] p-5">
								<p class="text-xs font-black uppercase tracking-[0.2em] text-slate-400">Claims flow</p>
								<p class="mt-2 text-3xl font-black text-white">Realtime</p>
								<p class="mt-2 text-sm text-slate-400">Track review stages and outcomes with less back-and-forth.</p>
							</div>
							<div class="rounded-3xl border border-white/8 bg-white/[0.03] p-5">
								<p class="text-xs font-black uppercase tracking-[0.2em] text-slate-400">Customer trust</p>
								<p class="mt-2 text-3xl font-black text-white">Clear</p>
								<p class="mt-2 text-sm text-slate-400">Readable policy details and ownership status across the app.</p>
							</div>
						</div>
						<div class="rounded-3xl border border-violet-300/12 bg-gradient-to-r from-violet-500/12 to-cyan-400/8 p-5">
							<div class="flex items-center gap-3">
								<div class="flex h-11 w-11 items-center justify-center rounded-2xl bg-white/10">
									<Globe class="h-5 w-5 text-cyan-100" />
								</div>
								<div>
									<p class="text-sm font-bold text-white">Built to scale across regions and provider teams</p>
									<p class="mt-1 text-sm text-slate-300">One consistent experience from discovery to support.</p>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</section>

	<section class="relative px-4 py-8 sm:px-6 lg:px-8">
		<div class="mx-auto max-w-7xl">
			<div class="grid gap-6 md:grid-cols-3">
				{#each capabilities as capability, index}
					<div class="panel-card p-7 animate-fade-in" style={`animation-delay: ${index * 140}ms`}>
						<div class={`inline-flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br ${capability.tone}`}>
							<capability.icon class="h-6 w-6" />
						</div>
						<h3 class="mt-6 text-xl font-black text-white">{capability.title}</h3>
						<p class="mt-3 text-sm leading-7 text-slate-300">{capability.copy}</p>
					</div>
				{/each}
			</div>
		</div>
	</section>

	<section class="relative px-4 py-24 sm:px-6 lg:px-8">
		<div class="mx-auto max-w-7xl">
			<div class="mb-12 flex flex-col gap-6 md:flex-row md:items-end md:justify-between">
				<div>
					<div class="brand-chip">
						<BadgeCheck class="h-4 w-4" />
						Featured policies
					</div>
					<h2 class="mt-6 text-4xl font-black tracking-tight text-white sm:text-5xl">Coverage that looks as clear as it feels.</h2>
					<p class="mt-4 max-w-2xl text-lg leading-8 text-slate-300">
						Browse plans designed for real customers, with pricing and policy details surfaced in a cleaner layout.
					</p>
				</div>
				<a href="/policies" class="inline-flex items-center gap-2 text-sm font-black uppercase tracking-[0.18em] text-violet-200 transition hover:gap-3 hover:text-white">
					View all plans
					<ArrowRight class="h-4 w-4" />
				</a>
			</div>

			<div class="grid grid-cols-1 gap-8 md:grid-cols-2 xl:grid-cols-3">
				{#if isLoading}
					{#each Array(3) as _}
						<div class="panel-card h-[360px] animate-pulse"></div>
					{/each}
				{:else}
					{#each policies.slice(0, 3) as policy}
						<div class="panel-card group flex flex-col overflow-hidden p-7 transition-transform duration-300 hover:-translate-y-1 hover:shadow-[0_22px_65px_rgba(7,10,30,0.42)]">
							<div class="flex items-start justify-between">
								<div class="flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-violet-500/22 via-fuchsia-400/14 to-transparent text-violet-100 ring-1 ring-inset ring-violet-200/12 transition-transform duration-300 group-hover:scale-110">
									<Shield class="h-7 w-7" />
								</div>
								<div class="text-right">
									<p class="text-3xl font-black text-white">${parseFloat(policy.premium_amount).toLocaleString()}</p>
									<p class="mt-1 text-[11px] font-black uppercase tracking-[0.18em] text-slate-400">annual premium</p>
								</div>
							</div>

							<div class="mt-8">
								<p class="text-[11px] font-black uppercase tracking-[0.22em] text-violet-200">{policy.policy_type} plan</p>
								<h3 class="mt-3 text-2xl font-black text-white">{policy.title}</h3>
								<p class="mt-4 line-clamp-3 text-sm leading-7 text-slate-300">{policy.description}</p>
							</div>

							<div class="mt-8 grid grid-cols-2 gap-4 rounded-3xl border border-white/8 bg-white/[0.03] p-4">
								<div>
									<p class="text-[10px] font-black uppercase tracking-[0.18em] text-slate-400">Coverage</p>
									<p class="mt-2 text-lg font-black text-white">${parseFloat(policy.coverage_amount).toLocaleString()}</p>
								</div>
								<div class="text-right">
									<p class="text-[10px] font-black uppercase tracking-[0.18em] text-slate-400">Provider</p>
									<p class="mt-2 text-sm font-bold text-slate-200">{policy.provider?.company_name || 'InsuraFlow'}</p>
								</div>
							</div>

							<div class="mt-8 flex-1"></div>

							{#if policy.is_owned}
								<Button variant="outline" class="mt-6 w-full !cursor-default border-emerald-300/15 bg-emerald-400/10 text-emerald-100 hover:bg-emerald-400/10">
									Already Owned
								</Button>
							{:else}
								<Button class="mt-6 w-full" onclick={() => handleBuy(policy.id)}>
									Get Protected
								</Button>
							{/if}
						</div>
					{/each}
				{/if}
			</div>
		</div>
	</section>

	<footer class="relative border-t border-white/8 px-4 py-14 sm:px-6 lg:px-8">
		<div class="mx-auto flex max-w-7xl flex-col items-center justify-between gap-5 text-center md:flex-row md:text-left">
			<div class="flex items-center gap-3">
				<div class="flex h-11 w-11 items-center justify-center rounded-2xl bg-gradient-to-br from-violet-500 via-fuchsia-500 to-indigo-500 shadow-[0_12px_30px_rgba(91,33,182,0.35)]">
					<ShieldCheck class="h-5 w-5 text-white" />
				</div>
				<div>
					<p class="text-[10px] font-black uppercase tracking-[0.24em] text-violet-300/80">Digital insurance</p>
					<p class="text-xl font-black tracking-tight text-white">InsuraFlow</p>
				</div>
			</div>
			<p class="text-sm font-medium text-slate-400">© 2026 InsuraFlow. Built for trust, speed, and calm operations.</p>
		</div>
	</footer>
</div>
