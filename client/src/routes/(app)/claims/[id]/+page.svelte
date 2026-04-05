<script lang="ts">
    import { page } from '$app/state';
    import { api } from '$lib/api/axios';
    import { auth } from '$lib/stores/auth.svelte';
    import { onMount } from 'svelte';
    import { Button } from '$lib/components';
    import { toast } from 'svelte-sonner';
    import AlertCircle from 'lucide-svelte/icons/alert-circle';
    import ArrowLeft from 'lucide-svelte/icons/arrow-left';
    import Calendar from 'lucide-svelte/icons/calendar';
    import Check from 'lucide-svelte/icons/check';
    import CheckCircle2 from 'lucide-svelte/icons/check-circle-2';
    import Clock from 'lucide-svelte/icons/clock';
    import DollarSign from 'lucide-svelte/icons/dollar-sign';
    import FileText from 'lucide-svelte/icons/file-text';
    import Shield from 'lucide-svelte/icons/shield';
    import User from 'lucide-svelte/icons/user';
    import X from 'lucide-svelte/icons/x';

    const id = page.params.id;
    let claim = $state<any>(null);
    let isLoading = $state(true);
    let isActioning = $state(false);

    onMount(fetchClaim);

    async function fetchClaim() {
        isLoading = true;
        try {
            const res = await api.get(`claims/${id}/`);
            claim = res.data;
        } catch (error) {
            toast.error('Failed to load claim details');
        } finally {
            isLoading = false;
        }
    }

    async function handleAction(action: 'approve' | 'reject') {
        isActioning = true;
        try {
            await api.post(`claims/${id}/${action}/`);
            toast.success(`Claim ${action}d successfully`);
            fetchClaim();
        } catch (error: any) {
            toast.error(error.response?.data?.error || `Failed to ${action} claim`);
        } finally {
            isActioning = false;
        }
    }

    function getStatusIcon(status: string) {
        switch (status?.toLowerCase()) {
            case 'approved': return { icon: CheckCircle2, color: 'text-emerald-200', bg: 'bg-emerald-500/14' };
            case 'rejected': return { icon: AlertCircle, color: 'text-rose-200', bg: 'bg-rose-500/14' };
            case 'under_review': return { icon: Clock, color: 'text-amber-200', bg: 'bg-amber-500/14' };
            case 'settled': return { icon: CheckCircle2, color: 'text-violet-200', bg: 'bg-violet-500/14' };
            default: return { icon: Clock, color: 'text-amber-200', bg: 'bg-amber-500/14' };
        }
    }
</script>

