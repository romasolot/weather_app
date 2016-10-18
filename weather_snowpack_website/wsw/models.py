from django.db import models
from django.template.defaultfilters import date

class Forecast(models.Model):
     class Meta:
         db_table = 'web_fx'
         ordering = ['-forecasttime']

     modelname = models.TextField(primary_key=True)
     forecasttime = models.DateField()
     windspdstr = models.TextField()
     winddirstr = models.TextField()
     geopstr = models.TextField()
     tempstr = models.TextField()
     psum = models.IntegerField()
     wind_1k = models. FloatField()
     temp_1k = models.FloatField()
     winddir_1k = models.FloatField()
     wind_2k = models.FloatField()
     temp_2k = models.FloatField()
     winddir_2k = models.FloatField()
     wind_3k = models.FloatField()
     temp_3k = models.FloatField()
     winddir_3k = models.FloatField()
     wind_4k = models.FloatField()
     temp_4k = models.FloatField()
     winddir_4k = models.FloatField()
     wind_5k = models.FloatField()
     temp_5k = models.FloatField()
     winddir_5k = models.FloatField()
     wind_6k = models.FloatField()
     temp_6k = models.FloatField()
     winddir_6k = models.FloatField()
     wind_7k = models.FloatField()
     temp_7k = models.FloatField()
     winddir_7k = models.FloatField()
     wind_8k = models.FloatField()
     temp_8k = models.FloatField()
     winddir_8k = models.FloatField()
     wind_9k = models.FloatField()
     temp_9k = models.FloatField()
     winddir_9k = models.FloatField()
     windspd = models.FloatField()
     windspd_max = models.FloatField()
     temp_base = models.FloatField()
     winddir = models.FloatField()
     temp_mtop = models.FloatField()

     def __str__(self):
        return self.headline

     def natural_key(self):
         return self.forecasttime

     @property
     def date_property(self):
         return '%s' % date(self.forecasttime, "n/j ga")

class Stations(models.Model):
    class Meta:
        db_table = 'web_station'
        ordering = ['-forecasttime']

    forecasttime = models.DateField(primary_key=True)
    temp_mtop = models.FloatField()
    windspd = models.FloatField()
    windspd_max = models.FloatField()
    wind_dir = models.FloatField()
    temp_base = models.FloatField()
    psum = models.IntegerField()

    def __str__(self):
        return self.headline

    def natural_key(self):
        return self.forecasttime

    @property
    def date_property(self):
        return '%s' % date(self.forecasttime, "n/j ga")