# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils.timezone import now


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=255, blank=False)
    full_name = models.CharField(max_length=255, blank=False)
    university_studies = models.CharField(max_length=255, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    passwords = models.CharField(max_length=200)
    salt = models.CharField(max_length=200)
    status = models.CharField(max_length=100)
    time_created = models.DateTimeField(default=now, blank=True)

    class Meta:
        db_table = 'Users'


class Userimage(models.Model):
    image_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True)

    class Meta:
        db_table = 'UserImage'
        unique_together = (('image_id', 'user'),)


class Universities(models.Model):
    uni_id = models.AutoField(primary_key=True)
    uni_name = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    ratings = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'Universities'


class Uniimage(models.Model):
    image_id = models.AutoField(primary_key=True)
    uni = models.ForeignKey('Universities', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uni_image/', blank=True, null=True)

    class Meta:
        db_table = 'UniImage'
        unique_together = (('image_id', 'uni'),)


class Unitofstudy(models.Model):
    uos_id = models.AutoField(primary_key=True)
    uni = models.ForeignKey('Universities', on_delete=models.CASCADE)
    unit_name = models.CharField(max_length=255, blank=True, null=True)
    ratings = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'UnitOfStudy'
        unique_together = (('uos_id', 'uni'),)


class Reviews(models.Model):
    reviews_id = models.AutoField(primary_key=True)
    uni = models.ForeignKey('Universities', on_delete=models.CASCADE)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    reviews = models.TextField(blank=True, null=True)
    time_posted = models.DateTimeField(default=now, blank=True)

    class Meta:
        db_table = 'Reviews'
        unique_together = (('reviews_id', 'uni', 'user'),)


class Experience(models.Model):
    exp_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', on_delete=models.CASCADE)
    uos = models.ForeignKey('Unitofstudy', models.DO_NOTHING)
    experience = models.TextField(blank=True, null=True)
    time_posted = models.DateTimeField(default=now, blank=True)

    class Meta:
        db_table = 'Experience'
        unique_together = (('exp_id', 'user', 'uos'),)


class Comments(models.Model):
    comments_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', on_delete=models.CASCADE)
    reviews = models.ForeignKey('Reviews', on_delete=models.CASCADE)
    comments = models.TextField(blank=True, null=True)
    time_posted = models.DateTimeField(default=now, blank=True)

    class Meta:
        db_table = 'Comments'
        unique_together = (('comments_id', 'user', 'reviews'),)


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
