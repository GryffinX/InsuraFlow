<script lang="ts">
	import { auth } from '$lib/stores/auth.svelte';
	import { Button, Input } from '$lib/components';
	import { toast } from 'svelte-sonner';
	import { goto } from '$app/navigation';
	import { page } from '$app/state';
	import { ShieldCheck, Mail } from 'lucide-svelte';

	let email = page.url.searchParams.get('email') || '';
	let otp = $state('');
	let isLoading = $state(false);
	let isResending = $state(false);

	async function handleVerify(e: Event) {
		e.preventDefault();
		if (!otp || otp.length !== 6) {
			toast.error('Please enter a valid 6-digit OTP');
			return;
		}

		isLoading = true;
		try {
			await auth.verifyOtp(email, otp);
			toast.success('Email verified successfully! You can now log in.');
			goto('/login');
		} catch (error: any) {
			const errorData = error.response?.data;
			toast.error(errorData?.error || 'Verification failed');
		} finally {
			isLoading = false;
		}
	}

	async function handleResend() {
		if (!email) return;
		
		isResending = true;
		try {
			await auth.resendOtp(email);
			toast.success('Verification code resent to your email');
		} catch (error: any) {
			const errorData = error.response?.data;
			toast.error(errorData?.error || 'Failed to resend OTP');
		} finally {
			isResending = false;
		}
	}
</script>

<div class="min-h-[calc(100vh-64px)] flex items-center justify-center p-4">
	<div class="max-w-md w-full bg-white rounded-2xl shadow-xl border border-slate-200 p-8 space-y-8">
		<div class="text-center space-y-2">
			<div class="inline-flex items-center justify-center p-3 bg-indigo-50 rounded-2xl mb-2">
				<Mail class="w-8 h-8 text-indigo-600" />
			</div>
			<h1 class="text-3xl font-bold text-slate-900 tracking-tight">Verify Email</h1>
			<p class="text-slate-500">Enter the 6-digit code sent to <span class="font-medium text-slate-900">{email}</span></p>
		</div>

		<form onsubmit={handleVerify} class="space-y-6">
			<Input
				label="Verification Code"
				id="otp"
				placeholder="123456"
				maxlength={6}
				required				bind:value={otp}
			/>

			<Button type="submit" class="w-full h-11" loading={isLoading}>
				Verify Account
			</Button>

			<div class="text-center">
				<p class="text-sm text-slate-500">
					Didn't receive the code? 
					<button 
						type="button"
						onclick={handleResend}
						disabled={isResending}
						class="text-indigo-600 font-medium hover:text-indigo-500 disabled:opacity-50"
					>
						{isResending ? 'Sending...' : 'Resend Code'}
					</button>
				</p>
			</div>

			<a href="/login" class="block w-full text-center text-sm font-medium text-slate-500 hover:text-slate-600">
				Back to Login
			</a>
		</form>
	</div>
</div>
