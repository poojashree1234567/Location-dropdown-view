from django.urls import path
from .views import *

urlpatterns = [

#Home path
    path('',Index.as_view(), name='index'),

# country path
    path('country',CountryView.as_view(), name='country'),
    path('country/<str:slug>/update/',CountryUpdateView.as_view(), name='country_update'),
    path('country/<slug:slug>/delete/',CountryDeleteView.as_view(), name='country_delete'),

#state path
    path('state',StateView.as_view(), name='state'),
    path('state_update/<str:slug>',StateUpdateView.as_view(), name='state_update'),
    path('state/<slug:slug>/delete/',StateDeleteView.as_view(), name='state_delete'),

#city path
    path('city',CityView.as_view(), name='city'),
    path('city_update/<str:slug>',CityUpdateView.as_view(), name='city_update'),
    path('city/<slug:slug>/delete/',CityDeleteView.as_view(), name='city_delete'),

    path('get_states/', get_states, name='get_states'),
    ]