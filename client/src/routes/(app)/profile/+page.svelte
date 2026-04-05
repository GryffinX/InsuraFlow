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

<div class="max-w-6xl mx-auto px-4 py-12">
    <div class="mb-10 animate-fade-in">
        <h1 class="text-4xl font-black text-slate-50 tracking-tight">Your Profile</h1>
        <p class="text-slate-400 mt-1 font-medium">Manage your account settings and personal information.</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-10">
        <!-- Sidebar -->
        <div class="lg:col-span-1 space-y-8">
            <div class="dashboard-card p-10 text-center relative overflow-hidden group">
                <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-violet-500/50 to-transparent"></div>
                <div class="w-28 h-28 bg-violet-500/10 rounded-3xl flex items-center justify-center text-violet-200 text-4xl font-black mx-auto mb-6 border border-violet-500/20 shadow-[0_0_50px_rgba(124,58,237,0.15)] group-hover:scale-105 transition-transform duration-500">
                    {user.username?.charAt(0).toUpperCase()}
                </div>
                <h2 class="text-2xl font-black text-slate-50 tracking-tight">{user.username}</h2>
                <p class="text-xs font-black text-slate-500 uppercase tracking-widest mt-2 font-mono">{user.formatted_id}</p>
                <div class="mt-4 inline-flex items-center gap-2 px-4 py-1.5 bg-white/5 rounded-full border border-white/5">
                    <span class="w-1.5 h-1.5 rounded-full bg-violet-400 animate-pulse"></span>
                    <p class="text-[10px] text-slate-400 font-black uppercase tracking-widest">{user.role}</p>
                </div>
                
                <div class="mt-8 pt-8 border-t border-white/8">
                    <span class={`inline-flex items-center gap-2 px-5 py-2 rounded-2xl text-[10px] font-black uppercase tracking-[0.2em] border shadow-sm ${user.is_verified ? 'bg-emerald-500/14 border-emerald-300/16 text-emerald-200' : 'bg-amber-500/14 border-amber-300/16 text-amber-200'}`}>
                        {#if user.is_verified}
                            <div class="w-1.5 h-1.5 rounded-full bg-emerald-400"></div>
                        {:else}
                            <div class="w-1.5 h-1.5 rounded-full bg-amber-400"></div>
                        {/if}
                        {user.is_verified ? 'Verified Account' : 'Pending Verification'}
                    </span>
                </div>
            </div>

            <div class="dashboard-card p-8 space-y-4">
                <div class="flex items-center gap-4 text-slate-400 hover:text-slate-200 transition-colors cursor-default">
                    <Mail class="w-4 h-4" />
                    <span class="text-sm font-medium">{user.email}</span>
                </div>
                <div class="flex items-center gap-4 text-slate-400 hover:text-slate-200 transition-colors cursor-default">
                    <Phone class="w-4 h-4" />
                    <span class="text-sm font-medium">{user.phone || 'No phone added'}</span>
                </div>
                <div class="flex items-center gap-4 text-slate-400 hover:text-slate-200 transition-colors cursor-default">
                    <Calendar class="w-4 h-4" />
                    <span class="text-sm font-medium">{user.dob ? new Date(user.dob).toLocaleDateString() : 'No birth date added'}</span>
                </div>
            </div>
        </div>

        <!-- Main Form -->
        <div class="lg:col-span-2 space-y-10">
            <div class="dashboard-card p-10 relative overflow-hidden">
                <div class="absolute top-0 right-0 w-64 h-64 bg-violet-600/5 blur-[100px] -z-10 rounded-full"></div>
                <h3 class="text-xl font-black text-slate-50 mb-8 flex items-center gap-3 tracking-tight">
                    <div class="p-2 bg-violet-500/10 rounded-lg">
                        <User class="w-5 h-5 text-violet-400" />
                    </div>
                    Personal Information
                </h3>
                <form onsubmit={handleUpdateProfile} class="space-y-8">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                        <Input label="Username" bind:value={user.username} required class="bg-white/[0.03] border-white/10 text-slate-50 h-14 rounded-2xl" />
                        <Input label="Email" type="email" bind:value={user.email} required class="bg-white/[0.03] border-white/10 text-slate-50 h-14 rounded-2xl" />
                        <Input label="Phone" bind:value={user.phone} class="bg-white/[0.03] border-white/10 text-slate-50 h-14 rounded-2xl" />
                        <Input label="Date of Birth" type="date" bind:value={user.dob} class="bg-white/[0.03] border-white/10 text-slate-50 h-14 rounded-2xl" />
                    </div>
                    <div class="space-y-2">
                        <label for="profile-address" class="block text-[10px] font-black uppercase tracking-widest text-slate-400 ml-1">Address</label>
                        <textarea 
                            id="profile-address"
                            class="block w-full rounded-2xl border-white/10 bg-white/[0.03] text-slate-50 shadow-sm focus:border-violet-500/50 focus:ring-0 sm:text-sm transition-all border p-5 outline-none placeholder:text-slate-600 min-h-[120px]" 
                            rows="3"
                            bind:value={user.address}
                            placeholder="Your primary residence address..."
                        ></textarea>
                    </div>
                    <div class="pt-4">
                        <Button type="submit" loading={isSubmitting} class="w-full md:w-auto px-10 h-12 rounded-xl font-black shadow-[0_12px_40px_rgba(124,58,237,0.2)]">
                            <Save class="w-4 h-4 mr-2" /> Save Changes
                        </Button>
                    </div>
                </form>
            </div>

            <div class="dashboard-card p-10 relative overflow-hidden">
                <div class="absolute bottom-0 left-0 w-64 h-64 bg-violet-600/5 blur-[100px] -z-10 rounded-full"></div>
                <h3 class="text-xl font-black text-slate-50 mb-8 flex items-center gap-3 tracking-tight">
                    <div class="p-2 bg-violet-500/10 rounded-lg">
                        <Lock class="w-5 h-5 text-violet-400" />
                    </div>
                    Security & Password
                </h3>
                <form onsubmit={handleChangePassword} class="space-y-8">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                        <Input label="New Password" type="password" bind:value={passwordData.new_password} required class="bg-white/[0.03] border-white/10 text-slate-50 h-14 rounded-2xl" />
                        <Input label="Confirm New Password" type="password" bind:value={passwordData.confirm_password} required class="bg-white/[0.03] border-white/10 text-slate-50 h-14 rounded-2xl" />
                    </div>
                    <div class="pt-4">
                        <Button type="submit" variant="outline" loading={isSubmitting} class="w-full md:w-auto px-10 h-12 rounded-xl font-bold border-white/10 hover:bg-white/5 text-slate-300">
                            Update Password
                        </Button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
