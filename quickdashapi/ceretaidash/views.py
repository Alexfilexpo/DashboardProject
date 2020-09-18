import base64
import datetime
import io
import json
import math
import requests
import urllib

import matplotlib.pyplot as plt

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View


def create_pie_chart_data(response_data):
    if len(response_data) == 1:
        total_length = datetime.timedelta(seconds=response_data['video_1']['speech_time']['total_length'])
        if 'speech_time' in response_data['video_1']:
            all_speech_time_data = response_data['video_1']['speech_time']
            speech_labels = []
            speech_sizes = []

            total_speech_perc = math.ceil(
                (all_speech_time_data['total_speech'] * 100) / all_speech_time_data['total_length'])
            total_no_speech_perc = int(
                ((all_speech_time_data['total_length'] - all_speech_time_data['total_speech']) * 100) /
                all_speech_time_data['total_length'])
            speech_labels.append('No speech')
            speech_sizes.append(total_no_speech_perc)
            for name, value in all_speech_time_data.items():
                if name == 'speech_f':
                    speech_labels.append('Woman')
                    speech_sizes.append(int((value * 100) / total_speech_perc))
                elif name == 'speech_m':
                    speech_labels.append('Man')
                    speech_sizes.append(int((value * 100) / total_speech_perc))

            speech_chart = create_pie_chart(labels=speech_labels, sizes=speech_sizes)

        if 'face_data' in response_data['video_1']:
            all_face_data = response_data['video_1']['face_data']
            screen_labels = []
            screen_sizes = []

            for name, value in all_face_data.items():
                if name == 'screen_f':
                    screen_labels.append('Woman')
                    screen_sizes.append(value)
                elif name == 'screen_m':
                    screen_labels.append('Man')
                    screen_sizes.append(value)
                elif name == 'screen_n':
                    screen_labels.append('Undetermined')
                    screen_sizes.append(value)

            screen_chart = create_pie_chart(labels=screen_labels, sizes=screen_sizes)
    else:
        total_seconds = 0

        # Screen presence lists
        screen_labels = []
        screen_sizes = []
        label_size_screen_dict = {}
        woman_sizes = 0
        man_sizes = 0
        undetermined_sizes = 0

        # Speech time lists
        speech_labels = []
        speech_sizes = []
        label_size_speech_dict = {}
        total_speech = 0
        woman_speech = 0
        man_speech = 0
        no_speech = 0

        video_amount = len(response_data)
        for video in response_data:

            # Gathering screen presence data
            for name, value in response_data[video]['face_data'].items():
                if name == 'screen_f':
                    label_size_screen_dict['Woman'] = 0
                    woman_sizes += value
                elif name == 'screen_m':
                    label_size_screen_dict['Man'] = 0
                    man_sizes += value
                elif name == 'screen_n':
                    label_size_screen_dict['Undetermined'] = 0
                    undetermined_sizes += value

            # Gathering speech time data
            all_speech_time_data = response_data[video]['speech_time']
            total_seconds += all_speech_time_data['total_length']
            total_speech_perc = math.ceil(
                (all_speech_time_data['total_speech'] * 100) / all_speech_time_data['total_length'])
            total_no_speech_perc = math.ceil(
                ((all_speech_time_data['total_length'] - all_speech_time_data['total_speech']) * 100) /
                all_speech_time_data['total_length'])
            label_size_speech_dict['No speech'] = 0
            total_speech += total_speech_perc
            no_speech += total_no_speech_perc
            for name, value in response_data[video]['speech_time'].items():
                if name == 'speech_f':
                    label_size_speech_dict['Woman'] = 0
                    woman_speech += int((value * 100) / total_speech_perc)
                elif name == 'speech_m':
                    label_size_speech_dict['Man'] = 0
                    man_speech += int((value * 100) / total_speech_perc)

        for name, value in label_size_speech_dict.items():
            if name == 'Woman':
                label_size_speech_dict['Woman'] = woman_speech // video_amount
            elif name == 'Man':
                label_size_speech_dict['Man'] = man_speech // video_amount
            elif name == 'No speech':
                label_size_speech_dict['No speech'] = no_speech // video_amount

        for gender, percentage in label_size_speech_dict.items():
            if gender == 'Woman':
                speech_labels.append('Woman')
                speech_sizes.append(percentage)
            elif gender == 'Man':
                speech_labels.append('Man')
                speech_sizes.append(percentage)
            elif gender == 'No speech':
                speech_labels.append('Undetermined')
                speech_sizes.append(percentage)

        speech_chart = create_pie_chart(labels=speech_labels, sizes=speech_sizes)

        # Processing screen data
        for name, value in label_size_screen_dict.items():
            if name == 'Woman':
                label_size_screen_dict['Woman'] = woman_sizes // video_amount
            elif name == 'Man':
                label_size_screen_dict['Man'] = man_sizes // video_amount
            elif name == 'Undetermined':
                label_size_screen_dict['Undetermined'] = undetermined_sizes // video_amount
        for gender, percentage in label_size_screen_dict.items():
            if gender == 'Woman':
                screen_labels.append('Woman')
                screen_sizes.append(percentage)
            elif gender == 'Man':
                screen_labels.append('Man')
                screen_sizes.append(percentage)
            elif gender == 'Undetermined':
                screen_labels.append('Undetermined')
                screen_sizes.append(percentage)

        h, m, s = str(datetime.timedelta(seconds=total_seconds)).split(':')
        total_length = '{}h {}m {}s'.format(h, m, s)

        screen_chart = create_pie_chart(labels=screen_labels, sizes=screen_sizes)
    return {
        'total_length': total_length,
        'speech_chart': speech_chart,
        'screen_chart': screen_chart,
    }


