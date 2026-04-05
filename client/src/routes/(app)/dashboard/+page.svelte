<script lang="ts">
	import { auth } from '$lib/stores/auth.svelte';
	import { api } from '$lib/api/axios';
	import { onMount } from 'svelte';
	import { Shield, FileText, Clock, CheckCircle, AlertCircle, ArrowRight, Users, Briefcase, Activity, Plus } from 'lucide-svelte';
	import { Button } from '$lib/components';

	let stats = $state({
		primary: { label: '', value: 0 as string | number, icon: Shield, color: 'text-indigo-600', bg: 'bg-indigo-50' },
		secondary: { label: '', value: 0 as string | number, icon: FileText, color: 'text-amber-600', bg: 'bg-amber-50' },
		tertiary: { label: '', value: 0 as string | number, icon: CheckCircle, color: 'text-emerald-600', bg: 'bg-emerald-50' }
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
				
				stats.primary = { label: 'Active Policies', value: mainData.filter(p => p.status === 'active').length, icon: Shield, color: 'text-indigo-600', bg: 'bg-indigo-50' };
				stats.secondary = { label: 'Pending Claims', value: secondaryData.filter(c => c.status === 'filed').length, icon: FileText, color: 'text-amber-600', bg: 'bg-amber-50' };
				stats.tertiary = { label: 'Total Coverage', value: `$${mainData.reduce((acc, p) => acc + parseFloat(p.policy?.coverage_amount || 0), 0).toLocaleString()}`, icon: CheckCircle, color: 'text-emerald-600', bg: 'bg-emerald-50' };
			} else if (role === 'provider') {
				const [policiesRes, claimsRes, customersRes] = await Promise.all([
					api.get('policies/'),
					api.get('claims/'),
					api.get('user-policies/')
				]);
				mainData = policiesRes.data.results || (Array.isArray(policiesRes.data) ? policiesRes.data : []);
				secondaryData = claimsRes.data.results || (Array.isArray(claimsRes.data) ? claimsRes.data : []);

				stats.primary = { label: 'Our Policies', value: mainData.length, icon: Shield, color: 'text-indigo-600', bg: 'bg-indigo-50' };
				stats.secondary = { label: 'Policy Claims', value: secondaryData.length, icon: FileText, color: 'text-amber-600', bg: 'bg-amber-50' };
				const customerData = customersRes.data.results || (Array.isArray(customersRes.data) ? customersRes.data : []);
				stats.tertiary = { label: 'Total Customers', value: customerData.length, icon: Users, color: 'text-emerald-600', bg: 'bg-emerald-50' };
			} else if (role === 'agent') {
				const [policiesRes, claimsRes] = await Promise.all([
					api.get('user-policies/'),
					api.get('claims/')
				]);
				mainData = policiesRes.data.results || (Array.isArray(policiesRes.data) ? policiesRes.data : []);
				secondaryData = claimsRes.data.results || (Array.isArray(claimsRes.data) ? claimsRes.data : []);

				stats.primary = { label: 'Managed Policies', value: mainData.length, icon: Shield, color: 'text-indigo-600', bg: 'bg-indigo-50' };
				stats.secondary = { label: 'Customer Claims', value: secondaryData.length, icon: FileText, color: 'text-amber-600', bg: 'bg-amber-50' };
				stats.tertiary = { label: 'Active Clients', value: new Set(mainData.map(p => p.user?.id || p.user)).size, icon: Users, color: 'text-emerald-600', bg: 'bg-emerald-50' };
			} else if (role === 'surveyor') {
				const claimsRes = await api.get('claims/');
				mainData = claimsRes.data.results || (Array.isArray(claimsRes.data) ? claimsRes.data : []);
				
				stats.primary = { label: 'Assigned Claims', value: mainData.length, icon: FileText, color: 'text-indigo-600', bg: 'bg-indigo-50' };
				stats.secondary = { label: 'Pending Review', value: mainData.filter(c => c.status === 'under_review').length, icon: Clock, color: 'text-amber-600', bg: 'bg-amber-50' };
				stats.tertiary = { label: 'Completed', value: mainData.filter(c => ['approved', 'rejected', 'settled'].includes(c.status)).length, icon: CheckCircle, color: 'text-emerald-600', bg: 'bg-emerald-50' };
			} else if (role === 'admin') {
				const [policiesRes, claimsRes] = await Promise.all([
					api.get('policies/'),
					api.get('claims/'),
				]);
				mainData = policiesRes.data.results || (Array.isArray(policiesRes.data) ? policiesRes.data : []);
				secondaryData = claimsRes.data.results || (Array.isArray(claimsRes.data) ? claimsRes.data : []);

				stats.primary = { label: 'Total Policies', value: mainData.length, icon: Shield, color: 'text-indigo-600', bg: 'bg-indigo-50' };
				stats.secondary = { label: 'Total Claims', value: secondaryData.length, icon: FileText, color: 'text-amber-600', bg: 'bg-amber-50' };
				stats.tertiary = { label: 'System Health', value: 'Optimal', icon: Activity, color: 'text-emerald-600', bg: 'bg-emerald-50' };
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
				return { icon: CheckCircle, color: 'text-emerald-500', bg: 'bg-emerald-50' };
			case 'pending':
			case 'filed':
			case 'under_review':
				return { icon: Clock, color: 'text-amber-500', bg: 'bg-amber-50' };
			case 'rejected':
			case 'cancelled':
				return { icon: AlertCircle, color: 'text-rose-500', bg: 'bg-rose-50' };
			default:
				return { icon: AlertCircle, color: 'text-slate-500', bg: 'bg-slate-50' };
		}
	}
