from django.shortcuts import render, redirect
from django.views import View
from .models import Country, State, City
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator

# Create your views here.

class Index(View):
    def get(self, request):
        return render(request, 'index.html')

class CountryView(View):
    def get(self, request):
        countries = Country.objects.all()
        context = {'countries': countries}
        return render(request, 'country.html', context)
    
    def post(self, request):
        country_name = request.POST.get('country_name')
        slug = request.POST.get('slug')
        code = request.POST.get('code')
        flag = request.FILES.get('flag')
        state_available = request.POST.get('state_available') == '1'  # Convert to boolean

        if state_available:
            state_available = True
        else:
            state_available = False

        print(state_available)
        # Check if the country already exists
        if Country.objects.filter(slug=slug).exists():
            messages.error(request, f"{country_name} already exists!")
            return redirect('country')

        Country.objects.create(
            name=country_name, 
            slug=slug, 
            code=code, 
            flag=flag, 
            is_state_available=state_available
        )
    
        messages.success(request, "Country added successfully!")
        return redirect('country')
    
class CountryUpdateView(View):
    def get(self, request, slug=None):
        countries = Country.objects.get(slug=slug)
        context = {'countries': countries}
        return render(request, 'countryupdate.html', context)
    
    def post(self, request, slug=None):
        country_name = request.POST.get('country_name')
        new_slug = request.POST.get('slug')
        code = request.POST.get('code')
        flag = request.FILES.get('flag')
        state_available = request.POST.get('state_available') == '1'

        countries = Country.objects.get(slug = slug)
        
        if country_name:
            countries.name= country_name

        if new_slug:
            countries.slug=new_slug

        if code:
            countries.code=code

        if flag:
            countries.flag=flag

        if not state_available:
            state_available = False
            countries.is_state_available = state_available
        else:
            countries.is_state_available = True

        countries.save()
        return redirect('country')
    
class CountryDeleteView(View):
    def get(self, request,slug):
        countries = Country.objects.get(slug = slug)
        countries.delete()
        return redirect('country')

class StateView(View):
    def get(self, request): 
        countryobj = Country.objects.filter(is_state_available = True)
        stateobj = State.objects.all()
        context = {'countries': countryobj, 'stateobj': stateobj}
        return render(request, 'state.html', context)
    
    def post(self, request):
        country_id = request.POST.get('country_id')
        state_name = request.POST.get('state_name')
        state_slug = request.POST.get('state_slug')
        language = request.POST.get('language')
        population = request.POST.get('population')

        countryobj = Country.objects.get(id=country_id)

        print(country_id, state_name, state_slug, language, population)

        State.objects.create(
            country = countryobj,
            name = state_name,
            slug = state_slug,
            language = language,
            population = population
        )
        return redirect('state')
    
class StateUpdateView(View):
    def get(self, request, slug=None): 
        stateobj = State.objects.get(slug = slug)
        countryobj = stateobj.country
        context = {'countryobj':countryobj,'stateobj': stateobj}
        return render(request, 'stateupdate.html', context)
    
    def post(self, request, slug=None):
        state_name = request.POST.get('state_name')
        state_slug = request.POST.get('state_slug')
        language = request.POST.get('language')
        population = request.POST.get('population')

        stateobj = State.objects.get(slug = slug)

        if state_name:
            stateobj.name= state_name

        if state_slug:
            stateobj.slug=state_slug

        if language:
            stateobj.language=language

        if population:
            stateobj.population=population
        
        stateobj.save()
        return redirect('state')
 
class CityView(View):
    def get(self, request):
        countries = Country.objects.all()
        states = State.objects.all()
        cities = City.objects.all()
        context = {'countries': countries, 'states': states, 'cities': cities}
        return render(request, 'city.html', context)

    def post(self, request):
        country_id = request.POST.get('country_id')
        state_id = request.POST.get('state_id')
        city_name = request.POST.get('city_name')
        city_slug = request.POST.get('city_slug')

        state = State.objects.get(id=state_id) if state_id else None
        countryobj = Country.objects.get(id=country_id)

        City.objects.create(
            country=countryobj,
            state=state,
            name=city_name,
            slug=city_slug
        )

        messages.success(request, "City added successfully!")
        return redirect('city')
    
    
class CityUpdateView(View):
    def get(self, request, slug=None):
        cities = City.objects.get(slug = slug)
        countries = cities.country
        states = cities.state
        context = {'countries': countries, 'states': states, 'cities': cities}
        return render(request, 'cityupdate.html', context)

    def post(self, request, slug=None):
        city_name = request.POST.get('city_name')
        city_slug = request.POST.get('city_slug')

        cities = City.objects.get(slug = slug)
        country_id = request.POST.get('country_id')
        state_id = request.POST.get('state_id')

        if city_name:
            cities.name=city_name

        if city_slug:
            cities.slug=city_slug

        if country_id:
            cities.country = Country.objects.get(id=country_id)

        if state_id:
            cities.state = State.objects.get(id=state_id)
        
        cities.save()
        return redirect('city')


@csrf_exempt
def get_states(request):
    if request.method == 'POST':
        country_id = request.POST.get('country_id')
        if country_id:
            states = list(State.objects.filter(country_id=country_id).values('id', 'name'))
            return JsonResponse(states, safe=False)
        return JsonResponse({'error': 'Country ID is required'}, status=400)
    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)