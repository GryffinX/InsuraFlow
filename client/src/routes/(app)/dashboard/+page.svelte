<script lang="ts">
	import { auth } from '$lib/stores/auth.svelte';
	import { api } from '$lib/api/axios';
	import { onMount } from 'svelte';
	import Activity from 'lucide-svelte/icons/activity';
	import AlertCircle from 'lucide-svelte/icons/alert-circle';
	import ArrowRight from 'lucide-svelte/icons/arrow-right';
	import CheckCircle from 'lucide-svelte/icons/check-circle';
	import Clock from 'lucide-svelte/icons/clock';
	import FileText from 'lucide-svelte/icons/file-text';
	import Plus from 'lucide-svelte/icons/plus';
	import Shield from 'lucide-svelte/icons/shield';
	import Users from 'lucide-svelte/icons/users';
	import { Button } from '$lib/components';

	type DashboardStat = {
		label: string;
		value: string | number;
		icon: typeof Shield;
		color: string;
		bg: string;
	};

	const statTone = {
		primary: { color: 'text-violet-200', bg: 'bg-violet-500/14 border border-violet-300/16' },
		secondary: { color: 'text-amber-200', bg: 'bg-amber-500/14 border border-amber-300/16' },
		tertiary: { color: 'text-emerald-200', bg: 'bg-emerald-500/14 border border-emerald-300/16' }
	};

	let stats = $state({
		primary: { label: '', value: 0 as string | number, icon: Shield, ...statTone.primary } satisfies DashboardStat,
		secondary: { label: '', value: 0 as string | number, icon: FileText, ...statTone.secondary } satisfies DashboardStat,
		tertiary: { label: '', value: 0 as string | number, icon: CheckCircle, ...statTone.tertiary } satisfies DashboardStat
	});

	let mainData = $state<any[]>([]);
	let secondaryData = $state<any[]>([]);
	let isLoading = $state(true);

	const role = auth.user?.role;

	onMount(async () => {
		try {
			if (role === 'customer') {
				const [policiesRes, claimsRes] = await Promise.all([
					api.get('user-policies/'),
					api.get('claims/')
				]);
				mainData = policiesRes.data.results || (Array.isArray(policiesRes.data) ? policiesRes.data : []);
				secondaryData = claimsRes.data.results || (Array.isArray(claimsRes.data) ? claimsRes.data : []);
				
				stats.primary = { label: 'Active Policies', value: mainData.filter((p) => p.status === 'active').length, icon: Shield, ...statTone.primary };
				stats.secondary = { label: 'Pending Claims', value: secondaryData.filter((c) => c.status === 'filed').length, icon: FileText, ...statTone.secondary };
				stats.tertiary = { label: 'Total Coverage', value: `$${mainData.reduce((acc, p) => acc + parseFloat(p.policy?.coverage_amount || 0), 0).toLocaleString()}`, icon: CheckCircle, ...statTone.tertiary };
			} else if (role === 'provider') {
				const [policiesRes, claimsRes, customersRes] = await Promise.all([
					api.get('policies/'),
					api.get('claims/'),
					api.get('user-policies/')
				]);
				mainData = policiesRes.data.results || (Array.isArray(policiesRes.data) ? policiesRes.data : []);
				secondaryData = claimsRes.data.results || (Array.isArray(claimsRes.data) ? claimsRes.data : []);

				stats.primary = { label: 'Our Policies', value: mainData.length, icon: Shield, ...statTone.primary };
				stats.secondary = { label: 'Policy Claims', value: secondaryData.length, icon: FileText, ...statTone.secondary };
				const customerData = customersRes.data.results || (Array.isArray(customersRes.data) ? customersRes.data : []);
				stats.tertiary = { label: 'Total Customers', value: customerData.length, icon: Users, ...statTone.tertiary };
			} else if (role === 'agent') {
				const [policiesRes, claimsRes] = await Promise.all([
					api.get('user-policies/'),
					api.get('claims/')
				]);
				mainData = policiesRes.data.results || (Array.isArray(policiesRes.data) ? policiesRes.data : []);
				secondaryData = claimsRes.data.results || (Array.isArray(claimsRes.data) ? claimsRes.data : []);

				stats.primary = { label: 'Managed Policies', value: mainData.length, icon: Shield, ...statTone.primary };
				stats.secondary = { label: 'Customer Claims', value: secondaryData.length, icon: FileText, ...statTone.secondary };
				stats.tertiary = { label: 'Active Clients', value: new Set(mainData.map((p) => p.user?.id || p.user)).size, icon: Users, ...statTone.tertiary };
			} else if (role === 'surveyor') {
				const claimsRes = await api.get('claims/');
				mainData = claimsRes.data.results || (Array.isArray(claimsRes.data) ? claimsRes.data : []);
				
				stats.primary = { label: 'Assigned Claims', value: mainData.length, icon: FileText, ...statTone.primary };
				stats.secondary = { label: 'Pending Review', value: mainData.filter((c) => c.status === 'under_review').length, icon: Clock, ...statTone.secondary };
				stats.tertiary = { label: 'Completed', value: mainData.filter((c) => ['approved', 'rejected', 'settled'].includes(c.status)).length, icon: CheckCircle, ...statTone.tertiary };
			} else if (role === 'admin') {
				const [policiesRes, claimsRes] = await Promise.all([
					api.get('policies/'),
					api.get('claims/'),
				]);
				mainData = policiesRes.data.results || (Array.isArray(policiesRes.data) ? policiesRes.data : []);
				secondaryData = claimsRes.data.results || (Array.isArray(claimsRes.data) ? claimsRes.data : []);

				stats.primary = { label: 'Total Policies', value: mainData.length, icon: Shield, ...statTone.primary };
				stats.secondary = { label: 'Total Claims', value: secondaryData.length, icon: FileText, ...statTone.secondary };
				stats.tertiary = { label: 'System Health', value: 'Optimal', icon: Activity, ...statTone.tertiary };
			}
		} catch (error) {
			console.error('Failed to load dashboard data', error);
		} finally {
			isLoading = false;
		}
	});

	function getStatusIcon(status: string) {
		switch (status.toLowerCase()) {
			case 'active':
			case 'approved':
			case 'settled':
				return { icon: CheckCircle, color: 'text-emerald-200', bg: 'bg-emerald-500/14' };
			case 'pending':
			case 'filed':
			case 'under_review':
				return { icon: Clock, color: 'text-amber-200', bg: 'bg-amber-500/14' };
			case 'rejected':
			case 'cancelled':
				return { icon: AlertCircle, color: 'text-rose-200', bg: 'bg-rose-500/14' };
			default:
				return { icon: AlertCircle, color: 'text-slate-200', bg: 'bg-slate-500/12' };
		}
	}