<div class="max-w-4xl mx-auto px-4 py-12">
    <div class="mb-8 flex items-center gap-4">
        <button onclick={() => history.back()} class="p-2 hover:bg-white/10 rounded-full transition-colors group">
            <ArrowLeft class="w-6 h-6 text-slate-400 group-hover:text-violet-200" />
        </button>
        <h1 class="text-3xl font-black tracking-tight text-slate-50">Claim Details</h1>
    </div>

    {#if isLoading}
        <div class="animate-pulse space-y-6">
            <div class="h-40 bg-white/5 rounded-3xl"></div>
            <div class="grid grid-cols-2 gap-6">
                <div class="h-32 bg-white/5 rounded-2xl"></div>
                <div class="h-32 bg-white/5 rounded-2xl"></div>
            </div>
        </div>
    {:else if claim}
        {@const status = getStatusIcon(claim.status)}
        <div class="space-y-8">
            <div class="dashboard-card overflow-hidden">
                <div class={`p-8 ${status.bg} border-b border-white/8 flex justify-between items-center`}>
                    <div class="flex items-center gap-6">
                        <div class={`p-4 rounded-2xl bg-white/10 backdrop-blur-md shadow-lg ${status.color}`}>
                            <status.icon class="w-8 h-8" />
                        </div>
                        <div>
                            <p class="text-[10px] font-black uppercase tracking-widest text-slate-400">Claim Status</p>
                            <h2 class={`text-3xl font-black capitalize tracking-tight ${status.color}`}>{claim.status.replace('_', ' ')}</h2>
                        </div>
                    </div>
                    <div class="text-right">
                        <p class="text-[10px] font-black uppercase tracking-widest text-slate-400">Claim ID</p>
                        <p class="text-xl font-mono font-black text-slate-50">#{claim.id}</p>
                    </div>
                </div>

                <div class="p-8 grid grid-cols-1 md:grid-cols-3 gap-8">
                    <div class="space-y-1">
                        <p class="text-slate-400 text-[10px] font-black uppercase tracking-widest">Amount Claimed</p>
                        <p class="text-3xl font-black text-slate-50">${parseFloat(claim.claim_amount).toLocaleString()}</p>
                    </div>
                    <div class="space-y-1">
                        <p class="text-slate-400 text-[10px] font-black uppercase tracking-widest">Date Filed</p>
                        <p class="text-lg font-bold text-slate-50">{new Date(claim.claim_date).toLocaleDateString()}</p>
                    </div>
                    <div class="space-y-1">
                        <p class="text-slate-400 text-[10px] font-black uppercase tracking-widest">Policy Number</p>
                        <p class="text-lg font-bold text-violet-300 font-mono tracking-wider">{claim.user_policy?.policy_number || 'N/A'}</p>
                    </div>
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div class="dashboard-card p-8 space-y-6">
                    <h3 class="font-bold text-slate-50 flex items-center gap-2">
                        <FileText class="w-5 h-5 text-violet-400" /> Reason for Claim
                    </h3>
                    <p class="text-slate-300 leading-relaxed italic text-lg opacity-90">
                        "{claim.claim_reason}"
                    </p>
                </div>

                <div class="dashboard-card p-8 space-y-6">
                    <h3 class="font-bold text-slate-50 flex items-center gap-2">
                        <Shield class="w-5 h-5 text-violet-400" /> Associated Policy
                    </h3>
                    <div class="flex items-center gap-4 group">
                        <div class="bg-white/5 p-4 rounded-2xl text-slate-400 group-hover:bg-violet-500/10 group-hover:text-violet-200 transition-colors">
                            <Shield class="w-6 h-6" />
                        </div>
                        <div>
                            <p class="font-bold text-slate-50 group-hover:text-violet-100 transition-colors">{claim.user_policy?.policy?.title || 'Unknown Policy'}</p>
                            <p class="text-[10px] text-slate-400 uppercase font-black tracking-widest mt-0.5">{claim.user_policy?.policy?.policy_type || 'Insurance'}</p>
                        </div>
                    </div>
                </div>
            </div>

            {#if claim.assigned_surveyor}
                <div class="bg-violet-500/10 border border-violet-300/16 p-8 rounded-[30px] flex items-center justify-between">
                    <div class="flex items-center gap-6">
                        <div class="w-14 h-14 bg-white/10 rounded-2xl flex items-center justify-center text-violet-200 border border-white/10 shadow-lg">
                            <User class="w-7 h-7" />
                        </div>
                        <div>
                            <p class="text-[10px] font-black text-violet-300 uppercase tracking-widest mb-1">Assigned Surveyor</p>
                            <p class="text-xl font-black text-slate-50">{claim.assigned_surveyor.username}</p>
                        </div>
                    </div>
                    <div class="text-right">
                        <p class="text-base font-bold text-slate-200 mb-0.5">{claim.assigned_surveyor.email}</p>
                        <p class="text-xs font-medium text-slate-400 tracking-wide">{claim.assigned_surveyor.phone || ''}</p>
                    </div>
                </div>
            {/if}

            {#if claim.status === 'under_review' && (auth.user?.role === 'admin' || (auth.user?.role === 'surveyor' && claim.assigned_surveyor?.id === auth.user?.id))}
                <div class="pt-8 border-t border-white/8 flex gap-6">
                    <Button 
                        class="flex-grow h-14 text-lg font-black bg-emerald-600 hover:bg-emerald-700 shadow-[0_12px_40px_rgba(16,185,129,0.25)]" 
                        loading={isActioning}
                        onclick={() => handleAction('approve')}
                    >
                        <Check class="w-5 h-5 mr-2" /> Approve Claim
                    </Button>
                    <Button 
                        variant="danger" 
                        class="flex-grow h-14 text-lg font-black shadow-[0_12px_40px_rgba(244,63,94,0.25)]" 
                        loading={isActioning}
                        onclick={() => handleAction('reject')}
                    >
                        <X class="w-5 h-5 mr-2" /> Reject Claim
                    </Button>
                </div>
            {/if}
        </div>
    {/if}
</div>
