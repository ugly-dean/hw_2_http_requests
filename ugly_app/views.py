from django.shortcuts import render
from django.core.paginator import Paginator

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
    ],
    "hot_members": [
        "ugly_dean",
        "alinazna",
        "artembabdustov",
        "keshaproletarskiy",
        "ann___a.m",
    ]
}


def index(request):
    page = paginate(INDEX_CONTEXT["quests"], request.GET.get('page'))
    return render(request, "index.html", {"index": INDEX_CONTEXT,
                                          "page": page,
                                          "hot_tags": INDEX_CONTEXT["hot_tags"],
                                          "hot_members": INDEX_CONTEXT["hot_members"]})


def hot(request):
    return render(request, "hot.html", {"index": INDEX_CONTEXT})


def tags(request, tag):
    return render(request, "tags.html", {"index": INDEX_CONTEXT,
                                         "tag": TAGS_CONTEXT[tag],
                                         "hot_tags": INDEX_CONTEXT["hot_tags"],
                                         "hot_members": INDEX_CONTEXT["hot_members"]})


def question(request, i):
    page = paginate(QUESTIONS_CONTEXT[i - 1]["answers"], request.GET.get('page'))
    return render(request, "question.html", {"index": INDEX_CONTEXT,
                                             "quest": QUESTIONS_CONTEXT[i - 1],
                                             "page": page,
                                             "hot_tags": INDEX_CONTEXT["hot_tags"],
                                             "hot_members": INDEX_CONTEXT["hot_members"]})


def login(request):
    return render(request, "login.html", {"hot_tags": INDEX_CONTEXT["hot_tags"],
                                          "hot_members": INDEX_CONTEXT["hot_members"]})


def signup(request):
    return render(request, "signup.html", {"hot_tags": INDEX_CONTEXT["hot_tags"],
                                           "hot_members": INDEX_CONTEXT["hot_members"]})


def ask(request):
    return render(request, "ask.html", {"index": INDEX_CONTEXT,
                                        "hot_tags": INDEX_CONTEXT["hot_tags"],
                                        "hot_members": INDEX_CONTEXT["hot_members"]})


def users(request, user_name):
    return render(request, "user_page.html", user_name)


def paginate(objects_list, per_page=1):
    p = Paginator(objects_list, 2)
    page = p.get_page(per_page)
    return page
