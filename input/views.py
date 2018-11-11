from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from urlG import get_url_from_points
from url_to_img_tag import * #annotate_urls
from urllib import parse

def index(request):

    context = {}
    return render(request, 'input/index.html', context)


def geturl(request):
    start_latitude =float(request.GET.get('start_latitude'))
    start_longitude = float(request.GET.get('start_longitude'))
    end_latitude = float(request.GET.get('end_latitude'))
    end_longitude =float( request.GET.get('end_longitude'))
    N = request.GET.get('N')

    # print("-------------")
    # print((start_latitude, start_longitude))
    # print((end_latitude, end_longitude))
    # print(type(start_latitude))
    # start = (42.348933, -71.097594)
    # end = (42.352140, -71.123463)
    urls = get_url_from_points((start_latitude, start_longitude), (end_latitude, end_longitude), N)
    report = annotate_urls(urls)
    export_to_csv(report)

    with open('output_report.csv', 'r') as f:
        f = [x.strip('\n') for x in f][1:]
        f = [x.split(',') for x in f]
        # Parse the location for the first input
        #for i in range(len(f)):
            #parsed_url = dict(parse.parse_qsl(parse.urlsplit(f[i][1]).query))
            #f[i][1] = parsed_url["location"]
        return render(request, 'input/result.html', {
            'result_list': f,
        })
