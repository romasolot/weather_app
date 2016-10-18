from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from wsw.models import Forecast, Stations
from django.core import serializers
from django.template.defaultfilters import *
from itertools import chain
import datetime
import json
import operator
from django.db.models import F, Value, CharField

def weather_json_formating(obj, requested_fields):
    return json.dumps(
        serializers.serialize('python', obj, fields=requested_fields, indent=4, use_natural_foreign_keys=True),
        ensure_ascii=False,
        default=date_handler)

def calculate_Pa(obj):
    timestamp_idx = next((idx for idx, x in enumerate(obj.values()) if date(x['forecasttime'], "n/j ga") == date(datetime.datetime.now() - datetime.timedelta(days=1), "n/j ga")), None)
    timestamp_idx = (1, obj.values().count()-1)[timestamp_idx==None]
    s = obj.values()[timestamp_idx]['psum']
    i = 0
    for d in obj:
        if(i < timestamp_idx):
            d.pa_ = (timestamp_idx - i) * s
        else:
            d.pa_ = (i - timestamp_idx) * s
        i += 1

    return obj

def date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError

def is_member(user):
    return user.groups.filter(name='Member').exists()

# @login_required
#@user_passes_test(is_member)
def dashboard(request):
    data = get_combined_data()
    return render(request, 'apps/dashboard.html', {'browser': request.META.get('HTTP_USER_AGENT', 'unknown') ,
                                                   'forecast_data': json.loads(weather_json_formating(data['forecast_opened'], ('forecasttime', 'windspdstr'))),
                                                   'stations_data': calculate_Pa(data['stations_opened']),
                                                   'container_1': weather_line_with_focus_chart(data['forecast'], data['stations']).get('chartcontainer'),
                                                   'container_2': weather_discretebarchart_with_date(data['combined_data_cleared']).get('chartcontainer'),
                                                   'charttype_1': weather_line_with_focus_chart(data['forecast'], data['stations']).get('charttype'),
                                                   'charttype_2': weather_discretebarchart_with_date(data['combined_data_cleared']).get('charttype'),
                                                   'chartdata_1': weather_line_with_focus_chart(data['forecast'], data['stations']).get('chartdata'),
                                                   'chartdata_2': weather_discretebarchart_with_date(data['combined_data_cleared']).get('chartdata'),
                                                   'extra_1': weather_line_with_focus_chart(data['forecast'], data['stations']).get('extra'),
                                                   'extra_2': weather_discretebarchart_with_date(data['combined_data_cleared']).get('extra'),
                                                   })

def weather_line_with_focus_chart(fdata, sdata):
    return {
        'charttype': "lineWithFocusChart",
        'chartdata': {
            'x': sorted(list(fdata['date_property'] + sdata['date_property'])),
            'name1': 'WINDSPD(forecast)',
            'y1': fdata['windspd'],
            'name2': 'WINDSPD(stations)',
            'y2': sdata['windspd'],
            'extra1': {
                "tooltip": {
                    "y_start": "",
                    "y_end": ""
                },
                "date_format": '%d/%b %H',
                "color_list": ['#5d8aa8', '#e32636']
            },
            'extra2': {
                "tooltip": {
                    "y_start": "",
                    "y_end": ""
                },
                "date_format": '%d/%b %H',
                "color_list": ['#ff55a3', '#5f9ea0']
            },
        },
        'chartcontainer': "linewithfocuschartcontainer",
        'extra': {
            'x_is_date': True,
            'x_axis_format': '%d/%b %H',
            'tag_script_js': True,
            'jquery_on_ready': False
        }
    }

def weather_discretebarchart_with_date(data):
    return {
        'charttype': "discreteBarChart",
        'chartdata': {
            'name': 'PSUM',
            'x': data['date_property'],
            'y': data['psum'],
            'extra': {
                "tooltip": {
                    "y_start": "",
                    "y_end": ""
                },
                "date_format": '%d/%b %H',
            },
        },
        'chartcontainer': "discretebarchartwithdatecontainer",
        'extra': {
            'x_is_date': True,
            'x_axis_format': '%d/%b %H',
            'tag_script_js': True,
            'jquery_on_ready': False,
        },
    }

