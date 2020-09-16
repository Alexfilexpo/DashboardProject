from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


CONTRACT_CHOICES = (
    ('strict', 'strict'),
    ('public', 'public'),
)


class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    entry_date = models.DateField()
    description = models.CharField(max_length=255)
    total_quota = models.PositiveIntegerField(default=0)
    total_hours_analysed = models.PositiveIntegerField(default=0)
    ceretai_user = models.BooleanField(default=False)
    test_user = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    current_quota = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.username


class Entries(models.Model):
    video_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    external_id = models.PositiveIntegerField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    entry_date = models.DateField()
    project = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Source(models.Model):
    source_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    contract_type = models.CharField(choices=CONTRACT_CHOICES, default='strict', max_length=50)

    def __str__(self):
        return self.name


class Production(models.Model):
    video_id = models.ForeignKey(Entries, on_delete=models.CASCADE)
    release_date = models.DateField()
    producer = models.CharField(max_length=50)
    country = models.CharField(max_length=255)
    language = models.CharField(max_length=255)
    imdb_id = models.PositiveIntegerField()
    genre = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    source_id = models.ForeignKey(Source, on_delete=models.CASCADE)
    gender_director = models.CharField(max_length=255)
    public = models.BooleanField(default=False)


class SpeechTimeline(models.Model):
    video_id = models.ForeignKey(Entries, on_delete=models.CASCADE)
    total_length = models.PositiveIntegerField()
    total_speech = models.PositiveIntegerField()
    speech_f = models.PositiveIntegerField()
    speech_m = models.PositiveIntegerField()
    timeline = models.TextField()

    def __str__(self):
        return str(self.video_id)


class ScreenTimeline(models.Model):
    video_id = models.ForeignKey(Entries, on_delete=models.CASCADE)
    screen_f = models.TextField()
    screen_m = models.TextField()
    images_with_faces = models.PositiveIntegerField()


class Face(models.Model):
    video_id = models.ForeignKey(Entries, on_delete=models.CASCADE)
    screen_f = models.PositiveIntegerField()
    screen_m = models.PositiveIntegerField()
    screen_n = models.PositiveIntegerField()
    main_f = models.PositiveIntegerField()
    main_m = models.PositiveIntegerField()
    center_f = models.PositiveIntegerField()
    center_m = models.PositiveIntegerField()
    confidence_f = models.FloatField(validators=[MinValueValidator(0.0)],)
    confidence_m = models.FloatField(validators=[MinValueValidator(0.0)],)


class Pose(models.Model):
    video_id = models.ForeignKey(Entries, on_delete=models.CASCADE)
    pitch_f = models.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)])
    roll_f = models.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)])
    yaw_f = models.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)])
    pitch_m = models.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)])
    roll_m = models.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)])
    yaw_m = models.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)])


class AgeAll(models.Model):
    video_id = models.ForeignKey(Entries, on_delete=models.CASCADE)
    avg_age = models.FloatField(validators=[MinValueValidator(0.0)],)
    avg_age_range = models.FloatField(validators=[MinValueValidator(0.0)],)
    a_0 = models.FloatField(validators=[MinValueValidator(0.0)],)
    a_15 = models.FloatField(validators=[MinValueValidator(0.0)],)
    a_30 = models.FloatField(validators=[MinValueValidator(0.0)],)
    a_45 = models.FloatField(validators=[MinValueValidator(0.0)],)
    a_60 = models.FloatField(validators=[MinValueValidator(0.0)],)
    a_75 = models.FloatField(validators=[MinValueValidator(0.0)],)
    a_90 = models.FloatField(validators=[MinValueValidator(0.0)],)


class AgeFemale(models.Model):
    video_id = models.ForeignKey(Entries, on_delete=models.CASCADE)
    avg_age_f = models.FloatField(validators=[MinValueValidator(0.0)], )
    avg_age_range = models.FloatField(validators=[MinValueValidator(0.0)], )
    a_0 = models.FloatField(validators=[MinValueValidator(0.0)], )
    a_15 = models.FloatField(validators=[MinValueValidator(0.0)], )
    a_30 = models.FloatField(validators=[MinValueValidator(0.0)], )
    a_45 = models.FloatField(validators=[MinValueValidator(0.0)], )
    a_60 = models.FloatField(validators=[MinValueValidator(0.0)], )
    a_75 = models.FloatField(validators=[MinValueValidator(0.0)], )
    a_90 = models.FloatField(validators=[MinValueValidator(0.0)], )


class AgeMale(models.Model):
    video_id = models.ForeignKey(Entries, on_delete=models.CASCADE)
    avg_age_m = models.FloatField(validators=[MinValueValidator(0.0)], )
    avg_age_range = models.FloatField(validators=[MinValueValidator(0.0)], )
    a_0 = models.FloatField(validators=[MinValueValidator(0.0)], )
    a_15 = models.FloatField(validators=[MinValueValidator(0.0)], )
    a_30 = models.FloatField(validators=[MinValueValidator(0.0)], )
    a_45 = models.FloatField(validators=[MinValueValidator(0.0)], )
    a_60 = models.FloatField(validators=[MinValueValidator(0.0)], )
    a_75 = models.FloatField(validators=[MinValueValidator(0.0)], )
    a_90 = models.FloatField(validators=[MinValueValidator(0.0)], )


