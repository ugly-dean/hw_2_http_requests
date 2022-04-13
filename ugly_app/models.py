from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(blank=True, null=True)

    def __str__(self):
        return f"{self.user}"

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        else:
            return None


class TagManager(models.Manager):
    def get_qs(self, _tag):
        return self.filter(tag=_tag)[0].question_set.all()

    def get_top_tags(self):
        TOP_COUNT = 10
        top = []
        for tag in self.all():
            top.append((tag.question_set.count(), tag.tag))
        top.sort(key=lambda num: num[0], reverse=True)
        return top[:TOP_COUNT]


class Tag(models.Model):
    tag = models.CharField(max_length=32)

    objects = TagManager()

    def __str__(self):
        return f"{self.tag}"


class QuestionManager(models.Manager):
    def get_new(self):
        return self.order_by('-create_date')

    def get_top(self):
        top = []
        for quest in self.all():
            top.append((quest.likequestion_set.filter(like_or_dislike=True).count(), quest))
        top.sort(key=lambda num: num[0], reverse=True)
        return top


class Question(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=1024)
    text = models.TextField()
    tags = models.ManyToManyField(Tag)

    objects = QuestionManager()

    def __str__(self):
        return f"Question {self.pk}. {self.title}"

    class Meta:
        ordering = ['-create_date']


class AnswerManager(models.Manager):
    def get_answers_for_quest(self, quest):
        return self.filter(question=quest)


class Answer(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    relevance = models.BooleanField(default=False)

    objects = AnswerManager()

    def __str__(self):
        return f"Answer {self.pk} for question {self.question_id}"

    class Meta:
        ordering = ['create_date']


class LikeQuestionManager(models.Manager):

    def get_likes(self, quest):
        return self.filter(question=quest) \
                   .filter(like_or_dislike=True)

    def get_dislikes(self, quest):
        return self.filter(question=quest) \
                   .filter(like_or_dislike=False)


class LikeQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    like_or_dislike = models.BooleanField()     # like - True, dislike - False
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = LikeQuestionManager()

    def __str__(self):
        event = 'dislikes'
        if self.like_or_dislike:
            event = 'likes'
        return f"{self.user.username} {event} question {self.question.pk}"


class LikeAnswerManager(models.Manager):

    def get_likes(self, ans):
        return self.filter(answer=ans) \
                   .filter(like_or_dislike=True)

    def get_dislikes(self, ans):
        return self.filter(answer=ans) \
                   .filter(like_or_dislike=False)


class LikeAnswer(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    like_or_dislike = models.BooleanField()     # like - True, dislike - False
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = LikeAnswerManager()

    def __str__(self):
        event = 'dislikes'
        if self.like_or_dislike:
            event = 'likes'
        return f"{self.user.username} {event} answer {self.answer.pk}"
