from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

BELT_CHOICES = (
    ('White', 'White'),
    ('Blue', 'Blue'),
    ('Purple', 'Purple'),
    ('Brown', 'Brown'),
    ('Black', 'Black'),
)

class Category(models.Model):
    name = models.CharField(db_index = True, max_length=30)
    url_name = models.CharField(db_index = True, blank=True, max_length=30)
    seo_name = models.CharField(max_length=30,blank=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.url_name = self.name.replace(' ','-').replace('/','-').replace('#','-sharp')
        super(Category, self).save(*args, **kwargs) # Call the "real" save() method.    

    class Meta:
        ordering = ['name']

class Tag(models.Model):
    name = models.CharField(db_index = True, max_length=30)
    category = models.ForeignKey(Category)

    def __unicode__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(User, null=True, blank=True, related_name='main_post')
    title = models.CharField(max_length=80)
    slug = models.SlugField(max_length=80)
    is_youtube = models.BooleanField(default=False)
    post_url = models.URLField('Link to share', blank = True, verify_exists=False)
    text = models.TextField(blank = True, help_text = "Add some commentary for your link or just say what's on your mind")
    category = models.ForeignKey(Category, null=True, blank = True)
    upvotes = models.IntegerField(null=True, blank=True, max_length=4, default=0)
    #related_cats = models.ManyToManyField(Category, verbose_name = 'Related Categories', null=True, blank=True, related_name = 'rel_cats')
    datetime = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/post/%s/%s" % (self.pk, self.slug)

    def check_youtube(self):
        if self.post_url[0:22] == 'http://www.youtube.com' or self.post_url[0:15] == 'http://youtu.be':
            return True
        return False
 
    def save(self):
        if not self.id:
            self.slug = slugify(self.title)
            self.is_youtube = self.check_youtube()
        super(Post, self).save()

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    handle = models.CharField(max_length=30, unique=True)
    email = models.EmailField(blank=True)
    bio = models.TextField(blank=True)
    points = models.IntegerField(max_length=7, default=0)
    upvoted = models.ManyToManyField(Post, related_name='upvoted_set')
    belt = models.CharField(default='White', max_length='10', choices=BELT_CHOICES)

    def __unicode__(self):
        return self.handle

    def get_absolute_url(self):
        return "/profile/%s" % self.handle

def profile_callback(user):
    profile = UserProfile.objects.create(user=user, handle=user.username)

