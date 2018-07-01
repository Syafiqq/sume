from django.shortcuts import get_object_or_404,render

from django.http import HttpResponse

from .models import Dokumen


def index(request):
    latest_dokumen_list = Dokumen.objects.order_by('-pub_date')[:5]
    context = {
        'latest_dokumen_list': latest_dokumen_list,
    }
    return render(request, 'app/index.html', context)

def detail(request, question_id):
    dokumen = get_object_or_404(Dokumen, pk=question_id)
    # return render(request, 'app/detail.html', {'dokumen':dokumen})

    filename = dokumen.filenya.name.split('/')[-1]
    response = HttpResponse(Dokumen.filenya, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

def openfile(request, question_id):
    filename = Dokumen.filenya.name.split('/')[-1]
    response = HttpResponse(object_name.file, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response