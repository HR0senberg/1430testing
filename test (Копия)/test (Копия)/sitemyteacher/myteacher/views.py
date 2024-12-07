from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseNotAllowed, HttpResponseBadRequest, \
    HttpResponseServerError, JsonResponse

from django.shortcuts import render, get_object_or_404, redirect
from .models import Teacher, Comment
from transformers import pipeline

classifier = pipeline("text-classification", model="SkolkovoInstitute/russian_toxicity_classifier")

def check_toxicity(text):
    result = classifier(text)
    label = result[0]['label']
    score = result[0]['score']
    return label, score


def is_valid_message(content):
    if len(content)<80:
        return True
    return False



def responce_error(request):
    pass


def index(request):
    teachers = Teacher.objects.all()
    math_subjects = ["Информатика", "Математика", "Физика"]
    russ_subjects = ["Русский и литература"]
    fiz_subjects = ["Физкультура"]
    his_subjects = ["История и обществознание"]
    eng_subjects = ["Английский язык"]
    bio_subjects = ["Биология", "География", "Химия", "Химия и биология"]
    izo_subjects = [ "Технология","Музыка","ИЗО", "ИЗО и технология"]
    dop_subjects = ["Советник директора", "ОБЖ", "Библиотекарь", "Педагог-организатор", "Специалист по ИКТ"]
    adm_subjects = ["Директор школы", "Зам директора школы"]

    return render(request, 'muchitel/index.html', {
        "teachers":teachers, "math_subjects":math_subjects,
        "russ_subjects": russ_subjects,
        "fiz_subjects": fiz_subjects,
        "his_subjects": his_subjects,
        "eng_subjects": eng_subjects,
        "bio_subjects": bio_subjects,
        "izo_subjects": izo_subjects,
        "dop_subjects": dop_subjects,
        "adm_subjects": adm_subjects,
    })

def teacher_page (request, slug):
    try:
        teacher = get_object_or_404(Teacher, slug=slug)

        if request.method == 'POST':
            content = request.POST.get('textarea', '').lstrip().rstrip()
            label, score = check_toxicity(content)
            if not content:
                return JsonResponse({'error': 'Сообщение не может быть пустым.'}, status=400)
            elif is_valid_message(content):
                return JsonResponse({'error': 'Слишком короткое сообщение'}, status=400)
            elif label=="toxic" and score >=0.99:
                return JsonResponse({'error': 'Сообщение токсичное'}, status=400)


            comment = Comment.objects.create(teacher=teacher, content=content)

            return JsonResponse({'content': comment.content, 'created_at': comment.created_at.strftime('%d-%m-%Y %H:%M')})

        comments = teacher.comments.all()
        return render(request, 'teacher/index.html', {'teacher': teacher, 'comments': comments})
    except Teacher.DoesNotExist:
        raise Http404()


def about(request):
    return render(request, 'aboutproject/index.html')

def rules(request):
    return render(request, 'rules/index.html')

def page_not_found(request, exception ):
    return HttpResponseNotFound("<h1>Страница не найдена</h1><h2>404</h2>")

def page_not_found_500(request): # for 500
    return HttpResponseServerError('500(')