</script>

<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <div class="mb-12 flex flex-col items-start justify-between gap-6 sm:flex-row sm:items-center">
        <div class="animate-fade-in">
            <div class="mb-3 flex items-center gap-3">
                <span class="rounded-full border border-violet-300/18 bg-violet-500/14 px-3 py-1 text-[10px] font-black uppercase tracking-widest text-violet-100">
                    {role} Dashboard
                </span>
            </div>
            <h1 class="text-4xl font-black tracking-tight text-slate-50">Welcome, {auth.user?.username}</h1>
            <p class="mt-1 text-lg font-medium text-slate-300">Here's an overview of your InsuraFlow workspace.</p>
        </div>

        <div class="flex gap-3">
            {#if role === 'customer'}
                <a href="/claims/new">
                    <Button class="h-12 px-6">
                        <Plus class="mr-2 h-5 w-5" /> File a Claim
                    </Button>
                </a>
            {/if}
            {#if role === 'provider' || role === 'admin'}
                <a href="/policies/new">
                    <Button class="h-12 px-6">
                        <Plus class="mr-2 h-5 w-5" /> Create Policy
                    </Button>
                </a>
            {/if}
        </div>
    </div>

	<!-- Stats Grid -->
	<div class="mb-12 grid grid-cols-1 gap-8 md:grid-cols-3">
		{#each Object.values(stats) as stat}
			<div class="dashboard-card flex items-center gap-6 p-8 transition-all duration-300 hover:-translate-y-1 hover:border-violet-300/22 hover:shadow-[0_28px_70px_rgba(76,29,149,0.26)]">
				<div class={`${stat.bg} ${stat.color} rounded-2xl p-5`}>
					<stat.icon class="h-7 w-7" />
				</div>
				<div>
					<p class="mb-1 text-xs font-black uppercase tracking-widest text-slate-400">{stat.label}</p>
					<p class="text-3xl font-black text-slate-50">{stat.value}</p>
				</div>
			</div>
		{/each}
	</div>

	<div class="grid grid-cols-1 gap-12 lg:grid-cols-2">
		<!-- Primary Data List -->
		<div class="dashboard-card flex flex-col overflow-hidden">
			<div class="flex items-center justify-between border-b border-white/8 bg-white/[0.03] p-8">
				<h2 class="text-2xl font-black tracking-tight text-slate-50">
					{role === 'surveyor' ? 'Assigned Claims' : 'Recent Policies'}
				</h2>
				<a href={role === 'surveyor' ? '/claims' : '/policies'} class="flex items-center gap-1 font-bold text-violet-200 transition-all hover:gap-2 hover:text-violet-100">
					View all <ArrowRight class="h-4 w-4" />
				</a>
			</div>
			<div class="divide-y divide-white/6">
				{#if isLoading}
					{#each Array(3) as _}
						<div class="flex gap-6 p-8 animate-pulse">
							<div class="h-14 w-14 rounded-2xl bg-white/6"></div>
							<div class="flex-grow space-y-3">
								<div class="h-5 w-1/3 rounded-lg bg-white/6"></div>
								<div class="h-4 w-1/4 rounded-lg bg-white/6"></div>
							</div>
						</div>
					{/each}
				{:else if mainData.length > 0}
					{#each mainData.slice(0, 5) as item}
						{@const statusStyle = getStatusIcon(item.status || 'active')}
						<div class="group flex items-center justify-between p-8 transition-colors hover:bg-white/[0.03]">
							<div class="flex items-center gap-6">
								<div class="rounded-2xl border border-white/8 bg-white/[0.04] p-4 text-slate-300 transition-colors group-hover:border-violet-300/18 group-hover:bg-violet-500/10 group-hover:text-violet-100">
									{#if role === 'surveyor'}
										<FileText class="h-6 w-6" />
									{:else}
										<Shield class="h-6 w-6" />
									{/if}
								</div>
								<div>
									{#if role === 'surveyor'}
										<p class="text-base font-bold tracking-tight text-slate-50 transition-colors group-hover:text-violet-100">Claim #{item.id}</p>
										<p class="text-sm font-medium text-slate-300">{item.user_policy?.policy?.title || 'Unknown'}</p>
									{:else if role === 'customer' || role === 'agent'}
										<p class="text-base font-bold tracking-tight text-slate-50 transition-colors group-hover:text-violet-100">{item.policy?.title || 'Unknown'}</p>
										<p class="text-sm font-medium text-slate-300">{item.policy_number} • {item.policy?.policy_type || 'Unknown'}</p>
									{:else}
										<p class="text-base font-bold tracking-tight text-slate-50 transition-colors group-hover:text-violet-100">{item.title || item.policy_number}</p>
										<p class="text-sm font-medium capitalize text-slate-300">{item.policy_type || 'Policy'}</p>
									{/if}
								</div>
							</div>
							<span class={`rounded-full border border-current/10 px-4 py-1.5 text-[10px] font-black uppercase tracking-widest ${statusStyle.bg} ${statusStyle.color}`}>
								{item.status || 'active'}
							</span>
						</div>
					{/each}
				{:else}
					<div class="p-20 text-center">
						<div class="mx-auto mb-6 flex h-16 w-16 items-center justify-center rounded-2xl border border-white/6 bg-white/[0.04]">
                            <Activity class="h-8 w-8 text-slate-500" />
                        </div>
						<p class="text-xs font-bold uppercase tracking-widest text-slate-400">Nothing to show yet</p>
					</div>
				{/if}
			</div>
		</div>

		<!-- Secondary Data List -->
		{#if role !== 'surveyor'}
		<div class="dashboard-card flex flex-col overflow-hidden">
			<div class="flex items-center justify-between border-b border-white/8 bg-white/[0.03] p-8">
				<h2 class="text-2xl font-black tracking-tight text-slate-50">Recent Claims</h2>
				<a href="/claims" class="flex items-center gap-1 font-bold text-violet-200 transition-all hover:gap-2 hover:text-violet-100">
					View all <ArrowRight class="h-4 w-4" />
				</a>
			</div>
			<div class="divide-y divide-white/6">
				{#if isLoading}
					{#each Array(3) as _}
						<div class="flex gap-6 p-8 animate-pulse">
							<div class="h-14 w-14 rounded-2xl bg-white/6"></div>
							<div class="flex-grow space-y-3">
								<div class="h-5 w-1/3 rounded-lg bg-white/6"></div>
								<div class="h-4 w-1/4 rounded-lg bg-white/6"></div>
							</div>
						</div>
					{/each}
				{:else if secondaryData.length > 0}
					{#each secondaryData.slice(0, 5) as claim}
						{@const status = getStatusIcon(claim.status)}
						<div class="group flex items-center justify-between p-8 transition-colors hover:bg-white/[0.03]">
							<div class="flex items-center gap-6">
								<div class={`${status.bg} ${status.color} rounded-2xl border border-current/10 p-4 transition-transform group-hover:scale-110`}>
									<status.icon class="h-6 w-6" />
								</div>
								<div>
									<p class="text-base font-bold tracking-tight text-slate-50 transition-colors group-hover:text-violet-100">Claim #{claim.id}</p>
									<p class="text-sm font-medium uppercase tracking-tight text-slate-300">{claim.status} • {new Date(claim.claim_date).toLocaleDateString()}</p>
								</div>
							</div>
							<p class="text-lg font-black text-slate-50">${parseFloat(claim.claim_amount).toLocaleString()}</p>
						</div>
					{/each}
				{:else}
					<div class="p-20 text-center">
                        <div class="mx-auto mb-6 flex h-16 w-16 items-center justify-center rounded-2xl border border-white/6 bg-white/[0.04]">
                            <FileText class="h-8 w-8 text-slate-500" />
                        </div>
						<p class="mb-6 text-xs font-bold uppercase tracking-widest text-slate-400">No recent claims</p>
						{#if role === 'customer'}
							<a href="/claims/new">
								<Button variant="outline" size="sm">File your first claim</Button>
							</a>
						{/if}
					</div>
				{/if}
			</div>
		</div>
		{/if}
	</div>
</div>

