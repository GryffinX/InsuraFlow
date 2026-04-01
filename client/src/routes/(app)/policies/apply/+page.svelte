<script lang="ts">
    import { api } from '$lib/api/axios';
    import { auth } from '$lib/stores/auth.svelte';
    import { onMount } from 'svelte';
    import { page } from '$app/state';
    import { goto } from '$app/navigation';
    import { Button } from '$lib/components';
    import { toast } from 'svelte-sonner';
    import { Shield, ArrowLeft, Calendar, DollarSign, Building } from 'lucide-svelte';

    let policyId = page.url.searchParams.get('id');
    let policy = $state<any>(null);
    let isLoading = $state(true);
    let isSubmitting = $state(false);

    onMount(async () => {
        if (!policyId) {
            goto('/policies');
            return;
        }

        try {
            const res = await api.get(`policies/${policyId}/`);
            policy = res.data;
        } catch (error) {
            toast.error('Failed to load policy details');
            goto('/policies');
        } finally {
            isLoading = false;
        }
    });

    async function handleConfirmApplication() {
        if (!policyId) return;
        isSubmitting = true;
        try {
            await api.post(`policies/${policyId}/buy/`);
            toast.success('Policy purchased successfully!');
            goto('/dashboard');
        } catch (error: any) {
            toast.error(error.response?.data?.error || 'Failed to complete purchase');
        } finally {
            isSubmitting = false;
        }
    }
</script>

<div class="max-w-3xl mx-auto px-4 py-12">
    <div class="mb-8 flex items-center gap-4">
        <button onclick={() => history.back()} class="p-2 hover:bg-slate-100 rounded-full transition-colors">
            <ArrowLeft class="w-6 h-6 text-slate-600" />
        </button>
        <h1 class="text-3xl font-bold text-slate-900">Confirm Purchase</h1>
    </div>

    {#if isLoading}
        <div class="bg-white rounded-3xl border border-slate-200 shadow-xl p-8 animate-pulse space-y-6">
            <div class="h-8 bg-slate-100 rounded w-1/3"></div>
            <div class="space-y-3">
                <div class="h-4 bg-slate-50 rounded w-full"></div>
                <div class="h-4 bg-slate-50 rounded w-5/6"></div>
            </div>
        </div>
    {:else if policy}
        <div class="bg-white rounded-3xl border border-slate-200 shadow-xl overflow-hidden">
            <div class="bg-indigo-600 p-8 text-white">
                <div class="flex items-center gap-4 mb-4">
                    <div class="bg-white/20 p-3 rounded-2xl backdrop-blur-sm">
                        <Shield class="w-8 h-8" />
                    </div>
                    <div>
                        <h2 class="text-2xl font-bold">{policy.policy_type} Protection</h2>
                        <p class="text-indigo-100">Plan: {policy.title}</p>
                    </div>
                </div>
            </div>

            <div class="p-8 space-y-8">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                    <div class="space-y-1">
                        <span class="text-sm font-medium text-slate-500 flex items-center gap-2">
                            <Building class="w-4 h-4" /> Provider
                        </span>
                        <p class="text-lg font-bold text-slate-900">{policy.provider?.company_name || 'N/A'}</p>
                    </div>
                    <div class="space-y-1">
                        <span class="text-sm font-medium text-slate-500 flex items-center gap-2">
                            <Calendar class="w-4 h-4" /> Duration
                        </span>
                        <p class="text-lg font-bold text-slate-900">12 Months (Annual)</p>
                    </div>
                </div>

                <div class="bg-slate-50 rounded-2xl p-6 space-y-4">
                    <div class="flex justify-between items-center">
                        <span class="text-slate-600">Coverage Amount</span>
                        <span class="text-xl font-bold text-slate-900">${policy.coverage_amount}</span>
                    </div>
                    <div class="flex justify-between items-center pt-4 border-t border-slate-200">
                        <div class="space-y-1">
                            <span class="text-slate-900 font-bold text-lg">Total Premium</span>
                            <p class="text-xs text-slate-500">Includes all applicable taxes</p>
                        </div>
                        <span class="text-3xl font-black text-indigo-600">${policy.premium_amount}</span>
                    </div>
                </div>

                <div class="pt-4 flex flex-col gap-4">
                    <Button 
                        size="lg" 
                        class="w-full h-14 text-lg font-bold shadow-lg shadow-indigo-200"
                        onclick={handleConfirmApplication}
                        loading={isSubmitting}
                    >
                        Confirm & Pay
                    </Button>
                    <p class="text-center text-xs text-slate-400">
                        By clicking confirm, you agree to the terms of service and policy disclosure document.
                    </p>
                </div>
            </div>
        </div>
    {/if}
</div>