class EmoAll(models.Model):
    video_id = models.ForeignKey(Entries, on_delete=models.CASCADE)
    smile = models.FloatField(validators=[MinValueValidator(0.0)], )
    smile_conf = models.FloatField(validators=[MinValueValidator(0.0)], )
    happy = models.FloatField(validators=[MinValueValidator(0.0)], )
    sad = models.FloatField(validators=[MinValueValidator(0.0)], )
    angry = models.FloatField(validators=[MinValueValidator(0.0)], )
    fear = models.FloatField(validators=[MinValueValidator(0.0)], )
    calm = models.FloatField(validators=[MinValueValidator(0.0)], )
    disgusted = models.FloatField(validators=[MinValueValidator(0.0)], )
    surprised = models.FloatField(validators=[MinValueValidator(0.0)], )
    confused = models.FloatField(validators=[MinValueValidator(0.0)], )


class EmoFemale(models.Model):
    video_id = models.ForeignKey(Entries, on_delete=models.CASCADE)
    smile_f = models.FloatField(validators=[MinValueValidator(0.0)], )
    smile_conf = models.FloatField(validators=[MinValueValidator(0.0)], )
    happy = models.FloatField(validators=[MinValueValidator(0.0)], )
    sad = models.FloatField(validators=[MinValueValidator(0.0)], )
    angry = models.FloatField(validators=[MinValueValidator(0.0)], )
    fear = models.FloatField(validators=[MinValueValidator(0.0)], )
    calm = models.FloatField(validators=[MinValueValidator(0.0)], )
    disgusted = models.FloatField(validators=[MinValueValidator(0.0)], )
    surprised = models.FloatField(validators=[MinValueValidator(0.0)], )
    confused = models.FloatField(validators=[MinValueValidator(0.0)], )


class EmoMale(models.Model):
    video_id = models.ForeignKey(Entries, on_delete=models.CASCADE)
    smile_f = models.FloatField(validators=[MinValueValidator(0.0)], )
    smile_conf = models.FloatField(validators=[MinValueValidator(0.0)], )
    happy = models.FloatField(validators=[MinValueValidator(0.0)], )
    sad = models.FloatField(validators=[MinValueValidator(0.0)], )
    angry = models.FloatField(validators=[MinValueValidator(0.0)], )
    fear = models.FloatField(validators=[MinValueValidator(0.0)], )
    calm = models.FloatField(validators=[MinValueValidator(0.0)], )
    disgusted = models.FloatField(validators=[MinValueValidator(0.0)], )
    surprised = models.FloatField(validators=[MinValueValidator(0.0)], )
    confused = models.FloatField(validators=[MinValueValidator(0.0)], )


class AgeGroup30(models.Model):
    video_id = models.ForeignKey(Entries, on_delete=models.CASCADE)
    perc_img = models.FloatField(validators=[MinValueValidator(0.0)], )
    center = models.FloatField(validators=[MinValueValidator(0.0)], )
    gender_conf = models.FloatField(validators=[MinValueValidator(0.0)], )
    age_range = models.FloatField(validators=[MinValueValidator(0.0)], )
    smile = models.FloatField(validators=[MinValueValidator(0.0)], )
    smile_conf = models.FloatField(validators=[MinValueValidator(0.0)], )
    happy = models.FloatField(validators=[MinValueValidator(0.0)], )
    sad = models.FloatField(validators=[MinValueValidator(0.0)], )
    angry = models.FloatField(validators=[MinValueValidator(0.0)], )
    fear = models.FloatField(validators=[MinValueValidator(0.0)], )
    calm = models.FloatField(validators=[MinValueValidator(0.0)], )
    disgusted = models.FloatField(validators=[MinValueValidator(0.0)], )
    surprised = models.FloatField(validators=[MinValueValidator(0.0)], )
    confused = models.FloatField(validators=[MinValueValidator(0.0)], )
    pitch = models.FloatField(validators=[MinValueValidator(0.0)], )
    roll = models.FloatField(validators=[MinValueValidator(0.0)], )
    yaw = models.FloatField(validators=[MinValueValidator(0.0)], )


class Keywords(models.Model):
    video_id = models.ForeignKey(Entries, on_delete=models.CASCADE)
    top_20_nouns_f = models.TextField()
    nouns_frequency_f = models.FloatField(validators=[MinValueValidator(0.0)], )
    top_20_nouns_m = models.TextField()
    nouns_frequency_m = models.FloatField(validators=[MinValueValidator(0.0)], )
    top_20_verbs_f = models.TextField()
    verbs_frequency_f = models.FloatField(validators=[MinValueValidator(0.0)], )
    top_20_verbs_m = models.TextField()
    verbs_frequency_m = models.FloatField(validators=[MinValueValidator(0.0)], )
    top_20_adjs_f = models.TextField()
    adjs_frequency_f = models.FloatField(validators=[MinValueValidator(0.0)], )
    top_20_adjs_m = models.TextField()
    adjs_frequency_m = models.FloatField(validators=[MinValueValidator(0.0)], )
    specific_keywords = models.TextField()
    spec_frequency_f = models.FloatField(validators=[MinValueValidator(0.0)], )
    spec_frequency_m = models.FloatField(validators=[MinValueValidator(0.0)], )

