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

<div class="max-w-3xl mx-auto px-4 py-12">
    <div class="mb-10 flex items-center gap-6 animate-fade-in">
        <a href="/dashboard" class="p-3 hover:bg-white/10 rounded-2xl transition-all group border border-white/5 hover:border-violet-500/30">
            <ArrowLeft class="w-6 h-6 text-slate-400 group-hover:text-violet-200" />
        </a>
        <div>
            <h1 class="text-4xl font-black text-slate-50 tracking-tight">File New Claim</h1>
            <p class="text-slate-400 mt-1 font-medium">Submit a request for reimbursement or direct payment.</p>
        </div>
    </div>

    {#if userPolicies.length === 0 && !isLoading}
        <div class="dashboard-card p-12 text-center relative overflow-hidden">
            <div class="absolute inset-0 bg-amber-500/5 blur-[80px] -z-10"></div>
            <div class="w-20 h-20 bg-amber-500/10 rounded-3xl flex items-center justify-center text-amber-200 mx-auto mb-6 border border-amber-500/20 shadow-lg">
                <Shield class="w-10 h-10" />
            </div>
            <h3 class="text-2xl font-black text-slate-50 tracking-tight">No Active Policies Found</h3>
            <p class="text-slate-400 mt-2 mb-8 font-medium">You need an active policy to file a claim.</p>
            <a href="/policies">
                <Button class="px-8 h-12 rounded-xl font-black shadow-[0_12px_40px_rgba(124,58,237,0.25)]">Browse Policies</Button>
            </a>
        </div>
    {:else}
        <form onsubmit={handleSubmit} class="dashboard-card p-10 space-y-10 relative overflow-hidden">
            <div class="absolute top-0 right-0 w-64 h-64 bg-violet-600/5 blur-[100px] -z-10 rounded-full"></div>
            
            <div class="space-y-8">
                <div class="space-y-2">
                    <label class="block text-[10px] font-black uppercase tracking-widest text-slate-400 ml-1" for="policy">
                        Select Your Policy
                    </label>
                    <div class="relative">
                        <select
                            id="policy"
                            class="block w-full rounded-2xl border-white/10 bg-white/[0.03] text-slate-50 shadow-sm focus:border-violet-500/50 focus:ring-0 sm:text-sm transition-all border p-4 outline-none font-bold h-14 appearance-none cursor-pointer"
                            bind:value={formData.user_policy_id}
                            required
                        >
                            <option value="" class="bg-[#0b0a24]">Choose an active policy</option>
                            {#each userPolicies as up}
                                <option value={up.id} class="bg-[#0b0a24]">{up.policy?.title || 'Unknown Policy'} ({up.policy_number})</option>
                            {/each}
                        </select>
                        <div class="absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none text-slate-500">
                            <Tag class="w-4 h-4" />
                        </div>
                    </div>
                </div>

                {#if selectedPolicy}
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 animate-fade-in">
                        <div class="bg-violet-500/10 p-5 rounded-2xl border border-violet-300/16 flex items-center gap-4 group transition-colors hover:bg-violet-500/15">
                            <div class="p-2.5 bg-white/10 rounded-xl text-violet-200">
                                <Building class="w-5 h-5" />
                            </div>
                            <div>
                                <p class="text-[10px] font-black text-violet-300 uppercase tracking-widest mb-0.5">Insurance Provider</p>
                                <p class="font-bold text-slate-50">{selectedPolicy.policy?.provider?.company_name || 'N/A'}</p>
                            </div>
                        </div>
                        <div class="bg-white/5 p-5 rounded-2xl border border-white/8 flex items-center gap-4 group transition-colors hover:bg-white/10">
                            <div class="p-2.5 bg-white/10 rounded-xl text-slate-300">
                                <Shield class="w-5 h-5" />
                            </div>
                            <div>
                                <p class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-0.5">Policy Type</p>
                                <p class="font-bold text-slate-50 capitalize">{selectedPolicy.policy?.policy_type || 'N/A'} Insurance</p>
                            </div>
                        </div>
                    </div>
                {/if}
            </div>

            <div class="grid grid-cols-1 gap-8">
                <div class="space-y-2">
                    <label class="block text-[10px] font-black uppercase tracking-widest text-slate-400 ml-1" for="claim_amount">
                        Claim Amount ($)
                    </label>
                    <div class="relative">
                        <input
                            id="claim_amount"
                            type="number"
                            step="0.01"
                            placeholder="0.00"
                            class="block w-full rounded-2xl border-white/10 bg-white/[0.03] text-slate-50 shadow-sm focus:border-violet-500/50 focus:ring-0 sm:text-sm transition-all border p-4 pl-12 outline-none font-bold h-14 placeholder:text-slate-600"
                            bind:value={formData.claim_amount}
                            required
                        />
                        <div class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 font-bold">
                            $
                        </div>
                    </div>
                </div>
            </div>

            <div class="space-y-2">
                <label class="block text-[10px] font-black uppercase tracking-widest text-slate-400 ml-1" for="reason">
                    Reason for Claim
                </label>
                <textarea
                    id="reason"
                    rows="4"
                    class="block w-full rounded-2xl border-white/10 bg-white/[0.03] text-slate-50 shadow-sm focus:border-violet-500/50 focus:ring-0 sm:text-sm transition-all border p-5 outline-none font-medium placeholder:text-slate-600 min-h-[140px]"
                    placeholder="Provide detailed information about the incident and the damages incurred..."
                    bind:value={formData.claim_reason}
                    required
                ></textarea>
            </div>

            <div class="pt-8 border-t border-white/8 flex justify-end gap-6">
                <a href="/dashboard">
                    <Button variant="outline" type="button" class="px-8 h-12 rounded-xl font-bold border-white/10 hover:bg-white/5 text-slate-300">Cancel</Button>
                </a>
                <Button type="submit" loading={isLoading} class="px-10 h-12 rounded-xl font-black shadow-[0_12px_40px_rgba(124,58,237,0.25)]">
                    <FileText class="w-4 h-4 mr-2" /> File Claim
                </Button>
            </div>
        </form>
    {/if}
</div>
