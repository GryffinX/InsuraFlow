<script lang="ts">
    import { page } from '$app/state';
    import { api } from '$lib/api/axios';
    import { auth } from '$lib/stores/auth.svelte';
    import { onMount } from 'svelte';
    import { Button } from '$lib/components';
    import { toast } from 'svelte-sonner';
    import { Shield, Check, ShoppingCart, ArrowLeft, Building, Calendar, DollarSign } from 'lucide-svelte';

    const id = page.params.id;
    let policy = $state<any>(null);
    let isLoading = $state(true);

    onMount(async () => {
        try {
            const res = await api.get(`policies/${id}/`);
            policy = res.data;
        } catch (error) {
            toast.error('Failed to load policy');
        } finally {
            isLoading = false;
        }
    });

    async function buyPolicy() {
        try {
            await api.post(`policies/${id}/buy/`);
            toast.success('Policy purchased successfully!');
            const res = await api.get(`policies/${id}/`);
            policy = res.data;
        } catch (error: any) {
            toast.error(error.response?.data?.error || 'Failed to purchase');
        }
    }
</script>

<div class="max-w-5xl mx-auto px-4 py-12">
    <div class="mb-8 flex items-center gap-4">
        <button onclick={() => history.back()} class="p-2 hover:bg-slate-100 rounded-full transition-colors">
            <ArrowLeft class="w-6 h-6 text-slate-600" />
        </button>
        <h1 class="text-3xl font-bold text-slate-900">Policy Details</h1>
    </div>

    {#if isLoading}
        <div class="animate-pulse space-y-8">
            <div class="h-64 bg-slate-100 rounded-3xl"></div>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div class="h-32 bg-slate-50 rounded-2xl"></div>
                <div class="h-32 bg-slate-50 rounded-2xl"></div>
                <div class="h-32 bg-slate-50 rounded-2xl"></div>
            </div>
        </div>
    {:else if policy}
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-12">
            <div class="lg:col-span-2 space-y-12">
                <div class="bg-indigo-600 rounded-3xl p-12 text-white relative overflow-hidden">
                    <div class="relative z-10">
                        <span class="px-4 py-1.5 bg-white/20 backdrop-blur-md rounded-full text-xs font-bold uppercase tracking-widest mb-6 inline-block">
                            {policy.policy_type} Protection
                        </span>
                        <h2 class="text-5xl font-black mb-4 leading-tight">{policy.title}</h2>
                        <p class="text-indigo-100 text-lg leading-relaxed max-w-xl">
                            {policy.description || 'Comprehensive coverage tailored for your peace of mind and long-term security.'}
                        </p>
                    </div>
                    <Shield class="absolute -bottom-12 -right-12 w-64 h-64 text-white/10" />
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                    <div class="bg-white p-8 rounded-3xl border border-slate-200 shadow-sm space-y-4">
                        <h3 class="font-bold text-slate-900 flex items-center gap-2">
                            <Check class="w-5 h-5 text-emerald-500" /> What's Covered
                        </h3>
                        <ul class="space-y-3">
                            {#each ['Accidental Damages', 'Third-party Liability', 'Natural Calamities', 'Theft Protection'] as feature}
                                <li class="text-slate-600 text-sm flex items-center gap-2">
                                    <div class="w-1.5 h-1.5 bg-indigo-400 rounded-full"></div> {feature}
                                </li>
                            {/each}
                        </ul>
                    </div>
                    <div class="bg-white p-8 rounded-3xl border border-slate-200 shadow-sm space-y-4">
                        <h3 class="font-bold text-slate-900 flex items-center gap-2">
                            <Info class="w-5 h-5 text-indigo-500" /> Additional Benefits
                        </li>
                        <ul class="space-y-3">
                            {#each ['24/7 Roadside Assistance', 'Cashless Hospitalization', 'Global Coverage Access'] as feature}
                                <li class="text-slate-600 text-sm flex items-center gap-2">
                                    <div class="w-1.5 h-1.5 bg-indigo-400 rounded-full"></div> {feature}
                                </li>
                            {/each}
                        </ul>
                    </div>
                </div>
            </div>

            <div class="lg:col-span-1 space-y-8">
                <div class="bg-white p-8 rounded-3xl border border-slate-200 shadow-xl sticky top-8 space-y-8">
                    <div>
                        <p class="text-slate-400 text-xs font-bold uppercase tracking-widest mb-2">Annual Premium</p>
                        <p class="text-5xl font-black text-slate-900">${parseFloat(policy.premium_amount).toLocaleString()}</p>
                    </div>

                    <div class="space-y-4 pt-8 border-t border-slate-100">
                        <div class="flex justify-between items-center text-sm">
                            <span class="text-slate-500 flex items-center gap-2"><Building class="w-4 h-4" /> Provider</span>
                            <span class="font-bold text-slate-900">{policy.provider?.company_name || 'N/A'}</span>
                        </div>
                        <div class="flex justify-between items-center text-sm">
                            <span class="text-slate-500 flex items-center gap-2"><Shield class="w-4 h-4" /> Coverage</span>
                            <span class="font-bold text-slate-900">${parseFloat(policy.coverage_amount).toLocaleString()}</span>
                        </div>
                        <div class="flex justify-between items-center text-sm">
                            <span class="text-slate-500 flex items-center gap-2"><Calendar class="w-4 h-4" /> Duration</span>
                            <span class="font-bold text-slate-900">12 Months</span>
                        </div>
                    </div>

                    <div class="pt-4">
                        {#if auth.user?.role === 'customer'}
                            {#if policy.is_owned}
                                <div class="bg-emerald-50 text-emerald-700 p-4 rounded-2xl text-center font-bold flex items-center justify-center gap-2">
                                    <Check class="w-5 h-5" /> You own this policy
                                </div>
                            {:else}
                                <Button class="w-full h-14 text-lg font-bold" onclick={buyPolicy}>
                                    <ShoppingCart class="w-5 h-5 mr-2" /> Buy Now
                                </Button>
                            {/if}
                        {:else if !auth.user}
                            <a href="/login" class="block">
                                <Button class="w-full h-14 text-lg font-bold">Login to Buy</Button>
                            </a>
                        {/if}
                    </div>
                </div>
            </div>
        </div>
    {/if}
</div>
