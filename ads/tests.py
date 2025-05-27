
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Ad

class AdModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_create_ad(self):
        ad = Ad.objects.create(
            user=self.user,
            title='Test Ad',
            description='Test Description',
            category='Books',
            condition='new'
        )
        self.assertEqual(ad.title, 'Test Ad')
        self.assertEqual(ad.user.username, 'testuser')
        self.assertIsNotNone(ad.created_at)
from .models import ExchangeProposal

class ExchangeProposalTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')

        self.ad1 = Ad.objects.create(
            user=self.user1,
            title='Item A',
            description='Desc A',
            category='Tech',
            condition='used'
        )
        self.ad2 = Ad.objects.create(
            user=self.user2,
            title='Item B',
            description='Desc B',
            category='Home',
            condition='new'
        )

    def test_create_proposal(self):
        proposal = ExchangeProposal.objects.create(
            ad_sender=self.ad1,
            ad_receiver=self.ad2,
            comment='Want to trade?',
            status='ожидает'
        )
        self.assertEqual(proposal.status, 'ожидает')
        self.assertEqual(proposal.ad_sender.title, 'Item A')
        self.assertEqual(proposal.ad_receiver.title, 'Item B')