# @login_required
#@user_passes_test(is_member)
def ex_ch1(request):
    f = get_combined_data()['forecast']
    s = get_combined_data()['stations']

    diff_dicts(f, s)
    diff_dicts(s, f)

    data = {
        'container': weather_line_with_focus_chart(f, s).get('chartcontainer'),
        'charttype': weather_line_with_focus_chart(f, s).get('charttype'),
        'chartdata': weather_line_with_focus_chart(f, s).get('chartdata'),
        'extra': weather_line_with_focus_chart(f, s).get('extra'),
    }
    return render(request, 'charts/line_with_focus_chart.html', data)

# @login_required
#@user_passes_test(is_member)
def ex_ch2(request):
    d = get_combined_data()['combined_data_cleared']
    data = {
        'container': weather_discretebarchart_with_date(d).get('chartcontainer'),
        'charttype': weather_discretebarchart_with_date(d).get('charttype'),
        'chartdata': weather_discretebarchart_with_date(d).get('chartdata'),
        'extra': weather_discretebarchart_with_date(d).get('extra'),
    }
    return render(request, 'charts/discretebarchart_with_date.html', data)

def prepare_data(dataset):
    forecasttime = []
    windspd = []
    temp_mtop = []
    temp_base = []
    psum = []
    fs = []

    for i in dataset:
        forecasttime.append(int(datetime.datetime.strptime(str(i.forecasttime), "%Y-%m-%d %H:%M:%S").timestamp() * 1000))
        windspd.append(int(i.windspd))
        temp_mtop.append(int(i.temp_mtop))
        temp_base.append(int(i.temp_base))
        psum.append(int(i.psum))
        fs.append(i.fs) # remove

    return {'date_property':forecasttime, 'windspd':windspd, 'temp_mtop':temp_mtop, 'temp_base':temp_base, 'psum':psum, 'fs':fs}

def get_combined_data():
    f = Forecast.objects.all().annotate(fs=Value('f', output_field=CharField()))
    s = Stations.objects.all().annotate(fs=Value('s', output_field=CharField()))

    ex_fs = f.exclude(forecasttime__in=s.values_list('forecasttime', flat=True))
    ex_sf = s.exclude(forecasttime__in=f.values_list('forecasttime', flat=True))

    ex_s = reprepare_data(prepare_data(ex_sf)['date_property'], s)
    ex_f = reprepare_data(prepare_data(ex_fs)['date_property'], f)

    fc = clear_data(ex_fs)
    sc = clear_data(ex_sf)

    ex_sc = reprepare_data(prepare_data(ex_sf)['date_property'], sc)
    ex_fc = reprepare_data(prepare_data(ex_fs)['date_property'], fc)

    return {'combined_data': prepare_data(sorted(list(chain(ex_f, ex_s)),key=operator.attrgetter('forecasttime'))),
            'combined_data_cleared': prepare_data(sorted(list(chain(ex_fc, ex_sc)), key=operator.attrgetter('forecasttime'))),
            'forecast': prepare_data(sorted(list(chain(ex_f)),key=operator.attrgetter('forecasttime'))),
            'stations': prepare_data(sorted(list(chain(ex_s)),key=operator.attrgetter('forecasttime'))),
            'forecast_cleared': prepare_data(sorted(list(chain(ex_fc)), key=operator.attrgetter('forecasttime'))),
            'stations_cleared': prepare_data(sorted(list(chain(ex_sc)), key=operator.attrgetter('forecasttime'))),
            'forecast_opened_cleared': fc,
            'stations_opened_cleared': sc,
            'forecast_opened': f,
            'stations_opened': s}

def diff_dicts(what_item, with_item):
    return (list(set(what_item.get('date_property')) - set(with_item.get('date_property'))))

def reprepare_data(list_date, income_dataset):
    dataset_up = list()
    dataset = list(income_dataset)
    for index, i in enumerate(dataset):
        date_in = int(datetime.datetime.strptime(str(i.forecasttime), "%Y-%m-%d %H:%M:%S").timestamp() * 1000)
        if(date_in not in list_date):
            if(index > 0):
                previous_obj = dataset[index - 1]
            else:
                previous_obj = dataset[index]
            previous_obj.forecasttime = datetime.datetime.fromtimestamp(date_in/1000)
            dataset_up.append(previous_obj)
        else:
            dataset_up.append(dataset[index])

    return dataset_up

def clear_data(income_list_obj):
    list_obj = list(income_list_obj)
    for index, i in enumerate(income_list_obj):
        if(0 == int(i.psum)):
            list_obj.remove(income_list_obj[index])

    return list_obj