<script lang="ts">
    import { page } from '$app/state';
    import { api } from '$lib/api/axios';
    import { auth } from '$lib/stores/auth.svelte';
    import { onMount } from 'svelte';
    import { Button } from '$lib/components';
    import { toast } from 'svelte-sonner';
    import ArrowLeft from 'lucide-svelte/icons/arrow-left';
    import Building from 'lucide-svelte/icons/building';
    import Calendar from 'lucide-svelte/icons/calendar';
    import Check from 'lucide-svelte/icons/check';
    import DollarSign from 'lucide-svelte/icons/dollar-sign';
    import Info from 'lucide-svelte/icons/info';
    import Shield from 'lucide-svelte/icons/shield';
    import ShoppingCart from 'lucide-svelte/icons/shopping-cart';

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
        <button onclick={() => history.back()} class="p-2 hover:bg-white/10 rounded-full transition-colors group">
            <ArrowLeft class="w-6 h-6 text-slate-400 group-hover:text-violet-200" />
        </button>
        <h1 class="text-3xl font-black tracking-tight text-slate-50">Policy Details</h1>
    </div>

    {#if isLoading}
        <div class="animate-pulse space-y-8">
            <div class="h-64 bg-white/5 rounded-3xl"></div>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div class="h-32 bg-white/5 rounded-2xl"></div>
                <div class="h-32 bg-white/5 rounded-2xl"></div>
                <div class="h-32 bg-white/5 rounded-2xl"></div>
            </div>
        </div>
    {:else if policy}
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-12">
            <div class="lg:col-span-2 space-y-12">
                <div class="bg-violet-600 rounded-3xl p-12 text-white relative overflow-hidden shadow-[0_20px_50px_rgba(124,58,237,0.3)]">
                    <div class="relative z-10">
                        <span class="px-4 py-1.5 bg-white/20 backdrop-blur-md rounded-full text-[10px] font-black uppercase tracking-widest mb-6 inline-block border border-white/20">
                            {policy.policy_type} Protection
                        </span>
                        <h2 class="text-5xl font-black mb-4 leading-tight tracking-tight">{policy.title}</h2>
                        <p class="text-violet-100 text-lg font-medium leading-relaxed max-w-xl opacity-90">
                            {policy.description || 'Comprehensive coverage tailored for your peace of mind and long-term security.'}
                        </p>
                    </div>
                    <Shield class="absolute -bottom-12 -right-12 w-64 h-64 text-white/10" />
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                    <div class="dashboard-card p-8 space-y-6">
                        <h3 class="font-bold text-slate-50 flex items-center gap-2">
                            <Check class="w-5 h-5 text-emerald-400" /> What's Covered
                        </h3>
                        <ul class="space-y-4">
                            {#each ['Accidental Damages', 'Third-party Liability', 'Natural Calamities', 'Theft Protection'] as feature}
                                <li class="text-slate-300 text-sm flex items-center gap-3">
                                    <div class="w-1.5 h-1.5 bg-violet-400 rounded-full shadow-[0_0_8px_rgba(167,139,250,0.5)]"></div> {feature}
                                </li>
                            {/each}
                        </ul>
                    </div>
                    <div class="dashboard-card p-8 space-y-6">
                        <h3 class="font-bold text-slate-50 flex items-center gap-2">
                            <Info class="w-5 h-5 text-violet-400" /> Additional Benefits
                        </h3>
                        <ul class="space-y-4">
                            {#each ['24/7 Roadside Assistance', 'Cashless Hospitalization', 'Global Coverage Access'] as feature}
                                <li class="text-slate-300 text-sm flex items-center gap-3">
                                    <div class="w-1.5 h-1.5 bg-violet-400 rounded-full shadow-[0_0_8px_rgba(167,139,250,0.5)]"></div> {feature}
                                </li>
                            {/each}
                        </ul>
                    </div>
                </div>
            </div>

            <div class="lg:col-span-1 space-y-8">
                <div class="dashboard-card p-8 sticky top-8 space-y-8 bg-white/[0.03]">
                    <div>
                        <p class="text-slate-400 text-[10px] font-black uppercase tracking-widest mb-2">Annual Premium</p>
                        <p class="text-5xl font-black text-slate-50 tracking-tight">${parseFloat(policy.premium_amount).toLocaleString()}</p>
                    </div>

                    <div class="space-y-4 pt-8 border-t border-white/8">
                        <div class="flex justify-between items-center text-sm">
                            <span class="text-slate-400 flex items-center gap-2"><Building class="w-4 h-4" /> Provider</span>
                            <span class="font-bold text-slate-50">{policy.provider?.company_name || 'N/A'}</span>
                        </div>
                        <div class="flex justify-between items-center text-sm">
                            <span class="text-slate-400 flex items-center gap-2"><Shield class="w-4 h-4" /> Coverage</span>
                            <span class="font-bold text-slate-50">${parseFloat(policy.coverage_amount).toLocaleString()}</span>
                        </div>
                        <div class="flex justify-between items-center text-sm">
                            <span class="text-slate-400 flex items-center gap-2"><Calendar class="w-4 h-4" /> Duration</span>
                            <span class="font-bold text-slate-50">12 Months</span>
                        </div>
                    </div>

                    <div class="pt-4">
                        {#if auth.user?.role === 'customer'}
                            {#if policy.is_owned}
                                <div class="bg-emerald-500/14 border border-emerald-300/16 text-emerald-200 p-4 rounded-2xl text-center font-bold flex items-center justify-center gap-2">
                                    <Check class="w-5 h-5" /> You own this policy
                                </div>
                            {:else}
                                <Button class="w-full h-14 text-lg font-black" onclick={buyPolicy}>
                                    <ShoppingCart class="w-5 h-5 mr-2" /> Buy Now
                                </Button>
                            {/if}
                        {:else if !auth.user}
                            <a href="/login" class="block">
                                <Button class="w-full h-14 text-lg font-black">Login to Buy</Button>
                            </a>
                        {/if}
                    </div>
                </div>
            </div>
        </div>
    {/if}
</div>
