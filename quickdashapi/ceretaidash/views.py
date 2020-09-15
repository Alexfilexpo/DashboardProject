import base64
import datetime
import io
import json
import math
import requests
import urllib

import matplotlib.pyplot as plt

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View

# from api.urls import LastEntryDetailView


class LastProcessedEntry(View):
    template_name = 'general_view.html'

    def get(self, request):
        # Get speech and screen data
        api_uri = request.build_absolute_uri(reverse_lazy('api:LastEntryDetailEndpoint', kwargs={'user': request.user.user_id}))
        entry_data = requests.get(api_uri)
        response_data = json.loads(entry_data.content)

        screen_chart = ''
        speech_chart = ''

        # Creating charts data
        if len(response_data) == 1:
            total_length = datetime.timedelta(seconds=response_data['video_1']['speech_time']['total_length'])
            if 'speech_time' in response_data['video_1']:
                all_speech_time_data = response_data['video_1']['speech_time']
                speech_labels = []
                speech_sizes = []

                total_speech_perc = math.ceil((all_speech_time_data['total_speech']*100)/all_speech_time_data['total_length'])
                total_no_speech_perc = int(((all_speech_time_data['total_length']-all_speech_time_data['total_speech'])*100)/all_speech_time_data['total_length'])
                speech_labels.append('No speech')
                speech_sizes.append(total_no_speech_perc)
                for name, value in all_speech_time_data.items():
                    if name == 'speech_f':
                        speech_labels.append('Woman')
                        speech_sizes.append(int((value*100)/total_speech_perc))
                    elif name == 'speech_m':
                        speech_labels.append('Man')
                        speech_sizes.append(int((value*100)/total_speech_perc))

                speech_chart = self.create_chart(labels=speech_labels, sizes=speech_sizes)

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

                screen_chart = self.create_chart(labels=screen_labels, sizes=screen_sizes)
        else:
            total_seconds = 0

            # Screen presence lists
            screen_labels = []
            screen_sizes = []
            label_size_screen_dict = {}
            woman_sizes = []
            man_sizes = []
            undetermined_sizes = []

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
                        woman_sizes.append(value)
                    elif name == 'screen_m':
                        label_size_screen_dict['Man'] = 0
                        man_sizes.append(value)
                    elif name == 'screen_n':
                        label_size_screen_dict['Undetermined'] = 0
                        undetermined_sizes.append(value)

                # Gathering speech time data
                # print(response_data[video]['speech_time']['total_length'])
                # videos_total_length = datetime.timedelta(seconds=response_data[video]['speech_time']['total_length'])
                # print(videos_total_length)
                all_speech_time_data = response_data[video]['speech_time']
                total_seconds += all_speech_time_data['total_length']
                total_speech_perc = math.ceil((all_speech_time_data['total_speech'] * 100) / all_speech_time_data['total_length'])
                total_no_speech_perc = int(((all_speech_time_data['total_length'] - all_speech_time_data['total_speech']) * 100)/all_speech_time_data['total_length'])
                label_size_speech_dict['No speech'] = 0
                total_speech += total_speech_perc
                no_speech += total_no_speech_perc
                for name, value in response_data[video]['speech_time'].items():
                    if name == 'speech_f':
                        label_size_speech_dict['Woman'] = 0
                        woman_speech += int((value*100)/total_speech_perc)
                    elif name == 'speech_m':
                        label_size_speech_dict['Man'] = 0
                        man_speech += int((value*100)/total_speech_perc)

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

            speech_chart = self.create_chart(labels=speech_labels, sizes=speech_sizes)

            # Processing screen data
            for name, value in label_size_screen_dict.items():
                if name == 'Woman':
                    label_size_screen_dict['Woman'] = sum(woman_sizes)//video_amount
                elif name == 'Man':
                    label_size_screen_dict['Man'] = sum(man_sizes)//video_amount
                elif name == 'Undetermined':
                    label_size_screen_dict['Undetermined'] = sum(undetermined_sizes)//video_amount
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

            screen_chart = self.create_chart(labels=screen_labels, sizes=screen_sizes)

            h, m, s = str(datetime.timedelta(seconds=total_seconds)).split(':')
            total_length = '{}h {}m {}s'.format(h, m, s)

        return render(request, self.template_name, {
            'programms_amount': len(response_data),
            'total_length': total_length,
            'screen_chart': screen_chart,
            'speech_chart': speech_chart
        })

    def create_chart(self, labels: list, sizes: list) -> str:
        fig1, ax1 = plt.subplots()  # Creating simple figure
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)  # Define figure as pie chart
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        chart = plt.gcf()  # Get current figure (chart)
        buffer = io.BytesIO()  # Creating buffer
        chart.savefig(buffer, format='png')  # Saving current chart
        buffer.seek(0)  # Define buffer to be read from start
        chart_sring = base64.b64encode(buffer.read())  # Encoding image to bytes object
        chart_uri = urllib.parse.quote(chart_sring)  # Quoting special characters and encoding non-ASCII text
        return chart_uri
