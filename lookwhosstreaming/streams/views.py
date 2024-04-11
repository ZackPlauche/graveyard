from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Q
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from datetime import datetime, date, timedelta

from .forms import *
from .models import *
from .handler import *

# Create your views here.

class Home(View):

    def get(self, request):

        # Context Variables
        streams = Stream.objects.all()
        live_streams = Stream.objects.filter(live=True)
        categories = [Category.objects.get_or_create(name=category)[0] for category in ['Music', 'Influencers', 'Gamers']]
        platforms = [Platform.objects.get_or_create(name=platform)[0] for platform in ['Instagram', 'YouTube', 'Twitch']]
        dates = [(date.today() + timedelta(days=x)) for x in range(-10, 11)]

        # Filters
        # Platform Filter
        if platform_query := request.GET.get('platform'):
            streams = streams.filter(platform__name=platform_query)
            live_streams = live_streams.filter(platform__name=platform_query)
        
        # Category Filter
        if category_query := request.GET.get('category'):
            streams = streams.filter(host__streamer__category__name=category_query)
            live_streams = live_streams.filter(host__streamer__category__name=category_query)

        # Date Filter
        if date_query := request.GET.get('date'):
            try:
                date_query = datetime.strptime(date_query, '%m-%d-%Y').date()
                streams = streams.filter(start_time__date=date_query)
                live_streams = live_streams.filter(start_time__date=date_query)
            except ValueError:
                print('Stream didn\'t work')
        else:
            # Show only streams that are live or haven't yet begun.
            streams = Stream.objects.filter(start_time__date=date.today()) | Stream.objects.filter(live = True) 

        context = {
            'platforms': platforms,
            'categories': categories,
            'dates': dates,
            'streams': streams,
            'live_streams': live_streams,
        }

        return render(request, 'streams/home/home_schedule.html', context)

class TopChart(View):

    def get(self, request):
        # Context Variables
        streams = Stream.objects.all().order_by('-score')
        categories = [Category.objects.get_or_create(name=category)[0] for category in ['Music', 'Influencers', 'Gamers']]
        platforms = [Platform.objects.get_or_create(name=platform)[0] for platform in ['Instagram', 'YouTube', 'Twitch']]

        # Filters
        # Platform Filter
        if platform_query:= request.GET.get('platform'):
            platform = Platform.objects.get(name__iexact=platform_query)
            streams = streams.filter(host__platform=platform)

        # Category Filter
        if category_query:= request.GET.get('category'):
            category = Category.objects.get(name__iexact=category_query)
            streams = streams.filter(host__streamer__category=category)
        
        # Time Filter
        if time_query := request.GET.get('time'):
            if time_query == "all-time":
                pass
            elif time_query == 'today':
                streams = streams.filter(start_time__day=datetime.now().day, start_time__year=datetime.now().year, start_time__month=datetime.now().month)
            elif time_query in {"7", "30"}:
                days = int(time_query)
                start_date = datetime.now() - timedelta(days=days)
                streams = streams.filter(start_time__gt=start_date)
            else:
                streams = streams.filter(start_time__day=datetime.now().day, start_time__year=datetime.now().year)
        else:
            time_query = None

        # Top 100 streams only
        streams = streams[:100]


        context = {
            'streams': streams,
            'platforms': platforms,
            'categories': categories,
            'active_platform': platform_query,
            'active_category': category_query,
            'time_query': time_query,
        }

        return render(request, 'streams/home/home_top_chart.html', context)




# Admin Pages ------------------------------------------------------------------


class Admin(LoginRequiredMixin, View):

    def get(self, request):
        streams = Stream.objects.all()

        if active_platform := request.GET.get('platform'):
            streams = streams.filter(platform__name=active_platform)

        if active_field := request.GET.get('field'):
            if active_field in {'host', 'platform'}:
                streams = streams.order_by(f'{active_field}__name')
            elif active_field in {'live', 'score'}:
                streams = streams.order_by(f'-{active_field}')
            else:
                streams = streams.order_by(f'{active_field}')

        platforms = Platform.objects.all()
        stream_fields = [field for field in Stream._meta.fields if field.verbose_name not in {'ID', 'shady', 'Likes Data', 'Viewer Data', 'Cover Frame'}]

        context = {
            'platforms': platforms,
            'streams': streams,
            'stream_fields': stream_fields,
            'active_platform': active_platform,
            'active_field': active_field,
        }

        return render(request, 'streams/admin/admin.html', context)


# Streamers --------------------------------------------------------------------
class StreamerList(LoginRequiredMixin, ListView):
    model = Streamer
    template_name = 'streams/admin/streamer/streamer_list.html'


class StreamerCreate(LoginRequiredMixin, View):
    def get(self, request):
        form = StreamerForm()
        platforms = Platform.objects.all()
        categories = Category.objects.all()
        context = {
            'form': form,
            'platforms': platforms,
            'categories': categories
        }
        return render(request, 'streams/admin/streamer/streamer_create.html', context)

    def post(self, request):
        if 'upload_file' in request.POST:
            successes, errors = process_watch_list_csv(request.FILES['csv'].read())
            print(f'Errors: {errors}')
            print(f'Successes: {successes}')
            return redirect('streams:streamer_create')
        else:
            form = StreamerForm(request.POST)
            if form.is_valid():
                # Get streamer category
                category_id = request.POST.get('category')
                category = Category.objects.get(id=category_id) if category_id else None
                if category:
                    streamer = Streamer.objects.create(name=form.cleaned_data['streamer_name'], category=category)
                else:
                    streamer = Streamer.objects.create(name=form.cleaned_data['streamer_name'])
                for platform in Platform.objects.all():
                    if request.POST.get(f'{platform.name.lower()}_username'):
                        username = request.POST.get(f'{platform.name.lower()}_username')
                        Account.objects.create(name = strip_username(username), platform = platform, streamer = streamer)
                return redirect('streams:streamer_list')


