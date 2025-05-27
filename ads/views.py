from .forms import ExchangeProposalForm
from .models import ExchangeProposal
from django.shortcuts import render, get_object_or_404, redirect
from .models import Ad
from .forms import AdForm
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from .forms import RegisterForm
from django.contrib.auth import login



@login_required
def ad_list(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    condition = request.GET.get('condition')

    ads = Ad.objects.all()

    if query:
        ads = ads.filter(title__icontains=query) | ads.filter(description__icontains=query)
    if category:
        ads = ads.filter(category__iexact=category)
    if condition:
        ads = ads.filter(condition__iexact=condition)

    paginator = Paginator(ads.order_by('-created_at'), 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'ads/ad_list.html', {
        'page_obj': page_obj,
        'query': query,
        'category': category,
        'condition': condition
    })



@login_required
def ad_create(request):
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            return redirect('ad_list')
    else:
        form = AdForm()
    
    return render(request, 'ads/ad_form.html', {'form': form})


@login_required
def ad_edit(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    if ad.user != request.user:
        return HttpResponseForbidden("Вы не автор этого объявления.")
    
    if request.method == 'POST':
        form = AdForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('ad_list')
    else:
        form = AdForm(instance=ad)
    return render(request, 'ads/ad_form.html', {'form': form})


@login_required
def ad_delete(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    if ad.user != request.user:
        return HttpResponseForbidden("Вы не автор этого объявления.")
    
    if request.method == 'POST':
        ad.delete()
        return redirect('ad_list')
    return render(request, 'ads/ad_confirm_delete.html', {'ad': ad})


@login_required
def create_proposal(request, ad_id):
    ad_sender = get_object_or_404(Ad, id=ad_id)

    if ad_sender.user != request.user:
        return HttpResponseForbidden("Вы можете предлагать обмен только от своих объявлений.")

    if request.method == 'POST':
        form = ExchangeProposalForm(request.POST)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.ad_sender = ad_sender
            proposal.status = 'ожидает'
            proposal.save()
            return redirect('ad_list')
    else:
        form = ExchangeProposalForm()

    return render(request, 'ads/proposal_form.html', {'form': form, 'ad_sender': ad_sender})



@login_required
def proposal_list(request):
    proposals = ExchangeProposal.objects.filter(
        ad_receiver__user=request.user
    ).order_by('-created_at')
    return render(request, 'ads/proposal_list.html', {'proposals': proposals})


@login_required
@require_POST
def update_proposal_status(request, proposal_id, status):
    proposal = get_object_or_404(ExchangeProposal, id=proposal_id)

    if proposal.ad_receiver.user != request.user:
        return HttpResponseForbidden("Вы не можете изменять это предложение.")

    if status in ['принята', 'отклонена']:
        proposal.status = status
        proposal.save()

    return redirect('proposal_list')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('ad_list')
    else:
        form = RegisterForm()
    return render(request, 'ads/register.html', {'form': form})