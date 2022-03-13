from django.http.response import Http404, HttpResponse, JsonResponse
from django.core.serializers import serialize
from core.models import Post, Tag, Category


class PublicAPI:
    fields = ('title', 'slug', 'thumbnail',
              'seo_overview', 'content', 'categories', 'tags', 'author', 'timestamp',)
    content_type = "application/json"

    def all_posts(self, request):
        tag = request.GET.get('tag')
        category = request.GET.get('category')

        # If we get tag anc category in query parameter
        if tag and category:
            tag = Tag.objects.filter(name__iexact=tag).first()
            category = Category.objects.filter(slug__iexact=category).first()
            posts = Post.objects.filter(
                published=True, tags__name=tag, categories__name=category.name)

        # If we get tag in query parameter
        elif tag and not category:
            tag = Tag.objects.filter(name__iexact=tag).first()
            posts = Post.objects.filter(
                published=True, tags__name=tag)

        # If we get category in query parameter
        elif category and not tag:
            category = Category.objects.filter(slug__iexact=category).first()
            posts = Post.objects.filter(
                published=True, categories__name=category.name)
        else:
            posts = Post.objects.filter(published=True)

        data = serialize("json", posts, fields=self.fields,
                         use_natural_foreign_keys=True)
        return HttpResponse(data, content_type=self.content_type)

    def user_posts(self, request, username):
        posts = Post.objects.filter(author__username=username, published=True)
        data = serialize("json", posts, fields=self.fields,
                         use_natural_foreign_keys=True)
        return HttpResponse(data, content_type=self.content_type)

    def single_post(self, request, post_id, slug):
        post = Post.objects.filter(id=post_id, slug=slug, published=True)
        data = serialize("json", post, fields=self.fields,
                         use_natural_foreign_keys=True)
        return HttpResponse(data, content_type=self.content_type)