</script>

<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-6 mb-12">
        <div class="animate-fade-in">
            <div class="flex items-center gap-3 mb-3">
                <span class="px-3 py-1 bg-indigo-100 text-indigo-700 rounded-full text-[10px] font-black uppercase tracking-widest">
                    {role} Dashboard
                </span>
            </div>
            <h1 class="text-4xl font-black text-slate-900 tracking-tight">Welcome, {auth.user?.username}</h1>
            <p class="text-slate-500 mt-1 font-medium text-lg">Here's an overview of your InsuraFlow workspace.</p>
        </div>
        
        <div class="flex gap-3">
            {#if role === 'customer'}
                <a href="/claims/new">
                    <Button class="h-12 px-6">
                        <Plus class="w-5 h-5 mr-2" /> File a Claim
                    </Button>
                </a>
            {/if}
            {#if role === 'provider' || role === 'admin'}
                <a href="/policies/new">
                    <Button class="h-12 px-6">
                        <Plus class="w-5 h-5 mr-2" /> Create Policy
                    </Button>
                </a>
            {/if}
        </div>
    </div>

	<!-- Stats Grid -->
	<div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
		{#each Object.values(stats) as stat}
			<div class="bg-white p-8 rounded-3xl border border-slate-200 shadow-sm flex items-center gap-6 hover:shadow-xl hover:shadow-slate-200/50 transition-all duration-300">
				<div class={`${stat.bg} ${stat.color} p-5 rounded-2xl`}>
					<stat.icon class="w-7 h-7" />
				</div>
				<div>
					<p class="text-xs font-black text-slate-400 uppercase tracking-widest mb-1">{stat.label}</p>
					<p class="text-3xl font-black text-slate-900">{stat.value}</p>
				</div>
			</div>
		{/each}
	</div>

	<div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
		<!-- Primary Data List -->
		<div class="bg-white rounded-[2.5rem] border border-slate-200 shadow-sm overflow-hidden flex flex-col">
			<div class="p-8 border-b border-slate-100 flex justify-between items-center bg-slate-50/50">
				<h2 class="text-2xl font-black text-slate-900 tracking-tight">
					{role === 'surveyor' ? 'Assigned Claims' : 'Recent Policies'}
				</h2>
				<a href={role === 'surveyor' ? '/claims' : '/policies'} class="text-indigo-600 font-bold hover:text-indigo-700 flex items-center gap-1 transition-all hover:gap-2">
					View all <ArrowRight class="w-4 h-4" />
				</a>
			</div>
			<div class="divide-y divide-slate-50">
				{#if isLoading}
					{#each Array(3) as _}
						<div class="p-8 animate-pulse flex gap-6">
							<div class="w-14 h-14 bg-slate-100 rounded-2xl"></div>
							<div class="flex-grow space-y-3">
								<div class="h-5 bg-slate-50 rounded-lg w-1/3"></div>
								<div class="h-4 bg-slate-50 rounded-lg w-1/4"></div>
							</div>
						</div>
					{/each}
				{:else if mainData.length > 0}
					{#each mainData.slice(0, 5) as item}
						{@const statusStyle = getStatusIcon(item.status || 'active')}
						<div class="p-8 flex items-center justify-between group hover:bg-slate-50/50 transition-colors">
							<div class="flex items-center gap-6">
								<div class="bg-white p-4 rounded-2xl shadow-sm border border-slate-100 text-slate-400 group-hover:text-indigo-600 transition-colors">
									{#if role === 'surveyor'}
										<FileText class="w-6 h-6" />
									{:else}
										<Shield class="w-6 h-6" />
									{/if}
								</div>
								<div>
									{#if role === 'surveyor'}
										<p class="text-base font-bold text-slate-900 group-hover:text-indigo-600 transition-colors tracking-tight">Claim #{item.id}</p>
										<p class="text-sm font-medium text-slate-500">{item.user_policy?.policy?.title || 'Unknown'}</p>
									{:else if role === 'customer' || role === 'agent'}
										<p class="text-base font-bold text-slate-900 group-hover:text-indigo-600 transition-colors tracking-tight">{item.policy?.title || 'Unknown'}</p>
										<p class="text-sm font-medium text-slate-500">{item.policy_number} • {item.policy?.policy_type || 'Unknown'}</p>
									{:else}
										<p class="text-base font-bold text-slate-900 group-hover:text-indigo-600 transition-colors tracking-tight">{item.title || item.policy_number}</p>
										<p class="text-sm font-medium text-slate-500 capitalize">{item.policy_type || 'Policy'}</p>
									{/if}
								</div>
							</div>
							<span class={`px-4 py-1.5 rounded-full text-[10px] font-black uppercase tracking-widest border ${statusStyle.bg} ${statusStyle.color} border-current/10`}>
								{item.status || 'active'}
							</span>
						</div>
					{/each}
				{:else}
					<div class="p-20 text-center">
						<div class="w-16 h-16 bg-slate-50 rounded-2xl flex items-center justify-center mx-auto mb-6">
                            <Activity class="w-8 h-8 text-slate-200" />
                        </div>
						<p class="text-slate-400 font-bold uppercase tracking-widest text-xs">Nothing to show yet</p>
					</div>
				{/if}
			</div>
		</div>

		<!-- Secondary Data List -->
		{#if role !== 'surveyor'}
		<div class="bg-white rounded-[2.5rem] border border-slate-200 shadow-sm overflow-hidden flex flex-col">
			<div class="p-8 border-b border-slate-100 flex justify-between items-center bg-slate-50/50">
				<h2 class="text-2xl font-black text-slate-900 tracking-tight">Recent Claims</h2>
				<a href="/claims" class="text-indigo-600 font-bold hover:text-indigo-700 flex items-center gap-1 transition-all hover:gap-2">
					View all <ArrowRight class="w-4 h-4" />
				</a>
			</div>
			<div class="divide-y divide-slate-50">
				{#if isLoading}
					{#each Array(3) as _}
						<div class="p-8 animate-pulse flex gap-6">
							<div class="w-14 h-14 bg-slate-100 rounded-2xl"></div>
							<div class="flex-grow space-y-3">
								<div class="h-5 bg-slate-50 rounded-lg w-1/3"></div>
								<div class="h-4 bg-slate-50 rounded-lg w-1/4"></div>
							</div>
						</div>
					{/each}
				{:else if secondaryData.length > 0}
					{#each secondaryData.slice(0, 5) as claim}
						{@const status = getStatusIcon(claim.status)}
						<div class="p-8 flex items-center justify-between hover:bg-slate-50/50 transition-colors group">
							<div class="flex items-center gap-6">
								<div class={`${status.bg} ${status.color} p-4 rounded-2xl border border-current/10 shadow-sm group-hover:scale-110 transition-transform`}>
									<status.icon class="w-6 h-6" />
								</div>
								<div>
									<p class="text-base font-bold text-slate-900 tracking-tight group-hover:text-indigo-600 transition-colors">Claim #{claim.id}</p>
									<p class="text-sm font-medium text-slate-500 uppercase tracking-tight">{claim.status} • {new Date(claim.claim_date).toLocaleDateString()}</p>
								</div>
							</div>
							<p class="text-lg font-black text-slate-900">${parseFloat(claim.claim_amount).toLocaleString()}</p>
						</div>
					{/each}
				{:else}
					<div class="p-20 text-center">
                        <div class="w-16 h-16 bg-slate-50 rounded-2xl flex items-center justify-center mx-auto mb-6">
                            <FileText class="w-8 h-8 text-slate-200" />
                        </div>
						<p class="text-slate-400 font-bold uppercase tracking-widest text-xs mb-6">No recent claims</p>
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
