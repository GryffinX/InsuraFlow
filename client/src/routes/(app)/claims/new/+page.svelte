<script lang="ts">
    import { api } from '$lib/api/axios';
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { Button, Input } from '$lib/components';
    import { toast } from 'svelte-sonner';
    import ArrowLeft from 'lucide-svelte/icons/arrow-left';
    import Building from 'lucide-svelte/icons/building';
    import FileText from 'lucide-svelte/icons/file-text';
    import Shield from 'lucide-svelte/icons/shield';
    import Tag from 'lucide-svelte/icons/tag';

    let userPolicies = $state<any[]>([]);
    
    let formData = $state({
        user_policy_id: '',
        claim_amount: '',
        claim_reason: '',
    });

    let isLoading = $state(false);

    const selectedPolicy = $derived(
        userPolicies.find(p => p.id.toString() === formData.user_policy_id.toString())
    );

    onMount(async () => {
        try {
            const policiesRes = await api.get('user-policies/');
            const rawPolicies = policiesRes.data.results || policiesRes.data;
            userPolicies = rawPolicies.filter((p: any) => p.status === 'active');
        } catch (error: any) {
            const msg = error.response?.data?.error || 'Failed to load required data';
            toast.error(msg);
            console.error('Fetch error:', error);
        }
    });

    async function handleSubmit(e: Event) {
        e.preventDefault();
        if (!formData.user_policy_id) return toast.error('Please select a policy');
        
        isLoading = true;
        try {
            const payload = {
                user_policy_id: formData.user_policy_id,
                claim_amount: formData.claim_amount,
                claim_reason: formData.claim_reason,
            };
            await api.post('claims/', payload);
            toast.success('Claim filed successfully');
            goto('/dashboard');
        } catch (error: any) {
            toast.error(error.response?.data?.error || error.response?.data?.detail || 'Failed to file claim');
        } finally {
            isLoading = false;
        }
    }
</script>

<div class="max-w-3xl mx-auto px-4 py-8">
    <div class="mb-8 flex items-center gap-4">
        <a href="/dashboard" class="p-2 hover:bg-slate-100 rounded-full transition-colors">
            <ArrowLeft class="w-6 h-6 text-slate-600" />
        </a>
        <div>
            <h1 class="text-3xl font-bold text-slate-900 tracking-tight">File New Claim</h1>
            <p class="text-slate-500 mt-1">Submit a request for reimbursement or direct payment.</p>
        </div>
    </div>

    {#if userPolicies.length === 0 && !isLoading}
        <div class="bg-amber-50 border border-amber-200 rounded-2xl p-8 text-center">
            <Shield class="w-12 h-12 text-amber-500 mx-auto mb-4" />
            <h3 class="text-lg font-bold text-amber-900">No Active Policies Found</h3>
            <p class="text-amber-700 mt-1 mb-6">You need an active policy to file a claim.</p>
            <a href="/policies">
                <Button>Browse Policies</Button>
            </a>
        </div>
    {:else}
        <form onsubmit={handleSubmit} class="bg-white rounded-3xl border border-slate-200 shadow-xl overflow-hidden p-8 space-y-8">
            <div class="space-y-6">
                <div class="space-y-2">
                    <label class="block text-sm font-bold text-slate-700 uppercase tracking-wider" for="policy">
                        Select Your Policy
                    </label>
                    <select
                        id="policy"
                        class="block w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 outline-none focus:ring-2 focus:ring-indigo-500 transition-all font-medium"
                        bind:value={formData.user_policy_id}
                        required
                    >
                        <option value="">Choose a policy</option>
                        {#each userPolicies as up}
                            <option value={up.id}>{up.policy?.title || 'Unknown Policy'} ({up.policy_number})</option>
                        {/each}
                    </select>
                </div>

                {#if selectedPolicy}
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 animate-in fade-in slide-in-from-top-2">
                        <div class="bg-indigo-50 p-4 rounded-2xl border border-indigo-100 flex items-center gap-3">
                            <Building class="w-5 h-5 text-indigo-600" />
                            <div>
                                <p class="text-[10px] font-bold text-indigo-400 uppercase tracking-widest">Provider</p>
                                <p class="font-bold text-indigo-900">{selectedPolicy.policy?.provider?.company_name || 'N/A'}</p>
                            </div>
                        </div>
                        <div class="bg-slate-50 p-4 rounded-2xl border border-slate-100 flex items-center gap-3">
                            <Tag class="w-5 h-5 text-slate-600" />
                            <div>
                                <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Policy Type</p>
                                <p class="font-bold text-slate-900 capitalize">{selectedPolicy.policy?.policy_type || 'N/A'}</p>
                            </div>
                        </div>
                    </div>
                {/if}
            </div>

            <div class="grid grid-cols-1 gap-8">
                <div class="space-y-2">
                    <label class="block text-sm font-bold text-slate-700 uppercase tracking-wider" for="claim_amount">
                        Claim Amount ($)
                    </label>
                    <input
                        id="claim_amount"
                        type="number"
                        step="0.01"
                        placeholder="0.00"
                        class="block w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 outline-none focus:ring-2 focus:ring-indigo-500 transition-all font-medium"
                        bind:value={formData.claim_amount}
                        required
                    />
                </div>
            </div>

            <div class="space-y-2">
                <label class="block text-sm font-bold text-slate-700 uppercase tracking-wider" for="reason">
                    Reason for Claim
                </label>
                <textarea
                    id="reason"
                    rows="4"
                    class="block w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 outline-none focus:ring-2 focus:ring-indigo-500 transition-all font-medium"
                    placeholder="Provide details about the incident..."
                    bind:value={formData.claim_reason}
                    required
                ></textarea>
            </div>

            <div class="pt-6 border-t border-slate-100 flex justify-end gap-4">
                <a href="/dashboard">
                    <Button variant="ghost" type="button">Cancel</Button>
                </a>
                <Button type="submit" loading={isLoading} class="px-8">
                    File Claim
                </Button>
            </div>
        </form>
    {/if}
</div>
