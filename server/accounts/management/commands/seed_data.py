from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from insurance.models import Provider, Agent, Policy, ServiceProvider, Surveyor
from datetime import date, timedelta
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed the database with sample users and policies'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # 1. Create Admin
        admin_user, _ = User.objects.get_or_create(
            username='admin',
            email='admin@insuraflow.com',
            defaults={'role': 'admin', 'is_verified': True}
        )
        if _:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write('Admin user created')

        # 2. Create Providers
        providers = []
        for i in range(1, 3):
            provider_user, _ = User.objects.get_or_create(
                username=f'provider{i}',
                email=f'provider{i}@insuraflow.com',
                defaults={'role': 'provider', 'is_verified': True}
            )
            if _:
                provider_user.set_password('provider123')
                provider_user.save()

            provider, _ = Provider.objects.get_or_create(
                registration_no=f'REG-{1000+i}',
                defaults={
                    'user': provider_user,
                    'company_name': f'SafeGuard {i}',
                    'contact_email': f'contact{i}@safeguard.com',
                    'head_office_address': f'Street {i}, Business Hub'
                }
            )
            providers.append(provider)
            self.stdout.write(f'Provider {provider.company_name} created')

        # 3. Create Agents
        agents = []
        for i in range(1, 3):
            agent_user, _ = User.objects.get_or_create(
                username=f'agent{i}',
                email=f'agent{i}@insuraflow.com',
                defaults={'role': 'agent', 'is_verified': True}
            )
            if _:
                agent_user.set_password('agent123')
                agent_user.save()

            agent, _ = Agent.objects.get_or_create(
                email=agent_user.email,
                defaults={
                    'user': agent_user,
                    'name': f'Agent {agent_user.username}',
                    'license_no': f'LIC-{5000+i}',
                    'phone_no': f'98765432{i}',
                    'region': 'Global',
                    'provider': random.choice(providers)
                }
            )
            agents.append(agent)
            self.stdout.write(f'Agent {agent.name} created')

        # 4. Create Surveyors
        for i in range(1, 3):
            surveyor_user, _ = User.objects.get_or_create(
                username=f'surveyor{i}',
                email=f'surveyor{i}@insuraflow.com',
                defaults={'role': 'surveyor', 'is_verified': True}
            )
            if _:
                surveyor_user.set_password('surveyor123')
                surveyor_user.save()

            surveyor, _ = Surveyor.objects.get_or_create(
                user=surveyor_user,
                defaults={
                    'name': f'Surveyor {i}',
                    'license_no': f'SUR-{7000+i}',
                    'phone': f'11223344{i}',
                    'email': surveyor_user.email,
                    'region': 'North' if i == 1 else 'South'
                }
            )
            self.stdout.write(f'Surveyor {surveyor.name} created')

        # 5. Create Policies (Catalog)
        plans_data = [
            {'title': 'Basic Health', 'description': 'Essential health coverage for individuals.', 'type': 'health', 'cov': 10000, 'prem': 150},
            {'title': 'Premium Health', 'description': 'Comprehensive health coverage with global access.', 'type': 'health', 'cov': 50000, 'prem': 1200},
            {'title': 'Standard Motor', 'description': 'Reliable motor insurance for your vehicle.', 'type': 'motor', 'cov': 20000, 'prem': 400},
            {'title': 'Luxury Motor', 'description': 'Premium protection for high-end vehicles.', 'type': 'motor', 'cov': 100000, 'prem': 2500},
        ]
        
        for p in plans_data:
            policy, _ = Policy.objects.get_or_create(
                title=p['title'],
                defaults={
                    'description': p['description'],
                    'policy_type': p['type'],
                    'coverage_amount': p['cov'],
                    'premium_amount': p['prem'],
                    'provider': random.choice(providers)
                }
            )
            self.stdout.write(f'Policy {policy.title} created')

        # 6. Create Service Providers (Hospitals/Garages)
        sp_data = [
            {'name': 'City General Hospital', 'type': 'hospital', 'lic': 'HOSP-001', 'city': 'Metropolis', 'addr': '123 Health Ave'},
            {'name': 'FastFix Auto Garage', 'type': 'garage', 'lic': 'GAR-992', 'city': 'Gotham', 'addr': '456 Motor St'},
            {'name': 'Wellness Clinic', 'type': 'hospital', 'lic': 'HOSP-773', 'city': 'Metropolis', 'addr': '789 Care Blvd'},
        ]

        for sp in sp_data:
            service_provider, _ = ServiceProvider.objects.get_or_create(
                licence_no=sp['lic'],
                defaults={
                    'name': sp['name'],
                    'provider_type': sp['type'],
                    'address': sp['addr'],
                    'city': sp['city'],
                    'contact_no': f'555-{random.randint(1000, 9999)}'
                }
            )
            self.stdout.write(f'Service Provider {service_provider.name} created')

        self.stdout.write(self.style.SUCCESS('Successfully seeded data'))