def create_bar_chart_data(response_data):
    videos_amount = len(response_data)
    if videos_amount == 1:
        age_labels = []
        age_sizes = []
        all_age_data = response_data['video_1']['age_all_data']
        for key, value in all_age_data.items():
            if key == 'a_0':
                age_labels.append('1-14')
                age_sizes.append(value)
            if key == 'a_15':
                age_labels.append('15-29')
                age_sizes.append(value)
            if key == 'a_30':
                age_labels.append('30-44')
                age_sizes.append(value)
            if key == 'a_45':
                age_labels.append('45-59')
                age_sizes.append(value)
            if key == 'a_60':
                age_labels.append('60-74')
                age_sizes.append(value)
            if key == 'a_75':
                age_labels.append('75-89')
                age_sizes.append(value)
            if key == 'a_90':
                age_labels.append('90 >')
                age_sizes.append(value)

        age_chart = create_bar_chart(labels=age_labels, sizes=age_sizes)
    else:
        age_labels = []
        age_sizes = []
        label_size_age_dict = {}
        a_0 = 0
        a_15 = 0
        a_30 = 0
        a_45 = 0
        a_60 = 0
        a_75 = 0
        a_90 = 0
        for video in response_data:
            all_age_data = response_data[video]['age_all_data']
            # print(all_age_data)
            for key, value in all_age_data.items():
                if key == 'a_0':
                    label_size_age_dict['1-14'] = 0
                    a_0 += value
                if key == 'a_15':
                    label_size_age_dict['15-29'] = 0
                    a_15 += value
                if key == 'a_30':
                    label_size_age_dict['30-44'] = 0
                    a_30 += value
                if key == 'a_45':
                    label_size_age_dict['45-59'] = 0
                    a_45 += value
                if key == 'a_60':
                    label_size_age_dict['60-74'] = 0
                    a_60 += value
                if key == 'a_75':
                    label_size_age_dict['75-89'] = 0
                    a_75 += value
                if key == 'a_90':
                    label_size_age_dict['90 >'] = 0
                    a_90 += value
        for age_cat, age in label_size_age_dict.items():
            if age_cat == '1-14':
                label_size_age_dict['1-14'] = a_0 // videos_amount
            if age_cat == '15-29':
                label_size_age_dict['15-29'] = a_15 // videos_amount
            if age_cat == '30-44':
                label_size_age_dict['30-44'] = a_30 // videos_amount
            if age_cat == '45-69':
                label_size_age_dict['45-59'] = a_45 // videos_amount
            if age_cat == '60-74':
                label_size_age_dict['60-74'] = a_60 // videos_amount
            if age_cat == '75-89':
                label_size_age_dict['75-89'] = a_75 // videos_amount
            if age_cat == '90 >':
                label_size_age_dict['90 >'] = a_90 // videos_amount
        for name, size in label_size_age_dict.items():
            age_labels.append(name)
            age_sizes.append(size)

        age_chart = create_bar_chart(labels=age_labels, sizes=age_sizes)

    return age_chart


