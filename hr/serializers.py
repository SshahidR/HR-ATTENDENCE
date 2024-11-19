from rest_framework import serializers

from sample_project.hr.models import CustomUser



class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = CustomUser 
        fields = ['id', 'username', 'password', 'email']
        
