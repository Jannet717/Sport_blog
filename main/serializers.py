from django.contrib.auth import get_user_model
from django.db.models import Avg
from rest_framework import serializers

from main.models import Image, Post, Category, Comment, Likes, Rating, Favorite

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', )




class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

    def _get_image_url(self, obj):
        if obj.image:
            url = obj.image.url
            request = self.context.get('request')
            if request is not None:
                url = request.build_absolute_uri(url)
        else:
            url = ''
        return url

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        return representation


class PostSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d/%m/%Y', read_only=True)
    image = ImageSerializer(many=True, read_only=True)
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Post
        fields = ('id', 'title', 'author', 'created_at', 'text', 'category', 'image')
        # fields = '__all__
        # title_ru, title_kg, text_ru, text_kg'
    def get_fields(self):
        action = self.context.get('action')
        fields = super().get_fields()
        if action == 'list':
                fields.pop('text')
                fields.pop('image')
                fields.pop('created_at')
        return fields

    def create(self, validated_data):
        request = self.context.get('request')
        print((request))
        images_data = request.FILES
        print(images_data)
        author = request.user
        print(author)

        post = Post.objects.create(author=author, **validated_data)
        print(validated_data)
        for image in images_data.getlist('images'):
            Image.objects.create(post=post, image=image)
            print(image)
        return post

    def update(self, instance, validated_data):
        request = self.context.get('request')
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()
        instance.images.all().delete()
        images_data = request.FILES
        for image in images_data.getlist('images'):
            Image.objects.create(post=instance, image=image)
        return instance


    def to_representation(self, instance):
        # RatingSerializer(instance.rating.all(), many=True).data
        # comments = CommentSerializer(instance.comments.all(), many=True).data
        representation = super().to_representation(instance)
        representation['images'] = ImageSerializer(instance.images.all(), many=True, context=self.context).data
        representation['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        representation['likes'] = instance.likes.all().count()
        representation['rating'] = instance.rating.aggregate(Avg('rating'))
        return representation


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        print(author)
        comment = Comment.objects.create(author=author, **validated_data)
        return comment


class LikesSerializer(serializers.ModelSerializer):

    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Likes
        fields = '__all__'


    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        post = validated_data.get('post')
        like = Likes.objects.get_or_create(author=author, post=post)[0]
        like.likes = True if like.likes is False else False
        like.save()
        return like
    # def create(self, validated_data):
    #     request = self.context.get('request')
    #     author = request.user
    #     likes = Likes.objects.get_or_create(author=author, **validated_data)
    #     return likes


# class FanSerializer(serializers.ModelSerializer):
#     full_name = serializers.SerializerMethodField()
#     class Meta:
#         model = User
#         fields = (
#             'username',
#             'full_name',
#         )
#     def get_full_name(self, obj):
#         return obj.get_full_name()

class RatingSerializer(serializers.ModelSerializer):

    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Rating
        fields = '__all__'

    # def validate(self, attrs):
    #     rating = attrs.get('rating')
    #     print(rating)
    #     if rating > 10:
    #         raise ValueError('Max rating 10')
    #     return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        post = validated_data.get('post')
        print(validated_data)
        rating = Rating.objects.get_or_create(author=author, post=post)[0]
        rating.rating = validated_data['rating']
        rating.save()
        return rating


class ParsingSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)



class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.email
        representation['post'] = instance.post.title
        return representation