def create_pie_chart(labels: list, sizes: list) -> str:
    fig1, ax1 = plt.subplots()  # Creating simple figure
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)  # Define figure as pie chart
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    chart = plt.gcf()  # Get current figure (chart)
    return convert_to_uri(figure=chart)


def create_bar_chart(labels: list, sizes: list) -> str:
    plt.bar(labels, sizes, color='grey')
    plt.xlabel("age in years")
    plt.ylabel("screen presence in %")
    chart = plt.gcf()
    return convert_to_uri(figure=chart)


def calc_avg_age(response_data):
    videos_amount = len(response_data)
    if videos_amount == 1:
        avg_female_age = response_data['video_1']['age_female_data']['avg_age_f']
        avg_male_age = response_data['video_1']['age_male_data']['avg_age_m']
    else:
        avg_female_age = 0
        avg_male_age = 0
        for video in response_data:
            avg_female_age += response_data[video]['age_female_data']['avg_age_f']
            avg_male_age += response_data[video]['age_male_data']['avg_age_m']
    return {
        'female_age': avg_female_age // videos_amount,
        'male_age': avg_male_age // videos_amount,
    }


def convert_to_uri(figure=None):
    if figure:
        buffer = io.BytesIO()  # Creating buffer
        figure.savefig(buffer, format='png')  # Saving current chart
        buffer.seek(0)  # Define buffer to be read from start
        chart_sring = base64.b64encode(buffer.read())  # Encoding image to bytes object
        chart_uri = urllib.parse.quote(chart_sring)  # Quoting special characters and encoding non-ASCII text
        return chart_uri


class LastProcessedEntry(View):
    template_name = 'general_view.html'

    def get(self, request):
        # Get speech and screen data
        try:
            request.user.user_id
        except:
            return render(request, 'registration/login.html')
        yesterday_date = datetime.date.today()-datetime.timedelta(days=1)
        api_uri = request.build_absolute_uri(reverse_lazy('api:DateFilteredVideoEndpoint', kwargs={'user': request.user.user_id, 'date_range': yesterday_date}))
        entry_data = requests.get(api_uri)
        response_data = json.loads(entry_data.content)
        if not response_data:
            return render(request, self.template_name, {'entry_date': yesterday_date})
        video_id = response_data['video_1']['entry']['video_id']
        entry_date = response_data['video_1']['entry']['entry_date']

        # Creating charts data
        pie_charts = create_pie_chart_data(response_data)
        plt.clf()

        return render(request, self.template_name, {
            'video_id': video_id,
            'entry_date': entry_date,
            'total_hours': request.user.total_quota,
            'hours_left': request.user.current_quota,
            'programms_amount': len(response_data),
            'total_length': pie_charts['total_length'],
            'screen_chart': pie_charts['screen_chart'],
            'speech_chart': pie_charts['speech_chart'],
        })


class EntryDetailResults(View):
    template_name = 'detailed_view.html'

    def get(self, request, date=None, title=None):
        api_uri = request.build_absolute_uri(reverse_lazy('api:DateFilteredVideoEndpoint', kwargs={'user': request.user.user_id, 'date_range': date}))
        entry_data = requests.get(api_uri)
        response_data = json.loads(entry_data.content)
        video_id = response_data['video_1']['entry']['video_id']
        entry_date = response_data['video_1']['entry']['entry_date']

        # Creating charts data
        bar_chart = create_bar_chart_data(response_data)
        charts = create_pie_chart_data(response_data)
        plt.clf()

        # Calculating avg age
        age = calc_avg_age(response_data)

        return render(request, self.template_name, {
            'video_id': video_id,
            'entry_date': entry_date,
            'total_hours': request.user.total_quota,
            'hours_left': request.user.current_quota,
            'programms_amount': len(response_data),
            'total_length': charts['total_length'],
            'screen_chart': charts['screen_chart'],
            'speech_chart': charts['speech_chart'],
            'bar_chart': bar_chart,
            'woman_avg_age': int(age['female_age']),
            'man_avg_age': int(age['male_age']),
        })