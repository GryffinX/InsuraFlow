<script lang="ts">
    import { api } from '$lib/api/axios';
    import { Button, Input } from '$lib/components';
    import { toast } from 'svelte-sonner';
    import { Mail, ArrowLeft } from 'lucide-svelte';

    let email = $state('');
    let isSubmitting = $state(false);
    let isSent = $state(false);

    async function handleSubmit(e: Event) {
        e.preventDefault();
        isSubmitting = true;
        try {
            await api.post('auth/password-reset/', { email });
            isSent = true;
            toast.success('Password reset email sent');
        } catch (error: any) {
            toast.error(error.response?.data?.error || 'Failed to send reset email');
        } finally {
            isSubmitting = false;
        }
    }
</script>

<div class="min-h-screen flex items-center justify-center bg-slate-50 px-4 py-12">
    <div class="max-w-md w-full space-y-8 bg-white p-10 rounded-3xl border border-slate-200 shadow-xl">
        <div class="text-center">
            <div class="bg-indigo-50 w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <Mail class="w-8 h-8 text-indigo-600" />
            </div>
            <h2 class="text-3xl font-extrabold text-slate-900 tracking-tight">Forgot password?</h2>
            <p class="mt-2 text-slate-500">No worries, we'll send you reset instructions.</p>
        </div>

        {#if !isSent}
            <form class="mt-8 space-y-6" onsubmit={handleSubmit}>
                <Input
                    label="Email address"
                    type="email"
                    placeholder="name@example.com"
                    required
                    bind:value={email}
                />

                <Button type="submit" class="w-full h-12 text-lg font-bold" loading={isSubmitting}>
                    Reset password
                </Button>
            </form>
        {:else}
            <div class="mt-8 bg-emerald-50 border border-emerald-100 rounded-2xl p-6 text-center">
                <p class="text-emerald-800 font-medium">Check your email for instructions to reset your password.</p>
            </div>
        {/if}

        <div class="text-center">
            <a href="/login" class="inline-flex items-center text-sm font-bold text-indigo-600 hover:text-indigo-500 transition-colors">
                <ArrowLeft class="w-4 h-4 mr-2" /> Back to login
            </a>
        </div>
    </div>
</div>
