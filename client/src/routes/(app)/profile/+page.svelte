<script lang="ts">
    import { auth } from '$lib/stores/auth.svelte';
    import { api } from '$lib/api/axios';
    import { Button, Input } from '$lib/components';
    import { toast } from 'svelte-sonner';
    import Calendar from 'lucide-svelte/icons/calendar';
    import Lock from 'lucide-svelte/icons/lock';
    import Mail from 'lucide-svelte/icons/mail';
    import MapPin from 'lucide-svelte/icons/map-pin';
    import Phone from 'lucide-svelte/icons/phone';
    import Save from 'lucide-svelte/icons/save';
    import User from 'lucide-svelte/icons/user';

    let user = $state({ ...auth.user });
    let isSubmitting = $state(false);
    let passwordData = $state({
        current_password: '',
        new_password: '',
        confirm_password: ''
    });

    async function handleUpdateProfile(e: Event) {
        e.preventDefault();
        isSubmitting = true;
        try {
            const res = await api.patch('auth/me/', user);
            toast.success('Profile updated successfully');
            // Update local storage if needed
            localStorage.setItem('user', JSON.stringify(res.data));
        } catch (error: any) {
            toast.error(error.response?.data?.error || 'Failed to update profile');
        } finally {
            isSubmitting = false;
        }
    }

    async function handleChangePassword(e: Event) {
        e.preventDefault();
        if (passwordData.new_password !== passwordData.confirm_password) {
            return toast.error('Passwords do not match');
        }
        isSubmitting = true;
        try {
            await api.patch('auth/me/', { password: passwordData.new_password });
            toast.success('Password changed successfully');
            passwordData = { current_password: '', new_password: '', confirm_password: '' };
        } catch (error: any) {
            toast.error(error.response?.data?.error || 'Failed to change password');
        } finally {
            isSubmitting = false;
        }
    }
</script>

<div class="max-w-4xl mx-auto px-4 py-12">
    <div class="mb-8">
        <h1 class="text-3xl font-bold text-slate-900">Your Profile</h1>
        <p class="text-slate-500 mt-1">Manage your account settings and personal information.</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Sidebar -->
        <div class="lg:col-span-1 space-y-6">
            <div class="bg-white rounded-3xl border border-slate-200 shadow-sm p-8 text-center">
                <div class="w-24 h-24 bg-indigo-100 rounded-full flex items-center justify-center text-indigo-600 text-3xl font-bold mx-auto mb-4">
                    {user.username?.charAt(0).toUpperCase()}
                </div>
                <h2 class="text-xl font-bold text-slate-900">{user.username}</h2>
                <p class="text-sm text-slate-500 font-mono mt-1">{user.formatted_id}</p>
                <p class="text-sm text-slate-500 capitalize">{user.role}</p>
                <div class="mt-6 pt-6 border-t border-slate-100">
                    <span class={`px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider ${user.is_verified ? 'bg-emerald-50 text-emerald-600' : 'bg-amber-50 text-amber-600'}`}>
                        {user.is_verified ? 'Verified' : 'Unverified'}
                    </span>
                </div>
            </div>
        </div>

        <!-- Main Form -->
        <div class="lg:col-span-2 space-y-8">
            <div class="bg-white rounded-3xl border border-slate-200 shadow-sm p-8">
                <h3 class="text-lg font-bold text-slate-900 mb-6 flex items-center gap-2">
                    <User class="w-5 h-5 text-indigo-600" /> Personal Information
                </h3>
                <form onsubmit={handleUpdateProfile} class="space-y-6">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <Input label="Username" bind:value={user.username} required />
                        <Input label="Email" type="email" bind:value={user.email} required />
                        <Input label="Phone" bind:value={user.phone} />
                        <Input label="Date of Birth" type="date" bind:value={user.dob} />
                    </div>
                    <div class="space-y-1">
                        <label for="profile-address" class="block text-sm font-medium text-slate-700">Address</label>
                        <textarea 
                            id="profile-address"
                            class="block w-full rounded-md border-slate-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm transition-colors border p-2 outline-none" 
                            rows="3"
                            bind:value={user.address}
                        ></textarea>
                    </div>
                    <Button type="submit" loading={isSubmitting} class="w-full md:w-auto">
                        <Save class="w-4 h-4 mr-2" /> Save Changes
                    </Button>
                </form>
            </div>

            <div class="bg-white rounded-3xl border border-slate-200 shadow-sm p-8">
                <h3 class="text-lg font-bold text-slate-900 mb-6 flex items-center gap-2">
                    <Lock class="w-5 h-5 text-indigo-600" /> Change Password
                </h3>
                <form onsubmit={handleChangePassword} class="space-y-6">
                    <Input label="New Password" type="password" bind:value={passwordData.new_password} required />
                    <Input label="Confirm New Password" type="password" bind:value={passwordData.confirm_password} required />
                    <Button type="submit" variant="outline" loading={isSubmitting} class="w-full md:w-auto">
                        Update Password
                    </Button>
                </form>
            </div>
        </div>
    </div>
</div>
