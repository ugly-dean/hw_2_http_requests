from django.shortcuts import render
from django.core.paginator import Paginator
from ugly_app.models import *

# Create your views here.

QUESTIONS_CONTEXT = [
    {
        "main_user": "ugly_dean",
        "user": f"user_{i}",
        "index": i,
        "title": f"Title of ugly question #{i}",
        "text": f"This is text for question #{i}. It can be much bigger. \
                    So I just want to see how it will be interpreted by \
                    my browser - checking my static html files.Much, much bigger. Huge text. Gigantic. More and more text. \
                    Stupid answer for stupid question...... This is not enough for \
                    testing static html files so let's put here something more.... \
                    Well, ok, that's enough!",
        "tags": ["ugly", "nasty", "awful", ],
        "likes": i * 10 + i * 3,
        "dislikes": i * 2 + 3,
        "answers": [
            {
                "user": f"user_{j}",
                "text": f"This is text for answer {j}... It can be much bigger. \
                    So I just want to see how it will be interpreted by \
                    my browser - checking my static html files.\n \
                    Much, much bigger. Huge text. Gigantic. More and more text. \
                    Stupid answer for stupid question...... This is not enough for \
                    testing static html files so let's put here something more.... \
                    Well, ok, that's enough!",
                "likes": j * 3,
                "dislikes": j + 3,
            } for j in range(1, 11)
        ],
        "answers_count": i * 11 - 15 + (i + 1) * 2,
    } for i in range(1, 11)
]


TAGS_CONTEXT = {
    "ugly": QUESTIONS_CONTEXT,
    "nasty": QUESTIONS_CONTEXT,
    "awful": QUESTIONS_CONTEXT,
}


INDEX_CONTEXT = {
    "user": "ugly_dean",
    "quests": QUESTIONS_CONTEXT,
    "tag": "ugly",
    "hot_tags": [
        "ugly",
        "nasty",
        "awful",
        "awkward",
        "disqusting",
    ]
}

HOT_MEMBERS = [
        "ugly_dean",
        "alinazna",
        "artembabdustov",
        "keshaproletarskiy",
        "ann___a.m",
    ]


def hot_tags():
    return Tag.objects.get_top_tags()


def new_questions_list():
    quests = []
    for quest in Question.objects.all():
        answers = Answer.objects.get_answers_for_quest(quest).count()
        likes = LikeQuestion.objects.get_likes(quest).count()
        dislikes = LikeQuestion.objects.get_dislikes(quest).count()
        quests.append((quest, answers, likes, dislikes))
    return quests


def hot_questions_list():
    quests = []
    for likes, quest in Question.objects.get_top():
        answers = Answer.objects.get_answers_for_quest(quest).count()
        dislikes = LikeQuestion.objects.get_dislikes(quest).count()
        quests.append((quest, answers, likes, dislikes))
    return quests


def index(request):
    return render(request, "index.html", {"index": INDEX_CONTEXT,
                                          "page": paginate(new_questions_list(), request.GET.get('page')),
                                          "hot_tags": hot_tags(),
                                          "hot_members": HOT_MEMBERS})


def hot(request):
    return render(request, "hot.html", {"index": INDEX_CONTEXT,
                                        "page": paginate(hot_questions_list(), request.GET.get('page')),
                                        "hot_tags": hot_tags(),
                                        "hot_members": HOT_MEMBERS})


def tag_questions_list(tag):
    quests = []
    for quest in Tag.objects.get_qs(tag):
        answers = Answer.objects.get_answers_for_quest(quest).count()
        likes = LikeQuestion.objects.get_likes(quest).count()
        dislikes = LikeQuestion.objects.get_dislikes(quest).count()
        quests.append((quest, answers, likes, dislikes))
    return quests


def tags(request, tag):
    return render(request, "tags.html", {"index": INDEX_CONTEXT,
                                         "tag": tag,
                                         "page": paginate(tag_questions_list(tag), request.GET.get('page')),
                                         "hot_tags": hot_tags(),
                                         "hot_members": HOT_MEMBERS})


def answers_list(quest):
    answers = []
    for ans in Answer.objects.get_answers_for_quest(quest):
        likes = LikeAnswer.objects.get_likes(ans).count()
        dislikes = LikeAnswer.objects.get_dislikes(ans).count()
        answers.append((ans, likes, dislikes))
    return answers


def one_question(quest):
    likes = LikeQuestion.objects.get_likes(quest).count()
    dislikes = LikeQuestion.objects.get_dislikes(quest).count()
    return quest, likes, dislikes


def question(request, i):
    quest = Question.objects.get(pk=i)
    return render(request, "question.html", {"index": INDEX_CONTEXT,
                                             "question": [one_question(quest)],
                                             "page": paginate(answers_list(quest), request.GET.get('page')),
                                             "hot_tags": hot_tags(),
                                             "hot_members": HOT_MEMBERS})


def login(request):
    return render(request, "login.html", {"hot_tags": INDEX_CONTEXT["hot_tags"],
                                          "hot_members": HOT_MEMBERS})


def signup(request):
    return render(request, "signup.html", {"hot_tags": INDEX_CONTEXT["hot_tags"],
                                           "hot_members": HOT_MEMBERS})


def ask(request):
    return render(request, "ask.html", {"index": INDEX_CONTEXT,
                                        "hot_tags": INDEX_CONTEXT["hot_tags"],
                                        "hot_members": HOT_MEMBERS})


def users(request, user_name):
    return render(request, "user_page.html", user_name)


def paginate(objects_list, per_page=1):
    p = Paginator(objects_list, 3)
    page = p.get_page(per_page)
    return page
