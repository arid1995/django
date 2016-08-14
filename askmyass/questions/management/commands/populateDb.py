from django.core.management.base import BaseCommand
from questions.models import Question, Tag, Profile, Answer, User

class Command(BaseCommand):
  args = '<foo bar ...>'
  help = 'our help string comes here'

  def fillDb(self):
    for i in range(0, 50):
      usr = User(username='me am drunk ' + str(i), password='password' + str(i), first_name='Kanye')
      usr.save()
      prof = Profile(avatar='/avatar.jpg', user = usr)
      prof.save()
      try:
        tbag = Tag.objects.get(name='beer' + str(i % 20))
        tbag.popularity += 1
      except Exception:
        tbag = Tag(name = 'beer' + str(i % 20), popularity = 1)
      tbag.save()

      quest = Question(title = str(i) + ' bottles of rum', text = str(10000 - i) + ' bottles remains', author = prof, votes = i)
      quest.save()
      quest.liked.add(prof)
      quest.tag.add(tbag)

      for j in range(0, 20):
        ans = Answer(text='I just drunk ' + str(i) + ' bottles of rum, I\'m a one sick fuck!', author=prof, question=quest)
        ans.votes = int(((i + j) * 6) % 40)
        ans.save()
        ans.voted.add(prof)


  def handle(self, *args, **options):
    self.fillDb()