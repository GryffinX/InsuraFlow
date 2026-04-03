<script lang="ts">
    import { page } from '$app/state';
    import { api } from '$lib/api/axios';
    import { auth } from '$lib/stores/auth.svelte';
    import { onMount } from 'svelte';
    import { Button } from '$lib/components';
    import { toast } from 'svelte-sonner';
    import { FileText, ArrowLeft, Clock, CheckCircle2, AlertCircle, Calendar, DollarSign, User, Shield, Check, X } from 'lucide-svelte';

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
            case 'approved': return { icon: CheckCircle2, color: 'text-emerald-600', bg: 'bg-emerald-50' };
            case 'rejected': return { icon: AlertCircle, color: 'text-red-600', bg: 'bg-red-50' };
            case 'under_review': return { icon: Clock, color: 'text-amber-600', bg: 'bg-amber-50' };
            case 'settled': return { icon: CheckCircle2, color: 'text-indigo-600', bg: 'bg-indigo-50' };
            default: return { icon: Clock, color: 'text-blue-600', bg: 'bg-blue-50' };
        }
    }
</script>

<div class="max-w-4xl mx-auto px-4 py-12">
    <div class="mb-8 flex items-center gap-4">
        <button onclick={() => history.back()} class="p-2 hover:bg-slate-100 rounded-full transition-colors">
            <ArrowLeft class="w-6 h-6 text-slate-600" />
        </button>
        <h1 class="text-3xl font-bold text-slate-900">Claim Details</h1>
    </div>

    {#if isLoading}
        <div class="animate-pulse space-y-6">
            <div class="h-40 bg-slate-100 rounded-3xl"></div>
            <div class="grid grid-cols-2 gap-6">
                <div class="h-32 bg-slate-50 rounded-2xl"></div>
                <div class="h-32 bg-slate-50 rounded-2xl"></div>
            </div>
        </div>
    {:else if claim}
        {@const status = getStatusIcon(claim.status)}
        <div class="space-y-8">
            <div class="bg-white rounded-3xl border border-slate-200 shadow-sm overflow-hidden">
                <div class={`p-8 ${status.bg} border-b border-slate-100 flex justify-between items-center`}>
                    <div class="flex items-center gap-4">
                        <div class={`p-3 rounded-2xl bg-white shadow-sm ${status.color}`}>
                            <status.icon class="w-8 h-8" />
                        </div>
                        <div>
                            <p class="text-xs font-bold uppercase tracking-widest opacity-60">Claim Status</p>
                            <h2 class={`text-2xl font-black capitalize ${status.color}`}>{claim.status.replace('_', ' ')}</h2>
                        </div>
                    </div>
                    <div class="text-right">
                        <p class="text-xs font-bold uppercase tracking-widest text-slate-400">Claim ID</p>
                        <p class="text-xl font-mono font-bold text-slate-900">#{claim.id}</p>
                    </div>
                </div>

                <div class="p-8 grid grid-cols-1 md:grid-cols-3 gap-8">
                    <div class="space-y-1">
                        <p class="text-slate-400 text-xs font-bold uppercase tracking-widest">Amount Claimed</p>
                        <p class="text-2xl font-black text-slate-900">${parseFloat(claim.claim_amount).toLocaleString()}</p>
                    </div>
                    <div class="space-y-1">
                        <p class="text-slate-400 text-xs font-bold uppercase tracking-widest">Date Filed</p>
                        <p class="text-lg font-bold text-slate-900">{new Date(claim.claim_date).toLocaleDateString()}</p>
                    </div>
                    <div class="space-y-1">
                        <p class="text-slate-400 text-xs font-bold uppercase tracking-widest">Policy Number</p>
                        <p class="text-lg font-bold text-indigo-600 font-mono">{claim.user_policy?.policy_number || 'N/A'}</p>
                    </div>
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div class="bg-white p-8 rounded-3xl border border-slate-200 shadow-sm space-y-6">
                    <h3 class="font-bold text-slate-900 flex items-center gap-2">
                        <FileText class="w-5 h-5 text-indigo-600" /> Reason for Claim
                    </h3>
                    <p class="text-slate-600 leading-relaxed italic">
                        "{claim.claim_reason}"
                    </p>
                </div>

                <div class="bg-white p-8 rounded-3xl border border-slate-200 shadow-sm space-y-6">
                    <h3 class="font-bold text-slate-900 flex items-center gap-2">
                        <Shield class="w-5 h-5 text-indigo-600" /> Associated Policy
                    </h3>
                    <div class="flex items-center gap-4">
                        <div class="bg-slate-100 p-3 rounded-xl text-slate-600">
                            <Shield class="w-6 h-6" />
                        </div>
                        <div>
                            <p class="font-bold text-slate-900">{claim.user_policy?.policy?.title || 'Unknown Policy'}</p>
                            <p class="text-xs text-slate-500 uppercase font-medium">{claim.user_policy?.policy?.policy_type || 'Insurance'}</p>
                        </div>
                    </div>
                </div>
            </div>

            {#if claim.assigned_surveyor}
                <div class="bg-indigo-50 border border-indigo-100 p-8 rounded-3xl flex items-center justify-between">
                    <div class="flex items-center gap-4">
                        <div class="w-12 h-12 bg-white rounded-full flex items-center justify-center text-indigo-600 border border-indigo-100">
                            <User class="w-6 h-6" />
                        </div>
                        <div>
                            <p class="text-xs font-bold text-indigo-400 uppercase tracking-widest">Assigned Surveyor</p>
                            <p class="text-lg font-bold text-indigo-900">{claim.assigned_surveyor.username}</p>
                        </div>
                    </div>
                    <div class="text-right text-indigo-600">
                        <p class="text-sm font-medium">{claim.assigned_surveyor.email}</p>
                        <p class="text-xs opacity-75">{claim.assigned_surveyor.phone || ''}</p>
                    </div>
                </div>
            {/if}

            {#if claim.status === 'under_review' && (auth.user?.role === 'admin' || (auth.user?.role === 'surveyor' && claim.assigned_surveyor?.id === auth.user?.id))}
                <div class="pt-8 border-t border-slate-100 flex gap-4">
                    <Button 
                        class="flex-grow h-14 text-lg font-bold bg-emerald-600 hover:bg-emerald-700" 
                        loading={isActioning}
                        onclick={() => handleAction('approve')}
                    >
                        <Check class="w-5 h-5 mr-2" /> Approve Claim
                    </Button>
                    <Button 
                        variant="danger" 
                        class="flex-grow h-14 text-lg font-bold" 
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
