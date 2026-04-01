<script lang="ts">
    import { page } from '$app/state';
    import { api } from '$lib/api/axios';
    import { Button, Input } from '$lib/components';
    import { toast } from 'svelte-sonner';
    import { goto } from '$app/navigation';
    import { Lock, ArrowLeft } from 'lucide-svelte';

    let newPassword = $state('');
    let confirmPassword = $state('');
    let isSubmitting = $state(false);

    const uid = page.url.searchParams.get('uid');
    const token = page.url.searchParams.get('token');

    async function handleSubmit(e: Event) {
        e.preventDefault();
        if (newPassword !== confirmPassword) {
            return toast.error('Passwords do not match');
        }
        isSubmitting = true;
        try {
            await api.post('auth/password-reset-confirm/', {
                uid,
                token,
                new_password: newPassword
            });
            toast.success('Password reset successfully');
            goto('/login');
        } catch (error: any) {
            toast.error(error.response?.data?.error || 'Failed to reset password');
        } finally {
            isSubmitting = false;
        }
    }
</script>

<div class="min-h-screen flex items-center justify-center bg-slate-50 px-4 py-12">
    <div class="max-w-md w-full space-y-8 bg-white p-10 rounded-3xl border border-slate-200 shadow-xl">
        <div class="text-center">
            <div class="bg-indigo-50 w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <Lock class="w-8 h-8 text-indigo-600" />
            </div>
            <h2 class="text-3xl font-extrabold text-slate-900 tracking-tight">Reset password</h2>
            <p class="mt-2 text-slate-500">Enter your new password below.</p>
        </div>

        <form class="mt-8 space-y-6" onsubmit={handleSubmit}>
            <Input
                label="New password"
                type="password"
                placeholder="••••••••"
                required
                bind:value={newPassword}
            />
            <Input
                label="Confirm new password"
                type="password"
                placeholder="••••••••"
                required
                bind:value={confirmPassword}
            />

            <Button type="submit" class="w-full h-12 text-lg font-bold" loading={isSubmitting}>
                Reset password
            </Button>
        </form>

        <div class="text-center">
            <a href="/login" class="inline-flex items-center text-sm font-bold text-indigo-600 hover:text-indigo-500 transition-colors">
                <ArrowLeft class="w-4 h-4 mr-2" /> Back to login
            </a>
        </div>
    </div>
</div>