class StreamerUpdate(LoginRequiredMixin, View):

    def get(self, request, pk):

        INITIAL_VALUES = {}
        streamer = Streamer.objects.get(pk=pk)
        INITIAL_VALUES['streamer_name'] = streamer.name

        for platform in Platform.objects.all():
            if account := streamer.account_set.filter(platform=platform):
                INITIAL_VALUES[f'{platform.name.lower()}_username'] = account[0].name

        INITIAL_VALUES['category'] = streamer.category

        form = StreamerForm(initial=INITIAL_VALUES)
        return render(request, 'streams/admin/streamer/streamer_update.html', {'form': form, 'streamer': streamer})

    def post(self, request, pk):
        form = StreamerForm(request.POST)
        if form.is_valid():

            # Get streamer object from view
            streamer = Streamer.objects.get(id=pk)

            # Get streamer category
            category_id = request.POST.get('category')
            category = Category.objects.get(id=category_id) if category_id else None

            # Update streamer data
            if category:
                streamer.category = category
                streamer.name = form.cleaned_data['streamer_name']
            else:
                streamer.category = None
                streamer.name = form.cleaned_data['streamer_name']
            streamer.save()

            # Update platform account data TODO: Don't let form pass empty value
            for platform in Platform.objects.all():
                if request.POST.get(f'{platform.name.lower()}_username'):
                    account_name = request.POST.get(f'{platform.name.lower()}_username')
                    account, account_create = streamer.account_set.get_or_create(platform=platform)
                    account.name = account_name
                    account.save()
        else:
            print(form.errors)
        return redirect('streams:streamer_list')


class StreamerDetail(LoginRequiredMixin, DetailView):
    model = Streamer
    template_name = 'streams/admin/streamer/streamer_detail.html'


class StreamerDelete(LoginRequiredMixin, View):

    def get(self, request, pk):
        api_account = Streamer.objects.get(pk=pk)
        api_account.delete()
        return redirect('streams:streamer_list')

# API Accounts -----------------------------------------------------------------


class APIAccountList(LoginRequiredMixin, ListView):
    model = APIAccount
    template_name = 'streams/admin/apiaccount/apiaccount_list.html'


class APIAccountDetail(LoginRequiredMixin, DetailView):
    model = APIAccount
    template_name = 'streams/admin/apiaccount/apiaccount_detail.html'


class APIAccountCreate(LoginRequiredMixin, View):

    def get(self, request):
        form = APIAccountForm()
        return render(request, 'streams/admin/apiaccount/apiaccount_create.html', {'form': form})

    def post(self, request):
        if 'upload_file' in request.POST:
            upload_api_accounts(request.FILES['csv'].read())
            return redirect('streams:apiaccount_list')

        else:
            form = APIAccountForm(request.POST)
            if form.is_valid(): 
                form.save()
                return redirect('streams:apiaccount_list')
            else:
                return render(request, 'streams/admin/apiaccount/apiaccount_create.html', {'form': form})


class APIAccountUpdate(LoginRequiredMixin, UpdateView):
    model = APIAccount
    fields = '__all__'
    template_name = 'streams/admin/apiaccount/apiaccount_form.html'
    success_url = '/admin/api-accounts/'


class APIAccountDelete(LoginRequiredMixin, View):

    def get(self, request, pk):
        api_account = APIAccount.objects.get(pk=pk)
        api_account.delete()
        return redirect('streams:apiaccount_list')

# Streams ----------------------------------------------------------------------


class StreamList(LoginRequiredMixin, ListView):
    model = Stream
    template_name = 'streams/admin/stream/stream_list.html'


class StreamDetail(LoginRequiredMixin, DetailView):
    model = Stream
    template_name = 'streams/admin/stream/stream_detail.html'


class StreamCreate(LoginRequiredMixin, View):
    def get(self, request):
        form2 = AddScheduleForm()
        form = StreamForm()
        context = {
            'form': form,
            'form2': form2
        }
        return render(request, 'streams/admin/stream/stream_form.html', context)

    def post(self, request):
        if 'upload_file' in request.POST:
            request.FILES['schedule'].read()
            return redirect('streams:stream_create')
        else:
            print('Manual Form')
            form = StreamForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('streams:stream_list')
            else:
                if form.errors:
                    for error in form.errors:
                        print(dir(error))
                return render(request, 'streams/admin/stream/stream_form.html', {'form': form})


class StreamUpdate(LoginRequiredMixin, UpdateView):
    model = Stream
    form_class = StreamForm
    template_name = 'streams/admin/stream/stream_form.html'
    success_url = '/admin/streams/'


class StreamDelete(LoginRequiredMixin, View):

    def get(self, request, pk):
        broadcast = Stream.objects.get(pk=pk)
        broadcast.delete()
        return redirect('streams:stream_list')
